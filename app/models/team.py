"""Team domain model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Team:
    """A group of users collaborating across projects."""

    id: str
    name: str
    slug: str
    owner_id: str
    member_ids: list = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "member_ids": list(self.member_ids),
        }
