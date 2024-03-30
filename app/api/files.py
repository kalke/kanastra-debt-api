import time

import polars as pl
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query

from app.dependencies import get_db
from app.models.debt import Debt
from app.models.file_upload import FileUpload, UploadStatus
from app.helpers.rename_columns import rename_columns
from app.schemas.file_upload_schema import FileUploadSchema
from app.schemas.file_upload_schema import FileUploadSchema, PaginatedFileResponse

router = APIRouter()

@router.get('/list', response_model=PaginatedFileResponse)
async def list_files(page: int = Query(default=1, ge=1), items_per_page: int = Query(default=10, ge=1), db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * items_per_page
    async with db as session:
        result = await session.execute(select(func.count(FileUpload.id)))
        total_items = result.scalar_one()
        total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page else 0)

        result = await session.execute(select(FileUpload).offset(skip).limit(items_per_page))
        files = result.scalars().all()

        files_data = [FileUploadSchema.model_validate(file) for file in files]

        return PaginatedFileResponse(
            data=files_data,
            page=page,
            items_per_page=items_per_page,
            total_items=total_items,
            total_pages=total_pages
        )


@router.post('/upload')
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail='Invalid file type')

    df = pl.read_csv(file.file)
    df = rename_columns(df)

    async with db as session:
        file_log = FileUpload(file_name=file.filename, row_count=len(df), upload_status=UploadStatus.UPLOADING)
        session.add(file_log)
        await session.commit()

        try:
            debts_data = df.to_dicts()
            start_time = time.time()

            async with session.begin():
                BATCH_SIZE = 1000
                for i in range(0, len(debts_data), BATCH_SIZE):
                    batch = debts_data[i:i + BATCH_SIZE]
                    await session.run_sync(lambda session: session.bulk_insert_mappings(Debt, [{**debt, 'file_upload_id': file_log.id} for debt in batch]))

            end_time = time.time()

            file_log = await session.get(FileUpload, file_log.id)
            if file_log:
                file_log.time_to_process = end_time - start_time
                file_log.upload_status = UploadStatus.SUCCESS
                await session.commit()

        except Exception as ex:
            await session.rollback()
            if file_log:
                file_log.upload_status = UploadStatus.FAILED
                await session.commit()

            raise HTTPException(status_code=500, detail='An error occurred during file processing') from ex

        return {'filename': file.filename, 'rows': len(df), 'log_id': file_log.id, 'total_time_to_add': file_log.time_to_process}
