"""HTTP routes for commenting on tasks."""

from fastapi import APIRouter

from app.repositories.comment_repository import CommentRepository
from app.services.comment_service import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])
_comment_service = CommentService(CommentRepository())


@router.post("/")
def add_comment(task_id: str, author_id: str, body: str) -> dict:
    comment = _comment_service.add_comment(task_id, author_id, body)
    return comment.to_dict()


@router.delete("/{comment_id}")
def delete_comment(comment_id: str) -> None:
    _comment_service.delete_comment(comment_id)
