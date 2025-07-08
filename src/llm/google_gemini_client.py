import copy
import json
import traceback
from typing import Type

import vertexai
from google.genai import types as genai_types
from google.oauth2 import service_account
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, GenerationConfig, Content, Part
import jsonref
from utils.pydantic_schema import remove_null_type_from_optional_fields
from .base import BaseLLMClient
from .models.history import HistoryPoint


class GeminiClient(BaseLLMClient):
    def __init__(
        self,
        # client: genai.Client,
        default_generation_config: genai_types.GenerateContentConfigDict,
        default_model_name: str,
    ):
        # self._client: genai.Client = client
        self._default_generation_config: genai_types.GenerateContentConfigDict = (
            default_generation_config
        )
        self._default_model_name = default_model_name

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
    def default_generation_config(self, config: genai_types.GenerateContentConfigDict) -> None:
        """Set the default generation configuration"""
        self._default_generation_config = config

    @classmethod
    async def create(
        cls,
        service_account_path: str,
        location: str | None = None,
        default_model_name: str | None = None,
        default_generation_config: genai_types.GenerateContentConfigDict | None = None,
    ):
        if default_model_name is None:
            default_model_name = "gemini-2.0-flash"
        credentials = service_account.Credentials.from_service_account_file(service_account_path)
        try:
            with open(service_account_path, 'r') as f:
                data = json.load(f)
                project_id = data.get("project_id")
                if not project_id:
                    raise ValueError("Key 'project_id' not found in service account file.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Service account file not found: {service_account_path}")
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            raise RuntimeError(f"Error reading project_id from {service_account_path}: {e}")

        try:
            vertexai.init(project=project_id, location=location, credentials=credentials)
           
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
                "response_schema": remove_null_type_from_optional_fields(jsonref.replace_refs(response_schema.model_json_schema())),
            }
        )
        print("local_generation_config", json.dumps(local_generation_config, indent=4))

        model = GenerativeModel(
            model_name or self._default_model_name
        )  # TODO will be deprecated on 2026 June 24[bug exists with client initialization]

        # Construct content list for the model
        contents = []

        # First add history points if they exist
        for history_point in history or []:
            # Map role name if needed (API expects "user" or "model")
            role = history_point.role
            if role == "assistant":
                role = "model"

            # Add message with appropriate role
            contents.append(Content(role=role, parts=[Part.from_text(history_point.message)]))

        contents.append(Content(role="user", parts=[Part.from_text(prompt)]))
        print("before response")
        response = await model.generate_content_async(
            contents=contents,
            generation_config=GenerationConfig(**local_generation_config),  # type: ignore
        )

        print("Response received.")
        print(response.candidates)
        # Basic check: Ensure candidates list is not empty and has content
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            # Log or handle cases with no valid response (e.g., safety filters)
            print(f"Warning: No valid response candidates found. Response: {response}")

            return ""


# --- Main Execution ---
if __name__ == "__main__":
    try:
        # --- Configuration ---
        # IMPORTANT: Replace with the actual path to your service account key file
        # Use environment variables or secure config management in production.
        SERVICE_ACCOUNT_FILE = "/home/elina-jan/Downloads/amaros-420712-1f28953e284e.json"
        LOCATION = None
        MODEL_NAME = "gemini-2.0-flash"  # Or "gemini-1.0-pro", etc.
        USER_PROMPT = "Explain how AI works."
        import asyncio

        gemini_client = asyncio.run(
            GeminiClient.create(service_account_path=SERVICE_ACCOUNT_FILE, location=None)
        )

        class A(BaseModel):
            text: str

        result = asyncio.run(gemini_client.generate_content(USER_PROMPT, response_schema=A))

        print("final result")
        print(result)

        result = asyncio.run(
            gemini_client.generate_content(
                USER_PROMPT,
                response_schema=A,
                history=[HistoryPoint(role="user", message="Answer in one word")],
            )
        )
        print("resulting")
        print(result)

    except (FileNotFoundError, RuntimeError, Exception) as e:
        traceback.print_exc()
        print(f"\nAn critical error occurred: {e}")
