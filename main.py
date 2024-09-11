from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Dict
from typing_extensions import Annotated, Doc

import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

from sqlalchemy.orm import Session

from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
# from OAuth2.config import pwd_context
from OAuth2.config import get_settings
from OAuth2.schemas import Token, TokenData, User, AnonymUser, UserInDB, UerStatus
from OAuth2.db.db_connection import engine
from OAuth2.db import models
from OAuth2.db.crud import get_user_schema_by_username
from OAuth2.dependencies import get_db_session
import uvicorn


settings = get_settings()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={"me": "Read information about the current user.", "items": "Read items."}
)

# models.Base.metadata.create_all(engine)

app = FastAPI()


def get_user(db_session: Annotated[Session, Depends(get_db_session)], username: str):
    return get_user_schema_by_username(db_session, username)
    # if username in db:
    #     user_dict = db[username]
    #     return UserInDB(**user_dict)


def authenticate_user(db_session: Annotated[Session, Depends(get_db_session)], username: str, password: str):
    user = get_user(db_session, username)
    if isinstance(user, AnonymUser) or not user.check_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) \
        + (expires_delta if expires_delta is not None else timedelta(minutes=15))
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
    return encode_jwt


async def get_current_user(db_session: Annotated[Session, Depends(get_db_session)], security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' \
        if security_scopes.scopes else "Bearer"
    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm])
        username: str = payload.get('sub')
        if username is None:
            raise AuthenticateException("Could not validate credentials", authenticate_value)
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise AuthenticateException("Could not validate credentials", authenticate_value)
    user = get_user(db_session, username=token_data.username)
    if user is None:
        raise AuthenticateException("Could not validate credentials", authenticate_value)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise AuthenticateException("Not enough permissions", authenticate_value)
        return user


async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=['me'])]):
    if current_user.status != UerStatus.ACTIVE :
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(db_session: Annotated[Session, Depends(get_db_session)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expire = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': user.username, 'scopes': form_data.scopes},
        expires_delta=access_token_expire
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def reader_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: Annotated[User, Security(get_current_active_user, scopes=['items'])]):
    return  [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}


class AuthenticateException(HTTPException):
    def __init__(self, detail: str, authenticate_value):
        headers={"WWW-Authenticate": authenticate_value}
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)