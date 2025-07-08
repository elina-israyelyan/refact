from pydantic import BaseModel
from typing import Any


class BaseAction(BaseModel):
    class ActionArgs(BaseModel):
        arg_name: str
        arg_type: str
    action_set_name: str
    action_method_name: str
    args: list[ActionArgs]
    is_async: bool
    

class BaseActionWithValues(BaseAction):
    class ActionArgsWithValues(BaseModel):
        arg_name: str
        arg_type: str
        arg_value: Any
    args: list[ActionArgsWithValues]

