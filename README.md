# TaskFlow API

A lightweight task and project management backend. Teams create projects,
break work into tasks, assign them to members, track time against them,
and leave comments as work progresses.

## Architecture

```
app/
  api/routes/     HTTP endpoints (FastAPI routers)
  services/       Business logic and orchestration
  repositories/   Persistence (in-memory for this reference implementation)
  models/         Domain dataclasses
  core/           Shared config, validators, exceptions, and utilities
```

Each layer only talks to the layer directly below it: routes call services,
services call repositories (plus other services where a workflow spans
domains, e.g. assigning a task sends a notification).

## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
