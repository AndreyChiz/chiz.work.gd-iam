
import pytest
from httpx import AsyncClient

@pytest.fixture
async def async_client():
    async with AsyncClient(base_url="http://localhost:8000/") as ac:
        yield ac