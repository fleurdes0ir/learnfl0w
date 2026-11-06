"""Rate limiting: per-user session limits."""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


async def check_daily_sessions(
    session: AsyncSession, user_id: uuid.UUID, max_per_day: int = 5
) -> None:
    """Raise ValueError if user exceeded daily session limit."""
    today = datetime.now(UTC).date()
    tomorrow = today + timedelta(days=1)
    stmt = select(func.count()).where(
        and_(
            Conversation.user_id == user_id,
            Conversation.started_at
            >= datetime.combine(today, datetime.min.time()).replace(tzinfo=UTC),
            Conversation.started_at
            < datetime.combine(tomorrow, datetime.min.time()).replace(tzinfo=UTC),
        )
    )
    count = (await session.execute(stmt)).scalar() or 0
    if count >= max_per_day:
        raise ValueError(f"Max {max_per_day} sessions per day")
