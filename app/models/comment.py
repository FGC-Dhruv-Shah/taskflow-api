"""Comment domain model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Comment:
    """A comment left on a task."""

    id: str
    task_id: str
    author_id: str
    body: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "author_id": self.author_id,
            "body": self.body,
        }
