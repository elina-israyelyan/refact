from typing import Any


def remove_null_type_from_optional_fields(
    schema: dict[str, Any] | list[Any]
) -> dict[str, Any] | list[Any]:
    if isinstance(schema, dict):
        if "anyOf" in schema:
            any_of_without_null = [
                s for s in schema["anyOf"] if s.get("type") != "null"
            ]
            if len(any_of_without_null) == 1:
                schema.pop("anyOf")
                schema.update(any_of_without_null[0])
            else:
                schema["anyOf"] = any_of_without_null

        for v in schema.values():
            remove_null_type_from_optional_fields(v)
    elif isinstance(schema, list):
        for item in schema:
            remove_null_type_from_optional_fields(item)
    return schema
