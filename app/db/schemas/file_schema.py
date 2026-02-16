# app/db/schemas/file_schema.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FileRead(BaseModel):
    id: UUID
    original_filename: str
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True  # allows ORM -> schema conversion
