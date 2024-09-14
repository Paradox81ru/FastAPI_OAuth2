from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError
from OAuth2.config import get_settings, oauth2_scheme
from OAuth2.db.crud import get_user_schema_by_username, has_jwt_token, remove_jwt_token
from OAuth2.db.db_connection import db_session
from typing_extensions import Annotated
from sqlalchemy.orm import Session

from OAuth2.schemas import AnonymUser, UerStatus, User, JWTTokenType

import jwt
import base64
from jwt.exceptions import ExpiredSignatureError

from OAuth2.exceptions import AuthenticateException

settings = get_settings()


def get_db_session():
    with db_session:
        try:
            yield db_session
        finally:
            db_session.close()



async def get_current_user(db_session: Annotated[Session, Depends(get_db_session)], security_scopes: SecurityScopes, 
                           token: Annotated[str, Depends(oauth2_scheme)]) -> AnonymUser | User:
    # Если токена нет, то это анонимный пользователь.
    if token is None:
        return AnonymUser()
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' \
        if security_scopes.scopes else "Bearer"
    try:
        payload: dict = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=['HS256'])
        # Актуален для проверки именно токен доступа.
        if payload.get('type') != JWTTokenType.ACCESS:
             raise AuthenticateException("Could not validate credentials", authenticate_value)
        jti: str = payload.get('jti')
        # Проверка, есть ли этот токен в базе.
        if not has_jwt_token(db_session, jti):
            # Если нет, то токен не валидный.
            raise AuthenticateException("Could not validate credentials", authenticate_value)
        username: str = payload.get('sub')
        if username is None:
            raise AuthenticateException("Could not validate credentials", authenticate_value)
        token_scopes = payload.get('scopes', [])
    except (ExpiredSignatureError) as err:
        # Если токен просрочен, то он всё равно раскодируется, чтобы найти JTI токена,    
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=['HS256'], options={"verify_signature": False})
        # по которому он удаляется из базы данных.
        remove_jwt_token(db_session, payload.get('jti'))
        raise AuthenticateException("JWT token is expired", authenticate_value)
    except (jwt.InvalidTokenError, ValidationError):
        raise AuthenticateException("Could not validate credentials", authenticate_value)
    user: User = get_user_schema_by_username(db_session, username).to_user()
    if not user:
        raise AuthenticateException("Could not validate credentials", authenticate_value)
    if user.status != UerStatus.ACTIVE:
        raise AuthenticateException("Inactive user", authenticate_value)
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise AuthenticateException("Not enough permissions", authenticate_value)
    return user


def check_role(allowed_roles: tuple[str, ...] | list[str]):
    """ Проверяет роль пользователя """
    def _check_role(user: Annotated[User, Depends(get_current_user)]):
        if user.role in allowed_roles:
            return True
        raise AuthenticateException("Not enough permissions", "Bearer")
    return _check_role


def is_auth(user: Annotated[User, Depends(get_current_user)]):
    """ Проверят на авторизованного пользователя """
    if isinstance(user, AnonymUser):
        raise AuthenticateException("Not authorized", "Bearer")


def is_not_auth(user: Annotated[User, Depends(get_current_user)]):
    """ Проверят на неавторизованного пользователя """
    if isinstance(user, User):
        raise AuthenticateException(f"Already authorized username '{user.username}' role {user.get_role()}", "Bearer")