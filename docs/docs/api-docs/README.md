<!-- markdownlint-disable -->

# API Overview

## Modules

- [`contaxy.clients`](./contaxy.clients.md#module-contaxyclients)
- [`contaxy.clients.auth`](./contaxy.clients.auth.md#module-contaxyclientsauth)
- [`contaxy.clients.deployment`](./contaxy.clients.deployment.md#module-contaxyclientsdeployment)
- [`contaxy.clients.extension`](./contaxy.clients.extension.md#module-contaxyclientsextension)
- [`contaxy.clients.file`](./contaxy.clients.file.md#module-contaxyclientsfile)
- [`contaxy.clients.json_db`](./contaxy.clients.json_db.md#module-contaxyclientsjson_db)
- [`contaxy.clients.project`](./contaxy.clients.project.md#module-contaxyclientsproject)
- [`contaxy.clients.shared`](./contaxy.clients.shared.md#module-contaxyclientsshared)
- [`contaxy.clients.system`](./contaxy.clients.system.md#module-contaxyclientssystem)
- [`contaxy.config`](./contaxy.config.md#module-contaxyconfig)
- [`contaxy.main`](./contaxy.main.md#module-contaxymain)
- [`contaxy.managers`](./contaxy.managers.md#module-contaxymanagers)
- [`contaxy.managers.auth`](./contaxy.managers.auth.md#module-contaxymanagersauth)
- [`contaxy.managers.components`](./contaxy.managers.components.md#module-contaxymanagerscomponents)
- [`contaxy.managers.deployment`](./contaxy.managers.deployment.md#module-contaxymanagersdeployment)
- [`contaxy.managers.deployment.docker`](./contaxy.managers.deployment.docker.md#module-contaxymanagersdeploymentdocker)
- [`contaxy.managers.deployment.docker_utils`](./contaxy.managers.deployment.docker_utils.md#module-contaxymanagersdeploymentdocker_utils)
- [`contaxy.managers.deployment.kube_utils`](./contaxy.managers.deployment.kube_utils.md#module-contaxymanagersdeploymentkube_utils)
- [`contaxy.managers.deployment.kubernetes`](./contaxy.managers.deployment.kubernetes.md#module-contaxymanagersdeploymentkubernetes)
- [`contaxy.managers.deployment.manager`](./contaxy.managers.deployment.manager.md#module-contaxymanagersdeploymentmanager)
- [`contaxy.managers.deployment.utils`](./contaxy.managers.deployment.utils.md#module-contaxymanagersdeploymentutils)
- [`contaxy.managers.extension`](./contaxy.managers.extension.md#module-contaxymanagersextension)
- [`contaxy.managers.file`](./contaxy.managers.file.md#module-contaxymanagersfile)
- [`contaxy.managers.file.minio`](./contaxy.managers.file.minio.md#module-contaxymanagersfileminio)
- [`contaxy.managers.json_db`](./contaxy.managers.json_db.md#module-contaxymanagersjson_db)
- [`contaxy.managers.json_db.inmemory_dict`](./contaxy.managers.json_db.inmemory_dict.md#module-contaxymanagersjson_dbinmemory_dict)
- [`contaxy.managers.json_db.postgres`](./contaxy.managers.json_db.postgres.md#module-contaxymanagersjson_dbpostgres)
- [`contaxy.managers.project`](./contaxy.managers.project.md#module-contaxymanagersproject)
- [`contaxy.managers.seed`](./contaxy.managers.seed.md#module-contaxymanagersseed)
- [`contaxy.managers.system`](./contaxy.managers.system.md#module-contaxymanagerssystem)
- [`contaxy.operations`](./contaxy.operations.md#module-contaxyoperations)
- [`contaxy.operations.auth`](./contaxy.operations.auth.md#module-contaxyoperationsauth)
- [`contaxy.operations.deployment`](./contaxy.operations.deployment.md#module-contaxyoperationsdeployment)
- [`contaxy.operations.extension`](./contaxy.operations.extension.md#module-contaxyoperationsextension)
- [`contaxy.operations.file`](./contaxy.operations.file.md#module-contaxyoperationsfile)
- [`contaxy.operations.json_db`](./contaxy.operations.json_db.md#module-contaxyoperationsjson_db)
- [`contaxy.operations.project`](./contaxy.operations.project.md#module-contaxyoperationsproject)
- [`contaxy.operations.seed`](./contaxy.operations.seed.md#module-contaxyoperationsseed)
- [`contaxy.operations.system`](./contaxy.operations.system.md#module-contaxyoperationssystem)
- [`contaxy.schema`](./contaxy.schema.md#module-contaxyschema): Data Models and Schemas.
- [`contaxy.schema.auth`](./contaxy.schema.auth.md#module-contaxyschemaauth)
- [`contaxy.schema.deployment`](./contaxy.schema.deployment.md#module-contaxyschemadeployment)
- [`contaxy.schema.exceptions`](./contaxy.schema.exceptions.md#module-contaxyschemaexceptions)
- [`contaxy.schema.extension`](./contaxy.schema.extension.md#module-contaxyschemaextension)
- [`contaxy.schema.file`](./contaxy.schema.file.md#module-contaxyschemafile)
- [`contaxy.schema.json_db`](./contaxy.schema.json_db.md#module-contaxyschemajson_db)
- [`contaxy.schema.project`](./contaxy.schema.project.md#module-contaxyschemaproject)
- [`contaxy.schema.shared`](./contaxy.schema.shared.md#module-contaxyschemashared)
- [`contaxy.schema.system`](./contaxy.schema.system.md#module-contaxyschemasystem)
- [`contaxy.utils`](./contaxy.utils.md#module-contaxyutils): Collection of utilities usable across all modules.
- [`contaxy.utils.auth_utils`](./contaxy.utils.auth_utils.md#module-contaxyutilsauth_utils)
- [`contaxy.utils.fastapi_utils`](./contaxy.utils.fastapi_utils.md#module-contaxyutilsfastapi_utils): Collection of utilities for FastAPI apps.
- [`contaxy.utils.file_utils`](./contaxy.utils.file_utils.md#module-contaxyutilsfile_utils)
- [`contaxy.utils.id_utils`](./contaxy.utils.id_utils.md#module-contaxyutilsid_utils): Utilities for generating IDs, tokens, and hashes.
- [`contaxy.utils.minio_utils`](./contaxy.utils.minio_utils.md#module-contaxyutilsminio_utils)
- [`contaxy.utils.postgres_utils`](./contaxy.utils.postgres_utils.md#module-contaxyutilspostgres_utils)
- [`contaxy.utils.state_utils`](./contaxy.utils.state_utils.md#module-contaxyutilsstate_utils): Utilities for managing global and request state for an FastAPI app.

## Classes

- [`auth.AuthClient`](./contaxy.clients.auth.md#class-authclient)
- [`deployment.DeploymentManagerClient`](./contaxy.clients.deployment.md#class-deploymentmanagerclient)
- [`extension.ExtensionClient`](./contaxy.clients.extension.md#class-extensionclient)
- [`file.FileClient`](./contaxy.clients.file.md#class-fileclient)
- [`json_db.JsonDocumentClient`](./contaxy.clients.json_db.md#class-jsondocumentclient)
- [`project.ProjectClient`](./contaxy.clients.project.md#class-projectclient)
- [`shared.BaseUrlSession`](./contaxy.clients.shared.md#class-baseurlsession)
- [`system.SystemClient`](./contaxy.clients.system.md#class-systemclient)
- [`config.DeploymentManager`](./contaxy.config.md#class-deploymentmanager): An enumeration.
- [`config.Settings`](./contaxy.config.md#class-settings): Platform Settings.
- [`auth.AuthManager`](./contaxy.managers.auth.md#class-authmanager)
- [`auth.LoginIdMapping`](./contaxy.managers.auth.md#class-loginidmapping)
- [`auth.ResourcePermissions`](./contaxy.managers.auth.md#class-resourcepermissions)
- [`auth.UserPassword`](./contaxy.managers.auth.md#class-userpassword)
- [`components.ComponentManager`](./contaxy.managers.components.md#class-componentmanager): Initializes and manages all platform components.
- [`docker.DockerDeploymentManager`](./contaxy.managers.deployment.docker.md#class-dockerdeploymentmanager)
- [`kubernetes.KubernetesDeploymentManager`](./contaxy.managers.deployment.kubernetes.md#class-kubernetesdeploymentmanager)
- [`manager.DeploymentManager`](./contaxy.managers.deployment.manager.md#class-deploymentmanager)
- [`utils.Labels`](./contaxy.managers.deployment.utils.md#class-labels): An enumeration.
- [`utils.MappedLabels`](./contaxy.managers.deployment.utils.md#class-mappedlabels)
- [`extension.ExtensionClient`](./contaxy.managers.extension.md#class-extensionclient): Handels the request forwarding to the installed extensions.
- [`extension.ExtensionManager`](./contaxy.managers.extension.md#class-extensionmanager): Installs and manages extensions.
- [`minio.MinioFileManager`](./contaxy.managers.file.minio.md#class-miniofilemanager)
- [`inmemory_dict.InMemoryDictJsonDocumentManager`](./contaxy.managers.json_db.inmemory_dict.md#class-inmemorydictjsondocumentmanager)
- [`postgres.PostgresJsonDocumentManager`](./contaxy.managers.json_db.postgres.md#class-postgresjsondocumentmanager)
- [`project.ProjectManager`](./contaxy.managers.project.md#class-projectmanager)
- [`seed.SeedManager`](./contaxy.managers.seed.md#class-seedmanager)
- [`system.SystemManager`](./contaxy.managers.system.md#class-systemmanager)
- [`auth.AuthOperations`](./contaxy.operations.auth.md#class-authoperations)
- [`deployment.DeploymentOperations`](./contaxy.operations.deployment.md#class-deploymentoperations)
- [`deployment.JobOperations`](./contaxy.operations.deployment.md#class-joboperations)
- [`deployment.ServiceOperations`](./contaxy.operations.deployment.md#class-serviceoperations)
- [`extension.ExtensionOperations`](./contaxy.operations.extension.md#class-extensionoperations)
- [`file.FileOperations`](./contaxy.operations.file.md#class-fileoperations)
- [`json_db.JsonDocumentOperations`](./contaxy.operations.json_db.md#class-jsondocumentoperations)
- [`project.ProjectOperations`](./contaxy.operations.project.md#class-projectoperations)
- [`seed.SeedOperations`](./contaxy.operations.seed.md#class-seedoperations)
- [`system.SystemOperations`](./contaxy.operations.system.md#class-systemoperations)
- [`auth.AccessLevel`](./contaxy.schema.auth.md#class-accesslevel): An enumeration.
- [`auth.AccessToken`](./contaxy.schema.auth.md#class-accesstoken)
- [`auth.ApiToken`](./contaxy.schema.auth.md#class-apitoken)
- [`auth.AuthorizeResponseType`](./contaxy.schema.auth.md#class-authorizeresponsetype): An enumeration.
- [`auth.AuthorizedAccess`](./contaxy.schema.auth.md#class-authorizedaccess)
- [`auth.OAuth2Error`](./contaxy.schema.auth.md#class-oauth2error): Basic exception for OAuth errors.
- [`auth.OAuth2ErrorDetails`](./contaxy.schema.auth.md#class-oauth2errordetails)
- [`auth.OAuth2TokenGrantTypes`](./contaxy.schema.auth.md#class-oauth2tokengranttypes): An enumeration.
- [`auth.OAuth2TokenRequestFormNew`](./contaxy.schema.auth.md#class-oauth2tokenrequestformnew): OAuth2 Token Endpoint Request Form.
- [`auth.OAuthToken`](./contaxy.schema.auth.md#class-oauthtoken)
- [`auth.OAuthTokenIntrospection`](./contaxy.schema.auth.md#class-oauthtokenintrospection)
- [`auth.TokenPurpose`](./contaxy.schema.auth.md#class-tokenpurpose): An enumeration.
- [`auth.TokenType`](./contaxy.schema.auth.md#class-tokentype): An enumeration.
- [`auth.User`](./contaxy.schema.auth.md#class-user)
- [`auth.UserBase`](./contaxy.schema.auth.md#class-userbase)
- [`auth.UserInput`](./contaxy.schema.auth.md#class-userinput)
- [`auth.UserRegistration`](./contaxy.schema.auth.md#class-userregistration)
- [`deployment.Deployment`](./contaxy.schema.deployment.md#class-deployment)
- [`deployment.DeploymentBase`](./contaxy.schema.deployment.md#class-deploymentbase)
- [`deployment.DeploymentCompute`](./contaxy.schema.deployment.md#class-deploymentcompute)
- [`deployment.DeploymentInput`](./contaxy.schema.deployment.md#class-deploymentinput)
- [`deployment.DeploymentStatus`](./contaxy.schema.deployment.md#class-deploymentstatus): An enumeration.
- [`deployment.DeploymentType`](./contaxy.schema.deployment.md#class-deploymenttype): An enumeration.
- [`deployment.Job`](./contaxy.schema.deployment.md#class-job)
- [`deployment.JobBase`](./contaxy.schema.deployment.md#class-jobbase)
- [`deployment.JobInput`](./contaxy.schema.deployment.md#class-jobinput)
- [`deployment.Service`](./contaxy.schema.deployment.md#class-service)
- [`deployment.ServiceBase`](./contaxy.schema.deployment.md#class-servicebase)
- [`deployment.ServiceInput`](./contaxy.schema.deployment.md#class-serviceinput)
- [`exceptions.ClientBaseError`](./contaxy.schema.exceptions.md#class-clientbaseerror): Basic exception class for all errors that should be shown to the client/user.
- [`exceptions.ClientValueError`](./contaxy.schema.exceptions.md#class-clientvalueerror): Client error that indicates that the client input is invalid.
- [`exceptions.PermissionDeniedError`](./contaxy.schema.exceptions.md#class-permissiondeniederror): Client error that indicates that a client does not have sufficient permission for the request.
- [`exceptions.ProblemDetails`](./contaxy.schema.exceptions.md#class-problemdetails)
- [`exceptions.ResourceAlreadyExistsError`](./contaxy.schema.exceptions.md#class-resourcealreadyexistserror): Client error that indicates that a resource that a client tried to create already exists.
- [`exceptions.ResourceNotFoundError`](./contaxy.schema.exceptions.md#class-resourcenotfounderror): Client error that indicates that a specified resource is not found.
- [`exceptions.ResourceUpdateFailedError`](./contaxy.schema.exceptions.md#class-resourceupdatefailederror): Client error that indicates that a requested update for a resource failed.
- [`exceptions.ServerBaseError`](./contaxy.schema.exceptions.md#class-serverbaseerror): Basic exception class for all server internal errors that should not be shown with details to the user.
- [`exceptions.UnauthenticatedError`](./contaxy.schema.exceptions.md#class-unauthenticatederror): Client error that indicates invalid, expired, or missing authentication credentials.
- [`extension.Extension`](./contaxy.schema.extension.md#class-extension)
- [`extension.ExtensionBase`](./contaxy.schema.extension.md#class-extensionbase)
- [`extension.ExtensionInput`](./contaxy.schema.extension.md#class-extensioninput)
- [`extension.ExtensionType`](./contaxy.schema.extension.md#class-extensiontype): An enumeration.
- [`file.File`](./contaxy.schema.file.md#class-file)
- [`file.FileBase`](./contaxy.schema.file.md#class-filebase)
- [`file.FileInput`](./contaxy.schema.file.md#class-fileinput)
- [`file.FileStream`](./contaxy.schema.file.md#class-filestream)
- [`json_db.JsonDocument`](./contaxy.schema.json_db.md#class-jsondocument)
- [`project.Project`](./contaxy.schema.project.md#class-project)
- [`project.ProjectBase`](./contaxy.schema.project.md#class-projectbase)
- [`project.ProjectCreation`](./contaxy.schema.project.md#class-projectcreation)
- [`project.ProjectInput`](./contaxy.schema.project.md#class-projectinput)
- [`project.Quota`](./contaxy.schema.project.md#class-quota)
- [`project.Statistics`](./contaxy.schema.project.md#class-statistics)
- [`shared.ActionInstruction`](./contaxy.schema.shared.md#class-actioninstruction): An enumeration.
- [`shared.CoreOperations`](./contaxy.schema.shared.md#class-coreoperations): An enumeration.
- [`shared.ExtensibleOperations`](./contaxy.schema.shared.md#class-extensibleoperations): An enumeration.
- [`shared.Resource`](./contaxy.schema.shared.md#class-resource)
- [`shared.ResourceAction`](./contaxy.schema.shared.md#class-resourceaction)
- [`shared.ResourceInput`](./contaxy.schema.shared.md#class-resourceinput)
- [`shared.ResourceMetadata`](./contaxy.schema.shared.md#class-resourcemetadata)
- [`system.SystemInfo`](./contaxy.schema.system.md#class-systeminfo)
- [`system.SystemState`](./contaxy.schema.system.md#class-systemstate): An enumeration.
- [`system.SystemStatistics`](./contaxy.schema.system.md#class-systemstatistics)
- [`file_utils.FileStreamWrapper`](./contaxy.utils.file_utils.md#class-filestreamwrapper)
- [`file_utils.FormMultipartStream`](./contaxy.utils.file_utils.md#class-formmultipartstream)
- [`file_utils.MultipartStreamTarget`](./contaxy.utils.file_utils.md#class-multipartstreamtarget): StreamTarget stores one chunk at a time in-memory and deletes it upon read.
- [`file_utils.SyncFromAsyncGenerator`](./contaxy.utils.file_utils.md#class-syncfromasyncgenerator): This genrator implementation wraps an async generator to make it compatible for sync implementations.
- [`state_utils.GlobalState`](./contaxy.utils.state_utils.md#class-globalstate): Holds a global state of one app instance (process).
- [`state_utils.RequestState`](./contaxy.utils.state_utils.md#class-requeststate): Holds a state for a single request.
- [`state_utils.State`](./contaxy.utils.state_utils.md#class-state)

## Functions

- [`auth.handle_oauth_error`](./contaxy.clients.auth.md#function-handle_oauth_error)
- [`shared.handle_errors`](./contaxy.clients.shared.md#function-handle_errors)
- [`components.install_components`](./contaxy.managers.components.md#function-install_components): Currently only a mock implementation.
- [`docker_utils.check_minimal_resources`](./contaxy.managers.deployment.docker_utils.md#function-check_minimal_resources)
- [`docker_utils.create_container_config`](./contaxy.managers.deployment.docker_utils.md#function-create_container_config)
- [`docker_utils.create_network`](./contaxy.managers.deployment.docker_utils.md#function-create_network): Create a new network to put the new container into it.
- [`docker_utils.define_mounts`](./contaxy.managers.deployment.docker_utils.md#function-define_mounts)
- [`docker_utils.delete_container`](./contaxy.managers.deployment.docker_utils.md#function-delete_container)
- [`docker_utils.extract_minimal_resources`](./contaxy.managers.deployment.docker_utils.md#function-extract_minimal_resources)
- [`docker_utils.get_project_container`](./contaxy.managers.deployment.docker_utils.md#function-get_project_container)
- [`docker_utils.get_project_container_selection_labels`](./contaxy.managers.deployment.docker_utils.md#function-get_project_container_selection_labels)
- [`docker_utils.get_project_containers`](./contaxy.managers.deployment.docker_utils.md#function-get_project_containers)
- [`docker_utils.get_this_container`](./contaxy.managers.deployment.docker_utils.md#function-get_this_container): This function returns the Docker container in which this code is running or None if it does not run in a container.
- [`docker_utils.handle_network`](./contaxy.managers.deployment.docker_utils.md#function-handle_network)
- [`docker_utils.list_deploy_service_actions`](./contaxy.managers.deployment.docker_utils.md#function-list_deploy_service_actions)
- [`docker_utils.map_container`](./contaxy.managers.deployment.docker_utils.md#function-map_container)
- [`docker_utils.map_job`](./contaxy.managers.deployment.docker_utils.md#function-map_job)
- [`docker_utils.map_service`](./contaxy.managers.deployment.docker_utils.md#function-map_service)
- [`docker_utils.read_container_logs`](./contaxy.managers.deployment.docker_utils.md#function-read_container_logs)
- [`kube_utils.build_deployment_metadata`](./contaxy.managers.deployment.kube_utils.md#function-build_deployment_metadata)
- [`kube_utils.build_kube_deployment_config`](./contaxy.managers.deployment.kube_utils.md#function-build_kube_deployment_config)
- [`kube_utils.build_kube_service_config`](./contaxy.managers.deployment.kube_utils.md#function-build_kube_service_config)
- [`kube_utils.build_pod_template_spec`](./contaxy.managers.deployment.kube_utils.md#function-build_pod_template_spec)
- [`kube_utils.build_project_network_policy_spec`](./contaxy.managers.deployment.kube_utils.md#function-build_project_network_policy_spec)
- [`kube_utils.check_or_create_project_network_policy`](./contaxy.managers.deployment.kube_utils.md#function-check_or_create_project_network_policy)
- [`kube_utils.create_pvc`](./contaxy.managers.deployment.kube_utils.md#function-create_pvc)
- [`kube_utils.create_service`](./contaxy.managers.deployment.kube_utils.md#function-create_service)
- [`kube_utils.get_deployment_selection_labels`](./contaxy.managers.deployment.kube_utils.md#function-get_deployment_selection_labels): Return selector identifying project services/jobs in the form Kubernetes expects a label selector.
- [`kube_utils.get_label_selector`](./contaxy.managers.deployment.kube_utils.md#function-get_label_selector): Bring label tuples into the form required by the Kubernetes client, e.g. 'key1=value1,key2=value2,key3=value3)'.
- [`kube_utils.get_pod`](./contaxy.managers.deployment.kube_utils.md#function-get_pod): Get the pod filtered by the project id and service id labels in the given Kubernetes namespace.
- [`kube_utils.map_deployment`](./contaxy.managers.deployment.kube_utils.md#function-map_deployment)
- [`kube_utils.map_kube_job`](./contaxy.managers.deployment.kube_utils.md#function-map_kube_job)
- [`kube_utils.map_kube_service`](./contaxy.managers.deployment.kube_utils.md#function-map_kube_service)
- [`kube_utils.wait_for_deletion`](./contaxy.managers.deployment.kube_utils.md#function-wait_for_deletion)
- [`kube_utils.wait_for_deployment`](./contaxy.managers.deployment.kube_utils.md#function-wait_for_deployment)
- [`kube_utils.wait_for_job`](./contaxy.managers.deployment.kube_utils.md#function-wait_for_job)
- [`utils.clean_labels`](./contaxy.managers.deployment.utils.md#function-clean_labels): Remove system labels that should not be settable by the user.
- [`utils.get_default_environment_variables`](./contaxy.managers.deployment.utils.md#function-get_default_environment_variables): Sets default environment variables that should be set for each container.
- [`utils.get_deployment_id`](./contaxy.managers.deployment.utils.md#function-get_deployment_id): Returns a valid deployment ID based on some specified metadata.
- [`utils.get_gpu_info`](./contaxy.managers.deployment.utils.md#function-get_gpu_info)
- [`utils.get_label_string`](./contaxy.managers.deployment.utils.md#function-get_label_string)
- [`utils.get_network_name`](./contaxy.managers.deployment.utils.md#function-get_network_name)
- [`utils.get_project_selection_labels`](./contaxy.managers.deployment.utils.md#function-get_project_selection_labels): Return a list of labels identifying project resources (system namespace, project id, deployment type).
- [`utils.get_template_mapping`](./contaxy.managers.deployment.utils.md#function-get_template_mapping)
- [`utils.get_volume_name`](./contaxy.managers.deployment.utils.md#function-get_volume_name)
- [`utils.map_endpoints_label_to_endpoints`](./contaxy.managers.deployment.utils.md#function-map_endpoints_label_to_endpoints)
- [`utils.map_endpoints_to_endpoints_label`](./contaxy.managers.deployment.utils.md#function-map_endpoints_to_endpoints_label)
- [`utils.map_labels`](./contaxy.managers.deployment.utils.md#function-map_labels): Transform label dict to a MappedLabels object.
- [`utils.replace_template_string`](./contaxy.managers.deployment.utils.md#function-replace_template_string): Return the input with replaced value according to the templates mapping.
- [`utils.replace_templates`](./contaxy.managers.deployment.utils.md#function-replace_templates): Returns the input dict where those values that are matching template strings are replaced.
- [`extension.map_service_to_extension`](./contaxy.managers.extension.md#function-map_service_to_extension)
- [`extension.parse_composite_id`](./contaxy.managers.extension.md#function-parse_composite_id): Extracts the resource and extension ID from an composite ID.
- [`auth_utils.construct_permission`](./contaxy.utils.auth_utils.md#function-construct_permission): Constructs a permission based on the provided `resource_name`  and `access_level`.
- [`auth_utils.is_access_level_granted`](./contaxy.utils.auth_utils.md#function-is_access_level_granted): Checks if the requested access level is allowed by the granted access level.
- [`auth_utils.is_jwt_token`](./contaxy.utils.auth_utils.md#function-is_jwt_token): Returns `True` if the provided token is an JWT token.
- [`auth_utils.is_permission_granted`](./contaxy.utils.auth_utils.md#function-is_permission_granted): Checks if the requested permission is allowed by the granted permission.
- [`auth_utils.is_valid_permission`](./contaxy.utils.auth_utils.md#function-is_valid_permission): Returns `True` if the `permission_str` is valid permission.
- [`auth_utils.parse_permission`](./contaxy.utils.auth_utils.md#function-parse_permission): Extracts the resource name and access level from a permission.
- [`auth_utils.parse_userid_from_resource_name`](./contaxy.utils.auth_utils.md#function-parse_userid_from_resource_name): Returns the user id from a user-resource name.
- [`auth_utils.setup_user`](./contaxy.utils.auth_utils.md#function-setup_user): Execute initial setup required for each new user.
- [`fastapi_utils.add_timing_info`](./contaxy.utils.fastapi_utils.md#function-add_timing_info)
- [`fastapi_utils.as_form`](./contaxy.utils.fastapi_utils.md#function-as_form): Adds an as_form class method to decorated models.
- [`fastapi_utils.patch_fastapi`](./contaxy.utils.fastapi_utils.md#function-patch_fastapi): Patch function to allow relative url resolution.
- [`file_utils.generate_file_id`](./contaxy.utils.file_utils.md#function-generate_file_id)
- [`id_utils.extract_project_id_from_resource_name`](./contaxy.utils.id_utils.md#function-extract_project_id_from_resource_name): Extract the project id from a provided resource name.
- [`id_utils.extract_user_id_from_resource_name`](./contaxy.utils.id_utils.md#function-extract_user_id_from_resource_name): Extract the user id from a provided resource name.
- [`id_utils.generate_readable_id`](./contaxy.utils.id_utils.md#function-generate_readable_id): Generates a human- and URL-friendly ID from arbritary text.
- [`id_utils.generate_short_uuid`](./contaxy.utils.id_utils.md#function-generate_short_uuid): Generates a short - 25 chars - UUID by using all ascii letters and digits.
- [`id_utils.generate_token`](./contaxy.utils.id_utils.md#function-generate_token): Generates a random token with the specified length.
- [`id_utils.get_project_resource_prefix`](./contaxy.utils.id_utils.md#function-get_project_resource_prefix): Creates a prefix usable to construct IDs for project resources.
- [`id_utils.hash_str`](./contaxy.utils.id_utils.md#function-hash_str): Generates a hash with a variable lenght from an abritary text.
- [`id_utils.is_email`](./contaxy.utils.id_utils.md#function-is_email): Returns `True` if the given `text` has the format of an email address.
- [`minio_utils.create_bucket`](./contaxy.utils.minio_utils.md#function-create_bucket): Create a bucket in the object storage configured by the client.
- [`minio_utils.create_minio_client`](./contaxy.utils.minio_utils.md#function-create_minio_client)
- [`minio_utils.delete_bucket`](./contaxy.utils.minio_utils.md#function-delete_bucket)
- [`minio_utils.get_bucket_name`](./contaxy.utils.minio_utils.md#function-get_bucket_name)
- [`minio_utils.purge_bucket`](./contaxy.utils.minio_utils.md#function-purge_bucket)
- [`postgres_utils.create_schema`](./contaxy.utils.postgres_utils.md#function-create_schema)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._