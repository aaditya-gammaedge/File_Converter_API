
import uuid
from sqlalchemy import Text, DateTime, func, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.db.models.enums import FileTypeEnum, FileStatusEnum


from datetime import datetime
from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class File(Base):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id", ondelete="CASCADE"),nullable=False)


    original_filename: Mapped[str] = mapped_column(Text, nullable=False)

    
    storage_path: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    
    file_type: Mapped[FileTypeEnum] = mapped_column(nullable=False)

    
    mime_type: Mapped[str] = mapped_column(Text, nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)

    
    status: Mapped[FileStatusEnum] = mapped_column(nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )   

    

    is_downloaded: Mapped[bool] = mapped_column(
    Boolean,
    default=False
)

    downloaded_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True


)

    expires_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    index=True   
)


