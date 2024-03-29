import uuid

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from config import config


class Debt(config.Base):
    __tablename__ = 'debt'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    government_id = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    debt_amount = Column(Integer, nullable=False)
    debt_due_date = Column(Date, nullable=False)
    file_upload_id = Column(Integer, ForeignKey('file_upload.id'))

    file_upload = relationship('FileUpload')
