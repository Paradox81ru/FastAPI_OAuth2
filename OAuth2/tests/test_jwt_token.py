from datetime import datetime, timedelta
from typing import final
from sqlalchemy import select, func
from Auth.db.models.user import User
from Auth.db.models.user_manager import UserManager
from Auth.db.models.jwt_token import JWTToken
from Auth.db.models.jwt_token_manager import JWTTokenManager, settings
from sqlalchemy.orm import Session
import uuid

from config import Settings
from tests.conftest import db_session


class TestJwtToken:
    """ Тестирует работу с JWT токенами. """
    @classmethod
    def _add_jwt_token(cls, db_session: Session, lifetime: int, username: str):
        """
        Добавляет данные о JWT токене.
        :param db_session: Сессия для работы с БД.
        :param lifetime: Время истечения срока токена в минутах.
        :param username: Имя пользователя, на которого выписывается токен.
        :return : Уникальный UUID код токена.
        :raises AssertionError:
        """
        jwt_token_manger = JWTTokenManager(db_session)
        jti = uuid.uuid4()
        data_expire = datetime.now() + timedelta(minutes=lifetime)
        jwt_token_manger.add_jwt_token(jti, data_expire, username)
        assert jwt_token_manger.has_jwt_token(jti)
        return jti

    def test_jwt_token(self, db_session: Session, api_settings: Settings):
        """
        Тестирует создание, поиск и удаление JWT токенов.
        :param db_session:  Сессия для работы с БД.
        :param api_settings: Настройки приложения.
        :raises AssertionError:
        """
        jwt_token_manager = JWTTokenManager(db_session)
        user_manager = UserManager(db_session)
        username: final = api_settings.init_user_login

        jti = uuid.uuid4()
        assert not jwt_token_manager.has_jwt_token(jti)

        self._add_jwt_token(db_session, -1, username)
        jti = self._add_jwt_token(db_session, -1, username)

        # Общее количество токенов у пользователя.
        token_count = jwt_token_manager.get_user_jwt_token_count(username)
        assert token_count == 2

        # token: JWTToken = jwt_token_manager.get_jwt_token(jti)
        # user: User = token.subject
        user = user_manager.get_user_by_jwt_token(jti)
        assert user.username == username
        assert len(user.jwt_tokens) == 2

        jwt_token_manager.remove_user_jwt_tokens(user.username)
        user = user_manager.get_user_by_username(username)
        assert len(user.jwt_tokens) == 0

    def test_remove_expire_tokens(self, db_session: Session, api_settings: Settings):
        """
        Тестирует удаление просроченных JWT токенов.
        :param db_session:  Сессия для работы с БД.
        :param api_settings: Настройки приложения.
        :raises AssertionError:
        """
        jwt_token_manger = JWTTokenManager(db_session)
        username: final = settings.init_director_login

        self._add_jwt_token(db_session, -2, username)
        self._add_jwt_token(db_session, -1, username)
        jti = self._add_jwt_token(db_session, 1, username)

        # У пользователя должно быть три токена.
        assert jwt_token_manger.get_user_jwt_token_count(username) == 3

        jwt_token_manger.remove_expire_token()
        # У пользователя должен остаться один токен.
        assert jwt_token_manger.get_user_jwt_token_count(username) == 1

        # Удаляется последний токен.
        jwt_token_manger.remove_jwt_token(jti)
        assert jwt_token_manger.get_user_jwt_token_count(username) == 0