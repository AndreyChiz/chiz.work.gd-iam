from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import db_master


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_master.dispose()


@app.get("/")
async def root():
    return {str(db_master.engine.url)}
