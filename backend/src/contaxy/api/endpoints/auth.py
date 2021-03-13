from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, Form, Query, status
from starlette.responses import RedirectResponse

from contaxy.api.dependencies import (
    ComponentManager,
    get_api_token,
    get_component_manager,
)
from contaxy.schema import (
    ApiToken,
    CoreOperations,
    ExtensibleOperations,
    OAuth2TokenRequestForm,
    OAuthToken,
    OAuthTokenIntrospection,
    OpenIDUserInfo,
    TokenType,
)
from contaxy.schema.extension import EXTENSION_ID_PARAM
from contaxy.schema.project import MAX_PROJECT_ID_LENGTH, MIN_PROJECT_ID_LENGTH
from contaxy.schema.shared import OPEN_URL_REDIRECT

router = APIRouter(
    tags=["auth"], responses={401: {"detail": "No API token was provided"}}
)


@router.get(
    "/auth/login",
    operation_id=ExtensibleOperations.OPEN_LOGIN_PAGE.value,
    summary="Open the login page.",
    status_code=status.HTTP_200_OK,
    responses={**OPEN_URL_REDIRECT},
)
def open_login_page(
    extension_id: Optional[str] = EXTENSION_ID_PARAM,
    component_manager: ComponentManager = Depends(get_component_manager),
) -> Any:
    """Returns or redirect to the login-page."""
    rr = RedirectResponse("/welcome", status_code=307)
    rr.set_cookie(key="session_token", value="test-token", path="/welcome")
    rr.set_cookie(key="user_token", value="test-user-token", path="/users/me")
    return rr


@router.get(
    "/auth/logout",
    operation_id=CoreOperations.LOGOUT_SESSION.value,
    summary="Logout a user session.",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
def logout_session(
    component_manager: ComponentManager = Depends(get_component_manager),
) -> Any:
    """Removes all session token cookies and redirects to the login page.

    When making requests to the this endpoint, the browser should be redirected to this endpoint.
    """
    return RedirectResponse("./login", status_code=307)


@router.get(
    "/auth/tokens",
    operation_id=CoreOperations.LIST_API_TOKENS.value,
    response_model=List[ApiToken],
    summary="List API tokens.",
    status_code=status.HTTP_200_OK,
)
def list_api_token(
    user_id: Optional[str] = Query(
        None,
        title="User ID",
        description="Return API tokens associated with this user.",
    ),
    project_id: Optional[str] = Query(
        None,
        title="Project ID",
        description="Return API tokens associated with this project.",
        min_length=MIN_PROJECT_ID_LENGTH,
        max_length=MAX_PROJECT_ID_LENGTH,
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Returns list of created API tokens for the specified user or project.

    If a user ID and a project ID is provided, a combined list will be returned.
    """


@router.post(
    "/auth/tokens",
    operation_id=CoreOperations.CREATE_TOKEN.value,
    response_model=str,
    summary="Create API or session token.",
    status_code=status.HTTP_200_OK,
)
def create_token(
    scopes: Optional[List[str]] = Query(
        None,
        title="Scopes",
        description="Scopes requested for this token. If none specified, the token will be generated with same set of scopes as the authorized token.",
    ),
    token_type: TokenType = Query(
        TokenType.SESSION_TOKEN,
        description="Type of the token.",
        type="string",
    ),
    description: Optional[str] = Query(
        None, description="Attach a short description to the generated token."
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Returns a session or API token with access on the specified resource.

    A permission is a single string that combines a global ID of a resource with a permission level:

    `{global_id}.{permission_level}`

    Permission levels are a hierarchical system that determines the kind of access that is granted on the resource.
    Permission levels are interpreted and applied inside resource operations. There are three permission levels:

    1. `admin` permission level allows read, write, and administrative access to the resource.
    2. `write` permission level allows read and write (edit) access to the resource.
    3. `read` permission level allows read-only (view) access to the resource.

    The permission level can also be suffixed with an optional restriction defined by the resource:
    `{global_id}.{permission_level}.{custom_restriction}`

    If no permissions are specified, the token will be generated with the same permissions as the authorized token.

    The API token can be deleted (revoked) at any time.
    In comparison, the session token cannot be revoked but expires after a short time (a few minutes).

    This operation can only be called with API tokens (or refresh tokens) due to security aspects.
    Session tokens are not allowed to create other tokens.
    Furthermore, tokens can only be created if the API token used for authorization is granted at least
    the same permission level on the given resource. For example, a token with `write` permission level on a given resource
    allows to create new tokens with `write` or `read` permission on that resource.
    If a restriction is attached to the permission, created tokens on the same permission level require the same restriction.
    """
    raise NotImplementedError


@router.post(
    "/auth/tokens/verify",
    operation_id=CoreOperations.VERIFY_TOKEN.value,
    # response_model=List[str],
    summary="Verify a Session or API Token.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def verify_token(
    token: Optional[str] = Body(
        None,
        title="Token",
        description="Token to verify.",
    ),
    permission: Optional[str] = Query(
        None,
        title="Resource Type ",
        description="The token is checked if is granted this permission. If none specified, only the existence or validity of the token itself is checked.",
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
) -> Any:
    """Verifies a session or API token for its validity and - if provided - if it has the specified permission.

    Returns an successful HTTP Status code if verification was successful, otherwise an error is returned.
    """
    raise NotImplementedError


# OAuth Endpoints


@router.post(
    "/auth/oauth/token",
    operation_id=CoreOperations.REQUEST_TOKEN.value,
    response_model=OAuthToken,
    summary="Request a token (OAuth2 Endpoint).",
    status_code=status.HTTP_200_OK,
)
def request_token(form_data: OAuth2TokenRequestForm = Depends()) -> Any:
    """Returns an access tokens, ID tokens, or refresh tokens depending on the request parameters.

     The token endpoint is used by the client to obtain an access token by
     presenting its authorization grant or refresh token.

     The token endpoint supports the following grant types:
     - [Password Grant](https://tools.ietf.org/html/rfc6749#section-4.3.2): Used when the application exchanges the user’s username and password for an access token.
         - `grant_type` must be set to `password`
         - `username` (required): The user’s username.
         - `password` (required): The user’s password.
         - `scope` (optional): Optional requested scope values for the access token.
     - [Refresh Token Grant](https://tools.ietf.org/html/rfc6749#section-6): Allows to use refresh tokens to obtain new access tokens.
         - `grant_type` must be set to `refresh_token`
         - `refresh_token` (required): The refresh token previously issued to the client.
         - `scope` (optional): Requested scope values for the new access token. Must not include any scope values not originally granted by the resource owner, and if omitted is treated as equal to the originally granted scope.
     - [Client Credentials Grant](https://tools.ietf.org/html/rfc6749#section-4.4.2): Request an access token using only its client
    credentials.
         - `grant_type` must be set to `client_credentials`
         - `scope` (optional): Optional requested scope values for the access token.
         - Client Authentication required (e.g. via client_id and client_secret or auth header)
     - [Authorization Code Grant](https://tools.ietf.org/html/rfc6749#section-4.1): Used to obtain both access tokens and refresh tokens based on an authorization code from the `/authorize` endpoint.
         - `grant_type` must be set to `authorization_code`
         - `code` (required): The authorization code that the client previously received from the authorization server.
         - `redirect_uri` (required): The redirect_uri parameter included in the original authorization request.
         - Client Authentication required (e.g. via client_id and client_secret or auth header)

    For password, client credentials, and refresh token flows, calling this endpoint is the only step of the flow.
    For the authorization code flow, calling this endpoint is the second step of the flow.

    This endpoint implements the [OAuth2 Token Endpoint](https://tools.ietf.org/html/rfc6749#section-3.2).
    """
    raise NotImplementedError


@router.post(
    "/auth/oauth/revoke",
    operation_id=CoreOperations.REVOKE_TOKEN.value,
    response_model=List[str],
    summary="Revoke a token (OAuth2 Endpoint).",
    status_code=status.HTTP_200_OK,
)
def revoke_token(
    token: str = Form(..., description="The token that should be revoked."),
    token_type_hint: Optional[str] = Form(
        None,
        description="A hint about the type of the token submitted for revokation.",
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
) -> Any:
    """Revokes a given token.

    This will delete the API token, preventing further requests with the given token.
    Because of caching, the API token might still be usable under certain conditions
    for some operations for a maximum of 15 minutes after deletion.

    This endpoint implements the OAuth2 Revocation Flow ([RFC7009](https://tools.ietf.org/html/rfc7009)).
    """
    raise NotImplementedError


@router.post(
    "/auth/oauth/introspect",
    operation_id=CoreOperations.INTROSPECT_TOKEN.value,
    response_model=OAuthTokenIntrospection,
    summary="Introspect a token (OAuth2 Endpoint).",
    status_code=status.HTTP_200_OK,
)
def introspect_token(
    token: str = Form(
        ..., description="The token that should be instrospected revoked."
    ),
    token_type_hint: Optional[str] = Form(
        None,
        description="A hint about the type of the token submitted for introspection (e.g. `access_token`, `id_token` and `refresh_token`).",
    ),
    component_manager: ComponentManager = Depends(get_component_manager),
) -> Any:
    """Introspects a given token.

    Returns a boolean that indicates whether it is active or not.
    If the token is active, additional data about the token is also returned.
    If the token is invalid, expired, or revoked, it is considered inactive.

    This endpoint implements the [OAuth2 Introspection Flow](https://www.oauth.com/oauth2-servers/token-introspection-endpoint/) ([RFC7662](https://tools.ietf.org/html/rfc7662)).
    """
    raise NotImplementedError


@router.get(
    "/auth/oauth/userinfo",
    operation_id=CoreOperations.GET_USERINFO.value,
    response_model=OpenIDUserInfo,
    summary="Get userinfo (OpenID Endpoint).",
    status_code=status.HTTP_200_OK,
)
def get_userinfo(
    component_manager: ComponentManager = Depends(get_component_manager),
    token: str = Depends(get_api_token),
) -> Any:
    """Returns information about the authenticated user.

    The access token obtained must be sent as a bearer token in the `Authorization` header.

    This endpoint implements the [OpenID UserInfo Endpoint](https://openid.net/specs/openid-connect-core-1_0.html#UserInfo).
    """
    return None


@router.get(
    "/auth/oauth/callback",
    operation_id=CoreOperations.LOGIN_CALLBACK.value,
    summary="Open the login page (OAuth2 Client Endpoint).",
    status_code=status.HTTP_200_OK,
)
def login_callback(
    code: str = Query(
        ..., description="The authorization code generated by the authorization server."
    ),
    state: Optional[str] = Query(None),
    component_manager: ComponentManager = Depends(get_component_manager),
) -> Any:
    """Callback to finish the login process (OAuth2 Client Endpoint).

    The authorization `code` is exchanged for an access and ID token.
    The ID token contains all relevant user information and is used to login the user.
    If the user does not exist, a new user will be created with the information from the ID token.

    Finally, the user is redirected to the webapp and a session/refresh token is set in the cookies.

    This method implements the [Authorization Response](https://tools.ietf.org/html/rfc6749#section-4.1.2) from RFC6749.
    """
    rr = RedirectResponse("/webapp", status_code=307)
    rr.set_cookie(key="session_token", value="test-token")
    rr.set_cookie(key="refresh-token", value="test-refresh-token")
    return rr