"""Cross-domain reporting: project budget and task-activity summaries."""

import logging
from datetime import datetime

from app.core import utils
from app.models.report import ProjectReport
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService

logger = logging.getLogger(__name__)


class ReportingService:
    """Builds read-only summaries by pulling from multiple repositories."""

    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        project_service: ProjectService,
    ) -> None:
        self._project_repository = project_repository
        self._task_repository = task_repository
        self._project_service = project_service

    def generate_project_report(self, project_id: str) -> ProjectReport:
        """Build a budget-and-activity snapshot for a single project."""
        project = self._project_repository.get(project_id)
        tasks = self._task_repository.list_by_project(project_id)
        archived_tasks = self._project_service.count_archived_tasks(project_id)
        return ProjectReport(
            project_id=project.id,
            project_name=project.name,
            budget_display=utils.format_currency(project.budget, project.currency),
            total_tasks=len(tasks),
            archived_tasks=archived_tasks,
        )

    def generate_project_history_report(self, project_id: str) -> dict:
        """Wrap :meth:`ProjectService.get_project_history` with report framing."""
        history = self._project_service.get_project_history(project_id)
        history["generated_at"] = utils.format_timestamp(datetime.utcnow())
        return history
