from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_master.dispose()


@app.get("/")
async def root():
    return {str(db_master.engine.url)}



