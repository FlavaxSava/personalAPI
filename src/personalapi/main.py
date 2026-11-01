import asyncio
import contextlib
import logging
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, FastAPI, Query
from sqlmodel import Session, col, select

from personalapi.db import get_session, init_db
from personalapi.models import GitHubEvent
from personalapi.scheduler import sync_github_forever

logging.basicConfig(level=logging.INFO)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    init_db()
    task = asyncio.create_task(sync_github_forever())
    yield
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "hello"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/github/events")
def list_github_events(
    session: Annotated[Session, Depends(get_session)],
    event_type: Annotated[str | None, Query(alias="type")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[GitHubEvent]:
    statement = (
        select(GitHubEvent).order_by(col(GitHubEvent.created_at).desc()).limit(limit)
    )
    if event_type is not None:
        statement = statement.where(GitHubEvent.type == event_type)
    return list(session.exec(statement).all())
