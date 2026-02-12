from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.db.models.job import Job

from app.db.models.file import File

from app.db.models.enums import JobStatusEnum, FileStatusEnum

from app.utils.redis import redis_client

class JobService:

    @staticmethod
    async def create_job(
        *,
        db: AsyncSession,
        user_id,
        file_id
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

        if file.status != FileStatusEnum.UPLOADED:
            raise ValueError("File not ready")

        
        job = Job(
            user_id=user_id,
            file_id=file.id,
            status=JobStatusEnum.PENDING
        )

        db.add(job)

        
        file.status = FileStatusEnum.PROCESSING

     
        await db.commit()

       
        await db.refresh(job)

       
        redis_client.rpush("convert_queue", str(job.id))

        return job


    @staticmethod
    async def get_job(

        *,
        db: AsyncSession,
        job_id,
        user_id
    ):
        
        result = await db.execute(
            select(Job).where(
                Job.id == job_id,
                Job.user_id == user_id
            )
        )
        return result.scalar_one_or_none()




