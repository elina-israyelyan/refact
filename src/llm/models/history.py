from pydantic import BaseModel


class HistoryPoint(BaseModel):
    """Represents a point in conversation history with a role and message"""

    role: str  # user' or 'model
    message: str
