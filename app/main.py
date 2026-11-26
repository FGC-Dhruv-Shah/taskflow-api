"""Application entry point: wires every router onto a single FastAPI app."""

from fastapi import FastAPI

from app.api.routes import comment_routes, project_routes, task_routes, team_routes, user_routes
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.api_version)

app.include_router(user_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(comment_routes.router)
app.include_router(team_routes.router)
