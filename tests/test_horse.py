import json

import pytest
from pydantic import ValidationError

from horseracing_sim.constants import Surface, Grade, DistanceCat, Strategy
from horseracing_sim.horse import Horse, Stats, Aptitudes


@pytest.fixture
def valid_stats():
    return {
        "speed": 1500.0,
        "stamina": 1200.0,
        "power": 1300.0,
        "guts": 1000.0,
        "wit": 1400.0,
    }


@pytest.fixture
def valid_aptitudes():
    return {
        "surfaces": {
            Surface.TURF.name: Grade.A.value,
            Surface.DIRT.name: Grade.F.value,
        },
        "distances": {
            DistanceCat.SPRINT.name: Grade.B.value,
            DistanceCat.MILE.name: Grade.A.value,
            DistanceCat.INTERMEDIATE.name: Grade.C.value,
            DistanceCat.LONG.name: Grade.E.value,
            DistanceCat.EXTENDED.name: Grade.G.value,
        },
        "strategies": {
            Strategy.FRONT.name: Grade.S.value,
            Strategy.PACE.name: Grade.A.value,
            Strategy.LATE.name: Grade.E.value,
            Strategy.END.name: Grade.G.value,
        },
    }


@pytest.fixture
def valid_horse():
    return {
        "$version": "horse-0.1.0",
        "id": "horse_12345",
        "name": "Thunder",
        "stats": {
            "speed": 1500.0,
            "stamina": 1200.0,
            "power": 1300.0,
            "guts": 1000.0,
            "wit": 1400.0,
        },
        "aptitudes": {
            "surfaces": {
                "turf": 7,
                "dirt": 6,
            },
            "distances": {
                "sprint": 7,
                "mile": 7,
                "intermediate": 6,
                "long": 5,
                "extended": 4,
            },
            "strategies": {
                "front": 7,
                "pace": 6,
                "late": 5,
                "end": 4,
            },
        },
    }


# ------------------------------------------------------------------
# Stats tests
# ------------------------------------------------------------------

class TestStats:

    def test_valid_stats(self, valid_stats):
        stats = Stats(**valid_stats)

        assert stats.speed == 1500.0
        assert stats.stamina == 1200.0
        assert stats.power == 1300.0
        assert stats.guts == 1000.0
        assert stats.wit == 1400.0

    @pytest.mark.parametrize(
        "field",
        ["speed", "stamina", "power", "guts", "wit"],
    )
    @pytest.mark.parametrize("value", [0.0, 2500.1, -1.0])
    def test_stats_out_of_range(self, valid_stats, field, value):
        valid_stats[field] = value

        with pytest.raises(ValidationError):
            Stats(**valid_stats)

    @pytest.mark.parametrize(
        "field",
        ["speed", "stamina", "power", "guts", "wit"],
    )
    @pytest.mark.parametrize("value", [1.0, 2500.0])
    def test_stats_boundary_values(self, valid_stats, field, value):
        valid_stats[field] = value

        stats = Stats(**valid_stats)

        assert getattr(stats, field) == value

    def test_stats_rejects_integer_in_strict_mode(self, valid_stats):
        valid_stats["speed"] = 1500

        stats = Stats(**valid_stats)

        assert stats.speed == 1500.0
        assert isinstance(stats.speed, float)

    def test_stats_rejects_extra_fields(self, valid_stats):
        valid_stats["luck"] = 100

        with pytest.raises(ValidationError):
            Stats(**valid_stats)

    def test_stats_rejects_missing_fields(self, valid_stats):
        del valid_stats["speed"]

        with pytest.raises(ValidationError):
            Stats(**valid_stats)

    def test_stats_is_frozen(self):
        stats = Stats(
            speed=1500.0,
            stamina=1200.0,
            power=1300.0,
            guts=1000.0,
            wit=1400.0,
        )

        with pytest.raises(ValidationError):
            stats.speed = 1000.0


# ------------------------------------------------------------------
# Aptitudes tests
# ------------------------------------------------------------------

class TestAptitudes:

    def test_valid_aptitudes(self, valid_aptitudes):
        aptitudes = Aptitudes(**valid_aptitudes)

        assert aptitudes.surfaces[Surface.TURF] == Grade.A
        assert aptitudes.distances[DistanceCat.SPRINT] == Grade.B
        assert aptitudes.strategies[Strategy.FRONT] == Grade.S

    def test_converts_uppercase_string_keys(self):
        aptitudes = Aptitudes(
            surfaces={"TURF": Grade.A},
            distances={"SPRINT": Grade.B},
            strategies={"FRONT": Grade.S},
        )

        assert Surface.TURF in aptitudes.surfaces
        assert DistanceCat.SPRINT in aptitudes.distances
        assert Strategy.FRONT in aptitudes.strategies

    def test_converts_lowercase_string_keys(self):
        aptitudes = Aptitudes(
            surfaces={"turf": Grade.A},
            distances={"sprint": Grade.B},
            strategies={"front": Grade.S},
        )

        assert Surface.TURF in aptitudes.surfaces
        assert DistanceCat.SPRINT in aptitudes.distances
        assert Strategy.FRONT in aptitudes.strategies

    def test_converts_mixed_case_string_keys(self):
        aptitudes = Aptitudes(
            surfaces={"TuRf": Grade.A},
            distances={"SpRiNt": Grade.B},
            strategies={"FrOnT": Grade.S},
        )

        assert Surface.TURF in aptitudes.surfaces
        assert DistanceCat.SPRINT in aptitudes.distances
        assert Strategy.FRONT in aptitudes.strategies

    def test_preserves_unknown_enum_keys_for_validation(self):
        with pytest.raises(ValidationError):
            Aptitudes(
                surfaces={"UNKNOWN": Grade.A},
                distances={"SPRINT": Grade.B},
                strategies={"FRONT": Grade.S},
            )

    def test_rejects_invalid_grade(self):
        with pytest.raises(ValidationError):
            Aptitudes(
                surfaces={"TURF": "INVALID"},
                distances={"SPRINT": Grade.B},
                strategies={"FRONT": Grade.S},
            )

    def test_rejects_extra_fields(self):
        with pytest.raises(ValidationError):
            Aptitudes(
                surfaces={"TURF": Grade.A},
                distances={"SPRINT": Grade.B},
                strategies={"FRONT": Grade.S},
                unknown={},
            )

    def test_rejects_missing_fields(self):
        with pytest.raises(ValidationError):
            Aptitudes(
                surfaces={"TURF": Grade.A},
                distances={"SPRINT": Grade.B},
            )

    def test_aptitudes_is_frozen(self):
        aptitudes = Aptitudes(
            surfaces={"TURF": Grade.A},
            distances={"SPRINT": Grade.B},
            strategies={"FRONT": Grade.S},
        )

        with pytest.raises(ValidationError):
            aptitudes.surfaces = {}


# ------------------------------------------------------------------
# Aptitudes conversion tests
# ------------------------------------------------------------------

class TestAptitudeKeyConversion:

    @pytest.mark.parametrize(
        "key, expected",
        [
            ("turf", Surface.TURF),
            ("dirt", Surface.DIRT),
        ],
    )
    def test_surface_key_conversion(self, key, expected):
        aptitudes = Aptitudes(
            surfaces={key: 7},
            distances={
                "sprint": 7,
                "mile": 7,
                "intermediate": 6,
                "long": 5,
                "extended": 4,
            },
            strategies={
                "front": 7,
                "pace": 6,
                "late": 5,
                "end": 4,
            },
        )

        assert expected in aptitudes.surfaces

    @pytest.mark.parametrize(
        "key, expected",
        [
            ("sprint", DistanceCat.SPRINT),
            ("mile", DistanceCat.MILE),
            ("intermediate", DistanceCat.INTERMEDIATE),
            ("long", DistanceCat.LONG),
            ("extended", DistanceCat.EXTENDED),
        ],
    )
    def test_distance_key_conversion(self, key, expected):
        aptitudes = Aptitudes(
            surfaces={"turf": 7, "dirt": 6},
            distances={key: 7},
            strategies={
                "front": 7,
                "pace": 6,
                "late": 5,
                "end": 4,
            },
        )

        assert expected in aptitudes.distances

    @pytest.mark.parametrize(
        "key, expected",
        [
            ("front", Strategy.FRONT),
            ("pace", Strategy.PACE),
            ("late", Strategy.LATE),
            ("end", Strategy.END),
        ],
    )
    def test_strategy_key_conversion(self, key, expected):
        aptitudes = Aptitudes(
            surfaces={"turf": 7, "dirt": 6},
            distances={
                "sprint": 7,
                "mile": 7,
                "intermediate": 6,
                "long": 5,
                "extended": 4,
            },
            strategies={key: 7},
        )

        assert expected in aptitudes.strategies


# ------------------------------------------------------------------
# Horse tests
# ------------------------------------------------------------------

class TestHorse:

    def test_valid_horse(self, valid_horse):
        horse = Horse(**valid_horse)

        assert horse.id == "horse_12345"
        assert horse.name == "Thunder"
        assert horse.version == "horse-0.1.0"
        assert isinstance(horse.stats, Stats)
        assert isinstance(horse.aptitudes, Aptitudes)

    def test_accepts_version_field_name(self, valid_horse):
        del valid_horse["$version"]
        valid_horse["version"] = "horse-0.1.0"

        horse = Horse(**valid_horse)

        assert horse.version == "horse-0.1.0"

    def test_rejects_invalid_horse_id(self, valid_horse):
        invalid_ids = [
            "horse_1234",
            "horse_123456",
            "horse_abcde",
            "Horse_12345",
            "12345",
        ]

        for invalid_id in invalid_ids:
            valid_horse["id"] = invalid_id

            with pytest.raises(ValidationError):
                Horse(**valid_horse)

    @pytest.mark.parametrize(
        "name",
        ["", "A", "A" * 19],
    )
    def test_rejects_invalid_name_length(self, valid_horse, name):
        valid_horse["name"] = name

        with pytest.raises(ValidationError):
            Horse(**valid_horse)

    def test_accepts_name_boundaries(self, valid_horse):
        for name in ["AB", "A" * 18]:
            valid_horse["name"] = name

            horse = Horse(**valid_horse)

            assert horse.name == name

    def test_rejects_extra_fields(self, valid_horse):
        valid_horse["unknown"] = "value"

        with pytest.raises(ValidationError):
            Horse(**valid_horse)

    def test_rejects_missing_fields(self, valid_horse):
        del valid_horse["name"]

        with pytest.raises(ValidationError):
            Horse(**valid_horse)

    def test_rejects_non_string_version(self, valid_horse):
        valid_horse["$version"] = 1.0

        with pytest.raises(ValidationError):
            Horse(**valid_horse)

    def test_horse_is_frozen(self, valid_horse):
        horse = Horse(**valid_horse)

        with pytest.raises(ValidationError):
            horse.name = "Lightning"

    def test_serialization_uses_version_alias(self, valid_horse):
        horse = Horse(**valid_horse)

        serialized = horse.model_dump()

        assert "$version" in serialized
        assert "version" not in serialized
        assert serialized["$version"] == "horse-0.1.0"

    def test_serialization_can_use_field_names(self, valid_horse):
        horse = Horse(**valid_horse)

        serialized = horse.model_dump(by_alias=False)

        assert "version" in serialized
        assert "$version" not in serialized


# ------------------------------------------------------------------
# Horse JSON tests
# ------------------------------------------------------------------

class TestHorseJsonLoading:

    def test_load_valid_horse_from_json(self, valid_horse):
        horse_json = json.dumps(valid_horse)

        horse = Horse.model_validate_json(horse_json)

        assert isinstance(horse, Horse)
        assert horse.id == "horse_12345"
        assert horse.name == "Thunder"

        assert horse.stats.speed == 1500.0

        assert horse.aptitudes.surfaces[Surface.TURF] == Grade.A
        assert horse.aptitudes.surfaces[Surface.DIRT] == Grade.B

        assert horse.aptitudes.distances[DistanceCat.SPRINT] == Grade.A
        assert horse.aptitudes.distances[DistanceCat.MILE] == Grade.A
        assert horse.aptitudes.distances[DistanceCat.INTERMEDIATE] == Grade.B
        assert horse.aptitudes.distances[DistanceCat.LONG] == Grade.C
        assert horse.aptitudes.distances[DistanceCat.EXTENDED] == Grade.D

        assert horse.aptitudes.strategies[Strategy.FRONT] == Grade.A
        assert horse.aptitudes.strategies[Strategy.PACE] == Grade.B
        assert horse.aptitudes.strategies[Strategy.LATE] == Grade.C
        assert horse.aptitudes.strategies[Strategy.END] == Grade.D
