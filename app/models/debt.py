import uuid

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from config import config


class Debt(config.Base):
    __tablename__ = 'debt'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    government_id = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    debt_amount = Column(Integer, nullable=False)
    debt_due_date = Column(Date, nullable=False)
    file_upload_id = Column(Integer, ForeignKey('file_upload.id'))
    debt_id = Column(String(36))

    file_upload = relationship('FileUpload')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'government_id': self.government_id,
            'email': self.email,
            'debt_amount': self.debt_amount,
            'debt_due_date': self.debt_due_date.isoformat(),
            'file_upload_id': self.file_upload_id,
            'debt_id': self.debt_id
        }
