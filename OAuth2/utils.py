from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
import jwt
import uuid
from uuid import UUID

from OAuth2.config import get_settings
from OAuth2.db.models.user import UserBuilder
from OAuth2.dependencies import get_db_session
from OAuth2.schemas import UserRoles, JWTTokenType, User
from OAuth2.db import crud
from sqlalchemy.orm import Session

settings = get_settings()


def init_users(db: Session):
    """ Добавление пользователей при первой инициализации базы данных """
    user_admin = UserBuilder('Admin', 'paradox81ru@yandex.ru').role(UserRoles.admin).set_password(settings.init_admin_password.get_secret_value()).build()
    user_system = UserBuilder('System', 'paradox81ru@gmail.com').role(UserRoles.system).set_password(settings.init_system_password.get_secret_value()).build()
    user_paradox = UserBuilder('Paradox', 'paradox81ru@mail.ru').name("Жорж", "Парадокс") \
                                .role(UserRoles.director).set_password(settings.init_director_password.get_secret_value()).build()
    user_user = UserBuilder("User", 'paradox81ru@hotmail.com').name('Пользователь').set_password(settings.init_user_password.get_secret_value()).build()
    users = (user_admin, user_system, user_paradox, user_user)
    crud.add_users(db, users)


def authenticate_user(db_session: Annotated[Session, Depends(get_db_session)], username: str, password: str):
    """ Возвращет авторизованного пользователя """
    user = crud.get_user_schema_by_username(db_session, username)
    if user is None or not user.check_password(password):
        return False
    return user.to_user()


def create_access_token(username: str, data: dict) -> tuple[UUID, str]:
    """ 
    Создаёт токен доступа
    :param username: имя пользователя, на которого выписывается токен доступа
    :param data: словарь с данными, которые нужно добавить в токен доступа
    :return : кортеж, где первое значение - uuid номер в формате UUID, 
                          второе значени - дата истесчения сркока токера, 
                          а третье значение это сам JWT токен в формате строки
    """
    token_expire = timedelta(minutes=settings.access_token_expire_minutes)
    return _sign_token(JWTTokenType.ACCESS, username, data, token_expire)


def create_refresh_token(username) -> tuple[UUID, str]:
    """ 
    Создаёт токен обновления
    :param username: имя пользователя, на которого выписывается токен обновления
    :return : кортеж, где первое значение - uuid номер в формате UUID, 
                          второе значени - дата истесчения сркока токера, 
                          а третье значение это сам JWT токен в формате строки
    """
    token_expire = timedelta(minutes=settings.refresh_token_expire_minutes)
    return _sign_token(JWTTokenType.REFRESH, username, {}, token_expire)


def _sign_token(type: JWTTokenType, username: str, data: dict[str, any], expires_delta: timedelta | None = None) -> tuple[UUID, str]:
    """
    Создёт JWT токен
    :param type: тип токена(access/refresh)
    :param subject: субъект, на которого выписывается токен;
    :param data: инфомация добавляемаяя в токен
    :param expires_delta: время жизни токена
    :return : кортеж, где первое значение - uuid номер в формате UUID, 
                          второе значени - дата истесчения сркока токера, 
                          а третье значение это сам JWT токен в формате строки
    """
    payload = data.copy()
    date_now = datetime.now(timezone.utc)
    expire =  (payload['nbf'] if 'nbf' in payload else date_now) + (expires_delta if expires_delta is not None else timedelta(minutes=15))
    jti = uuid.uuid4()

    _data = {'iss': "paradox81ru@mail.ru", 
             'sub': username, 
             'type': type,
             'jti': str(jti),
             'iat': date_now,
             'nbf': payload['nbf'] if 'nbf' in payload else date_now,
             'exp': expire
             }
    payload.update(_data)
    encode_jwt = jwt.encode(payload, settings.secret_key.get_secret_value(), algorithm="HS256")
    return jti, expire, encode_jwt
             