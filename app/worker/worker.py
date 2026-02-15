
import asyncio
from app.worker.redis_client import get_next_job
from app.worker.job_processor import process_job



async def start_worker():
    print("Worker started..............")

    while True:
        job_id = get_next_job()

        if job_id:
            print("Processing:", job_id)
            await process_job(job_id)


if __name__ == "__main__":
    asyncio.run(start_worker())




