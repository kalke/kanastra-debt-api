import io
import uuid

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_upload_file_integration():
    debt_id = str(uuid.uuid4())
    csv_content = f"governmentId,email,debtAmount,debtDueDate,debtId\n123,email@example.com,1000.0,2023-01-01,{debt_id}"
    byte_content = csv_content.encode('utf-8')
    file_object = io.BytesIO(byte_content)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = {'file': ('test.csv', file_object, 'text/csv')}
        response = await ac.post("/files/upload", files=files)

        assert response.status_code == 200

