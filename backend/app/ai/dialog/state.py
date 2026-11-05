"""Dialog manager: deterministic consultation flow. Pure logic, no I/O, no LLM.

The LLM (Langflow `slot-extractor`) only proposes slot updates and an `intent`; this module
decides the stage and the next action. See docs/architecture/ai-design.md and SPEC-005.
"""

from __future__ import annotations

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from enum import StrEnum

REQUIRED_SLOTS: tuple[str, ...] = (
    "interests",
    "current_skills",
    "work_style",
    "hours_per_week",
    "internship_target",
    "budget_pref",
)


class Stage(StrEnum):
    COLLECTING = "collecting"
    SUMMARIZING = "summarizing"
    CHOOSING_PATH = "choosing_path"
    GENERATING = "generating"
    DONE = "done"


class Intent(StrEnum):
    PROVIDE_INFO = "provide_info"
    CONFIRM_SUMMARY = "confirm_summary"
    CORRECT_SUMMARY = "correct_summary"
    CHOOSE_PATH = "choose_path"
    ASK_QUESTION = "ask_question"
    OFF_TOPIC = "off_topic"


class ActionKind(StrEnum):
    ASK_SLOT = "ask_slot"
    SUMMARIZE = "summarize"
    OFFER_PATHS = "offer_paths"
    ANSWER_QUESTION = "answer_question"
    REDIRECT = "redirect"
    GENERATE_ROADMAP = "generate_roadmap"
    FINISH = "finish"


@dataclass(frozen=True)
class Action:
    kind: ActionKind
    slot: str | None = None
    path: str | None = None


def _filled(value: object) -> bool:
    """A slot counts as filled when it holds a meaningful value (0 hours is not meaningful)."""
    if value is None:
        return False
    if isinstance(value, bool):
        return True
    if isinstance(value, int | float):
        return value > 0
    if isinstance(value, str | list | tuple | set | dict):
        return len(value) > 0
    return True


def missing_slots(slots: Mapping[str, object]) -> list[str]:
    return [name for name in REQUIRED_SLOTS if not _filled(slots.get(name))]


def is_valid_path(code: str | None, valid_codes: Collection[str]) -> bool:
    return code is not None and code in valid_codes


def _collect_or_summarize(slots: Mapping[str, object]) -> tuple[Stage, Action]:
    missing = missing_slots(slots)
    if missing:
        return Stage.COLLECTING, Action(ActionKind.ASK_SLOT, slot=missing[0])
    return Stage.SUMMARIZING, Action(ActionKind.SUMMARIZE)


def next_step(
    stage: Stage,
    slots: Mapping[str, object],
    intent: Intent,
    chosen_path: str | None,
    valid_paths: Collection[str],
) -> tuple[Stage, Action]:
    """Return the next stage and action given the already-merged slots and detected intent."""
    if stage is Stage.DONE:
        return Stage.DONE, Action(ActionKind.FINISH)
    if stage is Stage.GENERATING:
        return Stage.GENERATING, Action(ActionKind.GENERATE_ROADMAP, path=chosen_path)
    if intent is Intent.OFF_TOPIC:
        return stage, Action(ActionKind.REDIRECT)
    if intent is Intent.ASK_QUESTION:
        return stage, Action(ActionKind.ANSWER_QUESTION)

    if stage is Stage.COLLECTING:
        return _collect_or_summarize(slots)

    if stage is Stage.SUMMARIZING:
        if intent is Intent.CONFIRM_SUMMARY and not missing_slots(slots):
            return Stage.CHOOSING_PATH, Action(ActionKind.OFFER_PATHS)
        return _collect_or_summarize(slots)

    # Stage.CHOOSING_PATH
    if intent is Intent.CHOOSE_PATH and is_valid_path(chosen_path, valid_paths):
        return Stage.GENERATING, Action(ActionKind.GENERATE_ROADMAP, path=chosen_path)
    if intent is Intent.CORRECT_SUMMARY:
        return _collect_or_summarize(slots)
    return Stage.CHOOSING_PATH, Action(ActionKind.OFFER_PATHS)
