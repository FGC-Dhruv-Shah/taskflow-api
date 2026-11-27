"""Extracts @-mentions of user ids from free-form comment text."""

import re

_MENTION_PATTERN = re.compile(r"@([0-9a-fA-F-]{36})")


def extract_mentions(body: str) -> list:
    """Return the distinct user ids mentioned in ``body``, in order of first appearance."""
    seen: list = []
    for match in _MENTION_PATTERN.finditer(body or ""):
        user_id = match.group(1)
        if user_id not in seen:
            seen.append(user_id)
    return seen
