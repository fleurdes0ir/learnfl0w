"""Health endpoints (public)."""

import httpx
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import Settings, get_settings
from app.db.session import get_engine

router = APIRouter(tags=["Health"])


async def check_database() -> bool:
    try:
        async with get_engine().connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        return False
    return True


async def check_langflow_health(settings: Settings) -> dict[str, object]:
    """Probe Langflow /health_check endpoint."""
    try:
        async with httpx.AsyncClient(base_url=settings.langflow_base_url, timeout=5) as client:
            response = await client.get("/health_check")
            response.raise_for_status()
            return {"status": "ok", "details": response.json()}
    except Exception as e:
        return {"status": "error", "details": str(e)}


@router.get("/healthz")
async def get_health() -> JSONResponse:
    db_ok = await check_database()
    body = {
        "status": "ok" if db_ok else "degraded",
        "database": "ok" if db_ok else "error",
        "version": "0.1.0",
    }
    return JSONResponse(body, status_code=200 if db_ok else 503)


@router.get("/healthz/llm")
async def get_llm_health() -> dict[str, object]:
    """Report Langflow health and circuit breaker state per variant."""
    settings = get_settings()

    # Probe Langflow
    langflow_health = await check_langflow_health(settings)

    # Circuit breaker states (shared client instance or fetch from dependency)
    # ponytail: client global instance stored in app state, injected in SPEC-005
    providers = {}
    for variant in [settings.llm_provider, settings.llm_fallback_provider]:
        providers[variant] = {
            "state": "disabled",
            "circuit": "closed",
        }

    return {
        "langflow": langflow_health,
        "active_provider": settings.llm_provider,
        "providers": providers,
    }
