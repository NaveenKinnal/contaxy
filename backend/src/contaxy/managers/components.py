import threading
from typing import Optional

from fastapi import Request
from pydantic.networks import PostgresDsn

from contaxy import config
from contaxy.managers.auth import AuthManager
from contaxy.managers.extension import ExtensionManager
from contaxy.managers.file.minio import MinioFileManager
from contaxy.managers.project import ProjectManager
from contaxy.managers.system import SystemManager
from contaxy.managers.user import UserManager
from contaxy.operations import (
    FileOperations,
    JobOperations,
    JsonDocumentOperations,
    ServiceOperations,
)
from contaxy.operations.deployment import DeploymentOperations
from contaxy.schema.deployment import ServiceInput
from contaxy.schema.extension import CORE_EXTENSION_ID
from contaxy.schema.user import UserInput
from contaxy.utils.state_utils import GlobalState, RequestState


class ComponentManager:
    """Initializes and manages all platform components.

    The component manager is created for every request
    and will initialize all platform components based on the platform settings.
    It is the central point to access any other platform component.

    Individual components can store a global state via the `global_state` variable.
    This allows initializing certain objects (DB connections, HTTP clients, ...)
    only once per app instance (process) and share it with other components.

    There is also a `request_state` that can be used to share objects
    for a single request.
    """

    def __init__(self, request: Request):
        """Initializes the component manager.

        Args:
            request: Current request.
        """
        print(str(threading.get_ident()) + ": Initialize Componenten Manager")

        # Individual components can store global state via the `global_state` variable
        self._global_state = GlobalState(request.app.state)
        self._request_state = RequestState(request.app.state)

        # Initialized variables which will be lazyloaded
        self._auth_manager: Optional[AuthManager] = None
        self._extension_manager: Optional[ExtensionManager] = None
        self._user_manager: Optional[UserManager] = None
        self._project_manager: Optional[ProjectManager] = None
        self._system_manager: Optional[SystemManager] = None
        # Extensible managers: typed by its interface
        self._json_db_manager: Optional[JsonDocumentOperations] = None
        self._deployment_manager: Optional[DeploymentOperations] = None
        self._file_manager: Optional[FileOperations] = None

    # Allow component manger to be used as context manager
    def __enter__(self) -> "ComponentManager":
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # type: ignore
        self.close()

    def close(self) -> None:
        """Closes the component manager.

        This is called once the request is finished
        and will close the `request_state` and all its registered close callbacks.
        """
        print(str(threading.get_ident()) + ": Close Component Manager")
        self.request_state.close()
        del self._request_state

    @property
    def global_state(self) -> GlobalState:
        return self._global_state

    @property
    def request_state(self) -> RequestState:
        return self._request_state

    def get_system_manager(self) -> SystemManager:
        """Returns a System Manager instance."""
        if not self._system_manager:
            self._system_manager = SystemManager(self.global_state, self.request_state)  # type: ignore  # TODO: remove type ignore

        assert self._system_manager is not None
        return self._system_manager

    def get_user_manager(self) -> UserManager:
        """Returns a User Manager instance."""
        if not self._user_manager:
            self._user_manager = UserManager(self.global_state, self.request_state, self.get_json_db_manager())  # type: ignore  # TODO: remove type ignore

        assert self._user_manager is not None
        return self._user_manager

    def get_project_manager(self) -> ProjectManager:
        """Returns a Project Manager instance."""
        if not self._project_manager:
            self._project_manager = ProjectManager(self.global_state, self.request_state, self.get_json_db_manager())  # type: ignore  # TODO: remove type ignore

        assert self._project_manager is not None
        return self._project_manager

    def get_auth_manager(self) -> AuthManager:
        """Returns an Auth Manager instance."""
        if not self._auth_manager:
            self._auth_manager = AuthManager(self.global_state, self.request_state, self.get_json_db_manager())  # type: ignore  # TODO: remove type ignore

        assert self._auth_manager is not None
        return self._auth_manager

    def get_extension_manager(self) -> ExtensionManager:
        """Returns an Extension Manager instance."""
        if not self._extension_manager:
            self._extension_manager = ExtensionManager(self.global_state, self.request_state)  # type: ignore  # TODO: remove type ignore
        return self._extension_manager

    def get_json_db_manager(
        self, extension_id: Optional[str] = CORE_EXTENSION_ID
    ) -> JsonDocumentOperations:
        """Returns a JSON DB Manager instance.

        Depending on the provided `extenion_id`, this is either the configured core component
        or an initialized extension client.

        Args:
            extension_id: ID of the requested extension. Use `core` for the platform components.
        """
        if extension_id is not None and extension_id != CORE_EXTENSION_ID:
            return self.get_extension_manager().get_extension_client(extension_id)

        if not self._json_db_manager:
            from contaxy.managers.json_db.postgres import PostgresJsonDocumentManager

            self._json_db_manager = PostgresJsonDocumentManager(self.global_state, self.request_state)  # type: ignore  # TODO: remove type ignore
        return self._json_db_manager

    def get_file_manager(
        self, extension_id: Optional[str] = CORE_EXTENSION_ID
    ) -> FileOperations:
        """Returns a File Manager instance.

        Depending on the provided `extenion_id`, this is either the configured core component
        or an initialized extension client.

        Args:
            extension_id: ID of the requested extension. Use `core` for the platform components.
        """

        if extension_id is not None and extension_id != CORE_EXTENSION_ID:
            # Request is forwarded to extension
            return self.get_extension_manager().get_extension_client(extension_id)

        if not self._file_manager:
            self._file_manager = MinioFileManager(self.global_state, self.request_state, self.get_json_db_manager())  # type: ignore  # TODO: remove type ignore
        return self._file_manager

    def _get_deployment_manager(self) -> DeploymentOperations:
        # Lazyload deployment manager
        if not self._deployment_manager:
            if (
                self.global_state.settings.DEPLOYMENT_MANAGER
                == config.DeploymentManager.DOCKER
            ):
                from contaxy.managers.deployment.docker import DockerDeploymentManager

                self._deployment_manager = DockerDeploymentManager(  # type: ignore  # TODO: remove type ignore
                    self.global_state, self.request_state
                )
            elif (
                self.global_state.settings.DEPLOYMENT_MANAGER
                == config.DeploymentManager.KUBERNETES
            ):
                from contaxy.managers.deployment.kubernetes import (
                    KubernetesDeploymentManager,
                )

                self._deployment_manager = KubernetesDeploymentManager(  # type: ignore  # TODO: remove type ignore
                    self.global_state, self.request_state
                )

        assert self._deployment_manager is not None
        return self._deployment_manager

    def get_job_manager(
        self, extension_id: Optional[str] = CORE_EXTENSION_ID
    ) -> JobOperations:
        """Returns a Job Manager instance.

        Depending on the provided `extenion_id`, this is either the configured core component
        or an initialized extension client.

        Args:
            extension_id: ID of the requested extension. Use `core` for the platform components.
        """
        if extension_id is not None and extension_id != CORE_EXTENSION_ID:
            # Request is forwarded to extension
            return self.get_extension_manager().get_extension_client(extension_id)

        return self._get_deployment_manager()

    def get_service_manager(
        self, extension_id: Optional[str] = CORE_EXTENSION_ID
    ) -> ServiceOperations:
        """Returns a Service Manager instance.

        Depending on the provided `extenion_id`, this is either the configured core component
        or an initialized extension client.

        Args:
            extension_id: ID of the requested extension. Use `core` for the platform components.
        """
        if extension_id is not None and extension_id != CORE_EXTENSION_ID:
            # Request is forwarded to extension
            return self.get_extension_manager().get_extension_client(extension_id)

        return self._get_deployment_manager()


def install_components() -> None:
    """Currently only a mock implementation."""

    # create a mocked request for initializing the component manager
    import addict

    mocked_request = addict.Dict()
    # Load and add platform settings to
    global_state = GlobalState(mocked_request.app.state)  # type: ignore
    global_state.settings = config.settings

    # Initialize component manager
    component_manager = ComponentManager(mocked_request)  # type: ignore

    if not global_state.settings.POSTGRES_CONNECTION_URI:
        # Deploy postgres service in system project
        # Set database to use the system namespace
        POSTGRES_DB = global_state.settings.SYSTEM_NAMESPACE
        POSTGRES_PORT = "5432"
        # TODO: Generate credentials?
        POSTGRES_USER = "admin"
        POSTGRES_PASSWORD = "admin"

        service = component_manager.get_service_manager().deploy_service(
            config.SYSTEM_INTERNAL_PROJECT,
            ServiceInput(
                display_name="postgres",
                container_image="postgres",
                endpoints=[POSTGRES_PORT],
                parameters={
                    "POSTGRES_USER": POSTGRES_USER,
                    "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
                    "POSTGRES_DB": POSTGRES_DB,
                },
            ),
        )

        global_state.settings.POSTGRES_CONNECTION_URI = PostgresDsn(
            f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{service.id}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )

    # Create admin user
    user = component_manager.get_user_manager().create_user(
        UserInput(username=config.SYSTEM_ADMIN_USERNAME), technical_user=True
    )
    # Set initial user password -> SHOULD be changed after the first login
    component_manager.get_auth_manager().change_password(
        user.id, config.SYSTEM_ADMIN_INITIAL_PASSWORD
    )

    # TODO: Do other configurations

    # Close states
    component_manager.close()
    global_state.close()
