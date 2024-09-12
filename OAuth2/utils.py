from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
import jwt
from OAuth2.config import get_settings
from OAuth2.db.models.user import User, UserBuilder
from OAuth2.dependencies import get_db_session
from OAuth2.schemas import UserRoles
from OAuth2.db.crud import add_users, get_user_schema_by_username
from sqlalchemy.orm import Session

settings = get_settings()


def init_users(db: Session):
    """ Добавление пользователей при первой инициализации базы данных """
    user_admin = UserBuilder('Admin', 'paradox81ru@yandex.ru').role(UserRoles.admin).set_password('Cucumber_123').build()
    user_system = UserBuilder('System', 'paradox81ru@gmail.com').role(UserRoles.system).set_password('Cucumber_123').build()
    user_paradox = UserBuilder('Paradox', 'paradox81ru@mail.ru').name("Жорж", "Парадокс") \
                                .role(UserRoles.director).set_password('Cucumber_123').build()
    user_user = UserBuilder("User", 'paradox81ru@hotmail.com').name('Пользователь').set_password('Cucumber_123').build()
    users = (user_admin, user_system, user_paradox, user_user)
    add_users(db, users)


def authenticate_user(db_session: Annotated[Session, Depends(get_db_session)], username: str, password: str):
    """ Возвращет авторизованного пользователя """
    user = get_user_schema_by_username(db_session, username)
    if user is None or not user.check_password(password):
        return False
    return user.to_user()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """ Создаёт и возвращает JWT токен """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) \
        + (expires_delta if expires_delta is not None else timedelta(minutes=15))
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
    return encode_jwt