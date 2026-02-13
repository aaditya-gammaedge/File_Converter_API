FROM python:3.11-slim AS base



WORKDIR /app



COPY requirements.txt .



RUN pip install --no-cache-dir -r requirements.txt



COPY app ./app
COPY tests ./tests
COPY alembic ./alembic

FROM base AS test



RUN pip install --no-cache-dir pytest pytest-asyncio httpx



CMD ["pytest", "-v"]



FROM base AS prod



EXPOSE 8000



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]