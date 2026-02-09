from sqlalchemy import Enum

FileTypeEnum = Enum(
    "pdf",
    "doc",
    name="file_type_enum"
)

JobStatusEnum = Enum(
    "pending",
    "processing",
    "completed",
    "failed",
    name="job_status_enum"
)
