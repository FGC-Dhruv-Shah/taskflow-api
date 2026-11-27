"""Project domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """A workspace that groups related tasks."""

    id: str
    name: str
    slug: str
    owner_id: str
    budget: float = 0.0
    currency: str = "USD"
    budget_alert_threshold: float = 0.9
    last_alert_sent_at: Optional[datetime] = None
    is_archived: bool = False
    is_deleted: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

    def alert_due(self, utilization: float) -> bool:
        """Return whether ``utilization`` crosses this project's alert threshold."""
        return utilization >= self.budget_alert_threshold

    def budget_remaining(self, spent: float) -> float:
        """Return the unspent portion of the budget, floored at zero."""
        return max(self.budget - spent, 0.0)

    def has_recent_alert(self, since) -> bool:
        return self.last_alert_sent_at is not None and self.last_alert_sent_at >= since

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "owner_id": self.owner_id,
            "budget": self.budget,
            "currency": self.currency,
            "budget_alert_threshold": self.budget_alert_threshold,
            "is_archived": self.is_archived,
        }
