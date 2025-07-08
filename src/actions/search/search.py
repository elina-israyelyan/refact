import aiohttp
from .search_clients.wiki_client import WikiClientFactory, BaseWikiClient
from ..base import ActionSet

_default_wiki_client = WikiClientFactory.get_client()

class SearchActions(ActionSet):
    @staticmethod
    async def search(entity: str, wiki_client: BaseWikiClient = _default_wiki_client) -> str:
        async with aiohttp.ClientSession() as session:
            extract = await wiki_client.get_page_extract(session, title=entity)
            if not extract or "may refer to:" in extract:
                result = await wiki_client.search_page(session, entity)
                return f"No page found with title {entity}. Possible pages:\n" + "\n".join([f"- {r['title']}" for r in result])
            return extract

    @staticmethod
    async def lookup(entity: str, string: str, wiki_client: BaseWikiClient = _default_wiki_client) -> str:
        async with aiohttp.ClientSession() as session:
            extract = await wiki_client.lookup(session, entity, string)
            return extract

if __name__ == "__main__":
    print(SearchActions().list_action_methods())