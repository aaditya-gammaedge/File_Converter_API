# app/db/schemas/file_schema.py

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class FileRead(BaseModel):
    id: UUID
    original_filename: str
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True  # allows ORM -> schema conversion
