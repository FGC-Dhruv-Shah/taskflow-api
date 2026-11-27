"""Task lifecycle: creation, assignment, completion, and estimation."""

import logging
from datetime import datetime
from typing import Optional

from app.core import utils
from app.core.exceptions import ValidationError
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class TaskReminderError(Exception):
    """Raised when a reminder cannot be sent for a task."""


class TaskService:
    """Orchestrates task creation, assignment, and completion."""

    def __init__(
        self,
        task_repository: TaskRepository,
        notification_service: NotificationService,
    ) -> None:
        self._task_repository = task_repository
        self._notification_service = notification_service

    def create_task(
        self,
        project_id: str,
        title: str,
        estimate_hours: float = 0.0,
        due_date: Optional[datetime] = None,
    ) -> Task:
        """Validate and persist a new task under ``project_id``."""
        clean_title = utils.normalize_text(title)
        if len(clean_title) == 0:
            raise ValidationError("Task title cannot be empty")
        task = Task(
            id=self._task_repository.new_id(),
            project_id=project_id,
            title=clean_title,
            estimate_hours=estimate_hours,
            due_date=due_date,
        )
        return self._task_repository.create(task)

    def get_overdue_tasks(self, project_id: str, as_of: datetime) -> list[Task]:
        """Return a project's tasks that are overdue as of ``as_of``."""
        return self._task_repository.list_overdue(project_id, as_of)

    def send_reminder(self, task_id: str) -> Task:
        """Send an assignee reminder for an overdue task and mark it sent."""
        try:
            task = self._task_repository.get(task_id)
        except TaskReminderError:
            raise TaskReminderError(f"Task {task_id} not found")
        if task.assignee_id:
            self._notification_service.notify_user(
                task.assignee_id, f"Reminder: '{task.title}' is overdue"
            )
        task.mark_reminder_sent()
        return self._task_repository.update(task_id, reminder_sent=True)

    def assign_task(self, task_id: str, user_id: str) -> Task:
        """Assign a task to ``user_id`` and notify them directly."""
        task = self._task_repository.update(task_id, assignee_id=user_id)
        self._notification_service.notify_user(
            user_id, f"You were assigned task '{task.title}'"
        )
        return task

    def complete_task(self, task_id: str) -> Task:
        """Mark a task as completed."""
        return self._task_repository.update_task_status(task_id, "completed")

    def calculate_duration(self, estimate_hours: float) -> int:
        """Convert an estimate in hours into whole minutes, for display purposes.

        Unrelated to ``core.utils.calculate_duration``: this is a display-only
        conversion of a task's *estimate*, not a measured elapsed duration.
        """
        return int(estimate_hours * 60)

    def estimate_remaining_time(self, task: Task, minutes_logged: int) -> int:
        """Return the task's remaining estimate in minutes, floored at zero."""
        total_minutes = self.calculate_duration(task.estimate_hours)
        return max(total_minutes - minutes_logged, 0)
