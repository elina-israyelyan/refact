from typing import Optional

from pydantic import BaseModel


class HistoryPoint(BaseModel):
    """Represents a point in conversation history between a user and the assistant"""

    user_message: str
    assistant_response: Optional[str] = None
