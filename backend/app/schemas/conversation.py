"""Conversation schemas (SPEC-005)."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


# Request/Response models
class ConversationCreate(BaseModel):
    pass  # No input needed, session created for current user


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    id: UUID
    role: Literal["user", "assistant", "tool", "system"]
    content: str
    tool_calls: dict | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: UUID
    status: Literal["active", "completed", "abandoned"]
    state: Literal["collecting", "summarizing", "choosing_path", "generating", "done"]
    slots: dict
    started_at: datetime
    ended_at: datetime | None = None
    message_count: int = 0

    class Config:
        from_attributes = True


class ConversationDetail(ConversationResponse):
    messages: list[MessageResponse] = []


# SSE event types
class StreamEvent(BaseModel):
    type: Literal["token", "tool_status", "slots", "error", "done"]
    data: dict | str | None = None


# Internal: slot extractor output
class SlotExtractorOutput(BaseModel):
    slots_update: dict = Field(default_factory=dict)
    intent: Literal[
        "provide_info",
        "confirm_summary",
        "correct_summary",
        "choose_path",
        "ask_question",
        "off_topic",
    ]
    chosen_path: str | None = None
