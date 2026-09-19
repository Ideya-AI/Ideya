"""Where things are. One place, so no module re-derives the repo root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "research" / "topics"
PROMPTS = Path(__file__).resolve().parent / "prompts"
