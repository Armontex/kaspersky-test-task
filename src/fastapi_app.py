from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config.settings import settings
from .services.analyzer.api.routers import router as analyzer_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        yield
    finally:
        pass


def create_app():
    app = FastAPI(debug=settings.debug, lifespan=lifespan)
    app.include_router(analyzer_router)
    return app


app = create_app()
