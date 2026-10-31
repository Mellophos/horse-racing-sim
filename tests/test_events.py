import pytest
from pydantic import BaseModel, ConfigDict, ValidationError

from horseracing_sim.constants import Surface
from horseracing_sim.events import (
    CourseEvent,
    Straight,
    Corner,
    Slope,
    SurfaceChange,
    WidthChange,
    CourseEventType,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class EventContainer(BaseModel):
    """Helper model for testing the discriminated union."""
    model_config = ConfigDict(strict=True)

    event: CourseEventType


# ---------------------------------------------------------------------------
# CourseEvent
# ---------------------------------------------------------------------------

def test_course_event_valid():
    event = CourseEvent(trigger_at=100)
    assert event.trigger_at == 100


def test_course_event_trigger_at_zero():
    event = CourseEvent(trigger_at=0)
    assert event.trigger_at == 0


@pytest.mark.parametrize("trigger_at", [-1, -100])
def test_course_event_rejects_negative_trigger_at(trigger_at):
    with pytest.raises(ValidationError):
        CourseEvent(trigger_at=trigger_at)


@pytest.mark.parametrize("trigger_at", ["100", 100.0, True])
def test_course_event_rejects_non_integer_trigger_at(trigger_at):
    with pytest.raises(ValidationError):
        CourseEvent(trigger_at=trigger_at)


def test_course_event_rejects_extra_fields():
    with pytest.raises(ValidationError):
        CourseEvent(trigger_at=100, unknown="value")


def test_course_event_is_frozen():
    event = CourseEvent(trigger_at=100)

    with pytest.raises(ValidationError):
        event.trigger_at = 200


# ---------------------------------------------------------------------------
# Straight
# ---------------------------------------------------------------------------

def test_straight_valid():
    event = Straight(
        trigger_at=100,
        is_start=True,
        straight_id=1,
    )

    assert event.trigger_at == 100
    assert event.is_start is True
    assert event.straight_id == 1
    assert event.id == 0
    assert event.type == 0


@pytest.mark.parametrize("straight_type", [0, 1, 2, 3])
def test_straight_accepts_valid_types(straight_type):
    event = Straight(
        trigger_at=100,
        is_start=True,
        straight_id=1,
        type=straight_type,
    )

    assert event.type == straight_type


@pytest.mark.parametrize("straight_type", [-1, 4, 5])
def test_straight_rejects_invalid_types(straight_type):
    with pytest.raises(ValidationError):
        Straight(
            trigger_at=100,
            is_start=True,
            straight_id=1,
            type=straight_type,
        )


@pytest.mark.parametrize("straight_id", [-1, -100])
def test_straight_rejects_negative_straight_id(straight_id):
    with pytest.raises(ValidationError):
        Straight(
            trigger_at=100,
            is_start=True,
            straight_id=straight_id,
        )


def test_straight_rejects_missing_is_start():
    with pytest.raises(ValidationError):
        Straight(trigger_at=100, straight_id=1)


def test_straight_rejects_invalid_is_start():
    with pytest.raises(ValidationError):
        Straight(
            trigger_at=100,
            is_start=1,
            straight_id=1,
        )


def test_straight_id_is_fixed():
    with pytest.raises(ValidationError):
        Straight(
            trigger_at=100,
            id=1,
            is_start=True,
            straight_id=1,
        )


# ---------------------------------------------------------------------------
# Corner
# ---------------------------------------------------------------------------

def test_corner_valid():
    event = Corner(
        trigger_at=100,
        length=50,
        direction=1,
        number=2,
    )

    assert event.trigger_at == 100
    assert event.length == 50
    assert event.direction == 1
    assert event.number == 2
    assert event.id == 1


def test_corner_defaults():
    event = Corner(trigger_at=100, length=50)

    assert event.direction is None
    assert event.number == 0


@pytest.mark.parametrize("direction", [-1, 1, None])
def test_corner_accepts_valid_directions(direction):
    event = Corner(
        trigger_at=100,
        length=50,
        direction=direction,
    )

    assert event.direction == direction


@pytest.mark.parametrize("direction", [0, 2, -2, "1"])
def test_corner_rejects_invalid_directions(direction):
    with pytest.raises(ValidationError):
        Corner(
            trigger_at=100,
            length=50,
            direction=direction,
        )


@pytest.mark.parametrize("length", [0, -1, -100])
def test_corner_rejects_invalid_length(length):
    with pytest.raises(ValidationError):
        Corner(trigger_at=100, length=length)


@pytest.mark.parametrize("number", [0, 1, 2, 3, 4])
def test_corner_accepts_valid_numbers(number):
    event = Corner(trigger_at=100, length=50, number=number)
    assert event.number == number


@pytest.mark.parametrize("number", [-1, 5, 6])
def test_corner_rejects_invalid_numbers(number):
    with pytest.raises(ValidationError):
        Corner(trigger_at=100, length=50, number=number)


def test_corner_id_is_fixed():
    with pytest.raises(ValidationError):
        Corner(trigger_at=100, length=50, id=0)


# ---------------------------------------------------------------------------
# Slope
# ---------------------------------------------------------------------------

def test_slope_valid():
    event = Slope(
        trigger_at=100,
        length=200,
        gradient=2.5,
    )

    assert event.trigger_at == 100
    assert event.length == 200
    assert event.gradient == 2.5
    assert event.id == 2


@pytest.mark.parametrize("gradient", [-100, -3, 0, 3, 100])
def test_slope_accepts_valid_gradient(gradient):
    event = Slope(
        trigger_at=100,
        length=50,
        gradient=gradient,
    )

    assert event.gradient == gradient


@pytest.mark.parametrize("gradient", [-100.1, 100.1, -101, 101])
def test_slope_rejects_out_of_range_gradient(gradient):
    with pytest.raises(ValidationError):
        Slope(
            trigger_at=100,
            length=50,
            gradient=gradient,
        )


@pytest.mark.parametrize("length", [0, -1])
def test_slope_rejects_invalid_length(length):
    with pytest.raises(ValidationError):
        Slope(
            trigger_at=100,
            length=length,
            gradient=2.5,
        )


def test_slope_id_is_fixed():
    with pytest.raises(ValidationError):
        Slope(
            trigger_at=100,
            length=50,
            gradient=2.5,
            id=1,
        )


# ---------------------------------------------------------------------------
# SurfaceChange
# ---------------------------------------------------------------------------

def test_surface_change_valid():
    surface = next(iter(Surface))

    event = SurfaceChange(
        trigger_at=0,
        length=100,
        change_to=surface,
    )

    assert event.trigger_at == 0
    assert event.length == 100
    assert event.change_to == surface
    assert event.id == 3


def test_surface_change_rejects_invalid_length():
    surface = next(iter(Surface))

    with pytest.raises(ValidationError):
        SurfaceChange(
            trigger_at=100,
            length=0,
            change_to=surface,
        )


def test_surface_change_rejects_invalid_surface():
    with pytest.raises(ValidationError):
        SurfaceChange(
            trigger_at=100,
            length=100,
            change_to="invalid_surface",
        )


def test_surface_change_id_is_fixed():
    surface = next(iter(Surface))

    with pytest.raises(ValidationError):
        SurfaceChange(
            trigger_at=100,
            length=100,
            change_to=surface,
            id=0,
        )


# ---------------------------------------------------------------------------
# WidthChange
# ---------------------------------------------------------------------------

def test_width_change_valid():
    event = WidthChange(
        trigger_at=100,
        change_to=12.5,
    )

    assert event.trigger_at == 100
    assert event.change_to == 12.5
    assert event.id == 4


@pytest.mark.parametrize("width", [1, 1.0, 10.5, 100])
def test_width_change_accepts_valid_width(width):
    event = WidthChange(
        trigger_at=100,
        change_to=width,
    )

    assert event.change_to == width


@pytest.mark.parametrize("width", [0, -1, -10.5])
def test_width_change_rejects_invalid_width(width):
    with pytest.raises(ValidationError):
        WidthChange(
            trigger_at=100,
            change_to=width,
        )


def test_width_change_rejects_non_numeric_width():
    with pytest.raises(ValidationError):
        WidthChange(
            trigger_at=100,
            change_to="10.5",
        )


def test_width_change_id_is_fixed():
    with pytest.raises(ValidationError):
        WidthChange(
            trigger_at=100,
            change_to=10.5,
            id=0,
        )


# ---------------------------------------------------------------------------
# Discriminated union: CourseEventType
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("event_data", "expected_type"),
    [
        (
                {
                    "id": 0,
                    "trigger_at": 100,
                    "is_start": True,
                    "straight_id": 1,
                },
                Straight,
        ),
        (
                {
                    "id": 1,
                    "trigger_at": 200,
                    "length": 50,
                    "direction": -1,
                },
                Corner,
        ),
        (
                {
                    "id": 2,
                    "trigger_at": 300,
                    "length": 100,
                    "gradient": 2.5,
                },
                Slope,
        ),
        (
                {
                    "id": 3,
                    "trigger_at": 400,
                    "length": 100,
                    "change_to": next(iter(Surface)),
                },
                SurfaceChange,
        ),
        (
                {
                    "id": 4,
                    "trigger_at": 500,
                    "change_to": 10.5,
                },
                WidthChange,
        ),
    ],
)
def test_course_event_type_resolves_correct_subclass(
        event_data,
        expected_type,
):
    container = EventContainer(event=event_data)

    assert isinstance(container.event, expected_type)


@pytest.mark.parametrize("event_id", [-1, 5, 100, "invalid"])
def test_course_event_type_rejects_unknown_discriminator(event_id):
    with pytest.raises(ValidationError):
        EventContainer(
            event={
                "id": event_id,
                "trigger_at": 100,
            }
        )


def test_course_event_type_rejects_missing_discriminator():
    with pytest.raises(ValidationError):
        EventContainer(
            event={
                "trigger_at": 100,
                "length": 50,
            }
        )


def test_course_event_type_rejects_invalid_subclass_fields():
    with pytest.raises(ValidationError):
        EventContainer(
            event={
                "id": 0,
                "trigger_at": 100,
                "is_start": True,
                "straight_id": 1,
                "length": 50,
            }
        )


def test_course_event_type_rejects_wrong_field_for_discriminator():
    with pytest.raises(ValidationError):
        EventContainer(
            event={
                "id": 1,
                "trigger_at": 100,
                "is_start": True,
                "straight_id": 1,
            }
        )
