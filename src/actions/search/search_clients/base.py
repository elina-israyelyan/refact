from abc import ABC, abstractmethod
from typing import Any
import aiohttp

class BaseWikiClient(ABC):
    @abstractmethod
    async def search_page(self, session: aiohttp.ClientSession, query: str, limit: int = 5) -> list[dict[str, Any]]: 
        raise NotImplementedError
    @abstractmethod
    async def get_page_extract(self, session: aiohttp.ClientSession, title: str, sentences: int = 5) -> str: 
        raise NotImplementedError
    @abstractmethod
    async def get_full_page_content(self, session: aiohttp.ClientSession, title: str) -> str: 
        raise NotImplementedError
    @abstractmethod
    async def lookup(self, session: aiohttp.ClientSession, title: str, string: str) -> str: 
        raise NotImplementedError