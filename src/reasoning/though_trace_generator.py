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
        prompt = """
        Generate a structured thought process to answer the following query just like you did on previous examples:
        """
        prompt += f"\n{original_thought}\n"
        prompt += "\nProvide reasoning, determine if action is needed, and if calculation is needed."

        # Use the LLM client to generate a response with the ThoughtTrace schema
        response_text = await self.llm_client.generate_content(
            prompt, ThoughtTrace, history=prompting_history
        )
        print(f"[DEBUG] Thought trace response: {response_text}")

        # The client should return structured data that matches the ThoughtTrace model
        # If not, handle parsing/conversion here
        try:
            # This assumes generate_content returns JSON that can be parsed as ThoughtTrace
            return ThoughtTrace.model_validate_json(response_text)
        except Exception as e:
            # Fallback for when parsing fails
            print(f"Error parsing thought trace response: {e}")
            return ThoughtTrace(
                is_final=False,
                text=f"Error processing: {original_thought}",
                action=None,
                fact_found=False,
            )
