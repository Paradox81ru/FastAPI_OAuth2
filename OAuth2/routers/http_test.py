
from OAuth2.schemas import UserRoles
from typing import Annotated
from fastapi import APIRouter, Depends, Security

from OAuth2.dependencies import get_current_user
from OAuth2.schemas import User


router = APIRouter(
    prefix='/test',
    tags=['test'])


@router.get("/users/me", response_model=User)
async def reader_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/users/me/items")
async def read_own_items(current_user: Annotated[User, Security(get_current_user, scopes=['items'])]):
    return  [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/status")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok", "role": current_user.get_role()}

