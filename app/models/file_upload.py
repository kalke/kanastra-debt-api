import enum
from sqlalchemy import Column, String, Integer, DateTime, Float, Enum, func

from config import config

class UploadStatus(enum.Enum):

    UPLOADING = 'UPLOADING'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'

class FileUpload(config.Base):
    __tablename__ = 'file_upload'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), index=True)
    row_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    upload_status =  Column(Enum(UploadStatus), default=UploadStatus.UPLOADING)
    time_to_process = Column(Float, nullable=True)
