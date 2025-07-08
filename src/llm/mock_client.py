import random
from typing import Type
from pydantic import BaseModel
from .base import BaseLLMClient
from .models.history import HistoryPoint
from prompting_history_points import SEARCH_HISTORY_POINTS, CALCULATOR_HISTORY_POINTS
from google.genai import types as genai_types
import random
import json
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
        print(f"[DEBUG] Generating content for {json.dumps(response_schema.model_json_schema(), indent=4)}")
        # Try to match the prompt to a user message in the examples
        for example in SEARCH_HISTORY_POINTS + CALCULATOR_HISTORY_POINTS:
            for turn in example:
                if turn["role"] == "user" and turn["message"].lower() in prompt.lower():
                    last_model = next((t for t in reversed(example) if t["role"] == "model" and t["message"].startswith("Action") and "Finish[" in t["message"]), None)
                    if last_model:
                        import re
                        m = re.search(r"Finish\[(.*)\]", last_model["message"])
                        answer = m.group(1) if m else last_model["message"]
                        # Fill all fields with the answer or dummy values
                        dummy = {}
                        for name, field in response_schema.model_fields.items():
                            dummy[name] = answer if field.annotation == str else 0 if field.annotation in (int, float) else True if field.annotation == bool else None
                        return response_schema.model_validate(dummy).model_dump_json()
        # If no match, fill all fields with dummy values
        dummy = random.choice([{"action": {"is_async": True, "action_set_name": "SearchActions", "action_method_name": "search", "args": [{"arg_name": "entity", "arg_type": "str", "arg_value": "Python"}]}}, {"action": {"is_async": False, "action_set_name": "MathActions", "action_method_name": "sum", "args": [{"arg_name": "a", "arg_type": "int", "arg_value": 1}, {"arg_name": "b", "arg_type": "int", "arg_value": 2}]}}])
        print(dummy)
        for name, field in response_schema.model_fields.items():
            if name in dummy:
                continue
            if field.annotation == str:
                dummy[name] = "This is a mock answer."
            elif field.annotation in (int, float):
                dummy[name] = 42
            elif field.annotation == bool:
                dummy[name] = random.randint(0,10)==4
            elif field.annotation is not None and hasattr(field.annotation, "__origin__") and field.annotation.__origin__ is list:
                dummy[name] = []
            else:
                dummy[name] = None
        print(dummy)
        print(response_schema.model_json_schema())
        return response_schema.model_validate(dummy).model_dump_json()

    @property
    def default_model_name(self) -> str:
        return self._default_model_name

    @default_model_name.setter
    def default_model_name(self, model_name: str) -> None:
        self._default_model_name = model_name

    @property
    def default_generation_config(self):
        return self._default_generation_config.copy()

    @default_generation_config.setter
    def default_generation_config(self, config):
        self._default_generation_config = config 