"""Tests for conversation endpoints (SPEC-005)."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_session_unauthorized(client: AsyncClient):
    """Cannot create session without auth."""
    resp = await client.post("/api/v1/conversations")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_sessions_unauthorized(client: AsyncClient):
    """Cannot list sessions without auth."""
    resp = await client.get("/api/v1/conversations")
    assert resp.status_code == 401
