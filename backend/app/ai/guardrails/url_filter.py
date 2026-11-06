"""URL filtering: remove non-catalog URLs from stream."""

import re


def filter_urls(text: str) -> str:
    """Remove all URLs from text. Langflow responses should ref catalog via tools, not hardcoded URLs."""
    # ponytail: if we trust Langflow prompts, can skip this. Add when flows live in-repo.
    return re.sub(r"https?://\S+", "", text)
