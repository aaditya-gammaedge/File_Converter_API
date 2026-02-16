import os
import tempfile
import uuid

from sqlalchemy import select

from app.db.db import AsyncSessionLocal
from app.db.models.enums import FileStatusEnum, JobStatusEnum
from app.db.models.file import File
from app.db.models.job import Job
from app.services.storage_service import StorageService
from app.worker.converters.csv_json_excel_converter import (
    CSVtoExcelConverter, CSVtoJSONConverter)
from app.worker.converters.image_converter import (JPGtoPNGConverter,
                                                   PNGtoJPGConverter)
from app.worker.converters.pdf_docx_converter import (DOCXtoPDFConverter,
                                                      PDFtoDOCXConverter)


async def process_job(job_id: str):

    async with AsyncSessionLocal() as db:

        result = await db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if not job:
            return

        job.status = JobStatusEnum.PROCESSING
        await db.commit()

        file = await db.get(File, job.file_id)

        try:

            # ---------- TEMP FILES ----------

            temp_input = tempfile.NamedTemporaryFile(delete=False)
            temp_output = tempfile.NamedTemporaryFile(delete=False)

            # ---------- DOWNLOAD ORIGINAL ----------

            StorageService.download_file(file.storage_path, temp_input.name)

            ext = file.original_filename.split(".")[-1].lower()

            # ---------- CONVERT ----------

            if ext == "pdf":
                output_ext = "docx"
                output_path = temp_output.name + ".docx"

                converter = PDFtoDOCXConverter()
                converter.convert(temp_input.name, output_path)

            elif ext == "docx":
                output_ext = "pdf"
                output_path = temp_output.name + ".pdf"

                converter = DOCXtoPDFConverter()
                converter.convert(temp_input.name, output_path)

            elif ext in ["jpg", "png", "webp"]:
                output_ext = "png"
                output_path = temp_output.name + ".png"

                converter = JPGtoPNGConverter()
                converter.convert(temp_input.name, output_path)

            elif ext == "csv":
                output_ext = "json"
                output_path = temp_output.name + ".json"

                converter = CSVtoJSONConverter()
                converter.convert(temp_input.name, output_path)

            elif ext == "csv_excel":  # optional custom case
                output_ext = "xlsx"
                output_path = temp_output.name + ".xlsx"

                converter = CSVtoExcelConverter()
                converter.convert(temp_input.name, output_path)

            else:
                raise Exception("Unsupported file format")

            # ---------- UPLOAD RESULT ----------
            output_key = f"converted/{file.user_id}/{job.id}/output.{output_ext}"

            StorageService.upload_file(temp_output.name, output_key)

            # ---------- UPDATE DB ----------
            job.status = JobStatusEnum.COMPLETED
            job.output_storage_path = output_key
            file.status = FileStatusEnum.COMPLETED

            await db.commit()

            print("Job completed:", job_id)

        except Exception as e:
            job.status = JobStatusEnum.FAILED
            file.status = FileStatusEnum.FAILED
            await db.commit()

            print("Job failed:", str(e))
