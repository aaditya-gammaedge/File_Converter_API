from datetime import datetime
from sqlalchemy import select
from app.db.db import AsyncSessionLocal
from app.db.models.file import File
from app.utils.s3 import delete_from_s3


async def cleanup_expired_files():
    """
    Deletes files from S3 and DB
    where expires_at < current time
    """

    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(File).where(
                File.expires_at < datetime.utcnow()
            )
        )

        files = result.scalars().all()

        if not files:
            return

        for file in files:
            try:
                
                delete_from_s3(file.storage_key)

                
                await session.delete(file)

                print(f"Deleted expired file: {file.id}")

            except Exception as e:
                print(f"Cleanup failed for file {file.id}: {e}")

        await session.commit()


