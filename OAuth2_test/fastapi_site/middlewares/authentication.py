from typing import final
from fastapi.requests import HTTPConnection
from starlette.applications import Starlette
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError,  BaseUser

from fastapi_site.schemas import AnonymUser, User
from fastapi_site.utils import get_authorization_scheme_param

import httpx


class JWTTokenAuthBackend(AuthenticationBackend):
    def __init__(self, auth_server_host, auth_server_port):
        super().__init__()
        self._auth_server = f"http://{auth_server_host}:{auth_server_port}"

    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser] | None:
        if "Authorization" not in conn.headers:
            return AuthCredentials(), AnonymUser()
        
        bearer_authorization = conn.headers["Authorization"]
        scheme, _ = get_authorization_scheme_param(bearer_authorization)
        if scheme.lower() != "bearer":
            raise AuthenticationError("Not bearer authentication")
        user = await self.request_user(bearer_authorization)
        return AuthCredentials(['aaaa']), user

    async def request_user(self, bearer_authorization):
        api_url = f"{self._auth_server}/api/test/get_user"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers={"Authorization": bearer_authorization})
            if response.status_code == 401:
                error_msg = response.json()['detail']
                raise AuthenticationError(error_msg)
            user = response.json()
            return User(**user)
        return AnonymUser()