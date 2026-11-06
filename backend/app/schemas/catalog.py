"""Pydantic schemas for catalog endpoints."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CareerPathResponse(BaseModel):
    """Career path response."""

    id: UUID
    code: str
    name: str
    description: str


class CertificationBase(BaseModel):
    """Certification base fields."""

    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    provider: str = Field(..., min_length=1, max_length=255)
    level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    cost_type: str = Field(..., pattern="^(free|paid|freemium)$")
    url: str
    language: str = Field(default="en", max_length=10)
    description: str
    last_verified_at: date | None = None


class CertificationInput(CertificationBase):
    """Certification input (admin create/update)."""

    career_path_ids: list[UUID] | None = Field(default_factory=list)
    topic_tags: list[str] | None = Field(default_factory=list)


class CertificationResponse(CertificationBase):
    """Certification response."""

    id: UUID
    status: str
    last_verified_at: date | None = None


class MaterialBase(BaseModel):
    """Learning material base fields."""

    code: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)
    provider: str = Field(..., min_length=1, max_length=255)
    format: str = Field(..., pattern="^(video|article|course|book|lab)$")
    level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    cost_type: str = Field(..., pattern="^(free|paid|freemium)$")
    url: str
    language: str = Field(default="en", max_length=10)
    duration_minutes: int | None = None
    description: str
    last_verified_at: date | None = None


class MaterialInput(MaterialBase):
    """Material input (admin create/update)."""

    career_path_ids: list[UUID] | None = Field(default_factory=list)
    topic_tags: list[str] | None = Field(default_factory=list)


class MaterialResponse(MaterialBase):
    """Material response."""

    id: UUID
    status: str


class CatalogItemPage(BaseModel):
    """Paginated catalog items."""

    items: list[dict[str, str | object]]
    page: int
    page_size: int
    total: int


class LinkReportInput(BaseModel):
    """Link report input."""

    entity_type: str = Field(..., pattern="^(certification|material)$")
    entity_id: UUID


class LinkReportResponse(BaseModel):
    """Link report response."""

    id: UUID
    entity_type: str
    entity_id: UUID
    entity_name: str
    status: str
    created_at: datetime
