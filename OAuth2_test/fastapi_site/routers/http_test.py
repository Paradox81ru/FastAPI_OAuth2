from typing import Annotated
from fastapi import APIRouter, Depends, Request

# from fastapi_site.dependencies import validate_jwt_token
from OAuth2_test.fastapi_site.schemas import AnonymUser, User
import httpx

router = APIRouter(
    prefix="/test",
    tags=['test']
)

# @router.get("/get_user")
# async def get_user(bearer_authorization: Annotated[User | AnonymUser, Depends(validate_jwt_token)]):
#     if bearer_authorization == None:
#         return AnonymUser()
#     api_url = "http://127.0.0.1:8001/api/test/get_user"
#     async with httpx.AsyncClient() as client:
#         response = await client.get(api_url, headers={"Authorization": bearer_authorization})
#         user = response.json()
#         return User(**user)
#     return AnonymUser()


@router.get("/my-test")
async def my_test(request: Request):
    user = request.user
    return user


# @router.get("/users/me", dependencies=[Security(check_scope, scopes=['me'])])
# async def reader_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return  {"status": "ok", "username": current_user.username, "role": current_user.get_role() }


# @router.get("/users/me/items", dependencies=[Security(check_scope, scopes=['me', 'items'])])
# async def read_own_items(current_user: Annotated[User, Depends(get_current_user)]):
#     return  {"status": "ok", "username": current_user.username, "role": current_user.get_role() }


# @router.get("/status")
# async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"status": "ok", "username": current_user.username, "role": current_user.get_role()}


# @router.get("/only_admin", dependencies=[Depends(check_role([UserRoles.admin]))])
# async def read_only_admin(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"status": "ok", "role": current_user.get_role()}


# @router.get("/only_director", dependencies=[Depends(check_role([UserRoles.director]))])
# async def read_only_director(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"status": "ok", "role": current_user.get_role()}


# @router.get("/authorized_user", dependencies=[Depends(is_auth)])
# async def read_authorized_user(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"status": "ok", "username": current_user.username,  "role": current_user.get_role()}


# @router.get("/not_authorized_user", dependencies=[Depends(is_not_auth)])
# async def read_authorized_user(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"status": "ok", "role": current_user.get_role()}