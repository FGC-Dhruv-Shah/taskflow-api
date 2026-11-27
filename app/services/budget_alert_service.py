"""Checks project spend against its alert threshold and notifies when crossed."""

import logging
from datetime import datetime

from app.repositories.project_repository import ProjectRepository
from app.services.currency_converter import CurrencyConverter
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class BudgetAlertService:
    """Flags and notifies projects that have crossed their budget alert threshold."""

    def __init__(
        self,
        project_repository: ProjectRepository,
        currency_converter: CurrencyConverter,
        notification_service: NotificationService,
    ) -> None:
        self._project_repository = project_repository
        self._currency_converter = currency_converter
        self._notification_service = notification_service

    def check_and_alert(
        self, project_id: str, spent_amount: float, spent_currency: str, as_of: datetime
    ) -> dict:
        """Compare spend against budget, converting currency if needed, and notify if due."""
        project = self._project_repository.get(project_id)
        spent_in_budget_currency = self._currency_converter.convert(
            spent_amount, spent_currency, project.currency
        )
        utilization = spent_in_budget_currency / project.budget if project.budget else 0.0
        alert_sent = False
        if project.alert_due(utilization):
            self._notification_service.notify_project_members(
                project_id, f"Budget utilization at {utilization:.0%} for '{project.name}'"
            )
            self._project_repository.mark_alert_sent(project_id, as_of)
            alert_sent = True
        return {"project_id": project_id, "utilization": utilization, "alert_sent": alert_sent}
