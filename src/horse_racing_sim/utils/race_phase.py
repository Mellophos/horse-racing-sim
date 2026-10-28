def _round_div(n: int, d: int) -> int:
    return (2 * n + d) // (2 * d)


def phase_boundaries(distance: int) -> list:
    return [
        _round_div(distance * 4, 24),
        _round_div(distance * 16, 24),
        _round_div(distance * 20, 24),
        distance
    ]


def section_boundaries(distance: int) -> list:
    return [
        _round_div(distance * i, 24)
        for i in range(1, 25)
    ]


def get_current_phase(current_position: float,
                      course_distance: int) -> int:
    phases = phase_boundaries(course_distance)

    for n, phase_end in enumerate(phases):
        if current_position <= phase_end:
            return n

    raise ValueError(
        f'Position {current_position} is out of course distance range: '
        f'{course_distance}')


def get_current_section(current_position: float, course_distance: int) -> int:
    sections = section_boundaries(course_distance)

    for n, section_end in enumerate(sections):
        if current_position <= section_end:
            return n + 1

    raise ValueError(
        f'Position {current_position} is out of course distance range: '
        f'{course_distance}')
