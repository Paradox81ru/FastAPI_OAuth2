import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import get_settings
from Auth.routers import auth, http_test
from ui.routes import html

settings = get_settings()


# models.Base.metadata.create_all(engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="ui/static"), name="static")
app.include_router(auth.router, prefix='/api')
app.include_router(http_test.router, prefix='/api')
app.include_router(html.router, prefix="")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)