"""HTTP routes for task creation, assignment, and completion."""

from fastapi import APIRouter

from app.repositories.task_repository import TaskRepository
from app.services.notification_service import NotificationService
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
_task_service = TaskService(TaskRepository(), NotificationService())


@router.post("/")
def create_task(project_id: str, title: str, estimate_hours: float = 0.0) -> dict:
    task = _task_service.create_task(project_id, title, estimate_hours)
    return task.to_dict()


@router.post("/{task_id}/assign")
def assign_task(task_id: str, user_id: str) -> dict:
    task = _task_service.assign_task(task_id, user_id)
    return task.to_dict()


@router.post("/{task_id}/complete")
def complete_task(task_id: str) -> dict:
    task = _task_service.complete_task(task_id)
    return task.to_dict()
