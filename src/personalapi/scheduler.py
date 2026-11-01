import asyncio
import logging

from personalapi.config import settings
from personalapi.connectors.github import fetch_events, save_events

logger = logging.getLogger(__name__)


async def sync_github_forever() -> None:
    while True:
        try:
            events = await fetch_events()
            await asyncio.to_thread(save_events, events)
            logger.info(f"GitHub synced {len(events)} events successfully")
        except Exception:
            logger.exception("GitHub sync failed")
        await asyncio.sleep(settings.github_sync_interval_seconds)
