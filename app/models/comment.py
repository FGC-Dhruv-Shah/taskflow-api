"""Comment domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    """A comment left on a task."""

    id: str
    task_id: str
    author_id: str
    body: str
    mentioned_user_ids: list = field(default_factory=list)
    edited: bool = False
    edited_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def mark_edited(self, at: datetime) -> None:
        self.edited = True
        self.edited_at = at

    def has_mentions(self) -> bool:
        return len(self.mentioned_user_ids) > 0

    def preview(self, length: int = 50) -> str:
        """Return a truncated, single-line preview of the comment body."""
        flattened = " ".join(self.body.split())
        return flattened if len(flattened) <= length else flattened[:length].rstrip() + "..."

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "author_id": self.author_id,
            "body": self.body,
            "mentioned_user_ids": list(self.mentioned_user_ids),
            "edited": self.edited,
        }
