"""AI run logs (flow execution audits)."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AiRun(Base):
    """Log of every flow call: variant, latency, tokens, fallback. No message content."""

    __tablename__ = "ai_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True, index=True
    )
    flow_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    variant: Mapped[str] = mapped_column(String(20), nullable=False)  # router, vertex
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # success, failure
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    tokens_in: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tokens_out: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fallback_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC), nullable=False)

    def __repr__(self) -> str:
        return f"<AiRun {self.flow_name}__{self.variant} {self.status} {self.latency_ms}ms>"
