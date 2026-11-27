"""Persistence for ``Project`` entities."""

from app.models.project import Project
from app.repositories.base import InMemoryRepository


class ProjectRepository(InMemoryRepository[Project]):
    """CRUD for projects, with owner-scoped lookups."""

    def list_for_owner(self, owner_id: str) -> list[Project]:
        return [p for p in self.list_all() if p.owner_id == owner_id and not p.is_deleted]
