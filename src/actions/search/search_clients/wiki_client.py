import os
from typing import Any, Protocol

import aiohttp

from .base import BaseWikiClient
from .mock_client import MockWikiClient

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_PAGE_RAW_CONTENT_URL = (
    "https://en.wikipedia.org/w/index.php?title={title}&action=raw"
)


class WikiClient(BaseWikiClient):
    async def search_page(
        self, session: aiohttp.ClientSession, query: str, limit=5
    ) -> list[dict[str, Any]]:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": limit,
        }
        async with session.get(WIKIPEDIA_API_URL, params=params) as resp:
            data = await resp.json()
            return data["query"]["search"]

    async def get_page_extract(
        self, session: aiohttp.ClientSession, title: str, sentences=5
    ) -> str:
        params = {
            "action": "query",
            "prop": "extracts",
            "exintro": "true",
            "explaintext": "true",
            "redirects": "1",
            "exsentences": sentences,
            "exlimit": sentences,
            "titles": title,
            "format": "json",
            "utf8": 1,
        }
        async with session.get(WIKIPEDIA_API_URL, params=params) as resp:
            data = await resp.json()
            pages = data.get("query", {}).get("pages", {})
            if not pages:
                return ""
            extract = next(iter(pages.values())).get("extract")
            return extract

    async def get_full_page_content(
        self, session: aiohttp.ClientSession, title: str
    ) -> str:
        async with session.get(
            WIKIPEDIA_PAGE_RAW_CONTENT_URL.format(title=title)
        ) as response:
            if response.status != 200:
                return f"\u274c HTTP error: {response.status}"
            return (await response.read()).decode()

    async def lookup(
        self, session: aiohttp.ClientSession, title: str, string: str
    ) -> str:
        text = await self.get_full_page_content(session, title)
        if not text:
            return f"Could not find Wikipedia page for '{title}'."
        sentences = text.split("\n")
        for i, sentence in enumerate(sentences):
            if string.lower() in sentence.lower():
                return sentence
        return f"No sentence containing '{string}' found in the article."
