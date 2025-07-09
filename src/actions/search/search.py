import aiohttp

from settings import settings

from ..base import ActionSet
from .search_clients.search_client_factory import SearchClientFactory
from .search_clients.wiki_client import BaseWikiClient

SEARCH_CLIENT = SearchClientFactory.get_client(settings.WIKI_CLIENT_TYPE)


class SearchActions(ActionSet):
    @staticmethod
    async def search(entity: str) -> str:
        async with aiohttp.ClientSession() as session:
            extract = await SEARCH_CLIENT.get_page_extract(session, title=entity)
            if not extract or "may refer to:" in extract:
                result = await SEARCH_CLIENT.search_page(session, entity)
                return (
                    f"No page found with title {entity}. Possible pages:\n"
                    + "\n".join([f"- {r['title']}" for r in result])
                )
            return extract

    @staticmethod
    async def lookup(entity: str, string: str) -> str:
        async with aiohttp.ClientSession() as session:
            extract = await SEARCH_CLIENT.lookup(session, entity, string)
            return extract


# if __name__ == "__main__":
#     print(SearchActions().list_action_methods())
