from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user, get_db
from app.db.models.enums import JobStatusEnum
from app.services.job_service import JobService
from app.services.storage_service import StorageService

router = APIRouter(prefix="/download", tags=["Download"])


@router.get("/{job_id}")
async def download_file(
    job_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    job = await JobService.get_job(db=db, job_id=job_id, user_id=current_user.id)

    if not job or job.status != JobStatusEnum.COMPLETED:
        raise HTTPException(400, "File not ready")

    signed_url = StorageService.create_download_url(job.output_storage_path)

    return {"download_url": signed_url}

    file.is_downloaded = True
    file.downloaded_at = datetime.utcnow()

    await session.commit()
