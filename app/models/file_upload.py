from sqlalchemy import Column, String, Integer, DateTime, Float, func

from config import config

class FileUpload(config.Base):
    __tablename__ = 'file_upload'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), index=True)
    row_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    time_to_process = Column(Float)
