"""Team creation and membership management."""

import logging

from app.core import utils
from app.core.exceptions import ValidationError
from app.models.team import Team
from app.repositories.team_repository import TeamRepository
from app.services.audit_service import AuditService
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class TeamService:
    """Orchestrates team creation and membership changes."""

    def __init__(
        self,
        team_repository: TeamRepository,
        notification_service: NotificationService,
        audit_service: AuditService,
    ) -> None:
        self._team_repository = team_repository
        self._notification_service = notification_service
        self._audit_service = audit_service

    def create_team(self, name: str, owner_id: str) -> Team:
        """Validate and persist a new team, deriving its slug from ``name``."""
        clean_name = utils.normalize_text(name)
        if len(clean_name) == 0:
            raise ValidationError("Team name cannot be empty")
        team = Team(
            id=self._team_repository.new_id(),
            name=clean_name,
            slug=utils.slugify(clean_name),
            owner_id=owner_id,
            member_ids=[owner_id],
        )
        return self._team_repository.create(team)

    def add_member(self, team_id: str, user_id: str) -> Team:
        """Add ``user_id`` to the team's roster and notify the whole team."""
        team = self._team_repository.get(team_id)
        if user_id in team.member_ids:
            return team
        updated_members = [*team.member_ids, user_id]
        team = self._team_repository.update(team_id, member_ids=updated_members)
        self._notification_service.notify_team(team_id, f"A new member joined {team.name}")
        return team

    def remove_member(self, team_id: str, user_id: str) -> Team:
        """Remove ``user_id`` from the team's roster, if present."""
        team = self._team_repository.get(team_id)
        remaining = [m for m in team.member_ids if m != user_id]
        return self._team_repository.update(team_id, member_ids=remaining)

    def rename_team(self, team_id: str, new_name: str) -> Team:
        """Rename an existing team, deriving a fresh slug from ``new_name``."""
        clean_name = utils.normalize_text(new_name)
        if len(clean_name) == 0:
            raise ValidationError("Team name cannot be empty")
        team = self._team_repository.update(team_id, name=clean_name, slug=utils.slugify(clean_name))
        self._audit_service.record_event("team", team_id, "renamed")
        return team
