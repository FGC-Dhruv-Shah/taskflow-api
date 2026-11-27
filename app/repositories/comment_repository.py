"""Persistence for ``Comment`` entities."""

from app.models.comment import Comment
from app.repositories.base import InMemoryRepository


class CommentRepository(InMemoryRepository[Comment]):
    """CRUD for comments, scoped by task."""

    def list_by_task(self, task_id: str) -> list[Comment]:
        return [c for c in self.list_all() if c.task_id == task_id]

    def list_mentioning(self, user_id: str) -> list[Comment]:
        """Return every comment that mentions ``user_id``."""
        return [c for c in self.list_all() if user_id in c.mentioned_user_ids]

    def list_recent_edits(self, task_id: str) -> list[Comment]:
        """Return a task's edited comments, most recently edited first."""
        edited = [c for c in self.list_by_task(task_id) if c.edited]
        return sorted(edited, key=lambda c: c.edited_at or c.created_at, reverse=True)

    def count_by_task(self, task_id: str) -> int:
        return len(self.list_by_task(task_id))

    def count_by_author(self, author_id: str) -> int:
        return len([c for c in self.list_all() if c.author_id == author_id])
