"""Project lifecycle: creation, budget tracking, and archival."""

import logging
from datetime import datetime

from app.core import utils, validators
from app.core.exceptions import ValidationError
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class ProjectService:
    """Orchestrates project creation, budgeting, and archival."""

    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        notification_service: NotificationService,
    ) -> None:
        self._project_repository = project_repository
        self._task_repository = task_repository
        self._notification_service = notification_service

    def create_project(self, name: str, budget: float, owner_id: str) -> Project:
        """Validate and persist a new project, deriving its URL slug from ``name``."""
        clean_name = utils.normalize_text(name)
        if len(clean_name) == 0:
            raise ValidationError("Project name cannot be empty")
        validators.validate_project_name(clean_name)
        project = Project(
            id=self._project_repository.new_id(),
            name=clean_name,
            slug=utils.slugify(clean_name),
            owner_id=owner_id,
            budget=budget,
        )
        return self._project_repository.create(project)

    def update_budget(self, project_id: str, new_budget: float) -> Project:
        """Set a project's budget, logging the human-readable amount."""
        project = self._project_repository.update(project_id, budget=new_budget)
        logger.info(
            "Project %s budget updated to %s",
            project_id,
            utils.format_currency(new_budget, project.currency),
        )
        return project

    def archive_project(self, project_id: str, cascade: bool = True) -> Project:
        """Archive a project and, when ``cascade`` is set, archive its open tasks too.

        Archival is the project's terminal state: once archived, no further
        task creation is permitted against it, and every currently open task
        is moved to the ``"archived"`` status so dashboards stop surfacing
        work against a project nobody is actively tracking anymore. The
        cascade step is best-effort: a task that fails to update is logged
        and skipped rather than aborting the whole archival.
        """
        project = self._project_repository.get(project_id)
        if project.is_archived:
            logger.info("Project %s is already archived", project_id)
            return project

        if cascade:
            open_tasks = [
                task
                for task in self._task_repository.list_by_project(project_id)
                if task.status not in ("completed", "archived")
            ]
            for task in open_tasks:
                try:
                    self._task_repository.update_task_status(task.id, "archived")
                except Exception:  # pragma: no cover - defensive, see docstring
                    logger.exception("Failed to archive task %s, continuing", task.id)

        archived = self._project_repository.update(project_id, is_archived=True)
        self._notification_service.notify_project_members(
            project_id,
            f"Project '{project.name}' was archived at {utils.format_timestamp(datetime.utcnow())}",
        )
        return archived

    def get_project_history(self, project_id: str) -> dict:
        """Return a project's current state, including deleted/archived ones.

        Deletion in this system is soft: a deleted project's id still
        resolves here so that audit and reporting views can show what
        happened to it, instead of raising ``NotFoundError``.
        """
        project = self._project_repository.get(project_id)
        return {
            "project": project.to_dict(),
            "status": "deleted" if project.is_deleted else ("archived" if project.is_archived else "active"),
        }
