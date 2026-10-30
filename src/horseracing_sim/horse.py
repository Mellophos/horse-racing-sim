from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .constants import Surface, Grade, DistanceCat, Strategy


class Horse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    version: str = Field(alias="$version")
    id: str = Field(pattern=r"^horse_[0-9]{5}$")
    name: str = Field(min_length=2, max_length=18)
    stats: Stats
    aptitudes: Aptitudes


class Stats(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    speed: float = Field(ge=1, le=2500)
    stamina: float = Field(ge=1, le=2500)
    power: float = Field(ge=1, le=2500)
    guts: float = Field(ge=1, le=2500)
    wit: float = Field(ge=1, le=2500)


class Aptitudes(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    surfaces: dict[Surface, Grade]
    distances: dict[DistanceCat, Grade]
    strategies: dict[Strategy, Grade]

    @model_validator(mode="before")
    @classmethod
    def convert_string_keys_to_enum_values(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        enum_mappings = {
            "surfaces": Surface,
            "distances": DistanceCat,
            "strategies": Strategy,
        }

        for field_name, enum_cls in enum_mappings.items():
            if field_name in data and isinstance(data[field_name], dict):
                converted_dict = {}
                for k, v in data[field_name].items():
                    try:
                        enum_member = enum_cls[str(k).upper()]
                        converted_dict[enum_member.value] = v
                    except KeyError:
                        converted_dict[k] = v

                data[field_name] = converted_dict
        return data
