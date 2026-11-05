from fastapi.testclient import TestClient

from app.api import health
from app.main import app

client = TestClient(app)


def test_healthz_ok_when_database_up(monkeypatch) -> None:
    async def fake_db() -> bool:
        return True

    monkeypatch.setattr(health, "check_database", fake_db)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_healthz_degraded_when_database_down(monkeypatch) -> None:
    async def fake_db() -> bool:
        return False

    monkeypatch.setattr(health, "check_database", fake_db)
    response = client.get("/healthz")
    assert response.status_code == 503
    assert response.json()["database"] == "error"


def test_llm_health_reports_configured_providers() -> None:
    response = client.get("/healthz/llm")
    assert response.status_code == 200
    assert "active_provider" in response.json()
