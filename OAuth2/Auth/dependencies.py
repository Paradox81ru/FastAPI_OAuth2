import jwt
from fastapi import Depends, Form
from fastapi.security import SecurityScopes
from jwt.exceptions import ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from config import get_settings, oauth2_scheme
from Auth.db.db_connection import db_session
from Auth.exceptions import AuthenticateException
from Auth.schemas import AnonymUser, UerStatus, User, JWTTokenType, UserRoles, BaseUser
from Auth.db.models.user_manager import UserManager
from Auth.db.models.jwt_token_manager import JWTTokenManager

settings = get_settings()


def get_db_session():
    with db_session:
        try:
            yield db_session
        finally:
            db_session.close()


def _validate_token(session: Session, token: str, jwt_token_type: JWTTokenType) -> dict | None:
    """
    Проверят валидность токена, и если он валидный, то возвращает его содержимое
    :param session: сессия базы данных
    :param token: токен
    :param jwt_token_type: тип токена (доступа или обновления)
    :return: содержимое токена
    """

    jwt_token_manager = JWTTokenManager(session)
    if token is None:
        return None
    try:
        payload: dict = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=['HS256'])
        if payload.get('type') != jwt_token_type:
             raise AuthenticateException("The JWT token is damaged")
        jti: str = payload.get('jti')
        # Проверка, есть ли этот токен в базе.
        if not jwt_token_manager.has_jwt_token(jti):
            # Если нет, то токен не валидный.
            raise AuthenticateException("Could not validate credentials")
        # Если в токене не указан пользователь, то токен не валидный.
        if payload.get('sub') is None:
            raise AuthenticateException("Could not validate credentials")
        return payload
    except ExpiredSignatureError as err:
        # Если токен просрочен, то он всё равно раскодируется, чтобы найти JTI токена,    
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=['HS256'],
                             options={"verify_signature": False})
        # по которому он удаляется из базы данных.
        jwt_token_manager.remove_jwt_token(payload.get('jti'))
        raise AuthenticateException("The JWT token is expired")
    except (jwt.InvalidTokenError, ValidationError):
        raise AuthenticateException("The JWT token is damaged")


async def validate_access_token(session: Annotated[Session, Depends(get_db_session)],
                                token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """
    Проверяет валидность токена доступа
    :param session: сессия базы данных
    :param token: токен доступа
    :return:
    """
    return _validate_token(session, token, JWTTokenType.ACCESS)


async def validate_refresh_token(session: Annotated[Session, Depends(get_db_session)],
                                 token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """
    Проверяет валидность токена обновления
    :param session: сессия базы данных
    :param token: токен обновления
    :return:
    """
    return _validate_token(session, token, JWTTokenType.REFRESH)


async def get_current_user(session: Annotated[Session, Depends(get_db_session)],
                           payload: Annotated[dict, Depends(validate_access_token)]) -> (BaseUser, list):
    """
    Возвращает пользователя по токену доступа, или анонимного пользователя,
    если токена доступа не было предоставлено вообще
    :param session: сессия базы данных
    :param payload: содержимое токена
    :return: Пользователя и его scope (сфера деятельности)
    :raises AuthenticateException: Не удалось подтвердить учётные данные; Пользователь не доступен.
    """
    user_manager = UserManager(session)
    if payload is None:
        return AnonymUser(), None
    username: str = payload.get('sub')
    scopes = payload.get('scopes')
    user: User = user_manager.get_user_schema_by_username(username).to_user()
    if not user:
        raise AuthenticateException("Could not validate credentials")
    if user.status != UerStatus.ACTIVE:
        raise AuthenticateException("Inactive user")
    return user, scopes


def check_scope(payload: Annotated[dict, Depends(validate_access_token)], security_scopes: SecurityScopes):
    """
    Проверяет scopes
    :param payload: содержимое токена
    :param security_scopes: scope для проверки
    :raises AuthenticateException: Не достаточно прав
    """
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    if len(security_scopes.scopes) == 0:
        return
    if payload is None:
        raise AuthenticateException("Not enough permissions", authenticate_value)
    token_scopes = payload.get('scopes', [])
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise AuthenticateException("Not enough permissions", authenticate_value)


def check_role(allowed_roles: tuple[str, ...] | list[str] | list[UserRoles]):
    """
    Проверяет роль пользователя
    :param allowed_roles: ролли для проверки
    :return:
    :raises AuthenticateException: не достаточно прав
    """
    def _check_role(user: Annotated[User, Depends(get_current_user)]):
        if user.role in allowed_roles:
            return True
        raise AuthenticateException("Not enough permissions", "Bearer")
    return _check_role


def is_auth(user: Annotated[User, Depends(get_current_user)]):
    """
    Проверят на авторизованного пользователя
    :param user: текущий пользователь
     :raises AuthenticateException: не авторизован
    """
    if isinstance(user, AnonymUser):
        raise AuthenticateException("Not authorized", "Bearer")


def is_not_auth(user: Annotated[User, Depends(get_current_user)]):
    """
    Проверят на неавторизованного пользователя
    :param user: текущий пользователь
    :return:
    """
    if isinstance(user, User):
        raise AuthenticateException(f"Already authorized username '{user.username}' role {user.get_role()}",
                                    "Bearer")