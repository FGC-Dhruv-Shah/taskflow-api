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
    due_date: Optional[datetime] = None
    reminder_sent: bool = False
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_overdue(self, as_of: datetime) -> bool:
        """Return whether this task's due date has passed and it isn't done."""
        if self.due_date is None or self.status == "completed":
            return False
        return self.due_date < as_of

    def mark_reminder_sent(self) -> None:
        self.reminder_sent = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "status": self.status,
            "assignee_id": self.assignee_id,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "reminder_sent": self.reminder_sent,
        }
