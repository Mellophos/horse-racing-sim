import json
import re
from abc import ABC, abstractmethod
from pathlib import Path

from src.horse_racing_sim.config import DATA_DIR
from json_validator import JsonTemplateValidator



class JsonDataGenerator:
    def __init__(self, output_dir: str = "built_in"):
        self.output_dir = Path(DATA_DIR / output_dir)
        self.providers = []

    def add_provider(self, provider_class):
        provider = provider_class(self.output_dir)
        self.providers.append(provider)

    def run(self):
        print(f"Starting data generation in: {self.output_dir}")
        for provider in self.providers:
            provider.generate()
        print("Generation complete.")


class BaseJsonProvider(ABC):
    def __init__(self, output_dir: str | Path, template_path: str | Path):
        self.output_dir = Path(output_dir)
        self.validator = JsonTemplateValidator(template_path)

    def write_json(self, relative_path: str, data: dict):
        self.validator.validate(data)

        full_path = self.output_dir / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with full_path.open("w", encoding="utf-8") as f:
            f.write(self.format_json(data, indent=4))
        print(f"    Generated: {full_path}")

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
    def __init__(self, output_dir):
        super().__init__(
            output_dir,
            DATA_DIR / "horse.example.json"
        )

    def generate(self):
        horses = [
            # Write horse data here

        ]

        for horse in horses:
            horse_id = horse["horse_id"]
            path = self.output_dir / "horses" / f"{horse_id}.json"
            if path.exists():
                print(f"#-- Horse {horse_id} already exists.")
                continue

            self.write_json(f"horses/{horse_id}.json", horse)


class TrackProvider(BaseJsonProvider):
    def __init__(self, output_dir):
        super().__init__(
            output_dir,
            DATA_DIR / "track.example.json"
        )

    def generate(self):
        tracks = [
            # Write track data here

        ]

        for track in tracks:
            track_id = track["track_id"]
            path = self.output_dir / "tracks" / track_id
            if path.exists():
                print(f"#-- Track {track_id} already exists.")
                continue

            self.write_json(f"tracks/{track_id}/track.json", track)


if __name__ == "__main__":
    generator = JsonDataGenerator()

    generator.add_provider(HorseProvider)
    generator.add_provider(TrackProvider)

    generator.run()
