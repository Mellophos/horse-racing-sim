from enum import Enum, unique


@unique
class DistanceCat(Enum):
    SPRINT = (0, 1000, 1300)
    MILE = (1, 1301, 1899)
    INTERMEDIATE = (2, 1900, 2100)
    LONG = (3, 2101, 2700)
    EXTENDED = (4, 2701, 5000)

    def __init__(self, value, min_dist, max_dist):
        self._value_ = value
        self.min_dist = min_dist
        self.max_dist = max_dist

    @classmethod
    def from_distance(cls, distance: int) -> 'DistanceCat':
        for category in cls:
            if category.min_dist <= distance <= category.max_dist:
                return category
        raise ValueError('Distance out of categorisation range')


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
