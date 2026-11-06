"""Internal tool endpoints for Langflow flows (SPEC-005 T-3).

Catalog-related tools called from consultant-reply flow.
Read-only, require X-Internal-Token header.
Not part of public OpenAPI (docs/api/internal-tools.openapi.yaml).
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_session
from app.models.catalog import Certification, LearningMaterial
from app.schemas.catalog import CertificationResponse, MaterialResponse

router = APIRouter(prefix="/internal/tools", tags=["internal"])


async def _verify_internal_token(
    token: Annotated[str | None, Header()] = None,
) -> None:
    """Verify internal tool token."""
    settings = get_settings()
    if not settings.internal_tool_token or token != settings.internal_tool_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid internal token")


@router.get("/certifications", response_model=list[CertificationResponse])
async def certification_finder(
    q: str = Query("", min_length=0, max_length=200),
    career_path: str | None = Query(None),
    level: str | None = Query(None),
    limit: int = Query(5, ge=1, le=20),
    session: AsyncSession = Depends(get_session),
    _: None = Depends(_verify_internal_token),
) -> list[CertificationResponse]:
    """Find certifications by name or filter. Used by consultant-reply flow."""
    stmt = select(Certification).where(Certification.status == "active")

    if q:
        stmt = stmt.where(Certification.name.ilike(f"%{q}%"))
    if level:
        stmt = stmt.where(Certification.level == level)
    if career_path:
        from sqlalchemy import and_

        stmt = stmt.where(
            and_(
                Certification.career_path_ids.contains([career_path]),
            )
        )

    stmt = stmt.limit(limit)
    result = await session.execute(stmt)
    certs = result.scalars().all()
    return [CertificationResponse.model_validate(c) for c in certs]


@router.get("/materials", response_model=list[MaterialResponse])
async def material_finder(
    q: str = Query("", min_length=0, max_length=200),
    format: str | None = Query(None),
    language: str | None = Query(None),
    limit: int = Query(5, ge=1, le=20),
    session: AsyncSession = Depends(get_session),
    _: None = Depends(_verify_internal_token),
) -> list[MaterialResponse]:
    """Find learning materials by title or filter. Used by consultant-reply flow."""
    stmt = select(LearningMaterial).where(LearningMaterial.status == "active")

    if q:
        stmt = stmt.where(LearningMaterial.title.ilike(f"%{q}%"))
    if format:
        stmt = stmt.where(LearningMaterial.format == format)
    if language:
        stmt = stmt.where(LearningMaterial.language == language)

    stmt = stmt.limit(limit)
    result = await session.execute(stmt)
    materials = result.scalars().all()
    return [MaterialResponse.model_validate(m) for m in materials]
