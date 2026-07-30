"""Pre-write guard hook — called by Claude Code before any Write tool call.

Reads tool input JSON from stdin. Blocks writes to protected files by exiting
with code 2 (Claude Code's "block with message" exit code).

Protected paths (require correct tool/script instead):
  .sdlc/state.json         → use scripts/state_manager.py
  .github/agents/*.md      → manual review required
  .github/instructions/*.md → manual review required
  .github/prompts/*.prompt.md → manual review required
"""
from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

PROTECTED_EXACT = {
    ".sdlc/state.json",
}

PROTECTED_PREFIXES = [
    ".github/agents/",
    ".github/instructions/",
    ".github/prompts/",
]

BYPASS_ENV = "SDLC_HOOK_BYPASS"


def _normalise(path: str) -> str:
    """Normalise path to forward-slash relative form."""
    try:
        p = Path(path)
        # Try to make relative to repo root (heuristic: find .git ancestor)
        for parent in [p, *p.parents]:
            if (parent / ".git").exists():
                return str(p.relative_to(parent)).replace("\\", "/")
    except Exception:
        pass
    return path.replace("\\", "/")


def main() -> None:
    import os
    if os.environ.get(BYPASS_ENV):
        sys.exit(0)

    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    try:
        data = json.loads(raw)
        file_path = data.get("tool_input", {}).get("file_path", "")
    except (json.JSONDecodeError, AttributeError):
        sys.exit(0)

    normalised = _normalise(file_path)

    if normalised in PROTECTED_EXACT:
        print(
            f"BLOCKED: '{normalised}' is a protected file.\n"
            f"Use 'python scripts/state_manager.py <command>' to modify it.",
            flush=True,
        )
        sys.exit(2)

    for prefix in PROTECTED_PREFIXES:
        if normalised.startswith(prefix):
            print(
                f"BLOCKED: '{normalised}' is in a protected directory ({prefix}).\n"
                f"These files require a manual review before modification.",
                flush=True,
            )
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
