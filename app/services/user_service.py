"""User registration, authentication, and profile management."""

import hashlib
import logging

from app.core import utils, validators
from app.core.exceptions import ValidationError
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    """Orchestrates user registration and authentication."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def register_user(self, name: str, email: str, password: str) -> User:
        """Validate and persist a new user account."""
        validators.validate_email(email)
        validators.validate_password_strength(password)
        clean_name = utils.normalize_text(name)
        if len(clean_name) == 0:
            raise ValidationError("Name cannot be empty")
        if self._user_repository.email_exists(email):
            raise ValidationError(f"Email '{email}' is already registered")
        user = User(
            id=self._user_repository.new_id(),
            name=clean_name,
            email=email,
            password_hash=self._hash_password(password),
        )
        return self._user_repository.create(user)

    def authenticate_user(self, email: str, password: str, ip_address: str) -> User:
        """Return the user matching ``email``/``password``, raising on mismatch.

        ``ip_address`` is recorded against the login attempt for the new
        activity-tracking feature; every call site must now supply it.
        """
        user = self._user_repository.get_by_email(email)
        if user.password_hash != self._hash_password(password):
            raise ValidationError("Invalid email or password")
        logger.info("Login for %s from %s", email, ip_address)
        return user

    def update_profile(self, user_id: str, name: str) -> User:
        """Rename an existing user's display name."""
        clean_name = utils.normalize_text(name)
        if len(clean_name) == 0:
            raise ValidationError("Name cannot be empty")
        return self._user_repository.update(user_id, name=clean_name)

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
