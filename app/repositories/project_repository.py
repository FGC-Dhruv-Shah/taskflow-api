"""Persistence for ``Project`` entities."""

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
