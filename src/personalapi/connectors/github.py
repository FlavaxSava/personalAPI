import asyncio
import json
from datetime import datetime

import httpx
from sqlmodel import Session

from personalapi import models
from personalapi.config import settings
from personalapi.db import engine

BASE_URL = "https://api.github.com"


async def fetch_events() -> list[dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {settings.github_token.get_secret_value()}",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    url = f"{BASE_URL}/users/{settings.github_username}/events"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


def save_events(events: list[dict]) -> None:
    with Session(engine) as session:
        for event in events:
            row = models.GitHubEvent(
                id=event["id"],
                type=event["type"],
                repo_name=event["repo"]["name"],
                created_at=datetime.fromisoformat(event["created_at"]),
                raw=event,
            )
            session.merge(row)
        session.commit()


if __name__ == "__main__":
    events = asyncio.run(fetch_events())
    print(len(events))
    for event in events:
        print(event["type"])

    print(json.dumps(events[0], indent=2))
    save_events(events)
