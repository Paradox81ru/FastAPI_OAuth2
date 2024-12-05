import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from fastapi_site.middlewares.authentication import JWTTokenAuthBackend
from fastapi_site.routers import http_test

app = FastAPI()

app.include_router(http_test.router, prefix="/api")
app.add_middleware(AuthenticationMiddleware, 
                   backend=JWTTokenAuthBackend(),
                   on_error=lambda conn, exc: JSONResponse({"detail": str(exc)}, status_code=401)
                   )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)