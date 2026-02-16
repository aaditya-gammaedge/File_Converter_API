import uuid

import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    email = f"{uuid.uuid4()}@test.com"

    response = await client.post(
        "/auth/register", json={"email": email, "password": "aadi2003"}
    )

    print(response.json())

    assert response.status_code == 200
    assert response.json()["email"] == email


@pytest.mark.asyncio
async def test_register_duplicate(client):
    await client.post(
        "/auth/register",
        json={"email": "aayush.patidar@gmail.com", "password": "123456"},
    )

    response = await client.post(
        "/auth/register",
        json={"email": "aayush.patidar@gmail.com", "password": "123456"},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(
        "/auth/register",
        json={"email": "aaditya.jaiswal@gmail.com", "password": "aadi2003"},
    )

    response = await client.post(
        "/auth/login",
        json={"email": "aaditya.jaiswal@gmail.com", "password": "aadi2003"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_invalid(client):
    response = await client.post(
        "/auth/login", json={"email": "wrong@test.com", "password": "wrong"}
    )

    assert response.status_code == 401
