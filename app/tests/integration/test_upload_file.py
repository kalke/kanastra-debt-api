import os
import uuid
import shutil
from datetime import date

import pytest
import polars as pl
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.dependencies import get_db
from app.tests.test_dependencies import override_get_db

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_upload_file():

    df = pl.DataFrame({
        'name': ['henrique', 'kanastra'],
        'governmentId': ['123456789', '987654321'],
        'email': ['email1@example.com', 'email2@example.com'],
        'debtAmount': [1000.50, 2000.75],
        'debtDueDate': [date(2023, 1, 1), date(2023, 12, 31)],
        'debtId': [str(uuid.uuid4()), str(uuid.uuid4())]
    })

    if not os.path.exists('./tmp/'):
        os.makedirs('./tmp/')

    df.write_csv('./tmp/test.csv')

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        files = {'file': ('test.csv', './tmp/test.csv', 'text/csv')}
        response = await ac.post('/files/upload', files=files)

        assert response.status_code == 200

    shutil.rmtree('./tmp/')
