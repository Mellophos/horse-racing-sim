
import pytest
from pydantic import ValidationError

from horseracing_sim.course import Course
from horseracing_sim.constants import Surface, DistanceCat
from horseracing_sim.events import CourseEventType


@pytest.fixture
def valid_course_data():
    return {
        "$version": "1.0",
        "id": "course_00001_turf_flat_1600",
        "name": "Test Course",
        "surface": Surface.TURF,
        "distance": 1600,
        "width": 20.0,
    }


class TestCourseCreation:
    def test_create_valid_course(self, valid_course_data):
        course = Course(**valid_course_data)

        assert course.version == "1.0"
        assert course.id == "course_00001_turf_flat_1600"
        assert course.name == "Test Course"
        assert course.surface == Surface.TURF
        assert course.distance == 1600
        assert course.width == 20.0
        assert course.events == []

    def test_create_course_using_field_name(self, valid_course_data):
        valid_course_data["version"] = valid_course_data.pop("$version")

        course = Course(**valid_course_data)

        assert course.version == "1.0"

    def test_missing_required_field(self, valid_course_data):
        del valid_course_data["name"]

        with pytest.raises(ValidationError):
            Course(**valid_course_data)

    def test_extra_field_is_forbidden(self, valid_course_data):
        valid_course_data["unknown"] = "value"

        with pytest.raises(ValidationError):
            Course(**valid_course_data)

    def test_model_is_frozen(self, valid_course_data):
        course = Course(**valid_course_data)

        with pytest.raises(ValidationError):
            course.name = "Updated Course"


class TestCourseIdValidation:
    @pytest.mark.parametrize(
        "course_id",
        [
            "course_00001_turf_flat_1600",
            "course_12345_dirt_oval_2000",
            "course_99999_artificial_tight_3000",
        ],
    )
    def test_valid_id_formats(self, valid_course_data, course_id):
        # Keep the ID consistent with the surface and distance.
        parts = course_id.split("_")
        valid_course_data["id"] = course_id
        valid_course_data["surface"] = Surface[parts[2].upper()]
        valid_course_data["distance"] = int(parts[4])

        course = Course(**valid_course_data)

        assert course.id == course_id

    @pytest.mark.parametrize(
        "course_id",
        [
            "course_1_turf_flat_1600",
            "course_00001_grass_flat_1600",
            "course_00001_turf_Flat_1600",
            "course_00001_turf_flat_160",
            "course_00001_turf_flat_16000",
            "invalid_course_id",
        ],
    )
    def test_invalid_id_formats(self, valid_course_data, course_id):
        valid_course_data["id"] = course_id

        with pytest.raises(ValidationError):
            Course(**valid_course_data)

    def test_surface_mismatch(self, valid_course_data):
        valid_course_data["surface"] = Surface.DIRT

        with pytest.raises(
            ValidationError,
            match="does not match surface attribute",
        ):
            Course(**valid_course_data)

    def test_distance_mismatch(self, valid_course_data):
        valid_course_data["distance"] = 2000

        with pytest.raises(
            ValidationError,
            match="does not match distance attribute",
        ):
            Course(**valid_course_data)


class TestCourseFieldValidation:
    @pytest.mark.parametrize("distance", [1000, 1500, 3000, 5000])
    def test_valid_distance(self, valid_course_data, distance):
        valid_course_data["distance"] = distance
        valid_course_data["id"] = (
            f"course_00001_turf_flat_{distance}"
        )

        course = Course(**valid_course_data)

        assert course.distance == distance

    @pytest.mark.parametrize("distance", [999, 5001, 0, -100])
    def test_invalid_distance(self, valid_course_data, distance):
        valid_course_data["distance"] = distance
        valid_course_data["id"] = (
            f"course_00001_turf_flat_{distance:04d}"
        )

        with pytest.raises(ValidationError):
            Course(**valid_course_data)

    @pytest.mark.parametrize("width", [1, 1.0, 10.5, 100])
    def test_valid_width(self, valid_course_data, width):
        valid_course_data["width"] = width

        course = Course(**valid_course_data)

        assert course.width == width

    @pytest.mark.parametrize("width", [0, -1, -0.5])
    def test_invalid_width(self, valid_course_data, width):
        valid_course_data["width"] = width

        with pytest.raises(ValidationError):
            Course(**valid_course_data)

    @pytest.mark.parametrize("name", ["", None])
    def test_invalid_name(self, valid_course_data, name):
        valid_course_data["name"] = name

        with pytest.raises(ValidationError):
            Course(**valid_course_data)

    def test_invalid_surface(self, valid_course_data):
        valid_course_data["surface"] = "grass"

        with pytest.raises(ValidationError):
            Course(**valid_course_data)


class TestCourseProperties:
    def test_distance_cat(self, valid_course_data):
        course = Course(**valid_course_data)

        assert course.distance_cat == DistanceCat.from_distance(1600)

    def test_distance_cat_uses_current_distance(self, valid_course_data):
        valid_course_data["distance"] = 3000
        valid_course_data["id"] = "course_00001_turf_flat_3000"

        course = Course(**valid_course_data)

        assert course.distance_cat == DistanceCat.from_distance(3000)

    @pytest.mark.parametrize(
        ("layout", "expected"),
        [
            ("flat", "Flat"),
            ("oval", "Oval"),
            ("tight", "Tight"),
            ("undulating", "Undulating"),
        ],
    )
    def test_layout(self, valid_course_data, layout, expected):
        valid_course_data["id"] = (
            f"course_00001_turf_{layout}_1600"
        )

        course = Course(**valid_course_data)

        assert course.layout == expected


class TestCourseEvents:
    def test_events_default_to_empty_list(self, valid_course_data):
        course = Course(**valid_course_data)

        assert course.events == []

    def test_events_are_sorted_by_trigger_at(self, valid_course_data):
        events = [
            CourseEventType(
                # Replace with the required fields for your event model.
                type="example",
                trigger_at=300,
            ),
            CourseEventType(
                type="example",
                trigger_at=100,
            ),
            CourseEventType(
                type="example",
                trigger_at=200,
            ),
        ]

        valid_course_data["events"] = events

        course = Course(**valid_course_data)

        assert [
            event.trigger_at for event in course.events
        ] == [100, 200, 300]

    def test_events_with_same_trigger_at(self, valid_course_data):
        events = [
            CourseEventType(type="example", trigger_at=100),
            CourseEventType(type="example", trigger_at=100),
        ]

        valid_course_data["events"] = events

        course = Course(**valid_course_data)

        assert len(course.events) == 2
        assert all(event.trigger_at == 100 for event in course.events)

    def test_invalid_event(self, valid_course_data):
        valid_course_data["events"] = ["invalid"]

        with pytest.raises(ValidationError):
            Course(**valid_course_data)


class TestCourseSerialization:
    def test_serialization_uses_version_alias(self, valid_course_data):
        course = Course(**valid_course_data)

        data = course.model_dump()

        assert "$version" in data
        assert "version" not in data

    def test_serialization_includes_events(self, valid_course_data):
        course = Course(**valid_course_data)

        data = course.model_dump()

        assert data["events"] == []

    def test_serialization_preserves_course_data(self, valid_course_data):
        course = Course(**valid_course_data)

        data = course.model_dump()

        assert data["$version"] == "1.0"
        assert data["id"] == "course_00001_turf_flat_1600"
        assert data["name"] == "Test Course"
        assert data["distance"] == 1600
