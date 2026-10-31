from datetime import datetime

from sqlmodel import JSON, Column, Field, SQLModel


class GitHubEvent(SQLModel, table=True):
    id: str = Field(primary_key=True)
    type: str
    repo_name: str
    created_at: datetime = Field(index=True)
    raw: dict = Field(sa_column=Column(JSON, nullable=False))
