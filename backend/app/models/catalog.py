"""Catalog models: courses, career paths, certifications, materials."""

import uuid
from datetime import UTC, date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Course(Base):
    """University course (19 mappable IT courses + 11 non-IT)."""

    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    semester: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_mappable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)
    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Course {self.code} {self.name}>"


class CareerPath(Base):
    """Career path (e.g., DevOps, Data Analyst)."""

    __tablename__ = "career_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    template_stages: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )

    def __repr__(self) -> str:
        return f"<CareerPath {self.code} {self.name}>"


class CourseCareerpathMap(Base):
    """Many-to-many: course relevance to career paths."""

    __tablename__ = "course_career_map"

    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True
    )
    career_path_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("career_paths.id", ondelete="CASCADE"), primary_key=True
    )
    relevance: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1-3

    def __repr__(self) -> str:
        return f"<CourseCareerpathMap relevance={self.relevance}>"


class Certification(Base):
    """IT certification (e.g., AWS SAA, CKAD)."""

    __tablename__ = "certifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)  # beginner/intermediate/advanced
    cost_type: Mapped[str] = mapped_column(String(50), nullable=False)  # free/paid/freemium
    url: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    career_path_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=False, default=list
    )
    topic_tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    last_verified_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)
    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Certification {self.code} {self.name}>"


class LearningMaterial(Base):
    """Learning resource (video, article, course, book, lab)."""

    __tablename__ = "learning_materials"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    format: Mapped[str] = mapped_column(String(50), nullable=False)  # video/article/course/book/lab
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    cost_type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    career_path_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=False, default=list
    )
    topic_tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    last_verified_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)
    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )

    def __repr__(self) -> str:
        return f"<LearningMaterial {self.code} {self.title}>"
