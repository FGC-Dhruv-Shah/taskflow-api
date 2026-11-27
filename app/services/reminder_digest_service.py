"""Builds a cross-project overdue-task digest for a workspace owner."""

import logging
from datetime import datetime

from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

logger = logging.getLogger(__name__)


class ReminderDigestService:
    """Aggregates overdue tasks across every project an owner holds."""

    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository) -> None:
        self._project_repository = project_repository
        self._task_repository = task_repository

    def build_digest(self, owner_id: str, as_of: datetime) -> dict:
        """Return an overdue-task count per project owned by ``owner_id``."""
        projects = self._project_repository.list_for_owner(owner_id)
        per_project = {
            project.id: self._task_repository.count_overdue(project.id, as_of)
            for project in projects
        }
        return {
            "owner_id": owner_id,
            "projects": per_project,
            "total_overdue": sum(per_project.values()),
        }
