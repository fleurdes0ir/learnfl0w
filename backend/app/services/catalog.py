"""Catalog service: courses, career paths, certifications, materials."""

import uuid
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import CareerPath, Certification, Course, LearningMaterial
from app.schemas.catalog import (
    CertificationInput,
    MaterialInput,
)


class CatalogService:
    """Business logic for catalog operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_career_paths(self) -> list[CareerPath]:
        """List all active career paths."""
        result = await self.db.execute(
            select(CareerPath).where(CareerPath.is_active.is_(True)).order_by(CareerPath.code)
        )
        return list(result.scalars().all())

    async def list_certifications(
        self,
        career_path: str | None = None,
        cost_type: str | None = None,
        level: str | None = None,
        q: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Certification], int]:
        """List active certifications with filters."""
        filters = [Certification.status == "active"]

        if career_path:
            filters.append(Certification.career_path_ids.contains([career_path]))
        if cost_type:
            filters.append(Certification.cost_type == cost_type)
        if level:
            filters.append(Certification.level == level)
        if q:
            filters.append(
                or_(
                    Certification.name.ilike(f"%{q}%"),
                    Certification.description.ilike(f"%{q}%"),
                )
            )

        query = select(Certification).where(*filters)
        count_query = select(func.count()).select_from(query.subquery())

        total = (await self.db.execute(count_query)).scalar() or 0
        result = await self.db.execute(query.offset((page - 1) * page_size).limit(page_size))
        return list(result.scalars().all()), total

    async def list_materials(
        self,
        career_path: str | None = None,
        cost_type: str | None = None,
        level: str | None = None,
        format: str | None = None,
        language: str | None = None,
        q: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[LearningMaterial], int]:
        """List active learning materials with filters."""
        filters = [LearningMaterial.status == "active"]

        if career_path:
            filters.append(LearningMaterial.career_path_ids.contains([career_path]))
        if cost_type:
            filters.append(LearningMaterial.cost_type == cost_type)
        if level:
            filters.append(LearningMaterial.level == level)
        if format:
            filters.append(LearningMaterial.format == format)
        if language:
            filters.append(LearningMaterial.language == language)
        if q:
            filters.append(
                or_(
                    LearningMaterial.title.ilike(f"%{q}%"),
                    LearningMaterial.description.ilike(f"%{q}%"),
                )
            )

        query = select(LearningMaterial).where(*filters)
        count_query = select(func.count()).select_from(query.subquery())

        total = (await self.db.execute(count_query)).scalar() or 0
        result = await self.db.execute(query.offset((page - 1) * page_size).limit(page_size))
        return list(result.scalars().all()), total

    async def admin_list_catalog(
        self,
        item_type: str,
        status: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Any], int]:
        """Admin list catalog items (including inactive)."""
        if item_type == "certification":
            filters = []
            if status:
                filters.append(Certification.status == status)
            query: Any = (
                select(Certification).where(*filters).order_by(Certification.created_at.desc())
            )
        elif item_type == "material":
            filters = []
            if status:
                filters.append(LearningMaterial.status == status)
            query = (
                select(LearningMaterial)
                .where(*filters)
                .order_by(LearningMaterial.created_at.desc())
            )
        else:
            raise ValueError(f"Unknown catalog type: {item_type}")

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar() or 0
        result = await self.db.execute(query.offset((page - 1) * page_size).limit(page_size))
        return list(result.scalars().all()), total

    async def admin_create_certification(self, data: CertificationInput) -> Certification:
        """Create certification."""
        item = Certification(
            id=uuid.uuid4(),
            code=data.code,
            name=data.name,
            provider=data.provider,
            level=data.level,
            cost_type=data.cost_type,
            url=data.url,
            language=data.language,
            description=data.description,
            last_verified_at=data.last_verified_at,
            career_path_ids=data.career_path_ids or [],
            topic_tags=data.topic_tags or [],
            status="active",
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def admin_create_material(self, data: MaterialInput) -> LearningMaterial:
        """Create learning material."""
        item = LearningMaterial(
            id=uuid.uuid4(),
            code=data.code,
            title=data.title,
            provider=data.provider,
            format=data.format,
            level=data.level,
            cost_type=data.cost_type,
            url=data.url,
            language=data.language,
            duration_minutes=data.duration_minutes,
            description=data.description,
            last_verified_at=data.last_verified_at,
            career_path_ids=data.career_path_ids or [],
            topic_tags=data.topic_tags or [],
            status="active",
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def admin_update_certification(
        self, item_id: uuid.UUID, data: CertificationInput
    ) -> Certification | None:
        """Update certification."""
        result = await self.db.execute(select(Certification).where(Certification.id == item_id))
        item = result.scalars().one_or_none()
        if not item:
            return None

        for field, value in data.model_dump().items():
            setattr(item, field, value)

        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def admin_update_material(
        self, item_id: uuid.UUID, data: MaterialInput
    ) -> LearningMaterial | None:
        """Update learning material."""
        result = await self.db.execute(
            select(LearningMaterial).where(LearningMaterial.id == item_id)
        )
        item = result.scalars().one_or_none()
        if not item:
            return None

        for field, value in data.model_dump().items():
            setattr(item, field, value)

        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def admin_deactivate(self, item_type: str, item_id: uuid.UUID) -> bool:
        """Soft delete catalog item."""
        if item_type == "certification":
            result = await self.db.execute(select(Certification).where(Certification.id == item_id))
            item = result.scalars().one_or_none()
            if item:
                item.status = "inactive"
                await self.db.commit()
                return True
        elif item_type == "material":
            result = await self.db.execute(
                select(LearningMaterial).where(LearningMaterial.id == item_id)
            )
            item = result.scalars().one_or_none()
            if item:
                item.status = "inactive"
                await self.db.commit()
                return True

        return False
