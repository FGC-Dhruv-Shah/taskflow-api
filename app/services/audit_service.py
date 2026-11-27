"""Lightweight in-memory audit trail for account and team lifecycle events."""

import logging
import uuid

from app.models.audit_log import AuditLogEntry

logger = logging.getLogger(__name__)


class AuditService:
    """Records lifecycle events for later review."""

    def __init__(self) -> None:
        self._entries: list[AuditLogEntry] = []

    def record_event(self, entity_type: str, entity_id: str, action: str) -> AuditLogEntry:
        """Append a new audit entry and return it."""
        entry = AuditLogEntry(id=str(uuid.uuid4()), entity_type=entity_type, entity_id=entity_id, action=action)
        self._entries.append(entry)
        logger.info("Audit event recorded: %s %s %s", entity_type, entity_id, action)
        return entry

    def list_for_entity(self, entity_type: str, entity_id: str) -> list[AuditLogEntry]:
        """Return every recorded event for a given entity."""
        return [e for e in self._entries if e.entity_type == entity_type and e.entity_id == entity_id]
