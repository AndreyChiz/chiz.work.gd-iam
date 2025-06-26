import pytest
from fastapi import FastAPI, APIRouter, Depends
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master


@pytest.mark.asyncio
async def test_database_health():
    app = FastAPI()
    router = APIRouter()

    @router.get("/health/db")
    async def check_db(session: AsyncSession = Depends(db_master.session_getter)):
        await session.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database connected"}

    app.include_router(router)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Database connected"}
