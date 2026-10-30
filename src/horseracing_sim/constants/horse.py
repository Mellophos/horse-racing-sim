from enum import Enum, unique


@unique
class Grade(Enum):
    G = 1
    F = 2
    E = 3
    D = 4
    C = 5
    B = 6
    A = 7
    S = 8


@unique
class Strategy(Enum):
    RUNUAWAY = 0
    FRONT = 1
    PACE = 2
    LATE = 3
    END = 4


@unique
class Mood(Enum):
    AWFUL = 0
    BAD = 1
    NORMAL = 2
    GOOD = 3
    GREAT = 4
