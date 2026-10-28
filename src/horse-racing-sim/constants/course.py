from enum import Enum, unique


@unique
class DistanceCat(Enum):
    SPRINT = 0
    MILE = 1
    INTERMEDIATE = 2
    LONG = 3
    EXTENDED = 4


@unique
class Surface(Enum):
    TURF = 0
    DIRT = 1
    ARTIFICIAL = 2


@unique
class Season(Enum):
    SPRING = 0
    SUMMER = 1
    AUTUMN = 2
    WINTER = 3


@unique
class Weather(Enum):
    SUNNY = 0
    CLOUDY = 1
    RAIN = 2


@unique
class GroundCond(Enum):
    FIRM = 0
    GOOD = 1
    SOFT = 2
    HEAVY = 3
