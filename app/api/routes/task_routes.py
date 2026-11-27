"""HTTP routes for task creation, assignment, and completion."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter

from app.repositories.task_repository import TaskRepository
from app.services.notification_service import NotificationService
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
_task_service = TaskService(TaskRepository(), NotificationService())


@router.post("/")
def create_task(
    project_id: str, title: str, estimate_hours: float = 0.0, due_date: Optional[datetime] = None
) -> dict:
    task = _task_service.create_task(project_id, title, estimate_hours, due_date)
    return task.to_dict()


@router.get("/projects/{project_id}/overdue")
def get_overdue_tasks(project_id: str) -> list[dict]:
    tasks = _task_service.get_overdue_tasks(project_id, datetime.utcnow())
    return [t.to_dict() for t in tasks]


@router.post("/{task_id}/remind")
def send_reminder(task_id: str) -> dict:
    task = _task_service.send_reminder(task_id)
    return task.to_dict()


@router.post("/{task_id}/assign")
def assign_task(task_id: str, user_id: str) -> dict:
    task = _task_service.assign_task(task_id, user_id)
    return task.to_dict()


@router.post("/{task_id}/complete")
def complete_task(task_id: str) -> dict:
    task = _task_service.complete_task(task_id)
    return task.to_dict()
