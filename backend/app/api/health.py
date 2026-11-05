"""Health endpoints (public)."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import get_engine

router = APIRouter(tags=["Health"])


async def check_database() -> bool:
    try:
        async with get_engine().connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        return False
    return True


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
    settings = get_settings()
    # SPEC-011 T-3: probe Langflow /health_check and read circuit states from LangflowClient.
    return {
        "active_provider": settings.llm_provider,
        "providers": {
            settings.llm_provider: {"state": "disabled", "circuit": "closed"},
            settings.llm_fallback_provider: {"state": "disabled", "circuit": "closed"},
        },
    }
