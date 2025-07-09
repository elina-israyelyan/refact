import inspect
from typing import AsyncGenerator, Union, cast
from pydantic import BaseModel

from actions import ACTION_SETS, ACTION_MODELS_TUPLE
from input_transpiler.transpiler import InputTranspiler
from llm.base import BaseLLMClient
from llm.models.history import HistoryPoint
from utils.prompting_history_points import (
    PROMPTING_EXAMPLES_HISTORY_POINTS,
    GENERAL_INSTRUCTIONS_HISTORY_POINTS,
)
import traceback

from reasoning.though_trace_generator import ThoughtTraceGenerator
from reasoning.model.thought_trace import ThoughtTrace
from local_logging import logger
from ..exceptions import (
    RefactGeneric,
    RefactException,
    ActException,
    ReasonException,
    ZeroDivisionCustomException,
)


async def refact(
    initial_prompt: str, llm_client: BaseLLMClient
) -> AsyncGenerator[str, None]:
    try:
        # TODO [mid] Transpile input standardize it, and create a knowledge base
        # input_query = await InputTranspiler(llm_client=llm_client).transpile(initial_prompt)
        # yield f"Transpiled Query: {input_query.query} (intent: {input_query.intent})\n"

        thought_trace_generator_session = ThoughtTraceGenerator(llm_client=llm_client)

        flat_history = (
            GENERAL_INSTRUCTIONS_HISTORY_POINTS + PROMPTING_EXAMPLES_HISTORY_POINTS
        )

        user_query = f"[INITIAL_PROMPT]: {initial_prompt}"
        thought_trace = await generate_and_update_thought_trace_history(
            user_query, thought_trace_generator_session, flat_history
        )
        yield f"Thought 1: {thought_trace.text}\n"

        i = 0
        observation_count = 1
        while not thought_trace.is_finished and i < 10:
            i += 1
            if thought_trace.action:
                action_name = thought_trace.action.action_method_name
                action_set_name = thought_trace.action.action_set_name
                logger.debug(f"Preparing to run action: {action_name}")
                # Find the action class
                action_instance = None
                for action_instance in ACTION_SETS:
                    if action_instance.__class__.__name__ == action_set_name:
                        action = getattr(action_instance, action_name)

                arg_dict = {action_arg.arg_name: action_arg.arg_value for action_arg in thought_trace.action.args}  # type: ignore
                logger.debug(
                    f"Running action '{action_name}' with arguments: {arg_dict}"
                )
                try:
                    result = (
                        await action(**arg_dict)
                        if inspect.iscoroutinefunction(action)
                        or inspect.isasyncgenfunction(action)
                        else action(**arg_dict)
                    )
                    logger.debug(f"Action '{action_name}' result: {result}")
                    observation = f"Observation {observation_count}: {result}"
                except ZeroDivisionError:
                    raise ZeroDivisionCustomException()
                except Exception:
                    observation = f"error occured during action :{action_name}"
                observation_count += 1
                yield f"{observation}\n"

                flat_history.append(HistoryPoint(role="user", message=observation))
                observation_continuation_prompt = f"Continue previous thought and do implication based on the observation. If there was no observation or the result was not found, try to change your wording or approach in lookups. If you believe you have enough information to answer the question asked by user in [INITIAL_PROMPT], finalize your answer."
                thought_trace = await generate_and_update_thought_trace_history(
                    observation_continuation_prompt,
                    thought_trace_generator_session,
                    flat_history,
                )

                yield f"Thought {i}: {thought_trace.text}\n"
            else:
                observation_continuation_prompt = f"Continue from previous thought. If you did not get an observation, try to change your wording or approach in lookups. If you believe you have enough information to answer the question asked by user in [INITIAL_PROMPT], finalize your answer."
                thought_trace = await generate_and_update_thought_trace_history(
                    observation_continuation_prompt,
                    thought_trace_generator_session,
                    flat_history,
                )

                yield f"Thought {i}: {thought_trace.text}\n"
        yield f"Final answer: {thought_trace.text}\n"
    except ZeroDivisionCustomException as zde:
        raise zde
    except RefactGeneric as rg:
        raise rg
    except Exception as e:
        raise RefactException(str(e))


async def generate_and_update_thought_trace_history(
    prompt: str,
    thought_trace_generator: ThoughtTraceGenerator,
    history: list[HistoryPoint],
) -> ThoughtTrace:
    thought_trace = await thought_trace_generator.generate_thought_trace(
        original_thought=prompt, prompting_history=history
    )
    history.append(HistoryPoint(role="user", message=prompt))
    history.append(HistoryPoint(role="model", message=thought_trace.text))
    return thought_trace


async def act(action: Union[ACTION_MODELS_TUPLE]) -> str:  # type: ignore
    action = cast(BaseModel, action)
    action_set_name = action.__class__.__name__.split("___")[0]
    action_method_name = action.__class__.__name__.split("___")[1]
    action_instance = [
        action_instance
        for action_instance in ACTION_SETS
        if action_instance.__class__.__name__ == action_set_name
    ] or None

    if action_instance:
        method = getattr(action_instance[0], action_method_name)
        action_args = action.model_dump(exclude={"action_method_name"})
        try:
            result = (
                await method(**action_args)
                if inspect.iscoroutinefunction(method)
                or inspect.isasyncgenfunction(method)
                else method(**action_args)
            )
            return result
        except ZeroDivisionError:
            raise ZeroDivisionCustomException()
        except Exception as e:
            traceback.print_exc()
            raise ActException(str(e))

    return "Action not found"


async def reason(initial_prompt: str, llm_client: BaseLLMClient) -> str:
    try:
        thought_trace_generator = ThoughtTraceGenerator(llm_client=llm_client)
        thought_trace = await thought_trace_generator.generate_thought_trace(
            original_thought=initial_prompt, prompting_history=None
        )
        return thought_trace.text
    except Exception as e:
        raise ReasonException(str(e))
