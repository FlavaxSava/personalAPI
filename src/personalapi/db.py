from sqlmodel import SQLModel, create_engine

from personalapi import models # noqa: F401

engine = create_engine("sqlite:///personalapi.db")


def init_db() -> None:
    SQLModel.metadata.create_all(engine)