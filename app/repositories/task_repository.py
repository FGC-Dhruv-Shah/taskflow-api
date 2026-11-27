"""Persistence for ``Task`` entities, plus lightweight time-tracking."""

from datetime import datetime, timedelta

from app.core import utils
from app.models.task import Task
from app.repositories.base import InMemoryRepository


class TaskRepository(InMemoryRepository[Task]):
    """CRUD for tasks, with project-scoped lookups and time logging."""

    def __init__(self) -> None:
        super().__init__()
        self._time_entries: dict[str, list[dict]] = {}

    def list_by_project(self, project_id: str) -> list[Task]:
        return [t for t in self.list_all() if t.project_id == project_id]

    def list_overdue(self, project_id: str, as_of: datetime) -> list[Task]:
        """Return a project's tasks whose due date has passed."""
        return [t for t in self.list_by_project(project_id) if t.is_overdue(as_of)]

    def count_overdue(self, project_id: str, as_of: datetime) -> int:
        return len(self.list_overdue(project_id, as_of))

    def list_due_soon(self, project_id: str, as_of: datetime, within_hours: int = 24) -> list[Task]:
        """Return a project's open tasks due within ``within_hours`` of ``as_of``."""
        horizon = as_of + timedelta(hours=within_hours)
        return [
            t
            for t in self.list_by_project(project_id)
            if t.due_date is not None
            and t.status != "completed"
            and as_of <= t.due_date <= horizon
        ]

    def unsent_reminders(self, project_id: str, as_of: datetime) -> list[Task]:
        """Return overdue tasks that have not yet had a reminder sent."""
        return [t for t in self.list_overdue(project_id, as_of) if not t.reminder_sent]

    def update_task_status(self, task_id: str, status: str) -> Task:
        """Set ``status`` on the task and persist it in a single call."""
        return self.update(task_id, status=status, updated_at=datetime.utcnow())

    def log_time_entry(self, task_id: str, start: datetime, end: datetime) -> int:
        """Record a worked time entry for ``task_id`` and return its duration in seconds."""
        duration_seconds = utils.calculate_duration(start, end)
        self._time_entries.setdefault(task_id, []).append(
            {"start": start, "end": end, "duration_seconds": duration_seconds}
        )
        return duration_seconds

    def total_logged_seconds(self, task_id: str) -> int:
        return sum(entry["duration_seconds"] for entry in self._time_entries.get(task_id, []))
