from typing import Any, Type

from pydantic import BaseModel


class BaseAction(BaseModel):
    class ActionArgs(BaseModel):
        arg_name: str
        arg_type: Type[Any]

    action_set_name: str
    action_method_name: str
    args: list[ActionArgs]


class BaseActionWithValues(BaseAction):
    class ActionArgsWithValues(BaseModel):
        arg_name: str
        arg_type: str
        arg_value: Any

    args: list[ActionArgsWithValues]
