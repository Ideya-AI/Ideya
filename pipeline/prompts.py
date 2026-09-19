"""Prompt assembly: markdown per unit, shared blocks spliced in, slots filled by code.

`pipeline/prompts/<unit>.md` holds one unit's prompt. Two headings at column
zero split it: `# system` and `# prompt`; a file with neither is all prompt.

    {{> shared/style}}     splices pipeline/prompts/shared/style.md in place
    {{topic_title}}        a slot, filled from the keyword arguments

A slot left unfilled is an error, not an empty string, so a prompt can never
ship with a hole in it. Slot values that are not strings are rendered as
indented JSON, which is how a unit is handed structure.
"""

import json
import re

from .paths import PROMPTS

INCLUDE = re.compile(r"^\{\{>\s*([\w/.-]+)\s*\}\}\s*$", re.M)
SLOT = re.compile(r"\{\{\s*([\w.-]+)\s*\}\}")


def _read(name: str) -> str:
    path = PROMPTS / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"no prompt at {path}")
    return path.read_text(encoding="utf-8")


def _splice(text: str, depth=0) -> str:
    if depth > 3:
        raise RecursionError("prompt includes nest too deep")
    return INCLUDE.sub(lambda m: _splice(_read(m.group(1)), depth + 1).rstrip(), text)


def _render(value) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=1)


def _fill(text: str, slots: dict) -> str:
    missing = sorted({m.group(1) for m in SLOT.finditer(text)} - set(slots))
    if missing:
        raise KeyError(f"unfilled prompt slots: {', '.join(missing)}")
    return SLOT.sub(lambda m: _render(slots[m.group(1)]), text)


def split_sections(text: str) -> tuple[str, str]:
    """(system, prompt) from the `# system` / `# prompt` headings."""
    parts = re.split(r"^# (system|prompt)\s*$", text, flags=re.M)
    if len(parts) == 1:
        return "", text.strip()
    found = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}
    return found.get("system", ""), found.get("prompt", "")


def assemble(unit: str, **slots) -> tuple[str, str]:
    """(system_prompt, prompt) for a unit, fully spliced and filled."""
    text = _fill(_splice(_read(unit)), slots)
    return split_sections(text)
