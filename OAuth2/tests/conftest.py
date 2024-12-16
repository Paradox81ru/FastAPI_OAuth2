import os
from dataclasses import dataclass
from enum import StrEnum

import httpx

os.environ['IS_TEST'] = 'True'

from fastapi.testclient import TestClient
from main import app
from config import get_settings
from Auth.db.db_connection import db_session as session
import alembic.config
import alembic.environment

import alembic
import pytest

settings = get_settings()


class UserType(StrEnum):
    ADMIN = 'Admin'
    SYSTEM = 'System'
    DIRECTOR = 'Director'
    USER = "User"
    ANONYM = "Anonym"


@dataclass
class UserAuth:
    username: str
    password: str


def get_access_token(client: TestClient, user_auth: UserAuth, scope: list[str]):
    """
    Возвращает токен авторизации
    :param client: тестовый клиент
    :param user_auth: Логин и пароль пользователя
    :param scope: scope авторизации
    :return:
    """
    request_data = {'username': user_auth.username, 'password': user_auth.password, 'scope': " ".join(scope)}
    response = client.post("/api/oauth/token", data=request_data)
    return response.json()['access_token']


@pytest.fixture()
def users_data(api_settings) -> dict[UserType, UserAuth]:
    """ Данные для авторизации пользователя (логин и пароль) """
    users_data = {UserType.ADMIN: UserAuth(
                      UserType.ADMIN, api_settings.init_admin_password.get_secret_value()),
                  UserType.SYSTEM: UserAuth(
                      UserType.SYSTEM, api_settings.init_system_password.get_secret_value()),
                  UserType.DIRECTOR: UserAuth(
                      api_settings.init_director_login,
                      api_settings.init_director_password.get_secret_value()),
                  UserType.USER: UserAuth(
                      api_settings.init_user_login,
                      api_settings.init_user_password.get_secret_value())}
    return users_data


@pytest.fixture(autouse=True, scope='session')
def setup():
    # Перед началом теста тестовая база удаляется,
    if os.path.exists('db-test.sqlite3'):
        os.remove('db-test.sqlite3')

    alembic_cfg = alembic.config.Config('alembic.ini')
    # и с помощью alembic инициируется новая тестовая база.
    alembic.command.upgrade(alembic_cfg, 'head')
    yield
   
   
@pytest.fixture()
def db_session():
    yield session
    session.close()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture(scope='session')
def api_settings():
    return settings
