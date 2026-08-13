"""Create Framework — bootstrap a new Agentic SDLC run.

Initialises state.json, creates phase-output directories, and prints the
Copilot command to kick off Phase 1.  Run this whenever starting a new
feature or project ticket.

Usage:
    python scripts/create_sdlc_run.py --project FLASK-002 --feature "User Auth"
    python scripts/create_sdlc_run.py --reset          # re-initialise current run
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
STATE_FILE = ROOT / ".sdlc" / "state.json"
PHASE_OUTPUTS_ROOT = ROOT / ".sdlc" / "phase-outputs"

PHASES = {
    "1":  {"name": "Requirements",          "output_file": None,                               "agent": "requirements",    "prompt": ".github/prompts/01-requirements.prompt.md"},
    "2":  {"name": "Architecture",          "output_file": None,                               "agent": "architecture",    "prompt": ".github/prompts/02-architecture.prompt.md"},
    "3":  {"name": "Design Review",         "output_file": None,                               "agent": "design-review",   "prompt": ".github/prompts/03-design-review.prompt.md"},
    "4":  {"name": "Implementation Planning","output_file": None,                               "agent": "impl-planning",   "prompt": ".github/prompts/04-impl-plan.prompt.md"},
    "5":  {"name": "Implementation",        "output_file": None,                               "agent": "implementation",  "prompt": ".github/prompts/05-implementation.prompt.md"},
    "6":  {"name": "Code Review",           "output_file": None,                               "agent": "code-review",     "prompt": ".github/prompts/06-code-review.prompt.md"},
    "7":  {"name": "Verification",          "output_file": None,                               "agent": "verification",    "prompt": ".github/prompts/07-verification.prompt.md"},
    "8":  {"name": "Pull Request",          "output_file": ".sdlc/pr-description.md",          "agent": "pr",              "prompt": ".github/prompts/08-pr-description.prompt.md"},
}

PHASE_DIRS = {
    "1": "01-requirements",
    "2": "02-architecture",
    "3": "03-design-review",
    "4": "04-impl-planning",
    "5": "05-implementation",
    "6": "06-code-review",
    "7": "07-verification",
    "8": "08-pr",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _build_state(project: str, feature: str) -> dict:
    artifact_base = f"docs/artifacts/{project}"
    output_map = {
        "1": f"{artifact_base}/requirements.md",
        "2": f"{artifact_base}/architecture.md",
        "3": f"{artifact_base}/design-review.md",
        "4": f"{artifact_base}/impl-plan.md",
        "5": None,
        "6": f"{artifact_base}/review_report.md",
        "7": f"{artifact_base}/verification_report.md",
        "8": ".sdlc/pr-description.md",
    }
    phases: dict = {}
    for num, meta in PHASES.items():
        phases[num] = {
            "name": meta["name"],
            "status": "pending",
            "started_at": None,
            "completed_at": None,
            "retry_count": 0,
            "last_error": None,
            "phase_output_archive": None,
            "output_file": output_map[num],
            "agent": meta["agent"],
            "prompt": meta["prompt"],
        }
    return {
        "project": project,
        "feature": feature,
        "repository": ROOT.name,
        "started_at": _now(),
        "current_phase": 1,
        "phases": phases,
        "tasks": {},
        "last_updated": _now(),
    }


def _create_phase_dirs() -> None:
    for d in PHASE_DIRS.values():
        (PHASE_OUTPUTS_ROOT / d).mkdir(parents=True, exist_ok=True)


def _create_artifact_dirs(project: str) -> None:
    (ROOT / "docs" / "artifacts" / project).mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap a new Agentic SDLC run.")
    parser.add_argument("--project", default="FLASK-001", help="Jira project key, e.g. FLASK-002")
    parser.add_argument("--feature", default="Automated Documentation Sync", help="Feature description")
    parser.add_argument("--reset", action="store_true", help="Re-initialise without prompting (overwrites state)")
    args = parser.parse_args()

    if STATE_FILE.exists() and not args.reset:
        existing = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        print(f"State file already exists for project {existing['project']} (phase {existing['current_phase']}).")
        ans = input("Overwrite? [y/N] ").strip().lower()
        if ans != "y":
            print("Aborted — existing run preserved.")
            sys.exit(0)

    state = _build_state(args.project, args.feature)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

    _create_phase_dirs()
    _create_artifact_dirs(args.project)

    print(f"\nSDLC run created for {args.project} — {args.feature}")
    print(f"State: {STATE_FILE.relative_to(ROOT)}")
    print(f"Artifacts will go to: docs/artifacts/{args.project}/\n")
    print("To start the pipeline, open GitHub Copilot Chat and run:")
    print("  @orchestrator  (or invoke the orchestrator agent)")
    print("\nOr drive phases manually:")
    print("  python scripts/orchestrator.py --status")
    print("  python scripts/orchestrator.py --phase 1\n")


if __name__ == "__main__":
    main()
