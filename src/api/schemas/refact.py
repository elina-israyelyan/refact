from pydantic import BaseModel, Field
from actions import ACTION_MODELS_TUPLE
from typing import Union, Any


class RefactRequest(BaseModel):
    prompt: str = Field(..., description="User initial input")


class ActRequest(BaseModel):
    """Request schema for /act endpoint."""

    action: Union[ACTION_MODELS_TUPLE] = Field(
        ..., discriminator="action_method_name", description="Action to be executed"
    )


class ActResponse(BaseModel):
    """Response schema for /act endpoint."""

    result: Any = Field(..., description="Action result")


class ReasonRequest(RefactRequest):
    """Request schema for /reason endpoint."""

    pass


class ReasonResponse(BaseModel):
    """
    Response schema for /reason endpoint.
    """

    text: str = Field(..., description="Reasoning text")
