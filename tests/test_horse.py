import pytest
from pydantic import ValidationError

from src.horse_racing_sim.constants import Surface, Grade, DistanceCat, \
    Strategy
from src.horse_racing_sim.horse import Horse, Stats, Aptitudes

stats = {
    "speed": 100,
    "stamina": 100,
    "power": 100,
    "guts": 100,
    "wit": 100,
}

@pytest.fixture
def valid_stats():
    return {
        "speed": 1000,
        "stamina": 900,
        "power": 800,
        "guts": 700,
        "wit": 600,
    }


@pytest.fixture
def valid_aptitudes():
    return {
        "surfaces": {
            Surface.TURF: Grade.A,
        },
        "distances": {
            DistanceCat.MILE: Grade.B,
        },
        "strategies": {
            Strategy.FRONT: Grade.C,
        },
    }


@pytest.fixture
def valid_horse_data(valid_stats, valid_aptitudes):
    return {
        "horse_id": "horse_12345",
        "name": "Silver Comet",
        "stats": valid_stats,
        "aptitudes": valid_aptitudes,
    }


# ------------------------------------------------------------------
# Stats tests
# ------------------------------------------------------------------

@pytest.mark.parametrize(
    "field",
    ["speed", "stamina", "power", "guts", "wit"],
)
@pytest.mark.parametrize("value", [1, 2500, 100.5])
def test_stats_accept_valid_values(field, value):
    stats[field] = value

    result = Stats.model_validate(stats)

    assert getattr(result, field) == value


@pytest.mark.parametrize(
    "field",
    ["speed", "stamina", "power", "guts", "wit"],
)
@pytest.mark.parametrize("value", [0, 2501, -1])
def test_stats_reject_out_of_range_values(field, value):
    stats[field] = value

    with pytest.raises(ValidationError):
        Stats.model_validate(stats)


def test_stats_reject_missing_field():
    with pytest.raises(ValidationError):
        Stats.model_validate({
            "speed": 100,
            "stamina": 100,
            "power": 100,
            "guts": 100,
        })


def test_stats_reject_extra_field(valid_stats):
    valid_stats["luck"] = 100

    with pytest.raises(ValidationError):
        Stats.model_validate(valid_stats)


def test_stats_are_immutable():
    stats = Stats(
        speed=100,
        stamina=100,
        power=100,
        guts=100,
        wit=100,
    )

    with pytest.raises(ValidationError):
        stats.speed = 200


# ------------------------------------------------------------------
# Aptitudes tests
# ------------------------------------------------------------------

def test_aptitudes_accept_enum_keys(valid_aptitudes):
    aptitudes = Aptitudes.model_validate(valid_aptitudes)

    assert aptitudes.surfaces == valid_aptitudes["surfaces"]
    assert aptitudes.distances == valid_aptitudes["distances"]
    assert aptitudes.strategies == valid_aptitudes["strategies"]


@pytest.mark.parametrize(
    ("field", "enum_cls"),
    [
        ("surfaces", Surface),
        ("distances", DistanceCat),
        ("strategies", Strategy),
    ],
)
def test_aptitudes_convert_string_keys_to_enum_values(field, enum_cls):
    enum_member = next(iter(enum_cls))
    data = {
        "surfaces": {},
        "distances": {},
        "strategies": {},
    }
    data[field] = {enum_member.name.lower(): Grade.A}

    aptitudes = Aptitudes.model_validate(data)

    assert enum_member in getattr(aptitudes, field)
    assert getattr(aptitudes, field)[enum_member] == Grade.A


def test_aptitudes_convert_uppercase_string_keys(valid_aptitudes):
    enum_member = next(iter(Surface))
    valid_aptitudes["surfaces"] = {
        enum_member.name.upper(): Grade.A,
    }

    aptitudes = Aptitudes.model_validate(valid_aptitudes)

    assert aptitudes.surfaces[enum_member] == Grade.A


def test_aptitudes_reject_invalid_enum_key(valid_aptitudes):
    valid_aptitudes["surfaces"] = {"INVALID_SURFACE": Grade.A}

    with pytest.raises(ValidationError):
        Aptitudes.model_validate(valid_aptitudes)


def test_aptitudes_reject_invalid_grade(valid_aptitudes):
    valid_aptitudes["surfaces"] = {
        next(iter(Surface)): "INVALID_GRADE",
    }

    with pytest.raises(ValidationError):
        Aptitudes.model_validate(valid_aptitudes)


def test_aptitudes_reject_extra_field(valid_aptitudes):
    valid_aptitudes["weather"] = {}

    with pytest.raises(ValidationError):
        Aptitudes.model_validate(valid_aptitudes)


def test_aptitudes_are_immutable(valid_aptitudes):
    aptitudes = Aptitudes.model_validate(valid_aptitudes)

    with pytest.raises(ValidationError):
        aptitudes.surfaces = {}


# ------------------------------------------------------------------
# Horse tests
# ------------------------------------------------------------------

def test_horse_accepts_valid_data(valid_horse_data):
    horse = Horse.model_validate(valid_horse_data)

    assert horse.horse_id == "horse_12345"
    assert horse.name == "Silver Comet"
    assert isinstance(horse.stats, Stats)
    assert isinstance(horse.aptitudes, Aptitudes)


@pytest.mark.parametrize(
    "horse_id",
    [
        "horse_1234",  # Too few digits
        "horse_123456",  # Too many digits
        "Horse_12345",  # Wrong prefix casing
        "horse_abcde",  # Non-numeric suffix
        "horse-12345",  # Wrong separator
        "",
    ],
)
def test_horse_rejects_invalid_id(valid_horse_data, horse_id):
    valid_horse_data["horse_id"] = horse_id

    with pytest.raises(ValidationError):
        Horse.model_validate(valid_horse_data)


@pytest.mark.parametrize(
    "name",
    [
        "",
        "A" * 19,
    ],
)
def test_horse_rejects_invalid_name_length(valid_horse_data, name):
    valid_horse_data["name"] = name

    with pytest.raises(ValidationError):
        Horse.model_validate(valid_horse_data)


def test_horse_accepts_name_at_maximum_length(valid_horse_data):
    valid_horse_data["name"] = "A" * 18

    horse = Horse.model_validate(valid_horse_data)

    assert len(horse.name) == 18


def test_horse_rejects_extra_field(valid_horse_data):
    valid_horse_data["color"] = "black"

    with pytest.raises(ValidationError):
        Horse.model_validate(valid_horse_data)


def test_horse_rejects_missing_stats(valid_horse_data):
    del valid_horse_data["stats"]

    with pytest.raises(ValidationError):
        Horse.model_validate(valid_horse_data)


def test_horse_is_immutable(valid_horse_data):
    horse = Horse.model_validate(valid_horse_data)

    with pytest.raises(ValidationError):
        horse.name = "New Name"
