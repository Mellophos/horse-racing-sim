import re


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value to an inclusive range.

    Args:
        value: The value to clamp.
        minimum: The lower bound.
        maximum: The upper bound.

    Returns:
        The value constrained to [minimum, maximum].

    Raises:
        ValueError: If ``minimum`` > ``maximum``.
    """
    if minimum > maximum:
        raise ValueError("minimum must be <= maximum.")
    return max(min(value, maximum), minimum)


def soft_cap(
        x: float,
        cap: float,
        excess_factor: float = 1.0
) -> float:
    """Reduce the excess above a cap by a configurable factor.

    Args:
        x: The input value.
        cap: The threshold above which excess is reduced.
        excess_factor: The fraction of excess to retain, in [0, 1].

    Returns:
        The input value if x <= cap, otherwise, the cap plus the specified
        fraction of the excess.

    Raises:
        ValueError: If excess_factor is outside [0, 1].
    """
    if not 0 <= excess_factor <= 1:
        raise ValueError("excess_factor must be between 0 and 1.")
    return x if x <= cap else cap + (x - cap) * excess_factor


def bracket(position: int, total_items: int, num_brackets: int = 8) -> int:
    """Calculate the bracket number for an item's position.

    When the total number of items is less than the number of brackets,
    each item retains its own position as its bracket number. Otherwise,
    items are distributed across the specified number of brackets

    Args:
        position: The item's position.
        total_items: The total number of items.
        num_brackets: The number of brackets to distribute items across.

    Returns:
        The calculated 1-based bracket number.

    Raises:
        ValueError: If any argument is outside its valid range.

    """
    if position < 1:
        raise ValueError("position must be >= 1.")
    if total_items < 1:
        raise ValueError("total_items must be >= 1.")
    if num_brackets < 1:
        raise ValueError("num_brackets must be >= 1.")
    if position > total_items:
        raise ValueError("position must be less than or equal to total_items.")
    return (
        (position * num_brackets + total_items - 1) // total_items
        if total_items > num_brackets else position
    )


def lerp(v0: float, v1: float, t: float) -> float:
    """Linearly interpolate between two values.

    Args:
        v0: The starting value.
        v1: The ending value.
        t: The interpolation factor. Values outside [0, 1] perform linear
            extrapolation.

    Returns:
        The interpolated value as a float if ``inverse=False``.
        The fractional position (t) as a float if ``inverse=True``.
    """
    return v0 + t * (v1 - v0)


def inverse_lerp(v0: float, v1: float, value: float) -> float:
    """Calculate the fractional position of a value within a range.

    Args:
        v0: The starting value of the range.
        v1: The ending value of the range.
        value: The value whose fractional position is calculated.

    Returns:
        The fractional position of the value within the range.
        Values outside the range produce results outside [0, 1].

    Raises:
        ZeroDivisionError: If v0 and v1 are equal.
    """
    if v0 == v1:
        raise ZeroDivisionError("Cannot perform inverse lerp when v0 == v1.")
    return (value - v0) / (v1 - v0)


def imperial_to_metres(
        miles: float | int = 0,
        furlongs: float | int = 0,
        yards: float | int = 0,
        round_result: bool = False
) -> float:
    """Convert imperial distances to metres.

    The exact conversion factors are:
        - 1 mile: 1760 yards
        - 1 furlong: 220 yards
        - 1 yard: 0.9144 metres

    Args:
        miles: Distance in miles
        furlongs: Distance in furlongs
        yards: Distance in yards
        round_result: Whether to round off to nearest integer. Halfway
            floats are rounded up.

    Returns:
        The converted distance in metres as a float.
    """
    total_yards = (miles * 1760) + (furlongs * 220) + yards
    total_metres = total_yards * 0.9144

    if round_result:
        return (total_metres + 0.5) // 1
    return total_metres


def imperial_str_to_metres(
        distance_str: str,
        round_result: bool = False
) -> float:
    """Convert imperial distances written in strings to metres.

    The exact conversion factors are:
        - 1 mile: 1760 yards
        - 1 furlong: 220 yards
        - 1 yard: 0.9144 metres

    Args:
        distance_str: Distance to convert as a string.
        round_result: Whether to round off to nearest integer. Halfway
            floats are rounded up.

    Returns:
        The converted distance in metres as a float.

    Raises:
        ValueError: If distance_str is empty or invalid.
    """
    if not isinstance(distance_str, str):
        raise TypeError("distance_str must be a string.")

    pattern = r"(\d+(?:\.\d+)?)\s*([mfy])"
    validation_pattern = (
        r"\s*\d+(?:\.\d+)?\s*[mfy](?:\s*\d+(?:\.\d+)?\s*[mfy])*\s*"
    )

    conversion = {
        "m": 1760,
        "f": 220,
        "y": 1
    }

    if not distance_str.strip() or not re.fullmatch(
            validation_pattern, distance_str, re.IGNORECASE
    ):
        raise ValueError(f"Invalid string: {distance_str!r}")

    matches = re.findall(pattern, distance_str, re.IGNORECASE)

    total_yards = sum(
        float(value) * conversion[unit.lower()]
        for value, unit in matches
    )

    total_metres = total_yards * 0.9144

    if round_result:
        return (total_metres + 0.5) // 1
    return total_metres
