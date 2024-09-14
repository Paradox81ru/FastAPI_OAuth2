from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from OAuth2.config import get_settings
from OAuth2.dependencies import get_db_session, validate_refresh_token
from OAuth2.schemas import Token
from OAuth2.db.crud import add_jwt_token, remove_jwt_token
from OAuth2.utils import authenticate_user, create_access_token, create_refresh_token

settings = get_settings()

router = APIRouter(
    prefix='/oauth',
    tags=['oauth'])

@router.post("/token")
async def login_for_access_token(db_session: Annotated[Session, Depends(get_db_session)], 
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
    """ Выдача токена доступа при авторизации """
    user = authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    print(request)
    jti_a, expire_a, access_token = create_access_token(user.username, data={'scopes': form_data.scopes})
    jti_r, expire_r, refresh_token = create_refresh_token(user.username)
    add_jwt_token(db_session, jti_a, expire_a, user.username)
    add_jwt_token(db_session, jti_r, expire_r, user.username)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/token-refresh")
async def refresh_access_token(db_session: Annotated[Session, Depends(get_db_session)], payload: Annotated[dict, Depends(validate_refresh_token)]):
    """ Обновление токена доступа """
    jti = payload.get('jti')
    username = payload.get('sub')
    scopes = payload.get('scopes')

    jti_a, expire_a, access_token = create_access_token(username, data={'scopes': scopes})
    jti_r, expire_r, refresh_token = create_refresh_token(username)
    add_jwt_token(db_session, jti_a, expire_a, username)
    add_jwt_token(db_session, jti_r, expire_r, username)
    remove_jwt_token(db_session, jti)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")