import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.authentication import AuthenticationMiddleware

from config import get_settings
from fastapi_site.middlewares.authentication import JWTTokenAuthBackend
from fastapi_site.routers import http_test
from ui.routes import html

settings = get_settings()

app = FastAPI()

app.mount("/static", StaticFiles(directory="ui/static"), name="static")
app.include_router(http_test.router, prefix="/api")
app.include_router(html.router, prefix="")
app.add_middleware(AuthenticationMiddleware, 
                   backend=JWTTokenAuthBackend(settings.auth_server),
                   on_error=lambda conn, exc: JSONResponse({"detail": str(exc)}, status_code=401)
                   )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
