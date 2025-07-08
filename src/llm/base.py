from abc import ABC, abstractmethod
from typing import Type, Any

from google.genai import types as genai_types
from pydantic import BaseModel

from .models.history import HistoryPoint


class BaseLLMClient(ABC):

    @classmethod
    @abstractmethod
    async def create(
        cls,
        service_account_path: str,
        location: str | None = None,
        default_model_name: str | None = None,
        default_generation_config: genai_types.GenerateContentConfigDict | None = None,
    ) -> "BaseLLMClient":
        """Create a new instance of the LLM client"""
        raise NotImplementedError

    @abstractmethod
    async def generate_content(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        history: list[HistoryPoint] | None = None,
        model_name: str| None = None,
    ) -> str:
        """Generate content using the LLM with an optional response schema"""
        raise NotImplementedError

    @property
    @abstractmethod
    def default_model_name(self) -> str:
        """Get the default model name"""
        raise NotImplementedError

    @default_model_name.setter
    @abstractmethod
    def default_model_name(self, model_name: str) -> None:
        """Set the default model name"""
        raise NotImplementedError

    @property
    @abstractmethod
    def default_generation_config(self) -> Any:
        """Get the default generation configuration"""
        raise NotImplementedError

    @default_generation_config.setter
    @abstractmethod
    def default_generation_config(self, config: Any) -> None:
        """Set the default generation configuration"""
        raise NotImplementedError
