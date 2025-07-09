import inspect
from typing import Any, Type, Literal

from local_logging import logger
from .model import BaseAction
from pydantic import BaseModel, create_model


class ActionSet:
    def __init__(self):
        self.actions: list[BaseAction] = []
        self.action_models: list[Type[BaseModel]] = []

    def create_pydantic_base_models_for_actions(self) -> list[Type[BaseModel]]:
        if self.action_models:
            return self.action_models
        models = []
        for action in self.actions or self.list_actions():
            models.append(create_model(f"{action.action_set_name}___{action.action_method_name}", action_method_name=Literal[action.action_method_name], **{arg.arg_name: arg.arg_type for arg in action.args}))  # type: ignore
        return models

    def list_actions(self) -> list[BaseAction]:

        if self.actions:
            return self.actions
        actions = []
        for name, member in inspect.getmembers(self.__class__):
            if name.startswith("_"):
                continue  # Skip dunder and private
            if not (
                inspect.isfunction(member)
                or inspect.ismethod(member)
                or inspect.iscoroutinefunction(member)
                or inspect.isasyncgenfunction(member)
            ):
                continue
            # Only include methods defined in this class, not inherited
            if member.__qualname__.split(".")[0] != self.__class__.__name__:
                continue
            sig = inspect.signature(member)
            args = []
            for param_name, param in sig.parameters.items():
                if param_name in ("self", "cls"):
                    continue
                annotation = param.annotation
                if annotation is inspect.Parameter.empty:
                    arg_type = Any
                else:
                    arg_type = annotation
                args.append(BaseAction.ActionArgs(arg_name=param_name, arg_type=arg_type))

            actions.append(
                BaseAction(
                    action_method_name=name,
                    args=args,
                    action_set_name=self.__class__.__name__,
                )
            )
        self.actions = actions
        return actions
