from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from OAuth2.config import get_settings
from OAuth2.dependencies import get_db_session
from OAuth2.schemas import Token
from OAuth2.utils import authenticate_user, create_access_token

settings = get_settings()

router = APIRouter(
    prefix='/oauth',
    tags=['oauth'])

@router.post("/token")
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