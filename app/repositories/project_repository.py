"""Persistence for ``Project`` entities."""

from datetime import datetime

from app.models.project import Project
from app.repositories.base import InMemoryRepository


class ProjectRepository(InMemoryRepository[Project]):
    """CRUD for projects, with a soft-delete override.

    ``delete`` does not remove the row: it flags the project as deleted so
    that history and reporting views can still resolve the id. Callers that
    need an actual removal should filter on ``is_deleted`` themselves; this
    repository never purges a project from the store.
    """

    def delete(self, project_id: str) -> None:
        self.update(project_id, is_deleted=True)

    def list_for_owner(self, owner_id: str) -> list[Project]:
        return [p for p in self.list_all() if p.owner_id == owner_id and not p.is_deleted]

    def list_by_currency(self, currency: str) -> list[Project]:
        return [p for p in self.list_all() if p.currency == currency and not p.is_deleted]

    def mark_alert_sent(self, project_id: str, at: datetime) -> Project:
        """Record that a budget alert was just sent for this project."""
        return self.update(project_id, last_alert_sent_at=at)

    def list_alert_candidates(self, since: datetime) -> list[Project]:
        """Return non-archived projects that haven't had an alert since ``since``."""
        return [
            p
            for p in self.list_all()
            if not p.is_archived
            and not p.is_deleted
            and (p.last_alert_sent_at is None or p.last_alert_sent_at < since)
        ]
