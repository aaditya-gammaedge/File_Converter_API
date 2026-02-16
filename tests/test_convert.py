from unittest.mock import AsyncMock

import pytest

from app.api.auth.dependencies import get_current_user  # adjust path
from app.main import app
from app.services.job_service import JobService


@pytest.mark.asyncio
async def test_create_conversion_success(client, monkeypatch):

    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user
    monkeypatch.setattr(
        JobService,
        "create_job",
        AsyncMock(return_value=type("Job", (), {"id": "job-123"})()),
    )

    response = await client.post("/convert", params={"file_id": "file-123"})

    app.dependency_overrides.clear()

    assert response.status_code == 200




@pytest.mark.asyncio
async def test_create_conversion_fail(client, monkeypatch):

    from app.main import app

    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user

    monkeypatch.setattr(
        JobService, "create_job", AsyncMock(side_effect=ValueError("Invalid file"))
    )

    response = await client.post("/convert", params={"file_id": "file-123"})

    app.dependency_overrides.clear()

    assert response.status_code == 400
