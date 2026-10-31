from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from personalapi.db import get_session
from personalapi.models import GitHubEvent

app = FastAPI()


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
) -> list[GitHubEvent]:
    statement = select(GitHubEvent)
    return list(session.exec(statement).all())
