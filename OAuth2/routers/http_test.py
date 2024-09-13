
from OAuth2.schemas import UserRoles
from typing import Annotated
from fastapi import APIRouter, Depends, Security

from OAuth2.dependencies import get_current_user, check_role, is_auth, is_not_auth
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


@router.get("/only_admin", dependencies=[Depends(check_role([UserRoles.admin]))])
async def read_only_admin(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok", "role": current_user.get_role()}


@router.get("/only_director", dependencies=[Depends(check_role([UserRoles.director]))])
async def read_only_director(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok", "role": current_user.get_role()}


@router.get("/authorized_user", dependencies=[Depends(is_auth)])
async def read_authorized_user(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok", "role": current_user.get_role()}


@router.get("/not_authorized_user", dependencies=[Depends(is_not_auth)])
async def read_authorized_user(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok", "role": current_user.get_role()}