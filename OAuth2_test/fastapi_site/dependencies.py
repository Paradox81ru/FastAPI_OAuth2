from fastapi import HTTPException, Header, Depends, Request
from typing import Annotated

from fastapi.security import SecurityScopes
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from fastapi_site.exceptions import AuthenticateException
from fastapi_site.utils import get_authorization_scheme_param


# async def validate_jwt_token(request: Request) -> str| None:
#     authorization = request.headers.get("Authorization")
#     scheme, _ = get_authorization_scheme_param(authorization)
#     if not authorization or scheme.lower() != "bearer":
#             return None
#     return authorization

def check_scope(request: Request, security_scopes: SecurityScopes):
    """
    Проверяет scopes
    :param request: запрос
    :param security_scopes: scope для проверки
    :raises AuthenticateException: Не достаточно прав
    """
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    if len(security_scopes.scopes) == 0:
        return
    token_scopes = request.auth.scopes
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise AuthenticateException("Not enough permissions", authenticate_value)