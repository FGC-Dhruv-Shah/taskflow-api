"""HTTP routes for project creation, budgeting, and archival."""

from fastapi import APIRouter

from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.notification_service import NotificationService
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])
_project_service = ProjectService(
    ProjectRepository(), TaskRepository(), NotificationService()
)


@router.post("/")
def create_project(name: str, budget: float, owner_id: str) -> dict:
    project = _project_service.create_project(name, budget, owner_id)
    return project.to_dict()


@router.post("/{project_id}/archive")
def archive_project(project_id: str, cascade: bool = True) -> dict:
    project = _project_service.archive_project(project_id, cascade=cascade)
    return project.to_dict()


@router.get("/{project_id}/history")
def get_project_history(project_id: str) -> dict:
    return _project_service.get_project_history(project_id)


@router.patch("/{project_id}/budget")
def update_budget(project_id: str, new_budget: float) -> dict:
    project = _project_service.update_budget(project_id, new_budget)
    return project.to_dict()
