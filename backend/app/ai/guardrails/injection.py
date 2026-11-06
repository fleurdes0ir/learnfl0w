"""Prompt injection detection."""

import re


def detect_prompt_injection(text: str) -> bool:
    """Detect common prompt injection patterns. Raises ValueError if suspicious."""
    patterns = [
        r"(?i)(ignore|forget|disregard).*(?:previous|prior|above|instruction)",
        r"(?i)(you are now|pretend|act as).*(?:different|new|evil|hacker)",
        r"(?i)(forget|ignore).*context",
        r"(?i)(system prompt|system:)",
        r"(?i)\[system\].*",
        r"(?i)```.*(?:python|javascript|sql|bash).*```",
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False
