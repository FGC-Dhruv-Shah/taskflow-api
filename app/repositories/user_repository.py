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
