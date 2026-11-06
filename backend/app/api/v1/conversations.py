"""Conversation endpoints (SPEC-005)."""

from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentUser
from app.db.session import get_session
from app.models.conversation import Conversation
from app.schemas.conversation import (
    ConversationCreate,
    ConversationDetail,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from app.services.conversation import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


def _to_response(conv: Conversation) -> ConversationResponse:
    return ConversationResponse(
        id=conv.id,
        status=conv.status,
        state=conv.state,
        slots=conv.slots,
        started_at=conv.started_at,
        ended_at=conv.ended_at,
        message_count=len(conv.messages),
    )


def _to_detail(conv: Conversation) -> ConversationDetail:
    return ConversationDetail(
        id=conv.id,
        status=conv.status,
        state=conv.state,
        slots=conv.slots,
        started_at=conv.started_at,
        ended_at=conv.ended_at,
        message_count=len(conv.messages),
        messages=[
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                tool_calls=msg.tool_calls,
                created_at=msg.created_at,
            )
            for msg in conv.messages
        ],
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ConversationResponse)
async def create_session(
    _: ConversationCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: CurrentUser,
) -> ConversationResponse:
    """Create a new conversation session."""
    service = ConversationService(session, None, user.id)  # langflow=None for now
    conv = await service.create_session()
    await session.commit()
    return _to_response(conv)


@router.get("", response_model=list[ConversationResponse])
async def list_sessions(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: CurrentUser,
    include_completed: bool = False,
) -> list[ConversationResponse]:
    """List user's conversation sessions."""
    service = ConversationService(session, None, user.id)
    convs = await service.list_sessions(include_completed)
    return [_to_response(c) for c in convs]


@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: CurrentUser,
) -> ConversationDetail:
    """Get a conversation with its messages."""
    service = ConversationService(session, None, user.id)
    conv = await service.get_session(conversation_id)
    if not conv:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")
    return _to_detail(conv)


@router.post("/{conversation_id}/messages", status_code=status.HTTP_201_CREATED)
async def post_message(
    conversation_id: UUID,
    msg: MessageCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: CurrentUser,
) -> MessageResponse:
    """Post a message to a conversation (non-streaming)."""
    service = ConversationService(session, None, user.id)
    conv = await service.get_session(conversation_id)
    if not conv:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")

    try:
        assistant_msg = await service.post_message(conv, msg.content)
        await session.commit()
        return MessageResponse(
            id=assistant_msg.id,
            role=assistant_msg.role,
            content=assistant_msg.content,
            tool_calls=assistant_msg.tool_calls,
            created_at=assistant_msg.created_at,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e)) from e


@router.post("/{conversation_id}/messages/stream")
async def post_message_stream(
    conversation_id: UUID,
    msg: MessageCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: CurrentUser,
) -> StreamingResponse:
    """Post a message with SSE streaming response."""
    service = ConversationService(session, None, user.id)
    conv = await service.get_session(conversation_id)
    if not conv:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")

    async def event_generator() -> AsyncIterator[str]:
        try:
            async for event_data in service.post_message_stream(conv, msg.content):
                yield f"data: {event_data}\n\n"
            await session.commit()
        except ValueError as e:
            yield f"data: {{'error': '{str(e)}'}}\n\n"
        except Exception:
            yield "data: {'error': 'Internal error'}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    conversation_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: CurrentUser,
) -> None:
    """Delete (abandon) a conversation session."""
    service = ConversationService(session, None, user.id)
    conv = await service.get_session(conversation_id)
    if not conv:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")
    conv.status = "abandoned"
    await session.commit()
