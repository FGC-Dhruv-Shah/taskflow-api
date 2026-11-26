"""HTTP routes for team creation and membership."""

from fastapi import APIRouter

from app.repositories.team_repository import TeamRepository
from app.services.notification_service import NotificationService
from app.services.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["teams"])
_team_service = TeamService(TeamRepository(), NotificationService())


@router.post("/")
def create_team(name: str, owner_id: str) -> dict:
    team = _team_service.create_team(name, owner_id)
    return team.to_dict()


@router.post("/{team_id}/members")
def add_member(team_id: str, user_id: str) -> dict:
    team = _team_service.add_member(team_id, user_id)
    return team.to_dict()


@router.delete("/{team_id}/members/{user_id}")
def remove_member(team_id: str, user_id: str) -> dict:
    team = _team_service.remove_member(team_id, user_id)
    return team.to_dict()
