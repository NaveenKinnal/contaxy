from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Path, Query, Request, Response, status
from fastapi.responses import StreamingResponse

from contaxy.api.dependencies import (
    ComponentManager,
    get_api_token,
    get_component_manager,
)
from contaxy.managers.extension import parse_composite_id
from contaxy.schema import ExtensibleOperations, File, FileInput, ResourceAction
from contaxy.schema.auth import AccessLevel
from contaxy.schema.extension import EXTENSION_ID_PARAM
from contaxy.schema.file import FILE_KEY_PARAM
from contaxy.schema.project import PROJECT_ID_PARAM
from contaxy.schema.shared import OPEN_URL_REDIRECT, RESOURCE_ID_REGEX
from contaxy.utils.file_utils import FormMultipartStream, SyncFromAsyncGenerator

router = APIRouter(
    tags=["files"],
    responses={
        401: {"detail": "No API token was provided"},
        403: {"detail": "Forbidden - the user is not authorized to use this resource"},
    },
)


@router.get(
    "/projects/{project_id}/files",
    operation_id=ExtensibleOperations.LIST_FILES.value,
    response_model=List[File],
    summary="List project files.",
    status_code=status.HTTP_200_OK,
)
def list_files(
    project_id: str = PROJECT_ID_PARAM,
    recursive: bool = Query(True, description="Include all content of subfolders."),
    include_versions: bool = Query(
        False,
        description="Include all versions of all files.",
    ),
    prefix: Optional[str] = Query(
        None,
        description="Filter results to include only files whose names begin with this prefix.",
    ),
    extension_id: Optional[str] = EXTENSION_ID_PARAM,
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Lists all available files for the project.

    The files can be filtered by using a `prefix`. The prefix is applied on the full path (directory path + filename).

    All versions of the files can be included by setting `versions` to `true` (default is `false`).

    Set `recursive` to `false` to only show files and folders (prefixes) of the current folder.
    The current folder is either the root folder (`/`) or the folder selected by the `prefix` parameter (has to end with `/`).
    """
    component_manager.verify_access(
        token, f"projects/{project_id}/files", AccessLevel.READ
    )

    return component_manager.get_file_manager(extension_id).list_files(
        project_id, recursive, include_versions, prefix
    )


@router.post(
    "/projects/{project_id}/files/{file_key:path}",
    operation_id=ExtensibleOperations.UPLOAD_FILE.value,
    response_model=File,
    summary="Upload a file.",
    status_code=status.HTTP_200_OK,
)
def upload_file(
    request: Request,
    project_id: str = PROJECT_ID_PARAM,
    file_key: str = FILE_KEY_PARAM,
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Uploads a file to a file storage.

    The file will be streamed to the selected file storage (core platform or extension).

    This upload operation only supports to attach a limited set of file metadata.
    Once the upload is finished, you can use the [update_file_metadata operation](#files/update_file_metadata)
    to add or update the metadata of the files.

    The `file_key` allows to categorize the uploaded file under a virtual file structure managed by the core platform.
    This allows to create a directory-like structure for files from different extensions and file-storage types.
    The actual file path on the file storage might not (and doesn't need to) correspond to the provided `file_key`.
    This allows to move files (via [update_file_metadata operation](#files/update_file_metadata)) into differnt paths
    without any changes on the file storage (depending on the implementation).

    Additional file metadata (`additional_metadata`) can be set by using the `x-amz-meta-` prefix for HTTP header keys (e.g. `x-amz-meta-my-metadata`).
    This corresponds to how AWS S3 handles [custom metadata](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html).
    """
    component_manager.verify_access(
        token, f"projects/{project_id}/files", AccessLevel.WRITE
    )

    file_stream = SyncFromAsyncGenerator(
        request.stream(), component_manager.global_state.shared_namespace.async_loop
    )

    multipart_stream = FormMultipartStream(
        file_stream, request.headers, form_field="file", hash_algo="md5"
    )
    content_type = (
        multipart_stream.content_type
        if multipart_stream.content_type
        else "application/octet-stream"
    )
    return component_manager.get_file_manager().upload_file(
        project_id, file_key, multipart_stream, content_type
    )


@router.get(
    "/projects/{project_id}/files/{file_key:path}:metadata",
    operation_id=ExtensibleOperations.GET_FILE_METADATA.value,
    response_model=File,
    summary="Get file metadata.",
    status_code=status.HTTP_200_OK,
)
def get_file_metadata(
    project_id: str = PROJECT_ID_PARAM,
    file_key: str = FILE_KEY_PARAM,
    version: Optional[str] = Query(
        None,
        description="File version tag. If not specified, the latest version will be used.",
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Returns metadata about the specified file."""
    component_manager.verify_access(
        token,
        f"/projects/{project_id}/files/{file_key}:metadata",
        AccessLevel.READ,
    )

    file_key, extension_id = parse_composite_id(file_key)
    return component_manager.get_file_manager(extension_id).get_file_metadata(
        project_id, file_key, version
    )


@router.patch(
    "/projects/{project_id}/files/{file_key:path}",
    operation_id=ExtensibleOperations.UPDATE_FILE_METADATA.value,
    response_model=File,
    summary="Update file metadata.",
    status_code=status.HTTP_200_OK,
)
def update_file_metadata(
    file: FileInput,
    project_id: str = PROJECT_ID_PARAM,
    file_key: str = FILE_KEY_PARAM,
    version: Optional[str] = Query(
        None,
        description="File version tag. If not specified, the latest version will be used.",
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Updates the file metadata.

    This will not change the actual content or the key of the file.

    The update is applied on the existing metadata based on the JSON Merge Patch Standard ([RFC7396](https://tools.ietf.org/html/rfc7396)).
    Thereby, only the specified properties will be updated.
    """
    component_manager.verify_access(
        token,
        f"projects/{project_id}/files/{file_key}",
        AccessLevel.WRITE,
    )

    file_key, extension_id = parse_composite_id(file_key)
    return component_manager.get_file_manager(extension_id).update_file_metadata(
        file, project_id, file_key, version
    )


@router.get(
    "/projects/{project_id}/files/{file_key:path}:download",
    operation_id=ExtensibleOperations.DOWNLOAD_FILE.value,
    # TODO: response_model?
    summary="Download a file.",
    status_code=status.HTTP_200_OK,
)
def download_file(
    project_id: str = PROJECT_ID_PARAM,
    file_key: str = FILE_KEY_PARAM,
    version: Optional[str] = Query(
        None,
        description="File version tag. If not specified, the latest version will be used.",
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Downloads the selected file.

    If the file storage supports versioning and no `version` is specified, the latest version will be downloaded.
    """
    component_manager.verify_access(
        token,
        f"projects/{project_id}/files/{file_key}:download",
        AccessLevel.READ,
    )
    file_manager = component_manager.get_file_manager()
    metadata = file_manager.get_file_metadata(project_id, file_key, version)
    file_stream = file_manager.download_file(project_id, file_key, version)

    return StreamingResponse(
        file_stream,
        media_type=metadata.content_type,
        headers={"Content-Disposition": f"attachment;filename={file_key}"},
    )


@router.get(
    "/projects/{project_id}/files/{file_key:path}/actions",
    operation_id=ExtensibleOperations.LIST_FILE_ACTIONS.value,
    response_model=List[ResourceAction],
    summary="List file actions.",
    status_code=status.HTTP_200_OK,
)
def list_file_actions(
    project_id: str = PROJECT_ID_PARAM,
    file_key: str = FILE_KEY_PARAM,
    version: Optional[str] = Query(
        None,
        description="File version tag. If not specified, the latest version will be used.",
    ),
    extension_id: Optional[str] = EXTENSION_ID_PARAM,
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Lists all actions available for the specified file.

    The returned action IDs should be used when calling the [execute_file_action](#files/execute_file_action) operation.

    The action mechanism allows extensions to provide additional functionality on files. It works the following way:

    1. The user requests all available actions via the [list_file_actions](#files/list_file_actions) operation.
    2. The operation will be forwarded to all installed extensions that have implemented the [list_file_actions](#files/list_file_actions) operation.
    3. Extensions can run arbitrary code - e.g., request and check the file metadata for compatibility - and return a list of actions with self-defined action IDs.
    4. The user selects one of those actions and triggers the [execute_file_action](#files/execute_file_action) operation by providing the selected action- and extension-ID.
    5. The operation is forwarded to the selected extension, which can run arbitrary code to execute the selected action.
    6. The return value of the operation can be either a simple message  (shown to the user) or a redirect to another URL (e.g., to show a web UI).

    The same action mechanism is also used for other resources (e.g., services, jobs).
    It can support a very broad set of use-cases, for example: CSV Viewer, Tensorflow Model Deployment, ZIP Archive Explorer ...
    """
    component_manager.verify_access(
        token,
        f"projects/{project_id}/files/{file_key}/actions",
        AccessLevel.WRITE,
    )

    return component_manager.get_file_manager(extension_id).list_file_actions(
        project_id, file_key, version
    )


@router.get(
    "/projects/{project_id}/files/{file_key:path}/actions/{action_id}",
    operation_id=ExtensibleOperations.EXECUTE_FILE_ACTION.value,
    # TODO: what is the response model? add additional status codes?
    summary="Execute a file action.",
    status_code=status.HTTP_200_OK,
    responses={**OPEN_URL_REDIRECT},
)
def execute_file_action(
    project_id: str = PROJECT_ID_PARAM,
    file_key: str = FILE_KEY_PARAM,
    action_id: str = Path(
        ...,
        description="The action ID from the file actions operation.",
        regex=RESOURCE_ID_REGEX,
    ),
    version: Optional[str] = Query(
        None,
        description="File version tag. If not specified, the latest version will be used.",
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Executes the selected action.

    The actions need to be first requested from the [list_file_actions](#files/list_file_actions) operation.
    If the action is from an extension, the `action_id` must be a composite ID with the following format: `{extension_id}~{action_id}`.

    The action mechanism is further explained in the description of the [list_file_actions](#files/list_file_actions).
    """
    # TODO: write permission?
    component_manager.verify_access(
        token,
        f"projects/{project_id}/files/{file_key}/actions/{action_id}",
        AccessLevel.WRITE,
    )

    # TODO: only extract extension ID from action?
    action_id, extension_id = parse_composite_id(action_id)
    return component_manager.get_file_manager(extension_id).execute_file_action(
        project_id, file_key, action_id, version
    )


@router.delete(
    "/projects/{project_id}/files/{file_key:path}",
    operation_id=ExtensibleOperations.DELETE_FILE.value,
    summary="Delete a file.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_file(
    project_id: str = PROJECT_ID_PARAM,
    file_key: str = FILE_KEY_PARAM,
    version: Optional[str] = Query(
        None,
        description="File version tag. If not specified, all versions of the file will be deleted.",
    ),
    keep_latest_version: Optional[bool] = Query(
        False, description="Keep the latest version of the file."
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Deletes the specified file.

    If the file storage supports versioning and no `version` is specified, all versions of the file will be deleted.

    The parameter `keep_latest_version` is useful if you want to delete all older versions of a file.
    """
    component_manager.verify_access(
        token, f"projects/{project_id}/files/{file_key}", AccessLevel.WRITE
    )
    if keep_latest_version is None:
        keep_latest_version = False

    file_key, extension_id = parse_composite_id(file_key)
    component_manager.get_file_manager(extension_id).delete_file(
        project_id, file_key, version, keep_latest_version
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def modify_openapi_schema(openapi_schema: dict) -> Dict[str, Any]:

    request_body = {
        "required": True,
        "content": {
            "multipart/form-data": {
                "schema": {
                    "$ref": "#/components/schemas/Body_upload_file_projects__project_id__files__file_key___post"
                }
            }
        },
    }

    openapi_schema["paths"]["/projects/{project_id}/files/{file_key}"]["post"][
        "requestBody"
    ] = request_body

    component_schema = {
        "title": "Body_upload_file_projects__project_id__files__file_key___post",
        "required": ["file"],
        "type": "object",
        "properties": {
            "file": {"title": "File", "type": "string", "format": "binary"},
            # "file_name": {"title": "File Name", "type": "string"},
        },
    }

    if (
        "components" not in openapi_schema
        or "schemas" not in openapi_schema["components"]
    ):
        openapi_schema["components"] = {"schemas": {}}

    openapi_schema["components"]["schemas"][
        "Body_upload_file_projects__project_id__files__file_key___post"
    ] = component_schema

    return openapi_schema
