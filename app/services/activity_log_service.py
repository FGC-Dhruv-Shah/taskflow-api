"""Recent-activity feed for tasks, built on top of existing task records."""

import logging

from app.repositories.task_repository import TaskRepository

logger = logging.getLogger(__name__)


class ActivityLogService:
    """Surfaces a lightweight activity feed for a single task."""

    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def get_recent_activity_for_task(self, task_id: str) -> dict:
        """Return a summary of the most recent activity recorded for ``task_id``."""
        task = self._task_repository.get(task_id)
        time_entries = self._task_repository.get_time_entries(task_id)
        return {
            "task_title": task["title"],
            "current_status": task["status"],
            "logged_entries": len(time_entries),
            "total_logged_seconds": self._task_repository.total_logged_seconds(task_id),
        }
