"""Persistence for ``User`` entities."""

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.repositories.base import InMemoryRepository


class UserRepository(InMemoryRepository[User]):
    """CRUD plus email lookup for users."""

    def get_by_email(self, email: str) -> User:
        for user in self.list_all():
            if user.email == email:
                return user
        raise NotFoundError(f"No user registered with email '{email}'")

    def email_exists(self, email: str) -> bool:
        return any(user.email == email for user in self.list_all())

    def list_by_ids(self, user_ids: list) -> list[User]:
        """Return every known user whose id is in ``user_ids``, skipping unknown ids."""
        wanted = set(user_ids)
        return [user for user in self.list_all() if user.id in wanted]

    def list_active(self) -> list[User]:
        """Return every user account that is currently active."""
        return [user for user in self.list_all() if user.is_active]

    def count_active(self) -> int:
        return len(self.list_active())

    def search_by_name(self, query: str) -> list[User]:
        """Return users whose name contains ``query``, case-insensitively."""
        needle = query.lower()
        return [user for user in self.list_all() if needle in user.name.lower()]
