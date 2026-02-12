import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.file import File
from app.db.models.enums import FileStatusEnum, FileTypeEnum
from app.services.storage_service import StorageService




class FileService:

    @staticmethod
    async def create_file(
        *,
        db: AsyncSession,
        user_id,
        original_filename: str,
        file_type: FileTypeEnum,
        mime_type: str,
        size_bytes: int
    ):
        file_id = uuid.uuid4()
        storage_path = f"uploads/{user_id}/{file_id}/{original_filename}"

        file = File(
            id=file_id,
            user_id=user_id,
            original_filename=original_filename,
            storage_path=storage_path,
            file_type=file_type,
            mime_type=mime_type,
            size_bytes=size_bytes,
            status=FileStatusEnum.UPLOADING
        )

        db.add(file)
        await db.commit()

        
        upload_url = StorageService.create_upload_url(storage_path, mime_type)

        return file, {"signedUrl": upload_url}


    @staticmethod
    async def confirm_upload(
        *,
        db: AsyncSession,
        file_id,
        user_id
):
        result = await db.execute(
        select(File).where(
            File.id == file_id,
            File.user_id == user_id
        )
    )
        file = result.scalar_one_or_none()

        if not file:
            raise ValueError("File not found")

        exists = StorageService.file_exists(file.storage_path)

        if not exists:
            raise ValueError("File not uploaded")

        file.status = FileStatusEnum.UPLOADED
        await db.commit()

        return file
