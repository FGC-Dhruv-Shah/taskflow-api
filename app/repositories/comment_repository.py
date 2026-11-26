"""Persistence for ``Comment`` entities."""

from app.models.comment import Comment
from app.repositories.base import InMemoryRepository


class CommentRepository(InMemoryRepository[Comment]):
    """CRUD for comments, scoped by task."""

    def list_by_task(self, task_id: str) -> list[Comment]:
        return [c for c in self.list_all() if c.task_id == task_id]
