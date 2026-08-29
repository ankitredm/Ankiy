"""Environment-backed configuration for Ankiy.

Secrets belong in .env, not in personality profiles or source control.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_PROFILE_DIR = PROJECT_ROOT / "profiles"
DEFAULT_MEDIA_DIR = PROJECT_ROOT / "media"


def _as_path(value: str | None, fallback: Path) -> Path:
    return Path(value).expanduser() if value else fallback


def _ids(value: str | None) -> set[int]:
    """Parse a forgiving comma-separated Telegram numeric ID list."""
    if not value:
        return set()
    ids: set[int] = set()
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            ids.add(int(item))
        except ValueError as error:
            raise ValueError(
                "TELEGRAM_ALLOWED_USER_IDS must be comma-separated numeric IDs."
            ) from error
    return ids


@dataclass(frozen=True, slots=True)
class Settings:
    """All runtime settings, loaded once at application start."""

    llm_base_url: str
    llm_model: str
    llm_api_key: str | None
    owner_name: str
    default_profile: str
    data_dir: Path
    profile_dir: Path
    media_dir: Path
    telegram_bot_token: str | None
    telegram_allowed_user_ids: set[int] = field(default_factory=set)
    elevenlabs_api_key: str | None = None
    elevenlabs_voice_id: str | None = None
    elevenlabs_model: str = "eleven_multilingual_v2"
    image_api_key: str | None = None
    image_base_url: str = "https://api.openai.com/v1"
    image_model: str = "gpt-image-1"
    image_size: str = "1024x1024"

    @property
    def database_path(self) -> Path:
        return self.data_dir / "ankiy.sqlite3"

    @property
    def voice_enabled(self) -> bool:
        return bool(self.elevenlabs_api_key and self.elevenlabs_voice_id)

    @property
    def images_enabled(self) -> bool:
        return bool(self.image_api_key and self.image_base_url and self.image_model)

    @classmethod
    def from_env(cls, env_file: str | Path | None = None) -> "Settings":
        # Never override environment values injected by a shell/service.
        load_dotenv(dotenv_path=env_file or PROJECT_ROOT / ".env", override=False)
        return cls(
            llm_base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1").rstrip("/"),
            llm_model=os.getenv("LLM_MODEL", "llama3.2"),
            llm_api_key=os.getenv("LLM_API_KEY") or None,
            owner_name=os.getenv("OWNER_NAME", "friend"),
            default_profile=os.getenv("DEFAULT_PROFILE", "luna"),
            data_dir=_as_path(os.getenv("ANKIY_DATA_DIR"), DEFAULT_DATA_DIR),
            profile_dir=_as_path(os.getenv("ANKIY_PROFILE_DIR"), DEFAULT_PROFILE_DIR),
            media_dir=_as_path(os.getenv("ANKIY_MEDIA_DIR"), DEFAULT_MEDIA_DIR),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN") or None,
            telegram_allowed_user_ids=_ids(os.getenv("TELEGRAM_ALLOWED_USER_IDS")),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY") or None,
            elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID") or None,
            elevenlabs_model=os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
            image_api_key=os.getenv("IMAGE_API_KEY") or None,
            image_base_url=os.getenv("IMAGE_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            image_model=os.getenv("IMAGE_MODEL", "gpt-image-2"),
            image_size=os.getenv("IMAGE_SIZE", "1024x1024"),
        )

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.media_dir.mkdir(parents=True, exist_ok=True)
