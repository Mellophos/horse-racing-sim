import json
from importlib.resources import files

import pytest

from horseracing_sim.validation.json_validator import validate_json

ASSETS_DIR = files("horseracing_sim") / "assets"

JSON_FILES = [
    path
    for path in ASSETS_DIR.rglob("*.json")
    if "schemas" not in path.parts
]


@pytest.mark.parametrize(
    "json_path",
    JSON_FILES,
    ids=lambda path: str(path.relative_to(ASSETS_DIR)),
)
def test_json_assets(json_path):
    data = json.loads(
        json_path.read_text(encoding="utf-8")
    )

    validate_json(data)
