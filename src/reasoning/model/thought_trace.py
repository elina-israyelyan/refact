from typing import Optional

from pydantic import BaseModel, Field

from actions.model import BaseActionWithValues


class ThoughtTrace(BaseModel):
    is_finished: bool
    text: str
    action: Optional[BaseActionWithValues] = Field(default=None)
    fact_found: bool
