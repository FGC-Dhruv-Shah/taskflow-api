"""HTTP routes for project reporting."""

from fastapi import APIRouter

from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.notification_service import NotificationService
from app.services.project_service import ProjectService
from app.services.reporting_service import ReportingService

router = APIRouter(prefix="/reports", tags=["reports"])
_project_repository = ProjectRepository()
_task_repository = TaskRepository()
_project_service = ProjectService(_project_repository, _task_repository, NotificationService())
_reporting_service = ReportingService(_project_repository, _task_repository, _project_service)


@router.get("/projects/{project_id}")
def get_project_report(project_id: str) -> dict:
    return _reporting_service.generate_project_report(project_id).to_dict()


@router.get("/projects/{project_id}/history")
def get_project_history_report(project_id: str) -> dict:
    return _reporting_service.generate_project_history_report(project_id)
