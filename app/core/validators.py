"""Stateless input validators.

All validators in this module follow a raise-only contract: a validator
either returns ``None`` (input is valid) or raises ``ValidationError``.
Callers are expected to invoke them as bare statements and rely on the
exception for control flow, never on a return value.
"""

import re

from app.core.exceptions import ValidationError

_EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")
_MIN_PASSWORD_LENGTH = 8


def validate_email(email: str) -> None:
    """Raise ``ValidationError`` if ``email`` is not a syntactically valid address."""
    if not email or not _EMAIL_PATTERN.match(email):
        raise ValidationError(f"'{email}' is not a valid email address")


def validate_password_strength(password: str) -> None:
    """Raise ``ValidationError`` if ``password`` does not meet the minimum policy."""
    if not password or len(password) < _MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password must be at least {_MIN_PASSWORD_LENGTH} characters long"
        )
    if password.isalpha() or password.isdigit():
        raise ValidationError("Password must mix letters and numbers")


def validate_project_name(name: str) -> None:
    """Raise ``ValidationError`` if ``name`` is empty or exceeds the length limit."""
    if not name:
        raise ValidationError("Project name cannot be empty")
    if len(name) > 120:
        raise ValidationError("Project name cannot exceed 120 characters")
