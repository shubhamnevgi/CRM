from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.base import Base
from app import models  # noqa: F401
from app.db.session import engine
from app.routes import api_router

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get('/health', tags=['Health'])
def health_check() -> dict[str, str]:
    return {'status': 'ok'}


@app.on_event('startup')
def on_startup() -> None:
    # For local bootstrap. In production use Alembic migrations.
    Base.metadata.create_all(bind=engine)
