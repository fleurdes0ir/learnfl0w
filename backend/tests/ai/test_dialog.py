from app.ai.dialog.state import (
    REQUIRED_SLOTS,
    ActionKind,
    Intent,
    Stage,
    is_valid_path,
    missing_slots,
    next_step,
)

VALID = {"CP-01", "CP-05"}
FULL = {
    "interests": ["jaringan"],
    "current_skills": ["Linux"],
    "work_style": "praktik langsung",
    "hours_per_week": 8,
    "internship_target": "Semester 6",
    "budget_pref": "free",
}


def test_missing_slots_reports_in_required_order() -> None:
    assert missing_slots({}) == list(REQUIRED_SLOTS)
    assert missing_slots({"interests": ["a"], "hours_per_week": 0}) == [
        "current_skills",
        "work_style",
        "hours_per_week",
        "internship_target",
        "budget_pref",
    ]


def test_collecting_asks_first_missing_slot() -> None:
    stage, action = next_step(Stage.COLLECTING, {"interests": ["a"]}, Intent.PROVIDE_INFO, None, VALID)
    assert stage is Stage.COLLECTING
    assert action.kind is ActionKind.ASK_SLOT and action.slot == "current_skills"


def test_collecting_moves_to_summary_when_slots_complete() -> None:
    stage, action = next_step(Stage.COLLECTING, FULL, Intent.PROVIDE_INFO, None, VALID)
    assert stage is Stage.SUMMARIZING and action.kind is ActionKind.SUMMARIZE


def test_confirm_summary_offers_paths() -> None:
    stage, action = next_step(Stage.SUMMARIZING, FULL, Intent.CONFIRM_SUMMARY, None, VALID)
    assert stage is Stage.CHOOSING_PATH and action.kind is ActionKind.OFFER_PATHS


def test_confirm_with_missing_slot_goes_back_to_collecting() -> None:
    slots = {**FULL, "work_style": None}
    stage, action = next_step(Stage.SUMMARIZING, slots, Intent.CONFIRM_SUMMARY, None, VALID)
    assert stage is Stage.COLLECTING and action.slot == "work_style"


def test_correction_resummarizes_when_nothing_missing() -> None:
    stage, action = next_step(Stage.SUMMARIZING, FULL, Intent.CORRECT_SUMMARY, None, VALID)
    assert stage is Stage.SUMMARIZING and action.kind is ActionKind.SUMMARIZE


def test_valid_path_choice_starts_generation() -> None:
    stage, action = next_step(Stage.CHOOSING_PATH, FULL, Intent.CHOOSE_PATH, "CP-05", VALID)
    assert stage is Stage.GENERATING
    assert action.kind is ActionKind.GENERATE_ROADMAP and action.path == "CP-05"


def test_invalid_or_missing_path_keeps_offering_paths() -> None:
    for chosen in ("CP-99", None):
        stage, action = next_step(Stage.CHOOSING_PATH, FULL, Intent.CHOOSE_PATH, chosen, VALID)
        assert stage is Stage.CHOOSING_PATH and action.kind is ActionKind.OFFER_PATHS


def test_off_topic_and_questions_do_not_change_stage() -> None:
    for intent, kind in ((Intent.OFF_TOPIC, ActionKind.REDIRECT), (Intent.ASK_QUESTION, ActionKind.ANSWER_QUESTION)):
        stage, action = next_step(Stage.COLLECTING, {}, intent, None, VALID)
        assert stage is Stage.COLLECTING and action.kind is kind


def test_generating_and_done_are_terminal_flows() -> None:
    stage, action = next_step(Stage.GENERATING, FULL, Intent.PROVIDE_INFO, "CP-01", VALID)
    assert stage is Stage.GENERATING and action.kind is ActionKind.GENERATE_ROADMAP
    stage, action = next_step(Stage.DONE, FULL, Intent.PROVIDE_INFO, None, VALID)
    assert stage is Stage.DONE and action.kind is ActionKind.FINISH


def test_is_valid_path() -> None:
    assert is_valid_path("CP-01", VALID)
    assert not is_valid_path("CP-02", VALID)
    assert not is_valid_path(None, VALID)
