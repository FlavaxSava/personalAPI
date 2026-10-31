from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from personalapi import models  # noqa: F401

engine = create_engine("sqlite:///personalapi.db")


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
