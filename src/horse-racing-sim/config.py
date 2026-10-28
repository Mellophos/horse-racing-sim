from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
BUILT_IN_DIR = DATA_DIR / "built_in"
CUSTOM_DIR = DATA_DIR / "custom"
EXPORTS_DIR = DATA_DIR / "exports"

CUSTOM_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
