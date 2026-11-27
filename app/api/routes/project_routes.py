"""HTTP routes for project creation, budgeting, and archival."""

from datetime import datetime

from fastapi import APIRouter

from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.budget_alert_service import BudgetAlertService
from app.services.currency_converter import CurrencyConverter
from app.services.notification_service import NotificationService
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])
_project_repository = ProjectRepository()
_project_service = ProjectService(
    _project_repository, TaskRepository(), NotificationService()
)
_budget_alert_service = BudgetAlertService(
    _project_repository, CurrencyConverter(), NotificationService()
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


@router.post("/{project_id}/budget-alert-check")
def check_budget_alert(project_id: str, spent_amount: float, spent_currency: str = "USD") -> dict:
    return _budget_alert_service.check_and_alert(
        project_id, spent_amount, spent_currency, datetime.utcnow()
    )
