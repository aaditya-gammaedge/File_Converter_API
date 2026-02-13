import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from app.main import app
from app.api.auth.dependencies import get_current_user
from app.services.job_service import JobService
from app.services.storage_service import StorageService
from app.db.models.enums import JobStatusEnum



@pytest.mark.asyncio
async def test_download_success(client, monkeypatch):

    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user

    fake_job = type("Job", (), {
        "status": JobStatusEnum.COMPLETED,
        "output_storage_path": "path/to/file.pdf"
    })()

    monkeypatch.setattr(
        JobService,
        "get_job",
        AsyncMock(return_value=fake_job)
    )

    monkeypatch.setattr(
        StorageService,
        "create_download_url",
        Mock(return_value="https://signed-download-url.com")
    )

    job_id = str(uuid4())

    response = await client.get(f"/download/{job_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["download_url"] == "https://signed-download-url.com"







@pytest.mark.asyncio
async def test_download_not_completed(client, monkeypatch):
    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user

    fake_job = type("Job", (), {
        "status": JobStatusEnum.PROCESSING,
        "output_storage_path": "path/to/file.pdf"
    })()

    monkeypatch.setattr(
        JobService,
        "get_job",
        AsyncMock(return_value=fake_job)
    )

    job_id = str(uuid4())

    response = await client.get(f"/download/{job_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert "File not ready" in response.text







@pytest.mark.asyncio
async def test_download_job_not_found(client, monkeypatch):

    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user

    monkeypatch.setattr(
        JobService,
        "get_job",
        AsyncMock(return_value=None)
    )

    job_id = str(uuid4())

    response = await client.get(f"/download/{job_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert "File not ready" in response.text
