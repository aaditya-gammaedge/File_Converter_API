from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user

from app.api.auth.dependencies import get_db

from app.services.file_service import FileService

from app.db.models.enums import FileTypeEnum

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/presign")
async def presign_upload(

    original_filename: str,
    file_type: FileTypeEnum,
    mime_type: str,
    size_bytes: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    file, signed = await FileService.create_file(
        db=db,
        user_id=current_user.id,
        original_filename=original_filename,
        file_type=file_type,
        mime_type=mime_type,
        size_bytes=size_bytes
    )

    return {
        "file_id": str(file.id),
        "upload_url": signed["signedUrl"]
    }


@router.post("/confirm/{file_id}")
async def confirm_upload(
    file_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        await FileService.confirm_upload(
            db=db,
            file_id=file_id,
            user_id=current_user.id
        )
        return {"status": "uploaded"}
    except ValueError as e:
        raise HTTPException(400, str(e))







