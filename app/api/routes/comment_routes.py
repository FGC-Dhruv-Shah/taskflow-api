"""HTTP routes for commenting on tasks."""

from fastapi import APIRouter

from app.repositories.comment_repository import CommentRepository
from app.repositories.user_repository import UserRepository
from app.services.comment_service import CommentService
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/comments", tags=["comments"])
_comment_repository = CommentRepository()
_comment_service = CommentService(_comment_repository, UserRepository(), NotificationService())


@router.post("/")
def add_comment(task_id: str, author_id: str, body: str) -> dict:
    comment = _comment_service.add_comment(task_id, author_id, body)
    return comment.to_dict()


@router.patch("/{comment_id}")
def edit_comment(comment_id: str, new_body: str) -> dict:
    comment = _comment_service.edit_comment(comment_id, new_body)
    return comment.to_dict()


@router.get("/mentions/{user_id}")
def list_mentions(user_id: str) -> list[dict]:
    comments = _comment_repository.list_mentioning(user_id)
    return [c.to_dict() for c in comments]


@router.delete("/{comment_id}")
def delete_comment(comment_id: str) -> None:
    _comment_service.delete_comment(comment_id)
