from fastapi import HTTPException, Header, Depends, Request
from typing import Annotated

from fastapi.security import SecurityScopes
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from fastapi_site.exceptions import AuthenticateException
from fastapi_site.schemas import User, UserRoles, AnonymUser
from fastapi_site.utils import get_authorization_scheme_param


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


def check_role(allowed_roles: tuple[str, ...] | list[str] | list[UserRoles]):
    """
    Проверяет роль пользователя
    :param allowed_roles: роли для проверки
    :return:
    :raises AuthenticateException: не достаточно прав
    """
    def _check_role(request: Request):
        user_role = request.user.role
        if user_role in allowed_roles:
            return True
        raise AuthenticateException("Not enough permissions", "Bearer")
    return _check_role


def is_auth(request: Request):
    """
    Проверят на авторизованного пользователя
    :param request: запрос
    :raises AuthenticateException: не авторизован
    """
    user = request.user
    if not isinstance(user, User):
        raise AuthenticateException("Not authorized", "Bearer")


def is_anonym_user(request: Request):
    """
    Проверят на неавторизованного (анонимного) пользователя
    :param request: запрос
    :raises AuthenticateException: пользователь уже авторизован
    """
    user = request.user
    if not isinstance(user, AnonymUser):
        raise AuthenticateException(f"Already authorized username '{user.username}' role {user.get_role()}",
                                    "Bearer")