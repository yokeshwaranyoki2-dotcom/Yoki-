"""Central configuration. All secrets come from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
DB_PATH = os.getenv("DB_PATH", "yoki.db")
MEMORY_LIMIT = _int("MEMORY_LIMIT", 20)          # messages remembered per chat
COOLDOWN_SECONDS = _int("COOLDOWN_SECONDS", 3)   # min gap between a user's messages
MAX_INPUT_CHARS = 2000
ADMIN_IDS = {
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()
}


def validate() -> None:
    missing = [
        n for n, v in (("TELEGRAM_TOKEN", TELEGRAM_TOKEN), ("GEMINI_API_KEY", GEMINI_API_KEY)) if not v
    ]
    if missing:
        raise SystemExit(f"Missing in .env: {', '.join(missing)}")
