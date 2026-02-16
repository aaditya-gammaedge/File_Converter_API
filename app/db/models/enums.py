import enum

from sqlalchemy import Enum


class FileTypeEnum(str, enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    PNG = "png"
    JPG = "jpg"
    CSV = "csv"


class JobStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class FileStatusEnum(str, enum.Enum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
