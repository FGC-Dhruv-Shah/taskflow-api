"""HTTP routes for the per-task activity feed."""

from fastapi import APIRouter

from app.repositories.task_repository import TaskRepository
from app.services.activity_log_service import ActivityLogService

router = APIRouter(prefix="/activity", tags=["activity"])
_activity_log_service = ActivityLogService(TaskRepository())


@router.get("/tasks/{task_id}")
def get_recent_activity(task_id: str) -> dict:
    return _activity_log_service.get_recent_activity_for_task(task_id)
