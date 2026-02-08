import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()
load_dotenv("backend/.env")


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    def __init__(self) -> None:
        self.xai_api_key = os.getenv("XAI_API_KEY", "")
        self.xai_base_url = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
        self.xai_model = os.getenv("XAI_MODEL", "grok-2-latest")
        self.frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
        self.extractor_url = os.getenv("EXTRACTOR_URL", "http://localhost:8001")
        self.mock_llm = _to_bool(os.getenv("MOCK_LLM", "false"))
        self.max_context_chars = int(os.getenv("MAX_CONTEXT_CHARS", "12000"))
        self.max_extract_chars = int(os.getenv("MAX_EXTRACT_CHARS", "12000"))


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
