import json
import os
from dataclasses import dataclass, asdict


def _settings_path() -> str:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, "user_settings.json")


@dataclass
class AppSettings:
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"


def load_settings() -> AppSettings:
    path = _settings_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f) or {}
        return AppSettings(
            gemini_api_key=str(raw.get("gemini_api_key", "") or ""),
            gemini_model=str(raw.get("gemini_model", "gemini-1.5-flash") or "gemini-1.5-flash"),
        )
    except FileNotFoundError:
        return AppSettings()
    except Exception:
        return AppSettings()


def save_settings(settings: AppSettings) -> None:
    path = _settings_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, ensure_ascii=False, indent=2)

