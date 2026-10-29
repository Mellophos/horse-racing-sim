import json
from importlib import resources

HORSES_PACKAGE = "horse_racing_sim.assets.horses"


def get(horse_id: str | int) -> dict:
    """Gets a horse from assets with given ID."""
    if isinstance(horse_id, int):
        horse_id = f"horse_{horse_id:05d}"
    horse_id = horse_id.removesuffix(".json")
    filename = f"{horse_id}.json"

    file_path = resources.files(HORSES_PACKAGE).joinpath(filename)
    if not file_path.is_file():
        raise FileNotFoundError(f"Horse ID {horse_id!r} not found in assets.")

    with file_path.open("r") as f:
        return json.load(f)


def list_all() -> dict:
    """Lists all horses from assets."""
    ids = {}

    for item in resources.files(HORSES_PACKAGE).iterdir():
        if item.is_file() and item.name.endswith(".json"):
            with item.open() as f:
                data = json.load(f)
            ids[data["horse_id"]] = data["name"]

    return ids
