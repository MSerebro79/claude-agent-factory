import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")

MODEL = "claude-sonnet-4-6"
MAX_SEARCH_RESULTS = 3
MAX_TEXT_CHARS = 3000  # trim page text before sending to LLM

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.md"
    text = path.read_text(encoding="utf-8")
    # Extract content after the last "## System" or "## User message template" marker
    # Return the full file — main.py handles extraction
    return text


def validate_env() -> None:
    missing = []
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not EXA_API_KEY:
        missing.append("EXA_API_KEY")
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
