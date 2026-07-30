"""Agentic SDLC Orchestrator for Flask Task Manager — FLASK-001.

The orchestrator coordinates the 8-phase SDLC pipeline by reading state,
determining the next phase, printing the correct Copilot agent invocation
instructions, and gating transitions on output-file existence.

Usage:
    python scripts/orchestrator.py              # show current phase + instructions
    python scripts/orchestrator.py --run-all    # walk through all phases (dry-run mode)
    python scripts/orchestrator.py --phase N    # show instructions for a specific phase
    python scripts/orchestrator.py --report     # generate pipeline report
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
STATE_FILE = ROOT / ".sdlc" / "state.json"

PHASE_AGENTS = {
    1: ("requirements",    "01-requirements.prompt.md"),
    2: ("architecture",    "02-architecture.prompt.md"),
    3: ("design-review",   "03-design-review.prompt.md"),
    4: ("impl-planning",   "04-impl-plan.prompt.md"),
    5: ("implementation",  "05-implementation.prompt.md"),
    6: ("code-review",     "06-code-review.prompt.md"),
    7: ("verification",    "07-verification.prompt.md"),
    8: ("pr",              "08-pr-description.prompt.md"),
}


def _load_state() -> dict:
    if not STATE_FILE.exists():
        print(f"ERROR: state file not found — run from repo root", file=sys.stderr)
        sys.exit(1)
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _phase_summary(state: dict) -> list[dict]:
    rows = []
    for num, phase in state["phases"].items():
        output = phase.get("output_file")
        output_exists = (ROOT / output).exists() if output else None
        rows.append({
            "num": int(num),
            "name": phase["name"],
            "status": phase["status"],
            "agent": phase["agent"],
            "output_file": output,
            "output_exists": output_exists,
        })
    return sorted(rows, key=lambda r: r["num"])


def _print_phase_instructions(phase_num: int, state: dict) -> None:
    key = str(phase_num)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase_num} not found", file=sys.stderr)
        return
    phase = state["phases"][key]
    agent_name = phase["agent"]
    prompt_file = phase["prompt"]

    print("=" * 70)
    print(f"  SDLC Phase {phase_num}: {phase['name']}")
    print("=" * 70)
    print()
    print(f"  Status      : {phase['status']}")
    print(f"  Agent       : @{agent_name}")
    print(f"  Prompt file : {prompt_file}")
    if phase.get("output_file"):
        exists = (ROOT / phase["output_file"]).exists()
        marker = "EXISTS" if exists else "NOT YET CREATED"
        print(f"  Output file : {phase['output_file']}  [{marker}]")
    print()
    print("  To activate in GitHub Copilot Chat (VS Code):")
    print(f"    1. Open Copilot Chat panel")
    print(f"    2. Select agent: @{agent_name}")
    print(f"    3. Or use the prompt: @workspace /runPrompt {prompt_file}")
    print()
    print("  To advance state after the agent completes:")
    print(f"    python scripts/state_manager.py complete {phase_num}")
    print()


def cmd_show_current(state: dict) -> None:
    current = state["current_phase"]
    print()
    print(f"  Flask Task Manager — Agentic SDLC Pipeline")
    print(f"  Project: {state['project']} | {state['feature']}")
    print()

    rows = _phase_summary(state)
    completed = sum(1 for r in rows if r["status"] == "completed")
    print(f"  Progress: {completed}/8 phases completed")
    print()
    for row in rows:
        icon = {"pending": "[ ]", "in_progress": "[>]", "completed": "[x]",
                "failed": "[!]", "skipped": "[-]"}.get(row["status"], "[?]")
        active = " <== CURRENT" if row["num"] == current else ""
        print(f"    {icon}  Phase {row['num']}: {row['name']:30s} [{row['status']}]{active}")
    print()

    current_status = state["phases"][str(current)]["status"]
    if current_status in ("pending", "in_progress"):
        _print_phase_instructions(current, state)
    elif current_status == "completed":
        next_phase = current + 1
        if str(next_phase) in state["phases"]:
            print(f"  Phase {current} is complete. Ready for Phase {next_phase}.")
            _print_phase_instructions(next_phase, state)
        else:
            print("  All 8 phases completed! Run: python scripts/reporter.py")
    elif current_status == "failed":
        reason = state["phases"][str(current)].get("failure_reason", "unknown")
        print(f"  Phase {current} FAILED: {reason}")
        print(f"  Fix the issue, then: python scripts/state_manager.py reset {current}")


def cmd_show_phase(phase_num: int, state: dict) -> None:
    _print_phase_instructions(phase_num, state)


def cmd_run_all(state: dict) -> None:
    print("  Dry-run mode — showing all phase instructions in order")
    print()
    for phase_num in range(1, 9):
        _print_phase_instructions(phase_num, state)


def cmd_report(state: dict) -> None:
    from scripts.reporter import generate_report  # type: ignore
    report_path = generate_report(state)
    print(f"Report generated: {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-all", action="store_true",
                        help="Show instructions for all 8 phases")
    parser.add_argument("--phase", type=int, metavar="N",
                        help="Show instructions for a specific phase")
    parser.add_argument("--report", action="store_true",
                        help="Generate the SDLC pipeline report")
    args = parser.parse_args()

    state = _load_state()

    if args.report:
        cmd_report(state)
    elif args.run_all:
        cmd_run_all(state)
    elif args.phase:
        cmd_show_phase(args.phase, state)
    else:
        cmd_show_current(state)


if __name__ == "__main__":
    main()
