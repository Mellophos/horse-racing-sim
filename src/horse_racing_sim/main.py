import json

from .horse import Horse
from .config import BUILT_IN_DIR


def get_horse_from_json(horse_id: str | int) -> Horse:
    if isinstance(horse_id, int):
        horse_id = f"horse_{horse_id:0>5}"

    try:
        with open(
            BUILT_IN_DIR / "horses" / f"{horse_id}.json", "r"
        ) as f:
            json_string = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"No such Horse: {horse_id!r}")

    return Horse.model_validate(json_string)


if __name__ == "__main__":
    horse = get_horse_from_json(3)

    print(horse.model_dump())
