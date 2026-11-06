"""Conversation service (SPEC-005). Business logic for chat sessions."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.dialog.state import Action, ActionKind, Intent, Stage, missing_slots, next_step
from app.ai.guardrails import check_daily_sessions, detect_prompt_injection, filter_urls
from app.models.conversation import Conversation, Message

if TYPE_CHECKING:
    from app.ai.langflow.client import LangflowClient

MAX_TURNS_PER_SESSION = 25
MAX_SESSIONS_PER_DAY = 5


class ConversationService:
    def __init__(
        self, db: AsyncSession, langflow: LangflowClient | None, user_id: uuid.UUID
    ) -> None:
        self._db = db
        self._langflow = langflow
        self._user_id = user_id

    async def create_session(self) -> Conversation:
        """Create a new conversation session for the user."""
        await check_daily_sessions(self._db, self._user_id, MAX_SESSIONS_PER_DAY)
        conv = Conversation(user_id=self._user_id, status="active", state="collecting", slots={})
        self._db.add(conv)
        await self._db.flush()
        return conv

    async def list_sessions(self, include_completed: bool = False) -> list[Conversation]:
        """List user's conversations, most recent first."""
        stmt = (
            select(Conversation)
            .where(Conversation.user_id == self._user_id)
            .order_by(Conversation.started_at.desc())
        )
        if not include_completed:
            stmt = stmt.where(Conversation.status == "active")
        result = await self._db.execute(stmt)
        return list(result.scalars().all())

    async def get_session(self, conv_id: uuid.UUID) -> Conversation | None:
        """Get a conversation by ID, checking ownership."""
        stmt = select(Conversation).where(
            Conversation.id == conv_id, Conversation.user_id == self._user_id
        )
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()

    async def post_message(self, conv: Conversation, content: str) -> Message:
        """Process a user message and return the assistant response."""
        if conv.status != "active":
            raise ValueError("Conversation is not active")
        if conv.state == "done":
            raise ValueError("Conversation already completed")
        if len(content) > 4000:
            raise ValueError("Message too long (max 4000 chars)")
        if detect_prompt_injection(content):
            # ponytail: log incident without content when we have logging infra
            raise ValueError("Message rejected by input filter")

        # Count turns (user messages)
        stmt = select(func.count()).where(
            Message.conversation_id == conv.id, Message.role == "user"
        )
        turns = (await self._db.execute(stmt)).scalar() or 0
        if turns >= MAX_TURNS_PER_SESSION:
            raise ValueError("Maximum turns reached for this session")

        # Save user message
        user_msg = Message(conversation_id=conv.id, role="user", content=content)
        self._db.add(user_msg)
        await self._db.flush()

        # Call Langflow slot-extractor (TODO: implement after T-2 flow setup)
        # For now, just echo back with state transition
        # result = await self._langflow.run(
        #     "slot-extractor",
        #     input_value=content,
        #     session_id=str(conv.id),
        # )
        # extracted = SlotExtractorOutput.model_validate(result.payload)

        # Mock: assume user provides info
        extracted_intent = Intent.PROVIDE_INFO
        extracted_slots = {"interests": ["AI", "cloud"]}  # TODO: real extraction
        extracted_chosen_path = None

        # Merge slots
        conv.slots = {**conv.slots, **extracted_slots}

        # Decide next step
        valid_paths = ["CP-01", "CP-02", "CP-03"]  # TODO: load from catalog
        stage = Stage(conv.state)
        next_stage, action = next_step(
            stage, conv.slots, extracted_intent, extracted_chosen_path, valid_paths
        )

        # Update state
        conv.state = next_stage.value

        # Generate response based on action
        response_text = self._generate_response(action, conv.slots, missing_slots(conv.slots))
        response_text = filter_urls(response_text)

        # Save assistant message
        assistant_msg = Message(conversation_id=conv.id, role="assistant", content=response_text)
        self._db.add(assistant_msg)
        await self._db.flush()

        return assistant_msg

    def _generate_response(
        self, action: Action, slots: dict[str, object], missing: list[str]
    ) -> str:
        """Generate deterministic response text based on action."""
        if action.kind == ActionKind.ASK_SLOT:
            slot = action.slot or ""
            prompts = {
                "interests": "Apa bidang IT yang paling menarik bagi kamu?",
                "current_skills": "Skill apa saja yang sudah kamu miliki?",
                "work_style": "Kamu lebih suka kerja tim atau individu?",
                "hours_per_week": "Berapa jam per minggu bisa kamu alokasikan untuk belajar?",
                "internship_target": "Target magang kamu seperti apa?",
                "budget_pref": "Kamu preferensi budget untuk kursus atau sertifikasi?",
            }
            return prompts.get(slot, f"Tolong isi informasi tentang {slot}")

        if action.kind == ActionKind.SUMMARIZE:
            return f"Berikut ringkasan profil kamu: {slots}. Apakah sudah benar?"

        if action.kind == ActionKind.OFFER_PATHS:
            return "Berdasarkan profil kamu, saya rekomendasikan jalur karir berikut. Pilih satu."

        if action.kind == ActionKind.REDIRECT:
            return "Pertanyaan menarik! Tapi fokus dulu ke konsultasi ya."

        if action.kind == ActionKind.ANSWER_QUESTION:
            return "Baik, pertanyaan kamu akan saya jawab."

        if action.kind == ActionKind.GENERATE_ROADMAP:
            return "Roadmap sedang dibuat..."

        return "Terima kasih atas informasinya!"

    async def end_session(self, conv: Conversation) -> None:
        """Mark conversation as completed."""
        conv.status = "completed"
        conv.ended_at = func.now()
        await self._db.flush()

    async def post_message_stream(self, conv: Conversation, content: str) -> AsyncIterator[str]:
        """Stream response events (token, slots, etc). Yield JSON-encoded events."""
        import json

        if conv.status != "active":
            raise ValueError("Conversation is not active")
        if conv.state == "done":
            raise ValueError("Conversation already completed")

        # Validate input length
        if len(content) > 4000:
            raise ValueError("Message too long")
        if detect_prompt_injection(content):
            raise ValueError("Message rejected by input filter")

        # Count turns
        stmt = select(func.count()).where(
            Message.conversation_id == conv.id, Message.role == "user"
        )
        turns = (await self._db.execute(stmt)).scalar() or 0
        if turns >= MAX_TURNS_PER_SESSION:
            raise ValueError("Maximum turns reached for this session")

        # Save user message
        user_msg = Message(conversation_id=conv.id, role="user", content=content)
        self._db.add(user_msg)
        await self._db.flush()

        # Mock streaming: yield filtered events
        yield json.dumps({"type": "token", "data": "Terima"})
        yield json.dumps({"type": "token", "data": " kasih"})
        yield json.dumps({"type": "slots", "data": {"interests": ["AI"]}})
        yield json.dumps({"type": "done", "data": None})
