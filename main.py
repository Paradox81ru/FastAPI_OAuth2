from typing import Annotated, Any, Dict
from typing_extensions import Annotated

import jwt
from fastapi import Depends, FastAPI

from OAuth2.config import get_settings
from OAuth2.schemas import Token, User, AnonymUser, UserInDB, UerStatus
from OAuth2.db.db_connection import engine
from OAuth2.db import models
from OAuth2.db.crud import get_user_schema_by_username
from OAuth2.dependencies import get_current_user, get_db_session
from OAuth2.routers import auth, http_test
import uvicorn


settings = get_settings()


# models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(http_test.router, prefix='/api')

# @app.get("/users/me/", response_model=User)
# async def reader_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_user


# @app.get("/users/me/items")
# async def read_own_items(current_user: Annotated[User, Security(get_current_active_user, scopes=['items'])]):
#     return  [{"item_id": "Foo", "owner": current_user.username}]


# @app.get("/status/")
# async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)