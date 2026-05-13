"""
Prompt Loader — Loads agent prompts from markdown files in /prompt directory.
Prompts are never hardcoded in the code — always loaded from .md files.
"""

from pathlib import Path
from functools import lru_cache


# Project root (3 levels up from this file)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_PROMPT_DIR = _PROJECT_ROOT / "prompt"


@lru_cache(maxsize=10)
def load_prompt(prompt_name: str) -> str:
    """
    Load a prompt from the /prompt directory.

    Args:
        prompt_name: Name of the prompt file without extension.
                     E.g., "structure_agent" loads "prompt/structure_agent.md"

    Returns:
        Content of the prompt file as string.

    Raises:
        FileNotFoundError if prompt file doesn't exist.
    """
    prompt_path = _PROMPT_DIR / f"{prompt_name}.md"

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}\n"
            f"Available prompts: {list_prompts()}"
        )

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def list_prompts() -> list[str]:
    """List all available prompt files."""
    if not _PROMPT_DIR.exists():
        return []
    return [p.stem for p in _PROMPT_DIR.glob("*.md")]


def get_prompt_dir() -> Path:
    """Return the prompt directory path."""
    return _PROMPT_DIR
