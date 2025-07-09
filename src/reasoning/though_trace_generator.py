from local_logging import logger
from llm.google_gemini_client import BaseLLMClient
from llm.models.history import HistoryPoint
from .model.thought_trace import ThoughtTrace


class ThoughtTraceGenerator:
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client: BaseLLMClient = llm_client

    async def generate_thought_trace(
        self, original_thought: str, prompting_history: list[HistoryPoint] | None = None
    ) -> ThoughtTrace:
        # Define the prompt template for thought trace generation
        try:

            prompt = f"""
            {original_thought}
            Answer the question asked by providing reasoning.
            """

            # Use the LLM client to generate a response with the ThoughtTrace schema
            response_text = await self.llm_client.generate_content(
                prompt, ThoughtTrace, history=prompting_history
            )
            logger.debug(f"Thought trace response: {response_text}")

            # The client should return structured data that matches the ThoughtTrace model
            # If not, handle parsing/conversion here
            # This assumes generate_content returns JSON that can be parsed as ThoughtTrace
            return ThoughtTrace.model_validate_json(response_text)
        except Exception as e:
            logger.error(f"Error generating thought trace: {e}")
            return ThoughtTrace(
                is_finished=False,
                text=f"Error processing: {original_thought}",
                action=None,
                fact_found=False,
            )
