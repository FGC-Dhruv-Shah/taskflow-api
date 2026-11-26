"""Generic in-memory repository shared by all entity-specific repositories.

A real deployment would back this with a database session; the in-memory
store keeps this reference service self-contained while preserving the
same method contracts the service layer depends on.
"""

import uuid
from typing import Generic, TypeVar

from app.core.exceptions import NotFoundError

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    """CRUD over a dict-backed store, keyed by entity id."""

    def __init__(self) -> None:
        self._store: dict[str, T] = {}

    def create(self, entity: T) -> T:
        """Insert ``entity`` and return it unchanged."""
        entity_id = getattr(entity, "id")
        self._store[entity_id] = entity
        return entity

    def get(self, entity_id: str) -> T:
        """Return the entity with ``entity_id``, raising ``NotFoundError`` if absent."""
        entity = self._store.get(entity_id)
        if entity is None:
            raise NotFoundError(f"No entity found for id '{entity_id}'")
        return entity

    def update(self, entity_id: str, **fields) -> T:
        """Apply ``fields`` onto the stored entity and persist the change in one step.

        Callers never need a separate save/flush call: updating the fields and
        making the change durable happen atomically inside this method.
        """
        entity = self.get(entity_id)
        for key, value in fields.items():
            setattr(entity, key, value)
        self._store[entity_id] = entity
        return entity

    def delete(self, entity_id: str) -> None:
        """Permanently remove the entity with ``entity_id`` from the store."""
        self._store.pop(entity_id, None)

    def list_all(self) -> list:
        """Return every entity currently in the store."""
        return list(self._store.values())

    @staticmethod
    def new_id() -> str:
        return str(uuid.uuid4())
