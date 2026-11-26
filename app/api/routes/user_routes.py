"""HTTP routes for user registration, login, and profile management."""

from fastapi import APIRouter

from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
_user_service = UserService(UserRepository())


@router.post("/register")
def register(name: str, email: str, password: str) -> dict:
    user = _user_service.register_user(name, email, password)
    return user.to_dict()


@router.post("/login")
def login(email: str, password: str) -> dict:
    user = _user_service.authenticate_user(email, password)
    return user.to_dict()


@router.patch("/{user_id}")
def update_profile(user_id: str, name: str) -> dict:
    user = _user_service.update_profile(user_id, name)
    return user.to_dict()
