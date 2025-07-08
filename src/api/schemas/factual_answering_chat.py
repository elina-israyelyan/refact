from pydantic import BaseModel, Field


class FactualCheckerChatRequest(BaseModel):
    prompt: str = Field(..., description="User initial input")
