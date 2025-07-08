from pydantic import BaseModel, Field
from typing import Optional
from actions.model import BaseActionWithValues


class ThoughtTrace(BaseModel):
    is_final: bool
    text: str
    action: Optional[BaseActionWithValues] = Field(default=None)
    fact_found: bool
