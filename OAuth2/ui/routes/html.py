from typing import Annotated

from sqlalchemy.orm import Session

from Auth.db.models.jwt_token_manager import JWTTokenManager
from Auth.db.models.user_manager import UserManager
from Auth.dependencies import get_db_session, get_form_data
from Auth.schemas import FormData
from config import templates
from fastapi import APIRouter, Form, Request, Depends, HTTPException

router = APIRouter(
    prefix="",
    tags=["html"]
)

@router.get("/index")
async def main(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@router.post("/index")
async def get_tokens(db_session: Annotated[Session, Depends(get_db_session)], request: Request,
                     form_data: Annotated[FormData, Depends(get_form_data)]):
    user_manager = UserManager(db_session)
    jwt_token_manager = JWTTokenManager(db_session)
    user = user_manager.get_authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = jwt_token_manager.create_access_token(user.username, data={'scopes': form_data.scope})
    refresh_token = jwt_token_manager.create_refresh_token(user.username)
    return templates.TemplateResponse(
        request=request, name="tokens_show.html", context={"access_token": access_token,"refresh_token": refresh_token,
                                                           "scopes": form_data.scope}
    )