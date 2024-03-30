from enum import Enum
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class UploadStatus(str, Enum):
    UPLOADING = 'UPLOADING'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'


class FileUploadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    file_name: str
    row_count: int
    created_at: Optional[datetime] = None
    upload_status: UploadStatus
    time_to_process: Optional[float] = None


class PaginatedFileResponse(BaseModel):
    data: List[FileUploadSchema]
    page: int
    items_per_page: int
    total_items: int
    total_pages: int
