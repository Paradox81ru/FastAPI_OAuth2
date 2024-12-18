from typing import Annotated
from config import templates
from fastapi import APIRouter, Form, Request, Depends, HTTPException

router = APIRouter(
    prefix="",
    tags=["html"]
)

@router.get("/index")
async def main(request: Request):
    """ Главная HTML страница. """
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
