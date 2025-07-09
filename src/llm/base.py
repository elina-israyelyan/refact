from abc import ABC, abstractmethod
from typing import Any, Type

from google.genai import types as genai_types
from pydantic import BaseModel

from .models.history import HistoryPoint
import copy


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
        model_name: str | None = None,
    ) -> str:
        """Generate content using the LLM with an optional response schema"""
        raise NotImplementedError

    @property
    def default_model_name(self) -> str:
        """Get the default model name"""
        return self._default_model_name

    @default_model_name.setter
    def default_model_name(self, model_name: str) -> None:
        """Set the default model name"""
        self._default_model_name = model_name

    @property
    def default_generation_config(self) -> genai_types.GenerateContentConfigDict:
        """Get the default generation configuration"""
        return copy.deepcopy(self._default_generation_config)

    @default_generation_config.setter
    def default_generation_config(
        self, config: genai_types.GenerateContentConfigDict
    ) -> None:
        """Set the default generation configuration"""
        self._default_generation_config = config
