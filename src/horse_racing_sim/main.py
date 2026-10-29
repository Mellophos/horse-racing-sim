from pprint import pprint

from . import assets
from .horse import Horse


def main():
    horse_json = assets.horse.get("horse_00001")
    horse = Horse.model_validate(horse_json)
    pprint(horse)

    pprint(assets.horse.list_all())
