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