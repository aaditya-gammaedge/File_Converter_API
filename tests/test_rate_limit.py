import pytest
from unittest.mock import AsyncMock, Mock

from fastapi import HTTPException

from app.utils.rate_limiter import rate_limit


# -----------------------------------
# Helper Dummy Endpoint
# -----------------------------------

async def dummy_endpoint(*args, **kwargs):
    return {"success": True}


# -----------------------------------
# SUCCESS UNDER LIMIT
# -----------------------------------

@pytest.mark.asyncio
async def test_rate_limit_allows_under_limit(monkeypatch):

    fake_redis = Mock()
    fake_redis.get.return_value = "5"
    fake_redis.incr.return_value = 6

    monkeypatch.setattr(
        "app.utils.rate_limiter.redis_client",
        fake_redis
    )

    decorator = rate_limit(limit=10, window=60)
    wrapped = decorator(dummy_endpoint)

    fake_user = type("User", (), {"id": "123"})()

    response = await wrapped(current_user=fake_user)

    assert response == {"success": True}
    fake_redis.incr.assert_called_once()


# -----------------------------------
# BLOCK WHEN LIMIT EXCEEDED
# -----------------------------------

@pytest.mark.asyncio
async def test_rate_limit_blocks_when_exceeded(monkeypatch):

    fake_redis = Mock()
    fake_redis.get.return_value = "10"

    monkeypatch.setattr(
        "app.utils.rate_limiter.redis_client",
        fake_redis
    )

    decorator = rate_limit(limit=10, window=60)
    wrapped = decorator(dummy_endpoint)

    fake_user = type("User", (), {"id": "123"})()

    with pytest.raises(HTTPException) as exc:
        await wrapped(current_user=fake_user)

    assert exc.value.status_code == 429
    assert "Rate limit exceeded" in exc.value.detail


# -----------------------------------
# BLOCK WHEN NO USER
# -----------------------------------

@pytest.mark.asyncio
async def test_rate_limit_requires_auth(monkeypatch):

    fake_redis = Mock()

    monkeypatch.setattr(
        "app.utils.rate_limiter.redis_client",
        fake_redis
    )

    decorator = rate_limit()
    wrapped = decorator(dummy_endpoint)

    with pytest.raises(HTTPException) as exc:
        await wrapped()

    assert exc.value.status_code == 401
    assert "Authentication required" in exc.value.detail


# -----------------------------------
# EXPIRE SET ON FIRST REQUEST
# -----------------------------------

@pytest.mark.asyncio
async def test_rate_limit_sets_expire_on_first_request(monkeypatch):

    fake_redis = Mock()
    fake_redis.get.return_value = None
    fake_redis.incr.return_value = 1

    monkeypatch.setattr(
        "app.utils.rate_limiter.redis_client",
        fake_redis
    )

    decorator = rate_limit(limit=10, window=60)
    wrapped = decorator(dummy_endpoint)

    fake_user = type("User", (), {"id": "123"})()

    await wrapped(current_user=fake_user)

    fake_redis.expire.assert_called_once_with("rate_limit:123", 60)
