"""Comment creation and display formatting."""

from datetime import datetime

from app.core.exceptions import ValidationError
from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.repositories.user_repository import UserRepository
from app.services.mention_parser import extract_mentions
from app.services.notification_service import NotificationService

_MINUTE = 60
_HOUR = 60 * _MINUTE
_DAY = 24 * _HOUR


class CommentService:
    """Orchestrates comment creation and relative-time display formatting."""

    def __init__(
        self,
        comment_repository: CommentRepository,
        user_repository: UserRepository,
        notification_service: NotificationService,
    ) -> None:
        self._comment_repository = comment_repository
        self._user_repository = user_repository
        self._notification_service = notification_service

    def add_comment(self, task_id: str, author_id: str, body: str) -> Comment:
        """Validate and persist a new comment on ``task_id``, notifying any mentions."""
        if not body or not body.strip():
            raise ValidationError("Comment body cannot be empty")
        mentioned_ids = [u.id for u in self._user_repository.list_by_ids(extract_mentions(body))]
        comment = Comment(
            id=self._comment_repository.new_id(),
            task_id=task_id,
            author_id=author_id,
            body=body.strip(),
            mentioned_user_ids=mentioned_ids,
        )
        created = self._comment_repository.create(comment)
        for user_id in mentioned_ids:
            self._notification_service.notify_project_members(
                task_id, f"You were mentioned in a comment: {body.strip()[:80]}"
            )
        return created

    def edit_comment(self, comment_id: str, new_body: str) -> Comment:
        """Update an existing comment's body and re-scan it for mentions."""
        if not new_body or not new_body.strip():
            raise ValidationError("Comment body cannot be empty")
        mentioned_ids = [u.id for u in self._user_repository.list_by_ids(extract_mentions(new_body))]
        comment = self._comment_repository.update(
            comment_id, body=new_body.strip(), mentioned_user_ids=mentioned_ids
        )
        comment.mark_edited(datetime.utcnow())
        return comment

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
