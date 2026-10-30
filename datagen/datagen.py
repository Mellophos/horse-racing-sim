import json
import re
from abc import ABC, abstractmethod
from pathlib import Path

from jsonschema.validators import Draft202012Validator

from horse_racing_sim.validation.json_validator import load_schema

PROJECT_ROOT = Path(__file__).resolve().parents[1]

class JsonDataGenerator:
    def __init__(self):
        self.output_dir = Path(PROJECT_ROOT / "src/horseracing_sim/assets")
        self.providers = []

    def add_provider(self, provider_class, schema_identifier: str):
        provider = provider_class(self.output_dir, schema_identifier)
        self.providers.append(provider)

    def run(self):
        print(f"Starting data generation in: {self.output_dir}")
        for provider in self.providers:
            provider.generate()
        print("Generation complete.")


class BaseJsonProvider(ABC):
    def __init__(self, output_dir: str | Path, schema_identifier: str):
        self.output_dir = Path(output_dir)
        self.identifier = schema_identifier
        self.schema = load_schema(schema_identifier)

    def write_json(self, relative_path: str, data: dict):
        self.validate_json(data)

        full_path = self.output_dir / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with full_path.open("w", encoding="utf-8") as f:
            f.write(self.format_json(data, indent=4))
        print(f"    Generated: {full_path}")
        pass

    def validate_json(self, data: dict):
        validator = Draft202012Validator(self.schema)

        errors = sorted(
            validator.iter_errors(data),
            key=lambda error: list(error.absolute_path),
        )

        if errors:
            messages = "\n".join(
                f"- {'.'.join(map(str, error.absolute_path)) or '<root>'}: "
                f"{error.message}"
                for error in errors
            )

            raise ValueError(
                f"Validation failed ({self.identifier}):\n{messages}")

    @staticmethod
    def format_json(data, indent) -> str:
        formatted = json.dumps(data, ensure_ascii=False, indent=indent)

        def replace_array(m: re.Match[str]) -> str:
            content = m.group(1)
            return "[" + " ".join(
                content.split()) + "]" if content.strip() else "[]"

        formatted = re.sub(
            r"\[\s*([^\[\]]*?)\s*]",
            replace_array,
            formatted
        )
        return formatted

    @abstractmethod
    def generate(self):
        pass


class HorseProvider(BaseJsonProvider):
    def __init__(self, output_dir: Path, schema_identifier: str):
        super().__init__(output_dir, schema_identifier)

    def generate(self):
        horses = [
            # Write horse data here

        ]

        for horse in horses:
            horse_id = horse["id"]
            path = self.output_dir / "horses" / f"{horse_id}.json"
            if path.exists():
                print(f"#-- Horse {horse_id!r} already exists.")
                continue

            self.write_json(f"horses/{horse_id}.json", horse)

if __name__ == "__main__":
    generator = JsonDataGenerator()

    generator.add_provider(HorseProvider, "horse-0.1.0")

    generator.run()
