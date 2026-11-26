"""Task domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """A unit of work belonging to a project."""

    id: str
    project_id: str
    title: str
    status: str = "open"
    assignee_id: Optional[str] = None
    estimate_hours: float = 0.0
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "status": self.status,
            "assignee_id": self.assignee_id,
        }
