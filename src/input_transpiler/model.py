from typing import Type, Any

from pydantic import BaseModel


class Condition(BaseModel):
    pass


class StandardFactSearchInputQuery(BaseModel):
    conditions: list[Condition]
    entity: Any
    attribute: Type["StandardFactSearchInputQuery"] | None


class InputQuery(BaseModel):
    query: str
    intent: str
    needs_factual_verification: bool
