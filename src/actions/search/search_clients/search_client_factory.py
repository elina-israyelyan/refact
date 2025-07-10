from settings import settings

from .base import BaseWikiClient
from .mock_client import MockWikiClient
from .wiki_client import WikiClient


class SearchClientFactory:
    @staticmethod
    def get_client(client_type: str = "") -> BaseWikiClient:
        client_type = client_type or settings.SEARCH_CLIENT_TYPE
        if client_type == "mock":
            return MockWikiClient()
        elif client_type == "wiki":
            return WikiClient()
        else:
            raise ValueError(f"Invalid client type: {client_type}")
