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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)