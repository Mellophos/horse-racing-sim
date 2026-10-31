from pprint import pprint

from . import assets
from .course import Course
from .horse import Horse


def main():
    course_json = {
        "$version": "course-0.1.0",
        "id": "course_10006_turf_main_1400",
        "name": "Tokyo",
        "surface": 0,
        "distance": 1400,
        "width": 30,
        "events": [
            {
                "id": 0,
                "trigger_at": 0,
                "is_start": True,
                "straight_id": 0,
                "type": 1
            },
            {
                "id": 0,
                "trigger_at": 1400,
                "is_start": False,
                "straight_id": 0,
                "type": 1
            },
        ]
    }

    course = Course.model_validate(course_json)
    print(course)

    course_json = course.model_dump_json(indent=4)
    print(course_json)


def test_horse_model():
    horse_json = assets.horse.get("horse_00001")
    horse = Horse.model_validate(horse_json)
    pprint(horse)

    pprint(assets.horse.list_all())
