import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.dependencies import get_db
from app.tests.test_dependencies import override_get_db

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_list_files():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:

        response = await ac.get('/files/list')
        assert response.status_code == 200
        default_data = response.json()
        assert default_data['page'] == 1
        assert default_data['items_per_page'] == 10

        custom_page = 2
        custom_items_per_page = 5
        response = await ac.get(f'/files/list?page={custom_page}&items_per_page={custom_items_per_page}')
        assert response.status_code == 200
        custom_data = response.json()
        assert custom_data['page'] == custom_page
        assert custom_data['items_per_page'] == custom_items_per_page
        assert len(custom_data['data']) <= custom_items_per_page

        response = await ac.get('/files/list?page=1000&items_per_page=5')
        assert response.status_code == 200
        out_of_range_data = response.json()
        assert out_of_range_data['data'] == []
