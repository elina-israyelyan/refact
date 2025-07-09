from .calculator import MathActions
from .model import BaseAction
from .search import SearchActions
from .base import ActionSet
from typing import Type
from pydantic import BaseModel

ACTION_SETS: list[ActionSet] = [MathActions(), SearchActions()]

actions_models_list: list[Type[BaseModel]] = []
for action_instance in ACTION_SETS:
    actions_models_list.extend(
        action_instance.create_pydantic_base_models_for_actions()
    )

ACTION_MODELS_TUPLE: tuple[Type[BaseModel], ...] = tuple(actions_models_list)


__all__ = [
    "ACTION_SETS",
    "BaseAction",
    "SearchActions",
    "MathActions",
    "ACTION_MODELS_TUPLE",
]
