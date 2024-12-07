from fastapi import HTTPException, Header, Depends, Request
from typing import Annotated
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from fastapi_site.utils import get_authorization_scheme_param


# async def validate_jwt_token(request: Request) -> str| None:
#     authorization = request.headers.get("Authorization")
#     scheme, _ = get_authorization_scheme_param(authorization)
#     if not authorization or scheme.lower() != "bearer":
#             return None
#     return authorization