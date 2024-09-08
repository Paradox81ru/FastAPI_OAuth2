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
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from config import get_settings
from schemas import Token, TokenData, User, UserInDB
from db.database import Base, engine
from db import models
import uvicorn


settings = get_settings()


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": True,
    },
}


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={"me": "Read information about the current user.", "items": "Read items."}
)

models.Base.metadata.create_all(engine)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) \
        + (expires_delta if expires_delta is not None else timedelta(minutes=15))
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
    return encode_jwt


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise AuthenticateException("Could not validate credentials", authenticate_value)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise AuthenticateException("Not enough permissions", authenticate_value)
        return user


async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=['me'])]):
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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