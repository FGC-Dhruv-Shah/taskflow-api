"""Report output model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProjectReport:
    """A point-in-time summary of a project's budget and task activity."""

    project_id: str
    project_name: str
    budget_display: str
    total_tasks: int
    archived_tasks: int
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "budget_display": self.budget_display,
            "total_tasks": self.total_tasks,
            "archived_tasks": self.archived_tasks,
            "generated_at": self.generated_at.isoformat(),
        }
