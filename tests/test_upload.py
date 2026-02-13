import pytest
from unittest.mock import AsyncMock
from uuid import uuid4


from app.main import app
from app.api.auth.dependencies import get_current_user
from app.services.file_service import FileService
from app.db.models.enums import FileTypeEnum







@pytest.mark.asyncio
async def test_presign_upload_success(client, monkeypatch):

    # Fake user override
    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user

    fake_file_id = uuid4()

    monkeypatch.setattr(
        FileService,
        "create_file",
        AsyncMock(
            return_value=(
                type("File", (), {"id": fake_file_id})(),
                {"signedUrl": "https://signed-url.com"}
            )
        )
    )

    response = await client.post(
        "/upload/presign",
        params={
            "original_filename": "test.pdf",
            "file_type": FileTypeEnum.PDF.value,
            "mime_type": "application/pdf",
            "size_bytes": 1000
        }
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["file_id"] == str(fake_file_id)
    assert "upload_url" in response.json()






@pytest.mark.asyncio
async def test_confirm_upload_success(client, monkeypatch):

    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user

    monkeypatch.setattr(
        FileService,
        "confirm_upload",
        AsyncMock(return_value=None)
    )

    fake_file_id = str(uuid4())

    response = await client.post(f"/upload/confirm/{fake_file_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["status"] == "uploaded"





@pytest.mark.asyncio
async def test_confirm_upload_fail(client, monkeypatch):

    async def fake_user():
        return type("User", (), {"id": "user-123"})()

    app.dependency_overrides[get_current_user] = fake_user

    monkeypatch.setattr(
        FileService,
        "confirm_upload",
        AsyncMock(side_effect=ValueError("Invalid file"))
    )

    fake_file_id = str(uuid4())

    response = await client.post(f"/upload/confirm/{fake_file_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert "Invalid file" in response.text
