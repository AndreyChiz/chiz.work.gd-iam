import pytest


@pytest.mark.asyncio
async def test_ping(async_client):
    response = await async_client.get(
        "/v1/user",
    )
    assert response.status_code == 200
