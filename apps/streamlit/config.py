"""
Centralized configuration — all API keys and settings loaded via dotenv.
Import get_settings() wherever you need config values.
"""

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).resolve().parent.parent.parent
_env_path = _project_root / ".env"
load_dotenv(_env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # LLM APIs
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    minimax_api_key: str = os.getenv("MINIMAX_API_KEY", "")

    # Web Search
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")

    # Model Selection
    model_selection_strategy: str = os.getenv("MODEL_SELECTION_STRATEGY", "auto")

    # Paths
    exports_dir: Path = Path(os.getenv("EXPORTS_DIR", "exports"))
    templates_dir: Path = Path(os.getenv("TEMPLATES_DIR", "templates"))

    @property
    def has_openai(self) -> bool:
        return bool(self.openai_api_key and not self.openai_api_key.startswith("sk-your"))

    @property
    def has_minimax(self) -> bool:
        return bool(self.minimax_api_key and self.minimax_api_key != "your-minimax-key-here")

    @property
    def has_tavily(self) -> bool:
        return bool(self.tavily_api_key and not self.tavily_api_key.startswith("tvly-your"))

    def get_model_for_task(self, complexity: str = "simple") -> str:
        """Return model name based on task complexity and strategy."""
        strategy = self.model_selection_strategy

        if strategy == "simple":
            return "gpt-4o-mini"
        elif strategy == "complex":
            return "gpt-4o-mini"
        else:  # auto
            # Both simple and complex use gpt-4o-mini (best cost-benefit)
            return "gpt-4o-mini"


@lru_cache()
def get_settings() -> Settings:
    """Cached singleton — use this everywhere."""
    return Settings()
