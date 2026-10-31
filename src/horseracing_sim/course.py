from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator, \
    field_validator

from .constants import Surface, DistanceCat
from .events import CourseEventType


class Course(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        serialize_by_alias=True,
        populate_by_name=True,
    )

    version: str = Field(alias="$version")
    id: str = Field(
        pattern=r"^course_[0-9]{5}_(?:turf|dirt|artificial)_[a-z]+_[0-9]{4}$"
    )

    name: str = Field(min_length=1)
    surface: Surface
    distance: int = Field(ge=1000, le=5000)
    width: float = Field(ge=1)
    events: list[CourseEventType] = Field(default_factory=list)

    @property
    def distance_cat(self) -> DistanceCat:
        return DistanceCat.from_distance(self.distance)

    @property
    def layout(self) -> str:
        return self.id.split("_")[3].capitalize()

    @model_validator(mode="after")
    def validate_id_consistency(self) -> Self:
        _, _, id_surface, _, id_distance = self.id.split("_")

        if id_surface.upper() != self.surface.name:
            raise ValueError(
                f"ID surface '{id_surface}' does not match "
                f"surface attribute '{self.surface.name}'"
            )

        if int(id_distance) != self.distance:
            raise ValueError(
                f"ID distance '{id_distance}' does not match "
                f"distance attribute '{self.distance}'"
            )

        return self

    @field_validator("events", mode="after")
    @classmethod
    def sort_events(cls, events: list[CourseEventType]) -> list[
        CourseEventType]:
        return sorted(events, key=lambda e: e.trigger_at)
