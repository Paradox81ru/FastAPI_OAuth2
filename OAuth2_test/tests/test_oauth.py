from starlette.testclient import TestClient

from tests.conftest import UserType, UserAuth, UserRoles, UerStatus, get_access_token
import httpx

""" 
!!!!                                                ВАЖНО                                                       !!!! 
!!!! Для работы данных тестов требуется, чтобы был запущен сервер авторизации. Причем надо учитывать,           !!!! 
!!!! что при запуске сервера авторизации, он запускается не с тестовыми параметрами, а с рабочими,              !!!! 
!!!! поэтому логины и пароли проверяются из рабочей базы. Соответственно в conftest-е Oauth2Settings настройки  !!!! 
!!!! загружаются не из tests/.env, а из Auth/.env.                                                              !!!!
"""

class TestPermissions:
    def test_get_user(self, client: TestClient, oauth_server, users_data, api_settings, oauth2_settings):
        """ Поверяет получение пользователя """
        token = get_access_token(users_data[UserType.USER], oauth_server, [])
        headers = {'Authorization': f"Bearer {token}"}
        response = client.get("/api/test/get_user", headers=headers)
        assert response.status_code == 200
        user, scopes = response.json()
        assert user['username'] == users_data[UserType.USER].username
        assert user['role'] == UserRoles.visitor
        assert user['status'] == UerStatus.ACTIVE

    def test_get_anonym_user(self, client: TestClient, oauth_server, users_data, api_settings, oauth2_settings):
        """ Поверяет получение пользователя """
        response = client.get("/api/test/get_user")
        assert response.status_code == 200
        user, scopes = response.json()
        assert user['username'] == 'Anonym'
        assert user['role'] == UserRoles.visitor
        assert user['status'] == UerStatus.ACTIVE

    def test_get_user_damaged_token_negative(self, client: TestClient, oauth_server, users_data, api_settings, oauth2_settings):
        """ Поверяет попытку получение пользователя с повреждённым токеном """
        # Немного изменяется токен доступа.
        token = get_access_token(users_data[UserType.USER], oauth_server, []) + "!"
        headers = {'Authorization': f"Bearer {token}"}
        response = client.get("/api/test/get_user", headers=headers)
        assert response.status_code == 401
        error = response.json()['detail']
        assert error == "The JWT token is damaged"

    def test_get_user_not_bearer_negative(self, client: TestClient, oauth_server, users_data, api_settings, oauth2_settings):
        """ Поверяет попытку получение пользователя с неправильной авторизацией """
        # В заголовке неправильно указан тип авторизации
        token = get_access_token(users_data[UserType.USER], oauth_server, []) + "!"
        headers = {'Authorization': f"Beare {token}"}
        response = client.get("/api/test/get_user", headers=headers)
        assert response.status_code == 401
        error = response.json()['detail']
        assert error == "Not bearer authentication"
