import time

import polars as pl
from sqlalchemy.orm import Session
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query

from app.dependencies import get_db
from app.models.debt import Debt
from app.models.file_upload import FileUpload
from app.helpers.rename_columns import rename_columns
from app.schemas.file_upload_schema import FileUploadSchema
from app.schemas.file_upload_schema import FileUploadSchema, PaginatedFileResponse

router = APIRouter()

@router.get('/list', response_model=PaginatedFileResponse)
async def list_files(page: int = Query(default=1, ge=1), items_per_page: int = Query(default=10, ge=1),db: Session = Depends(get_db)):
    skip = (page - 1) * items_per_page
    with db as session:
        total_items = session.query(FileUpload).count()
        total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page else 0)

        files = session.query(FileUpload).offset(skip).limit(items_per_page).all()

        files_data = [FileUploadSchema.model_validate(file) for file in files]

        return PaginatedFileResponse(
            data=files_data,
            page=page,
            items_per_page=items_per_page,
            total_items=total_items,
            total_pages=total_pages
        )


@router.post('/upload')
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail='Invalid file type')

    df = pl.read_csv(file.file)
    df = rename_columns(df)

    with db as session:
        file_log = FileUpload(file_name=file.filename, row_count=len(df))
        session.add(file_log)
        session.flush()

        debts_data = df.to_dicts()
        for debt_data in debts_data:
            debt_data['file_upload_id'] = file_log.id

        start_time = time.time()
        session.bulk_insert_mappings(Debt, debts_data)
        end_time = time.time()
        session.commit()

        total_time = end_time - start_time

        return {'filename': file.filename, 'rows': len(df), 'log_id': file_log.id , 'total_time_to_add': total_time}

