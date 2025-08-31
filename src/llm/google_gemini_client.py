import json
from typing import Type

import jsonref
import vertexai
from google.genai import types as genai_types
from google.oauth2 import service_account
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, GenerationConfig, Content, Part

from local_logging import logger
from utils.pydantic_schema import remove_null_type_from_optional_fields
from .base import BaseLLMClient
from .models.history import HistoryPoint


class GeminiClient(BaseLLMClient):
    def __init__(
        self,
        default_generation_config: genai_types.GenerateContentConfigDict,
        default_model_name: str,
    ):
        self._default_generation_config: genai_types.GenerateContentConfigDict = (
            default_generation_config
        )
        self._default_model_name = default_model_name

    @classmethod
    def create(
        cls,
        service_account_path: str,
        location: str | None = None,
        default_model_name: str | None = None,
        default_generation_config: genai_types.GenerateContentConfigDict | None = None,
    ) -> "GeminiClient":
        if default_model_name is None:
            default_model_name = "gemini-2.0-flash"
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path
        )
        try:
            with open(service_account_path, "r") as f:
                data = json.load(f)
                project_id = data.get("project_id")
                if not project_id:
                    raise ValueError(
                        "Key 'project_id' not found in service account file."
                    )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Service account file not found: {service_account_path}"
            )
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            raise RuntimeError(
                f"Error reading project_id from {service_account_path}: {e}"
            )

        try:
            vertexai.init(
                project=project_id, location=location, credentials=credentials
            )

            return cls(
                default_generation_config=default_generation_config or {},
                default_model_name=default_model_name,
            )
        except Exception as e:
            raise e

    async def generate_content(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        history: list[HistoryPoint] | None = None,
        model_name: str | None = None,
    ) -> str:
        local_generation_config = dict(self._default_generation_config)
        local_generation_config.update(
            {
                "response_mime_type": "application/json",
                "response_schema": remove_null_type_from_optional_fields(
                    jsonref.replace_refs(response_schema.model_json_schema())  # type: ignore
                ),
            }
        )

        model = GenerativeModel(
            model_name or self._default_model_name
        )  # TODO will be deprecated on 2026 June 24[bug exists with client initialization]

        contents = []

        for history_point in history or []:
            role = history_point.role
            contents.append(
                Content(role=role, parts=[Part.from_text(history_point.message)])
            )

        contents.append(Content(role="user", parts=[Part.from_text(prompt)]))
        response = await model.generate_content_async(
            contents=contents,
            generation_config=GenerationConfig(**local_generation_config),  # type: ignore
        )

        logger.debug("Response received.")
        logger.debug(response.candidates)
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            logger.warning(
                f"Warning: No valid response candidates found. Response: {response}"
            )

            return ""
