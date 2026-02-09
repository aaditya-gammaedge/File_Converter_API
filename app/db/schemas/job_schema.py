# app/db/schemas/job_schema.py

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional



class JobCreateResponse(BaseModel):
    id: UUID
    file_id: UUID
    status: str

    class Config:
        from_attributes = True



class JobRead(BaseModel):
    id: UUID
    file_id: UUID
    status: str
    output_file_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
