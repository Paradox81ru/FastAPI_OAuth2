
from typing import Annotated

from fastapi import APIRouter, Depends, Security

from Auth.dependencies import get_current_user_and_scope, check_role, check_scope, is_auth, is_not_auth
from Auth.schemas import User, AnonymUser
from Auth.schemas import UserRoles

router = APIRouter(
    prefix='/test',
    tags=['test'])


@router.get("/users/me", dependencies=[Security(check_scope, scopes=['me'])])
async def reader_users_me(user_and_scope: Annotated[tuple[User, list], Depends(get_current_user_and_scope)]):
    current_user, scope = user_and_scope
    return  {"status": "ok", "username": current_user.username, "role": current_user.get_role() }


@router.get("/users/me/items", dependencies=[Security(check_scope, scopes=['me', 'items'])])
async def read_own_items(user_and_scope: Annotated[tuple[User, list], Depends(get_current_user_and_scope)]):
    current_user, scope = user_and_scope
    return  {"status": "ok", "username": current_user.username, "role": current_user.get_role() }


@router.get("/status")
async def read_system_status(user_and_scope: Annotated[tuple[User, list], Depends(get_current_user_and_scope)]):
    current_user, scope = user_and_scope
    return {"status": "ok", "username": current_user.username, "role": current_user.get_role()}


@router.get("/only_admin", dependencies=[Depends(check_role([UserRoles.admin]))])
async def read_only_admin(user_and_scope: Annotated[tuple[User, list], Depends(get_current_user_and_scope)]):
    current_user, scope = user_and_scope
    return {"status": "ok", "role": current_user.get_role()}


@router.get("/only_director", dependencies=[Depends(check_role([UserRoles.director]))])
async def read_only_director(user_and_scope: Annotated[tuple[User, list], Depends(get_current_user_and_scope)]):
    current_user, scope = user_and_scope
    return {"status": "ok", "role": current_user.get_role()}


@router.get("/authorized_user", dependencies=[Depends(is_auth)])
async def read_authorized_user(user_and_scope: Annotated[tuple[User, list], Depends(get_current_user_and_scope)]):
    current_user, scope = user_and_scope
    return {"status": "ok", "username": current_user.username,  "role": current_user.get_role()}


@router.get("/not_authorized_user", dependencies=[Depends(is_not_auth)])
async def read_authorized_user(user_and_scope: Annotated[tuple[User, list], Depends(get_current_user_and_scope)]):
    current_user, scope = user_and_scope
    return {"status": "ok", "role": current_user.get_role()}