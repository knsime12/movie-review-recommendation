from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = BASE_DIR / "backend"
MODEL_DIR = BACKEND_DIR / "models"
DATA_DIR = BASE_DIR / "data"