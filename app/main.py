from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import db_master
from app.api import api_v1_router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_master.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router, prefix=settings.api.api_v1.prefix)


@app.get("/")
async def root():
    return {str(db_master.engine.url)}