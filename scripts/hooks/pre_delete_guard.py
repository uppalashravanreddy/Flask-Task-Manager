"""Pre-delete guard hook — called by Claude Code before Bash tool calls.

Scans the command string for rm/del/Remove-Item operations targeting protected
paths. Blocks the command by exiting with code 2.

Protected paths (cannot be deleted):
  .sdlc/state.json
  .sdlc/phase-outputs/**
  .github/agents/*.md
  .github/instructions/*.md
  .github/prompts/*.prompt.md
  .github/skills/*.md
  .github/copilot-instructions.md
  docs/artifacts/FLASK-001/*.md
  src/doc_sync/*.py
  tests/**/*.py
"""
from __future__ import annotations

import json
import re
import sys

PROTECTED_PATTERNS = [
    r"\.sdlc[\\/]state\.json",
    r"\.sdlc[\\/]phase-outputs",
    r"\.github[\\/]agents[\\/]",
    r"\.github[\\/]instructions[\\/]",
    r"\.github[\\/]prompts[\\/]",
    r"\.github[\\/]skills[\\/]",
    r"\.github[\\/]copilot-instructions",
    r"docs[\\/]artifacts[\\/]FLASK-001",
    r"src[\\/]doc_sync[\\/]",
    r"tests[\\/]",
]

DELETE_COMMANDS = re.compile(
    r"\b(rm\b|del\b|Remove-Item\b|rmdir\b|rd\b)",
    re.IGNORECASE,
)


def _is_delete_command(cmd: str) -> bool:
    return bool(DELETE_COMMANDS.search(cmd))


def _targets_protected(cmd: str) -> str | None:
    for pattern in PROTECTED_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return pattern
    return None


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    try:
        data = json.loads(raw)
        command = data.get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError):
        sys.exit(0)

    if not _is_delete_command(command):
        sys.exit(0)

    matched = _targets_protected(command)
    if matched:
        print(
            f"BLOCKED: Command targets a protected path (matches: {matched}).\n"
            f"Protected files cannot be deleted. Review the SDLC pipeline before "
            f"removing any outputs, agent definitions, or state files.\n"
            f"Command was: {command[:120]}",
            flush=True,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
