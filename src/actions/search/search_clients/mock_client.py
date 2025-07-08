# --- MOCK WIKI CLIENT ---
import random
from typing import Any
import aiohttp
from .base import BaseWikiClient

class MockWikiClient(BaseWikiClient):
    def __init__(self, config: dict | None = None):
        self.config = config or {"mode": "default"}

    async def search_page(self, session: aiohttp.ClientSession, query: str, limit=5) -> list[dict[str, Any]]:
        if self.config.get("mode") == "empty":
            return []
        return [
            {"title": f"Mock Article {i+1} for '{query}'", "snippet": f"This is a mock snippet for '{query}' (result {i+1})."}
            for i in range(limit)
        ]

    async def get_page_extract(self, session: aiohttp.ClientSession, title: str, sentences=5) -> str:
        if self.config.get("mode") == "empty":
            return ""
        return f"This is a mock extract for '{title}' with {sentences} sentences."

    async def get_full_page_content(self, session: aiohttp.ClientSession, title: str) -> str:
        if self.config.get("mode") == "empty":
            return ""
        return f"Full mock content for '{title}'."

    async def lookup(self, session: aiohttp.ClientSession, title: str, string: str) -> str:
        if self.config.get("mode") == "empty":
            return f"Could not find Wikipedia page for '{title}'."
        if string.lower() in title.lower():
            return f"Mock sentence containing '{string}' in '{title}'."
        return f"No sentence containing '{string}' found in the article."