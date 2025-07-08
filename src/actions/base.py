from typing import Any
import inspect
from .model import BaseAction


class ActionSet:
    def call_methods(self, method_name: str, *args, **kwargs) -> Any:
        return getattr(self, method_name)(*args, **kwargs)

    def list_action_methods(self) -> list[BaseAction]:
        """
        Returns a dictionary of all developer-defined methods (excluding inherited, dunder, and private methods),
        their arguments, and whether they are async.
        Example:
        {
            'sum': {
                'args': {'a': 'float', 'b': 'float'},
                'is_async': False
            },
            'search': {
                'args': {'entity': 'str'},
                'is_async': True
            }
        }
        """
        methods = []
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
                    arg_type = "Any"
                else:
                    arg_type = str(
                        annotation
                    )  # TODO[LOW]: to have a json serializable output. think of a better way.
                args.append(BaseAction.ActionArgs(arg_name=param_name, arg_type=arg_type))
            is_async = inspect.iscoroutinefunction(member) or inspect.isasyncgenfunction(member)
            methods.append(
                BaseAction(
                    action_method_name=name,
                    args=args,
                    is_async=is_async,
                    action_set_name=self.__class__.__name__,
                )
            )
        return methods


# ActionSet[int]().call_methods("sss" "") + 23
