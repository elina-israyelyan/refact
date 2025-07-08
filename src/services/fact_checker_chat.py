import inspect
from typing import AsyncGenerator
from actions.model import BaseActionWithValues
from input_transpiler.transpiler import InputTranspiler
from reasoning.though_trace_generator import ThoughtTraceGenerator
from llm.base import BaseLLMClient
from llm.models.history import HistoryPoint
from actions.base import ActionSet
from actions.calculator import MathActions
from actions.search.search import SearchActions
from prompting_history_points import HISTORY_POINTS

async def start_fact_checker_chat(initial_prompt: str, llm_client: BaseLLMClient) -> AsyncGenerator[str, None]:
    # Step 1: Transpile input and yield to user
    # input_query = await InputTranspiler(llm_client=llm_client).transpile(initial_prompt)
    # yield f"Transpiled Query: {input_query.query} (intent: {input_query.intent})\n"

    # Step 2: Gather available actions
    available_actions = []
    for action_cls in [MathActions, SearchActions]:
        available_actions.extend(action_cls().list_action_methods())

    # Step 3: Prepare history points (validate with HistoryPoint)
    validated_history = []
    for example in HISTORY_POINTS:
        validated_example = []
        for point in example:
            try:
                validated_example.append(HistoryPoint(**point))
            except Exception:
                continue
        if validated_example:
            validated_history.append(validated_example)

    # Step 4: Start the thought trace generator
    thought_trace_generator_session = ThoughtTraceGenerator(llm_client=llm_client)
    # Flatten history for initial context
    initial_context = f"Available actions:\n{available_actions}\n\n"
    flat_history = [HistoryPoint(role="user", message=initial_context)] + [pt for example in validated_history for pt in example]
    
    user_query  = f"[INITIAL_PROMPT]: {initial_prompt}"

    thought_trace = await thought_trace_generator_session.generate_thought_trace(
        original_thought=user_query,
        prompting_history=flat_history
    )
    print(f"[DEBUG] Original Thought trace: {thought_trace}")
    yield f"Thought: {thought_trace.text}\n"
    flat_history.append(HistoryPoint(role="user", message=user_query))
    flat_history.append(HistoryPoint(role="model", message=thought_trace.text))
    # Step 5: Reasoning/action loop
    i = 0
    observation_count = 1
    while not thought_trace.is_final and i < 10:
        i += 1
        if thought_trace.action:
            action_name = thought_trace.action.action_method_name
            print(f"[DEBUG] Preparing to run action: {action_name}")
            # Find the action class
            action_instance = None
            for action_cls in [MathActions, SearchActions]:
                if hasattr(action_cls, action_name):
                    action_instance = action_cls()
                    break
            if action_instance:
                method = getattr(action_instance, action_name)
                # Use the provided argument values from action.args
                print(thought_trace.action.args)
                arg_dict = {action_arg.arg_name: action_arg.arg_value for action_arg in thought_trace.action.args} # type: ignore
                print(f"[DEBUG] Running action '{action_name}' with arguments: {arg_dict}")
                result = await method(**arg_dict) if inspect.iscoroutinefunction(method) else method(**arg_dict)
                print(f"[DEBUG] Action '{action_name}' result: {result}")
                observation = f"Observation {observation_count} {result}"
            else:
                print(f"[DEBUG] Action class for '{action_name}' not found.")
                observation = f"Observation {observation_count} Action {action_name} not found. Try rewording or using a different lookup."
            observation_count += 1
            yield f"{observation}\n"

            flat_history.append(HistoryPoint(role="user", message=observation))
            observation_continuation_prompt=f"Continue previous thought and do implication based on the observation. If there was no observation or the result was not found, try to change your wording or approach in lookups. If you believe you have enough information to answer the question asked by user in [INITIAL_PROMPT], finalize your answer."
            thought_trace = await thought_trace_generator_session.generate_thought_trace(
                original_thought=observation_continuation_prompt,
                prompting_history=flat_history
            )
            flat_history.append(HistoryPoint(role="user", message=observation_continuation_prompt))
            flat_history.append(HistoryPoint(role="model", message=thought_trace.text))

            yield f"Thought: {thought_trace.text}\n"
        else:
            observation_continuation_prompt=f"Continue from previous thought. If you did not get an observation, try to change your wording or approach in lookups. If you believe you have enough information to answer the question asked by user in [INITIAL_PROMPT], finalize your answer."
            thought_trace = await thought_trace_generator_session.generate_thought_trace(
                original_thought=observation_continuation_prompt,
                prompting_history=flat_history
            )
            flat_history.append(HistoryPoint(role="user", message=observation_continuation_prompt))
            flat_history.append(HistoryPoint(role="model", message=thought_trace.text))
            yield f"Thought: {thought_trace.text}\n"
    # Final answer
    yield f"Final answer: {thought_trace.text}\n"

