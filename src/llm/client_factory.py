from .google_gemini_client import GeminiClient
from .mock_client import MockLLMClient

class ClientFactory:
    @staticmethod
    async def get_client(client_type: str):
        if client_type == "gemini":
            return await GeminiClient.create(service_account_path="/home/elina-jan/Downloads/amaros-420712-1f28953e284e.json")
        elif client_type == "mock":
            return MockLLMClient()
        else:
            raise ValueError(f"Invalid client type: {client_type}")