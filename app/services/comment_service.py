"""Comment creation and display formatting."""

from datetime import datetime

from app.core.exceptions import ValidationError
from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository

_MINUTE = 60
_HOUR = 60 * _MINUTE
_DAY = 24 * _HOUR


class CommentService:
    """Orchestrates comment creation and relative-time display formatting."""

    def __init__(self, comment_repository: CommentRepository) -> None:
        self._comment_repository = comment_repository

    def add_comment(self, task_id: str, author_id: str, body: str) -> Comment:
        """Validate and persist a new comment on ``task_id``."""
        if not body or not body.strip():
            raise ValidationError("Comment body cannot be empty")
        comment = Comment(
            id=self._comment_repository.new_id(),
            task_id=task_id,
            author_id=author_id,
            body=body.strip(),
        )
        return self._comment_repository.create(comment)

    def delete_comment(self, comment_id: str) -> None:
        """Remove a comment permanently."""
        self._comment_repository.delete(comment_id)

    def format_timestamp(self, dt: datetime) -> str:
        """Render ``dt`` as a relative time for display, e.g. ``'3 hours ago'``.

        Deliberately separate from ``core.utils.format_timestamp`` (which
        renders an absolute ISO-8601 string for audit logs): comment display
        and audit logging have different formatting needs, so this is its
        own local helper rather than a wrapper around the shared one.
        """
        elapsed = (datetime.utcnow() - dt).total_seconds()
        if elapsed < _MINUTE:
            return "just now"
        if elapsed < _HOUR:
            return f"{int(elapsed // _MINUTE)} minutes ago"
        if elapsed < _DAY:
            return f"{int(elapsed // _HOUR)} hours ago"
        return f"{int(elapsed // _DAY)} days ago"
