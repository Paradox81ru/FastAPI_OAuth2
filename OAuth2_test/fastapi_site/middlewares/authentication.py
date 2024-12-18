from typing import final
from fastapi.requests import HTTPConnection
from starlette.applications import Starlette
from starlette.authentication import (AuthCredentials, AuthenticationBackend, AuthenticationError,  BaseUser,
                                      HTTPException)

from fastapi_site.schemas import AnonymUser, User
from fastapi_site.utils import get_authorization_scheme_param

import httpx


class JWTTokenAuthBackend(AuthenticationBackend):
    """ Клас реализации JWT авторизации для Middleware.  """
    def __init__(self, auth_server_host, auth_server_port):
        super().__init__()
        self._auth_server = f"http://{auth_server_host}:{auth_server_port}"

    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser] | None:
        """
        Интерфейс авторизации. Обеспечивает отправку токена доступа на сервис авторизации, и полученную
        ответную информацию о пользователе и scope, при авторизации, добавляет в Request.
        :param conn:
        :return:
        :raises AuthenticationError: Токен не относится к типу Bearer.
        """
        if "Authorization" not in conn.headers:
            return AuthCredentials(), AnonymUser()
        
        bearer_authorization = conn.headers["Authorization"]
        scheme, _ = get_authorization_scheme_param(bearer_authorization)
        if scheme.lower() != "bearer":
            raise AuthenticationError("Not bearer authentication")
        user, scope = await self.request_user(bearer_authorization)
        return AuthCredentials(scope), user

    async def request_user(self, bearer_authorization):
        """
        Запрос пользователя к сервису OAuth2 авторизации.
        :param bearer_authorization: Токен доступа.
        :return: Кортеж составляющий модель пользователя и scope, указанный при авторизации.
        :raises AuthenticationError: Ошибка авторизации.
        :raises HTTPException: Ошибка ответа от сервера.
        """
        api_url = f"{self._auth_server}/api/oauth/get_user"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers={"Authorization": bearer_authorization})
            if response.status_code == 200:
                user, scopes = response.json()
                return User(**user), scopes
            if response.status_code == 401:
                error_msg = response.json()['detail']
                raise AuthenticationError(error_msg)
            raise HTTPException(response.status_code, response.json()['detail'])
