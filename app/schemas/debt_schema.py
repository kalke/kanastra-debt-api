from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DebtSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    government_id: str
    email: str
    debt_amount: int
    debt_due_date: date
    debt_id: str
    file_upload_log_id: Optional[int] = None
