from datetime import datetime, timedelta
from typing import final
from sqlalchemy import select, func
from OAuth2.db import models
from sqlalchemy.orm import Session
from OAuth2.db import crud
import uuid


def _add_jwt_token(db_session: Session, lifetime: int, username: str):
    """
    Добавляеет данные о JWT токене
    :param db_session: сессия базы данных
    :param jti: уникальный UUID код JWT токена
    :param lifetime: время истечения срока токена в минутах
    :param username: имя пользователя, на которого выписывается токен
    :return : уникальный UUID код токена
    """
    jti = uuid.uuid4()
    data_expire = datetime.now() + timedelta(minutes=lifetime)
    crud.add_jwt_token(db_session, jti, data_expire, username)
    assert crud.has_jwt_token(db_session, jti)
    return jti



def test_jwt_token(db_session: Session):
    """ Тестирвет создание, поиск и удаление JWT токенов """
    username: final = 'User'

    jti = uuid.uuid4()
    assert not crud.has_jwt_token(db_session, jti)

    _add_jwt_token(db_session, -1, username)
    jti = _add_jwt_token(db_session, -1, username)

    # Общее количество токенов у пользователя.
    token_count = crud.get_user_jwt_token_count(db_session, username)
    assert token_count == 2

    token: models.JWTToken = crud.get_jwt_token(db_session, jti)   
    user: models.User = token.subject
    assert user.username == username
    assert len(user.jwt_tokens) == 2

    crud.remove_user_jwt_tokens(db_session, user.username)
    user = crud.get_user_by_username(db_session, username)
    assert len(user.jwt_tokens) == 0


def test_remove_expire_tokens(db_session: Session):
    """ Тестирует удаление просроченных JWT токенов """
    username: final = 'Paradox'

    _add_jwt_token(db_session, -2, username)
    _add_jwt_token(db_session, -1, username)
    jti =_add_jwt_token(db_session, 1, username)

    # У пользователя должно быть три токена.
    assert crud.get_user_jwt_token_count(db_session, username) == 3

    crud.remove_expire_token(db_session)
    # У пользователя должен остаться один токен.
    assert crud.get_user_jwt_token_count(db_session, username) == 1

    # Удаляется последний токен.
    crud.remove_jwt_token(db_session, jti)
    assert crud.get_user_jwt_token_count(db_session, username) == 0