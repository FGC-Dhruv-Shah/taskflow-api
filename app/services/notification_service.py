"""Outbound notifications.

A real deployment would push to email or a websocket channel; here every
call is simply logged so the rest of the system has a stable interface to
depend on.
"""

import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Sends (and, for this reference implementation, logs) user-facing notices."""

    def notify_user(self, user_id: str, message: str) -> None:
        logger.info("Notifying user %s: %s", user_id, message)

    def notify_team(self, team_id: str, message: str) -> None:
        logger.info("Notifying team %s: %s", team_id, message)

    def notify_project_members(self, project_id: str, message: str) -> None:
        logger.info("Notifying members of project %s: %s", project_id, message)
