from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileUploadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    file_name: str
    row_count: int
    created_at: Optional[datetime] = None
    time_to_process: float


class PaginatedFileResponse(BaseModel):
    data: List[FileUploadSchema]
    page: int
    items_per_page: int
    total_items: int
    total_pages: int
