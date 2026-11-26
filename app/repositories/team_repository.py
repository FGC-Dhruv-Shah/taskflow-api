"""Persistence for ``Team`` entities."""

from app.models.team import Team
from app.repositories.base import InMemoryRepository


class TeamRepository(InMemoryRepository[Team]):
    """CRUD for teams, with membership lookups."""

    def list_for_member(self, user_id: str) -> list[Team]:
        return [t for t in self.list_all() if user_id in t.member_ids]
