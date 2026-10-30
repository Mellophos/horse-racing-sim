import json
from functools import lru_cache
from importlib.resources import files

from jsonschema.validators import Draft202012Validator


@lru_cache(maxsize=32)
def load_schema(identifier: str) -> dict:
    name, version = parse_schema_identifier(identifier)

    schema_path = (
            files("horse_racing_sim")
            / "assets"
            / "schemas"
            / name
            / version
            / "schema.json"
    )

    if not schema_path.is_file():
        raise ValueError(f"Schema not found: {schema_path}")

    return json.loads(schema_path.read_text(encoding="utf-8"))


def parse_schema_identifier(identifier: str) -> tuple[str, str]:
    try:
        name, version = identifier.rsplit("-", 1)
    except ValueError:
        raise ValueError(f"Invalid schema identifier: {identifier}")

    if not name or not version:
        raise ValueError(f"Invalid schema identifier: {identifier}")

    return name, version


def validate_json(data: dict) -> None:
    identifier = data.get("$version")
    if not isinstance(identifier, str):
        raise ValueError("Missing or invalid schema")

    schema = load_schema(identifier)
    validator = Draft202012Validator(schema)

    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: list(error.absolute_path),
    )

    if errors:
        messages = "\n".join(
            f"- {'.'.join(map(str, error.absolute_path)) or '<root>'}: "
            f"{error.message}"
            for error in errors
        )

        raise ValueError(f"Validation failed ({identifier}):\n{messages}")
