"""Audit log entry model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuditLogEntry:
    """A single recorded account/team lifecycle event."""

    id: str
    entity_type: str
    entity_id: str
    action: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "action": self.action,
            "created_at": self.created_at.isoformat(),
        }
