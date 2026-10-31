from typing import Literal, Annotated

from pydantic import BaseModel, ConfigDict, Field

from .constants import Surface


class CourseEvent(BaseModel):
    """Base class for events that occur at a specific point on a Course.

    Each event is triggered at a specified distance from the start of the
    Course. Subclasses define the additional information associated with
    each type of course event.

    Attributes:
        trigger_at: Distance in metres from the start of the course
            at which the event takes effect.
    """
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    trigger_at: int = Field(ge=0)


class Straight(CourseEvent):
    """Represent a straight section on the Course.

    Each straight section is marked by two separate events.

    Attributes:
        trigger_at: Distance in metres from the start of the course
            at which the event takes effect.
        is_start: ``true`` if the event marks the beginning of a straight,
            ``false`` if it marks the end.
        straight_id: Identifies the physical straight section. The same
            straight should ideally have the exact same ID.
        type: Optional, defaults to ``0`` (no specification).
            Identifies the type of straight: ``1`` for homestraight,
            ``2`` for backstraight, ``3`` for false straight.
    """
    id: Literal[0] = 0
    is_start: bool
    straight_id: int = Field(ge=0)
    type: Literal[0, 1, 2, 3] = 0


class Corner(CourseEvent):
    """Represent a curved section on the Course.

    Attributes:
        trigger_at: Distance in metres from the start of the course
            at which the event takes effect.
        length: Length of the Corner
        direction: Direction of the Corner. ``-1`` for left turn, ``1`` for
            right turn.
        number: Optional, defaults to ``0`` (no specification). Usually
            seen in Japanese tracks. Labelling for various corner sections
            on the Course, from ``1`` to ``4``.
    """
    id: Literal[1] = 1
    length: int = Field(ge=1)
    direction: Literal[-1, 1] | None = None
    number: Literal[0, 1, 2, 3, 4] = 0


class Slope(CourseEvent):
    """Represent a sloped section on the Course.

    Attributes:
        trigger_at: Distance in metres from the start of the course
            at which the event takes effect.
        length: Length of the Slope
        gradient: Gradient of the sloped section as a percentage, from
            ``-100`` to ``100``. Please avoid writing values past
            ``-3`` and ``3`` as horses may struggle taking extreme gradients.
    """
    id: Literal[2] = 2
    length: int = Field(ge=1)
    gradient: float = Field(ge=-100, le=100)


class SurfaceChange(CourseEvent):
    """Represent a change in surface on the Course.

    **This event should be used sparingly.** For Courses where the starting
    chute is a different surface, define the event with ``trigger_at=0``.

    Attributes:
        trigger_at: Distance in metres from the start of the course
            at which the event takes effect.
        length: How long the new surface runs for
        change_to: Surface to change to
    """
    id: Literal[3] = 3
    length: int = Field(ge=1)
    change_to: Surface


class WidthChange(CourseEvent):
    """Represent a change in the Course's maximum width.

    This event might not affect much in a Race, avoid using it unless you
    actually need it.

    Attributes:
        trigger_at: Distance in metres from the start of the course
            at which the event takes effect.
        change_to: New value to change Course width to.
    """
    id: Literal[4] = 4
    change_to: float = Field(ge=1)


CourseEventType = Annotated[
    Straight | Corner | Slope | SurfaceChange | WidthChange,
    Field(discriminator="id")
]
