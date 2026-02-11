from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user
from app.api.auth.dependencies import get_db
from app.services.job_service import JobService


router = APIRouter(prefix="/convert", tags=["Convert"])


@router.post("")
async def create_conversion(
    file_id : str, 
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
        try:
            job = await JobService.create_job(
                db=db,
                user_id=current_user.id,
                file_id=file_id
        )
            return {"job_id": str(job.id)}
        except ValueError as e:
            raise HTTPException(400, str(e))
        

    