import json
from pathlib import Path


class JsonTemplateValidator:
    def __init__(self, template_path: str | Path):
        self.template_path = Path(template_path)

        with self.template_path.open(encoding="utf-8") as f:
            self.template = json.load(f)

    def validate(self, data: dict):
        self._validate_value(
            data,
            self.template,
            path="$",
        )

    def _validate_value(self, data, template, path):
        # Special handling for dynamic track configurations.
        if path == "$.configurations":
            self._validate_configurations(data, path)
            return

        if isinstance(template, dict):
            if not isinstance(data, dict):
                raise ValueError(f"{path}: expected an object")

            missing = template.keys() - data.keys()
            extra = data.keys() - template.keys()

            if missing or extra:
                raise ValueError(
                    f"{path}: missing keys={sorted(missing)}, "
                    f"unexpected keys={sorted(extra)}"
                )

            for key, expected in template.items():
                self._validate_value(
                    data[key],
                    expected,
                    f"{path}.{key}",
                )

        elif isinstance(template, list):
            if not isinstance(data, list):
                raise ValueError(f"{path}: expected an array")

            # Use the example's first element as the type template.
            if template:
                for i, item in enumerate(data):
                    self._validate_value(
                        item,
                        template[0],
                        f"{path}[{i}]",
                    )

        elif isinstance(template, bool):
            if not isinstance(data, bool):
                raise ValueError(f"{path}: expected a boolean")

        elif isinstance(template, int):
            if not isinstance(data, int) or isinstance(data, bool):
                raise ValueError(f"{path}: expected an integer")

        elif isinstance(template, float):
            if not isinstance(data, (int, float)) or isinstance(data, bool):
                raise ValueError(f"{path}: expected a number")

        elif not isinstance(data, type(template)):
            raise ValueError(
                f"{path}: expected {type(template).__name__}, "
                f"got {type(data).__name__}"
            )

    def _validate_configurations(self, data, path):
        if not isinstance(data, dict) or not data:
            raise ValueError(
                f"{path}: expected a non-empty object"
            )

        allowed_surfaces = {"turf", "dirt", "artificial"}
        extra = data.keys() - allowed_surfaces

        if extra:
            raise ValueError(
                f"{path}: unsupported surfaces {sorted(extra)}"
            )

        for surface, layouts in data.items():
            if not isinstance(layouts, dict) or not layouts:
                raise ValueError(
                    f"{path}.{surface}: at least one layout is required"
                )

            for layout, distances in layouts.items():
                if not isinstance(layout, str) or not layout:
                    raise ValueError(
                        f"{path}.{surface}: invalid layout name"
                    )

                if not isinstance(distances, list) or not distances:
                    raise ValueError(
                        f"{path}.{surface}.{layout}: "
                        "expected a non-empty array"
                    )

                for distance in distances:
                    if (
                        not isinstance(distance, int)
                        or isinstance(distance, bool)
                        or distance <= 0
                    ):
                        raise ValueError(
                            f"{path}.{surface}.{layout}: "
                            "distances must be positive integers"
                        )