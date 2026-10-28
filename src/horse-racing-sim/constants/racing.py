from enum import Enum, unique


@unique
class RacePhase(Enum):
    EARLY = 0
    MID = 1
    LATE = 2
    FINAL = 3
