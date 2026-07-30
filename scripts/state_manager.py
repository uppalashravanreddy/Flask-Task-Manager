"""SDLC state manager for the Flask Task Manager Agentic Pipeline.

Usage:
    python scripts/state_manager.py status
    python scripts/state_manager.py start <phase>
    python scripts/state_manager.py complete <phase>
    python scripts/state_manager.py fail <phase> "<reason>"
    python scripts/state_manager.py reset <phase>
    python scripts/state_manager.py task-complete <TASK-ID>
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / ".sdlc" / "state.json"
VALID_STATUSES = {"pending", "in_progress", "completed", "failed", "skipped"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load() -> dict:
    if not STATE_FILE.exists():
        print(f"ERROR: state file not found at {STATE_FILE}", file=sys.stderr)
        sys.exit(1)
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _save(state: dict) -> None:
    state["last_updated"] = _now()
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def cmd_status(state: dict) -> None:
    print(f"Project : {state['project']} — {state['feature']}")
    print(f"Current Phase: {state['current_phase']}")
    print()
    for num, phase in state["phases"].items():
        icon = {"pending": "[ ]", "in_progress": "[>]", "completed": "[x]",
                "failed": "[!]", "skipped": "[-]"}.get(phase["status"], "[?]")
        print(f"  {icon} Phase {num}: {phase['name']:25s} [{phase['status']}]")
    if state.get("tasks"):
        print()
        print("  Implementation Tasks:")
        for tid, task in state["tasks"].items():
            icon = "[x]" if task.get("completed") else "[ ]"
            print(f"    {icon} {tid}: {task.get('name', '')}")


def cmd_start(state: dict, phase: int) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    prev = str(phase - 1)
    if phase > 1 and state["phases"][prev]["status"] != "completed":
        print(f"ERROR: Phase {prev} must be completed before starting Phase {phase}",
              file=sys.stderr)
        sys.exit(1)
    state["phases"][key]["status"] = "in_progress"
    state["phases"][key]["started_at"] = _now()
    if state.get("started_at") is None:
        state["started_at"] = _now()
    state["current_phase"] = phase
    _save(state)
    print(f"Phase {phase} ({state['phases'][key]['name']}) started.")


def cmd_complete(state: dict, phase: int) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    output_file = state["phases"][key].get("output_file")
    if output_file:
        root = Path(__file__).parent.parent
        if not (root / output_file).exists():
            print(f"WARNING: output file {output_file} does not exist — completing anyway",
                  file=sys.stderr)
    state["phases"][key]["status"] = "completed"
    state["phases"][key]["completed_at"] = _now()
    next_phase = phase + 1
    if str(next_phase) in state["phases"]:
        state["current_phase"] = next_phase
    _save(state)
    print(f"Phase {phase} ({state['phases'][key]['name']}) completed.")
    if str(next_phase) in state["phases"]:
        next_name = state["phases"][str(next_phase)]["name"]
        print(f"Next: Phase {next_phase} — {next_name}")


def cmd_fail(state: dict, phase: int, reason: str) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    state["phases"][key]["status"] = "failed"
    state["phases"][key]["failure_reason"] = reason
    _save(state)
    print(f"Phase {phase} marked as FAILED: {reason}")


def cmd_reset(state: dict, phase: int) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    state["phases"][key]["status"] = "pending"
    state["phases"][key]["started_at"] = None
    state["phases"][key]["completed_at"] = None
    state["phases"][key].pop("failure_reason", None)
    state["current_phase"] = phase
    _save(state)
    print(f"Phase {phase} reset to pending.")


def cmd_task_complete(state: dict, task_id: str) -> None:
    if "tasks" not in state:
        state["tasks"] = {}
    if task_id not in state["tasks"]:
        state["tasks"][task_id] = {"name": task_id}
    state["tasks"][task_id]["completed"] = True
    state["tasks"][task_id]["completed_at"] = _now()
    _save(state)
    print(f"Task {task_id} marked complete.")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    state = _load()
    command = args[0]

    if command == "status":
        cmd_status(state)
    elif command == "start" and len(args) >= 2:
        cmd_start(state, int(args[1]))
    elif command == "complete" and len(args) >= 2:
        cmd_complete(state, int(args[1]))
    elif command == "fail" and len(args) >= 3:
        cmd_fail(state, int(args[1]), args[2])
    elif command == "reset" and len(args) >= 2:
        cmd_reset(state, int(args[1]))
    elif command == "task-complete" and len(args) >= 2:
        cmd_task_complete(state, args[1])
    else:
        print(f"ERROR: unknown command or missing arguments: {args}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
