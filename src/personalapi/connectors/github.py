import asyncio

import httpx

from personalapi.config import settings

BASE_URL = "https://api.github.com"

async def fetch_events() -> list[dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {settings.github_token.get_secret_value()}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    url = f"{BASE_URL}/users/{settings.github_username}/events"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    events = asyncio.run(fetch_events())
    print(len(events))
    for event in events:
        print(event["type"])

    import json
    print(json.dumps(events[0], indent=2))