from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import db_master


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_master.dispose()

app = FastAPI()

@app.get("/")
async def root():
    return {str(db_master.engine.url)}