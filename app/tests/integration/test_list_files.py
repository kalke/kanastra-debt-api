import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_list_files():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/files/list")
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert 'page' in data
        assert 'items_per_page' in data
        assert 'total_items' in data
        assert 'total_pages' in data