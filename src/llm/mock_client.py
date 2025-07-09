import json
import random
from typing import Type

from local_logging import logger

from google.genai import types as genai_types
from pydantic import BaseModel

from utils.prompting_history_points import (
    CALCULATOR_HISTORY_POINTS,
    SEARCH_HISTORY_POINTS,
)

from .base import BaseLLMClient
from .models.history import HistoryPoint


class MockLLMClient(BaseLLMClient):
    def __init__(self):
        self._default_model_name = "mock"
        self._default_generation_config = {}

    @classmethod
    async def create(
        cls,
        service_account_path: str,
        location: str | None = None,
        default_model_name: str | None = None,
        default_generation_config: genai_types.GenerateContentConfigDict | None = None,
    ):
        return cls()

    async def generate_content(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        history: list[HistoryPoint] | None = None,
        model_name: str | None = None,
    ) -> str:
        last_model_message = None

        # If no match, fill all fields with dummy values
        dummy = random.choice(
            [
                {
                    "action": {
                        "action_set_name": "SearchActions",
                        "action_method_name": "search",
                        "args": [
                            {
                                "arg_name": "entity",
                                "arg_type": "str",
                                "arg_value": "Python",
                            }
                        ],
                    }
                },
                {
                    "action": {
                        "action_set_name": "MathActions",
                        "action_method_name": "sum",
                        "args": [
                            {"arg_name": "a", "arg_type": "int", "arg_value": 1},
                            {"arg_name": "b", "arg_type": "int", "arg_value": 2},
                        ],
                    }
                },
            ]
        )
        for name, field in response_schema.model_fields.items():
            if name in dummy:
                continue
            if field.annotation == str:
                dummy[name] = "This is a mock answer."
            elif field.annotation in (int, float):
                dummy[name] = 42
            elif field.annotation == bool:
                dummy[name] = random.randint(0, 10) == 4
            elif (
                field.annotation is not None
                and hasattr(field.annotation, "__origin__")
                and field.annotation.__origin__ is list
            ):
                dummy[name] = []
            else:
                dummy[name] = None
        return response_schema.model_validate(dummy).model_dump_json()
