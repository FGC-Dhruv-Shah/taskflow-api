"""User domain model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    """A registered TaskFlow account."""

    id: str
    name: str
    email: str
    password_hash: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
        }
