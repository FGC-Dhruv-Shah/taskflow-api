"""Persistence for ``Task`` entities, plus lightweight time-tracking."""

from datetime import datetime

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

    def update_task_status(self, task_id: str, status: str) -> Task:
        """Apply the new ``status`` to the in-memory task object."""
        task = self.get(task_id)
        task.status = status
        task.updated_at = datetime.utcnow()
        return task

    def save(self, task: Task) -> Task:
        """Persist a task object."""
        self._store[task.id] = task
        return task

    def log_time_entry(self, task_id: str, start: datetime, end: datetime) -> int:
        """Record a worked time entry for ``task_id`` and return its duration in seconds."""
        duration_seconds = utils.calculate_duration(start, end)
        self._time_entries.setdefault(task_id, []).append(
            {"start": start, "end": end, "duration_seconds": duration_seconds}
        )
        return duration_seconds

    def get_time_entries(self, task_id: str) -> list[dict]:
        """Return every logged time entry for ``task_id``, most recent first."""
        return list(reversed(self._time_entries.get(task_id, [])))

    def total_logged_seconds(self, task_id: str) -> int:
        return sum(entry["duration_seconds"] for entry in self._time_entries.get(task_id, []))
