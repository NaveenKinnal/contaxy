import ipaddress
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import docker
import psutil

from contaxy.config import settings
from contaxy.managers.deployment.utils import (
    DEFAULT_DEPLOYMENT_ACTION_ID,
    Labels,
    clean_labels,
    get_deployment_id,
    get_gpu_info,
    get_network_name,
    get_volume_name,
    log,
    map_labels,
)
from contaxy.schema import ResourceAction
from contaxy.schema.deployment import (
    DeploymentCompute,
    DeploymentStatus,
    DeploymentType,
    Job,
    JobInput,
    Service,
    ServiceInput,
)

# we create networks in the range of 172.33-255.0.0/24
# Docker by default uses the range 172.17-32.0.0, so we should be save using that range
INITIAL_CIDR_FIRST_OCTET = 10
INITIAL_CIDR_SECOND_OCTET = 0
INITIAL_CIDR = f"{INITIAL_CIDR_FIRST_OCTET}.{INITIAL_CIDR_SECOND_OCTET}.0.0/24"

system_cpu_count = psutil.cpu_count()
system_memory_in_mb = round(psutil.virtual_memory().total / 1024 / 1024, 1)
system_gpu_count = get_gpu_info()


def map_container(
    container: docker.models.containers.Container,
) -> Dict[str, Any]:
    labels = map_labels(container.labels)

    host_config = container.attrs["HostConfig"]
    compute_resources = DeploymentCompute(
        max_cpus=host_config["NanoCpus"] / 1e9,
        max_memory=host_config["Memory"] / 1000 / 1000,
        max_gpus=None,  # TODO: fill with sensible information - where to get it from?
        min_lifetime=labels.min_lifetime,
        volume_Path=labels.volume_path,
        # TODO: add max_volume_size, max_replicas
    )

    try:
        status = DeploymentStatus(container.status).value
    except ValueError:
        status = DeploymentStatus.UNKNOWN.value

    started_at = container.attrs.get("State", {}).get("StartedAt", None)
    stopped_at = container.attrs.get("State", {}).get("FinishedAt", None)

    def transform_env_list(envs: list) -> Dict[str, str]:
        transformed_envs = {}
        for env in envs:
            split_env = env.split("=")
            transformed_envs[split_env[0]] = split_env[1] if len(split_env) == 2 else ""
        return transformed_envs

    parameters = transform_env_list(
        container.attrs.get("Config", {}).get("Env", [])
    )  # dict([x for x in [container_env.split("=") for container_env in container_envs]])

    return {
        "container_image": container.image.tags[0],
        "command": " ".join(container.attrs.get("Args", [])),
        "compute": compute_resources,
        "metadata": labels.metadata,
        "deployment_type": labels.deployment_type,
        "description": labels.description,
        "display_name": labels.display_name,
        "endpoints": labels.endpoints,
        #         "exit_code": container.attrs.get("State", {}).get("ExitCode", -1),
        "icon": labels.icon,
        "id": container.id,
        "internal_id": container.id,
        "parameters": parameters,
        "started_at": started_at,
        "status": status,
        "stopped_at": stopped_at,
    }


def map_service(
    container: docker.models.containers.Container,
) -> Service:
    transformed_container = map_container(container=container)
    return Service(**transformed_container)


def map_job(container: docker.models.containers.Container) -> Job:
    transformed_container = map_container(container=container)
    return Job(**transformed_container)


# TODO: copied from ML Hub
def create_network(
    client: docker.client, name: str, labels: Dict[str, str]
) -> docker.models.networks.Network:
    """Create a new network to put the new container into it.

    Containers are separated by networks to prevent them from seeing each other.
    Determine whether a new subnet has to be used. Otherwise, the default Docker subnet would be used
    and, as a result, the amount of networks that can be created is strongly limited.
    We create networks in the range of 172.33-255.0.0/24 whereby Docker by default uses the range 172.17-32.0.0
    See: https://stackoverflow.com/questions/41609998/how-to-increase-maximum-docker-network-on-one-server ; https://loomchild.net/2016/09/04/docker-can-create-only-31-networks-on-a-single-machine/

    Args:
        network_name (str): name of the network to be created
        network_labels (Dict[str, str]): labels that will be attached to the network
    Raises:
        docker.errors.APIError: Thrown by `docker.client.networks.create` upon error.

    Returns:
        docker.Network: the newly created network or the existing network with the given name

    """

    networks = client.networks.list()
    highest_cidr = ipaddress.ip_network(INITIAL_CIDR)

    # determine subnet for the network to be created by finding the highest subnet so far.
    # E.g. when you have three subnets 172.33.1.0, 172.33.2.0, and 172.33.3.0, highest_cidr will be 172.33.3.0
    for network in networks:
        if network.name.lower() == name.lower():
            log(f"Network {name} already exists")
            return network

        has_all_properties = (
            network.attrs["IPAM"]
            and network.attrs["IPAM"]["Config"]
            and len(network.attrs["IPAM"]["Config"]) > 0
            and network.attrs["IPAM"]["Config"][0]["Subnet"]
        )
        if has_all_properties:
            cidr = ipaddress.ip_network(network.attrs["IPAM"]["Config"][0]["Subnet"])

            if (
                cidr.network_address.packed[0] == INITIAL_CIDR_FIRST_OCTET
                and cidr.network_address.packed[1] >= INITIAL_CIDR_SECOND_OCTET
                and cidr > highest_cidr
            ):
                highest_cidr = cidr

    # take the highest cidr and add 256 bits, so that if the highest subnet was 172.33.2.0, the new subnet is 172.33.3.0
    next_cidr = ipaddress.ip_network(
        (highest_cidr.network_address + 256).exploded + "/24"
    )
    if next_cidr.network_address.packed[0] > INITIAL_CIDR_FIRST_OCTET:
        raise RuntimeError("No more possible subnet addresses exist")

    log(f"Create network {name} with subnet {next_cidr.exploded}")
    ipam_pool = docker.types.IPAMPool(
        subnet=next_cidr.exploded, gateway=(next_cidr.network_address + 1).exploded
    )
    ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])

    return client.networks.create(
        name=name, check_duplicate=True, ipam=ipam_config, labels=labels
    )


def handle_network(
    client: docker.client, project_id: str
) -> docker.models.networks.Network:
    network_name = get_network_name(project_id)
    try:
        network = client.networks.get(network_id=network_name)
    except docker.errors.NotFound:
        network = create_network(
            client=client,
            name=network_name,
            labels={
                Labels.NAMESPACE.value: settings.SYSTEM_NAMESPACE,
                Labels.PROJECT_NAME.value: project_id,
            },
        )

        backend_container = get_this_container(client)
        if backend_container:
            is_backend_connected_to_network = backend_container.attrs[
                "NetworkSettings"
            ]["Networks"].get(network_name, False)
            if not is_backend_connected_to_network:
                try:
                    network.connect(backend_container)
                except docker.errors.APIError:
                    # Remove the network again as it is not connected to any service.
                    network.remove()
                    raise RuntimeError(
                        f"Could not connect the backend container to the network {network_name}"
                    )

    return network


def get_this_container(client: docker.client) -> docker.models.containers.Container:
    """This function returns the Docker container in which this code is running or None if it does not run in a container.

    Args:
        client (docker.client): The Docker client object

    Returns:
        docker.models.containers.Container: If this code runs in a container, it returns this container otherwise None
    """

    # "Detect" whether it runs in a container by checking the following environment variables
    hostname = os.getenv("HOSTNAME", False)
    if not os.getenv("IS_CONTAXY_CONTAINER", False) or hostname is None:
        return None
    return client.containers.get(hostname)


def check_minimal_resources(
    min_cpus: int,
    min_memory: int,
    min_gpus: int,
    compute_resources: DeploymentCompute = None,
) -> None:
    if min_cpus > system_cpu_count:
        raise RuntimeError(
            f"The minimal amount of cpus of {min_cpus} cannot be fulfilled as the system has only {system_cpu_count} cpus."
        )
    if min_memory > system_memory_in_mb:
        raise RuntimeError(
            f"The minimal amount of memory of {min_memory}MB cannot be fulfilled as the system has only {system_memory_in_mb}MB memory"
        )
    if min_gpus > system_gpu_count:
        raise RuntimeError(
            f"The minimal amount of gpus of {min_gpus} cannot be fulfilled as the system has only {system_gpu_count} gpus."
        )

    if compute_resources is None:
        return

    if compute_resources.max_replicas is not None:
        raise RuntimeError("Replicas are not supported in Docker-mode")


def extract_minimal_resources(
    compute_resources: DeploymentCompute,
) -> Tuple[int, int, int]:
    min_cpus = (
        compute_resources.min_cpus if compute_resources.min_cpus is not None else 0
    )
    min_memory = (
        compute_resources.min_memory if compute_resources.min_memory is not None else 0
    )
    min_gpus = (
        compute_resources.min_gpus if compute_resources.min_gpus is not None else 0
    )

    return min_cpus, min_memory, min_gpus


def define_mounts(
    project_id: str,
    container_name: str,
    compute_resources: DeploymentCompute,
    service_requirements: Optional[List[str]] = [],
) -> list:
    mounts = []
    if service_requirements and "docker" in service_requirements:
        # TODO: IMPORTANT mark container as having extended privileges so that on a higher level the platform
        # can prevent that a non-admin creates a container with the Docker socket mounted
        mounts.append(
            docker.types.Mount(
                target="/var/run/docker.sock", source="/var/run/docker.sock"
            )
        )

    if (
        compute_resources.volume_path is not None
        and compute_resources.volume_path != ""
    ):
        mount_type = "bind" if settings.HOST_DATA_ROOT_PATH is not None else "volume"
        mounts.append(
            docker.types.Mount(
                target=str(compute_resources.volume_path),
                source=f"{settings.HOST_DATA_ROOT_PATH}{get_volume_name(project_id, container_name)}",
                labels={
                    Labels.NAMESPACE.value: settings.SYSTEM_NAMESPACE,
                    Labels.PROJECT_NAME.value: project_id,
                    Labels.DEPLOYMENT_NAME.value: container_name,
                },
                type=mount_type,
            )
        )

    return mounts


def create_container_config(
    service: Union[JobInput, ServiceInput],
    project_id: str,
) -> Dict[str, Any]:

    if service.display_name is None:
        raise RuntimeError("Service name not defined")

    compute_resources = service.compute or DeploymentCompute()
    (
        min_cpus,
        min_memory,
        min_gpus,
    ) = extract_minimal_resources(compute_resources=compute_resources)
    check_minimal_resources(
        min_cpus=min_cpus,
        min_memory=min_memory,
        min_gpus=min_gpus,
    )

    deployment_type = (
        DeploymentType.SERVICE if type(service) == ServiceInput else DeploymentType.JOB
    )
    container_name = get_deployment_id(
        project_id,
        deployment_name=service.display_name,
        deployment_type=deployment_type,
    )

    max_cpus = (
        compute_resources.max_cpus if compute_resources.max_cpus is not None else 1
    )
    max_memory = (
        compute_resources.max_memory if compute_resources.max_memory is not None else 6
    )
    # Make sure that the user-entered compute requirements are not bigger than the system's maximum available
    nano_cpus = min(max_cpus, system_cpu_count) * 1e9
    # Additionally for memory Docker requires at least 4MB for a container
    mem_limit = f"{max(6, min(max_memory, system_memory_in_mb))}MB"

    mounts = define_mounts(
        project_id=project_id,
        container_name=container_name,
        compute_resources=compute_resources,
        service_requirements=service.requirements,
    )

    environment = service.parameters or {}
    # The user MUST not be able to manually set (which) GPUs to use
    if "NVIDIA_VISIBLE_DEVICES" in environment:
        del environment["NVIDIA_VISIBLE_DEVICES"]
    if compute_resources.max_gpus is not None and compute_resources.max_gpus > 0:
        # TODO: add logic to prevent overcommitting of GPUs!
        environment["NVIDIA_VISIBLE_DEVICES"] = str(compute_resources.max_gpus)

    if compute_resources.max_volume_size is not None:
        environment[f"{settings.SYSTEM_NAMESPACE.upper()}_MAX_VOLUME_SIZE_MB"] = str(
            compute_resources.max_volume_size
        )
    min_lifetime = (
        compute_resources.min_lifetime
        if compute_resources.min_lifetime is not None
        else "0"
    )

    endpoints_label = ",".join(service.endpoints) if service.endpoints else None
    requirements_label = (
        ",".join(service.requirements) if service.requirements else None
    )
    metadata = clean_labels(service.metadata)
    return {
        "image": service.container_image,
        "command": service.command or None,
        "detach": True,
        "environment": environment,
        "labels": {
            Labels.DISPLAY_NAME.value: service.display_name,
            Labels.NAMESPACE.value: settings.SYSTEM_NAMESPACE,
            Labels.MIN_LIFETIME.value: min_lifetime,
            Labels.PROJECT_NAME.value: project_id,
            Labels.DEPLOYMENT_NAME.value: container_name,
            Labels.ENDPOINTS.value: endpoints_label,
            Labels.REQUIREMENTS.value: requirements_label,
            **metadata,
        },
        "name": container_name,
        "nano_cpus": int(nano_cpus),
        "mem_limit": mem_limit,
        "network": get_network_name(project_id),
        "restart_policy": {"Name": "on-failure", "MaximumRetryCount": 10},
        "mounts": mounts if mounts != [] else None,
    }


def list_deploy_service_actions(
    project_id: str, deploy_input: Union[ServiceInput, JobInput]
) -> List[ResourceAction]:
    compute_resources = deploy_input.compute or DeploymentCompute()
    min_cpus, min_memory, min_gpus = extract_minimal_resources(compute_resources)
    try:
        check_minimal_resources(
            min_cpus=min_cpus, min_memory=min_memory, min_gpus=min_gpus
        )
    except RuntimeError:
        return []

    return [
        ResourceAction(
            action_id=DEFAULT_DEPLOYMENT_ACTION_ID,
            display_name=DEFAULT_DEPLOYMENT_ACTION_ID,
        )
    ]