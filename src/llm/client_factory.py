from .google_gemini_client import GeminiClient
from .mock_client import MockLLMClient
from settings import settings


class ClientFactory:
    @staticmethod
    async def get_client(client_type: str):
        if client_type == "gemini":
            return await GeminiClient.create(
                service_account_path=settings.GEMINI_SA_CREDENTIAL_PATH
            )
        elif client_type == "mock":
            return MockLLMClient()
        else:
            raise ValueError(f"Invalid client type: {client_type}")
