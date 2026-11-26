"""Project domain model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Project:
    """A workspace that groups related tasks."""

    id: str
    name: str
    slug: str
    owner_id: str
    budget: float = 0.0
    currency: str = "USD"
    is_archived: bool = False
    is_deleted: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "owner_id": self.owner_id,
            "budget": self.budget,
            "is_archived": self.is_archived,
        }
