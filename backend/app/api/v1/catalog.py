"""Catalog endpoints: career paths, certifications, materials."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import RequireAdmin
from app.db.session import get_session
from app.schemas.catalog import (
    CareerPathResponse,
    CatalogItemPage,
    CertificationInput,
    CertificationResponse,
    MaterialInput,
    MaterialResponse,
)
from app.services.catalog import CatalogService

router = APIRouter()


@router.get("/career-paths", response_model=list[CareerPathResponse])
async def list_career_paths(
    db: AsyncSession = Depends(get_session),
) -> list[CareerPathResponse]:
    """List all active career paths."""
    service = CatalogService(db)
    paths = await service.list_career_paths()
    return [
        CareerPathResponse(
            id=p.id,
            code=p.code,
            name=p.name,
            description=p.description,
        )
        for p in paths
    ]


@router.get("/certifications")
async def list_certifications(
    career_path: Annotated[str | None, Query()] = None,
    cost_type: Annotated[str | None, Query()] = None,
    level: Annotated[str | None, Query()] = None,
    q: Annotated[str | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """List active certifications with filters."""
    service = CatalogService(db)
    items, total = await service.list_certifications(
        career_path=career_path,
        cost_type=cost_type,
        level=level,
        q=q,
        page=page,
        page_size=page_size,
    )
    return {
        "items": [
            CertificationResponse(
                id=c.id,
                code=c.code,
                name=c.name,
                provider=c.provider,
                level=c.level,
                cost_type=c.cost_type,
                url=c.url,
                language=c.language,
                description=c.description,
                last_verified_at=c.last_verified_at,
                status=c.status,
            )
            for c in items
        ],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.get("/materials")
async def list_materials(
    career_path: Annotated[str | None, Query()] = None,
    cost_type: Annotated[str | None, Query()] = None,
    level: Annotated[str | None, Query()] = None,
    format: Annotated[str | None, Query()] = None,
    language: Annotated[str | None, Query()] = None,
    q: Annotated[str | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """List active learning materials with filters."""
    service = CatalogService(db)
    items, total = await service.list_materials(
        career_path=career_path,
        cost_type=cost_type,
        level=level,
        format=format,
        language=language,
        q=q,
        page=page,
        page_size=page_size,
    )
    return {
        "items": [
            MaterialResponse(
                id=m.id,
                code=m.code,
                title=m.title,
                provider=m.provider,
                format=m.format,
                level=m.level,
                cost_type=m.cost_type,
                url=m.url,
                language=m.language,
                duration_minutes=m.duration_minutes,
                description=m.description,
                last_verified_at=m.last_verified_at,
                status=m.status,
            )
            for m in items
        ],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.get("/admin/catalog/{item_type}", dependencies=[Depends(RequireAdmin)])
async def admin_list_catalog(
    item_type: str,
    status: Annotated[str | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    db: AsyncSession = Depends(get_session),
) -> CatalogItemPage:
    """Admin: list catalog items (including inactive)."""
    if item_type not in ["certification", "material"]:
        raise HTTPException(status_code=400, detail="Invalid catalog type")

    service = CatalogService(db)
    items, total = await service.admin_list_catalog(item_type, status, page, page_size)

    return CatalogItemPage(
        items=[
            {
                "id": str(item.id),
                "code": item.code,
                "name": getattr(item, "name", None) or getattr(item, "title", None),
                "status": item.status,
            }
            for item in items
        ],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.post("/admin/catalog/{item_type}", dependencies=[Depends(RequireAdmin)])
async def admin_create_catalog_item(
    item_type: str,
    data: CertificationInput | MaterialInput,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Admin: create catalog item."""
    service = CatalogService(db)

    if item_type == "certification":
        if isinstance(data, CertificationInput):
            item = await service.admin_create_certification(data)
            return {"id": str(item.id), "code": item.code, "status": item.status}
        raise HTTPException(status_code=422, detail="Invalid certification data")
    elif item_type == "material":
        if isinstance(data, MaterialInput):
            item = await service.admin_create_material(data)  # type: ignore[assignment]
            return {"id": str(item.id), "code": item.code, "status": item.status}
        raise HTTPException(status_code=422, detail="Invalid material data")
    else:
        raise HTTPException(status_code=400, detail="Invalid catalog type")


@router.put("/admin/catalog/{item_type}/{item_id}", dependencies=[Depends(RequireAdmin)])
async def admin_update_catalog_item(
    item_type: str,
    item_id: UUID,
    data: CertificationInput | MaterialInput,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Admin: update catalog item."""
    service = CatalogService(db)

    item: Any = None
    if item_type == "certification" and isinstance(data, CertificationInput):
        item = await service.admin_update_certification(item_id, data)
    elif item_type == "material" and isinstance(data, MaterialInput):
        item = await service.admin_update_material(item_id, data)
    else:
        raise HTTPException(status_code=400, detail="Invalid catalog type or data")

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"id": str(item.id), "code": item.code, "status": item.status}


@router.delete("/admin/catalog/{item_type}/{item_id}", dependencies=[Depends(RequireAdmin)])
async def admin_deactivate_catalog_item(
    item_type: str,
    item_id: UUID,
    db: AsyncSession = Depends(get_session),
) -> None:
    """Admin: deactivate catalog item (soft delete)."""
    service = CatalogService(db)
    success = await service.admin_deactivate(item_type, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
