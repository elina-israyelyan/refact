from llm.base import BaseLLMClient

from .model import InputQuery


class InputTranspiler:
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client: BaseLLMClient = llm_client

    async def transpile(self, input_prompt: str) -> InputQuery:
        prompt = f"""
        Analyze the following user input and provide structured information:

        User Input: {input_prompt}

        Extract the core query, identify the intent, and determine if factual verification is needed.
        """

        response_text = await self.llm_client.generate_content(prompt, InputQuery)

        try:
            return InputQuery.model_validate_json(response_text)
        except Exception as e:
            print(f"Error parsing input query: {e}")
            return InputQuery(
                query=input_prompt, intent="unknown", needs_factual_verification=True
            )
