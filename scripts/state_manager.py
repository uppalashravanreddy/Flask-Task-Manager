"""SDLC state manager for the Flask Task Manager Agentic Pipeline.

Usage:
    python scripts/state_manager.py status
    python scripts/state_manager.py start <phase>
    python scripts/state_manager.py complete <phase>
    python scripts/state_manager.py fail <phase> "<reason>"
    python scripts/state_manager.py retry <phase>
    python scripts/state_manager.py reset <phase>
    python scripts/state_manager.py task-complete <TASK-ID>
    python scripts/state_manager.py phase-output <phase>
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT       = Path(__file__).parent.parent
STATE_FILE = ROOT / ".sdlc" / "state.json"
PHASE_OUTPUTS_ROOT = ROOT / ".sdlc" / "phase-outputs"
VALID_STATUSES = {"pending", "in_progress", "completed", "failed", "skipped"}
MAX_RETRIES = 2

PHASE_ARCHIVE_DIRS = {
    1: "01-requirements",
    2: "02-architecture",
    3: "03-design-review",
    4: "04-impl-planning",
    5: "05-implementation",
    6: "06-code-review",
    7: "07-verification",
    8: "08-pr",
}


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


def _copy_phase_output(phase_num: int, state: dict) -> str | None:
    """Copy canonical output to .sdlc/phase-outputs/<dir>/ with metadata header."""
    phase    = state["phases"][str(phase_num)]
    out_file = phase.get("output_file")
    if not out_file:
        return None
    src = ROOT / out_file
    if not src.exists():
        return None

    archive_dir = PHASE_ARCHIVE_DIRS.get(phase_num)
    if not archive_dir:
        return None
    dest_dir = PHASE_OUTPUTS_ROOT / archive_dir
    dest_dir.mkdir(parents=True, exist_ok=True)

    ts   = _now().replace(":", "-")
    dest = dest_dir / f"{ts}_{src.name}"
    header = (
        f"<!-- phase-output-archive\n"
        f"     phase: {phase_num}\n"
        f"     name: {phase['name']}\n"
        f"     archived_at: {_now()}\n"
        f"     source: {out_file}\n"
        f"-->\n"
    )
    dest.write_text(header + src.read_text(encoding="utf-8"), encoding="utf-8")
    rel = str(dest.relative_to(ROOT))
    state["phases"][str(phase_num)]["phase_output_archive"] = rel
    return rel


def cmd_status(state: dict) -> None:
    print(f"Project      : {state['project']} -- {state['feature']}")
    print(f"Current Phase: {state['current_phase']}")
    print(f"Last Updated : {state.get('last_updated', 'never')}")
    print()
    for num_str, phase in sorted(state["phases"].items(), key=lambda x: int(x[0])):
        icon = {
            "pending":     "[ ]",
            "in_progress": "[>]",
            "completed":   "[x]",
            "failed":      "[!]",
            "skipped":     "[-]",
        }.get(phase["status"], "[?]")
        retries = f" (retry {phase.get('retry_count', 0)}/{MAX_RETRIES})" \
            if phase.get("retry_count", 0) > 0 else ""
        err_note = f"  ERROR: {phase['last_error']}" \
            if phase.get("last_error") else ""
        print(f"  {icon} Phase {num_str}: {phase['name']:25s} [{phase['status']}]{retries}{err_note}")
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
        print(
            f"ERROR: Phase {prev} must be completed before starting Phase {phase}",
            file=sys.stderr,
        )
        sys.exit(1)
    state["phases"][key]["status"]     = "in_progress"
    state["phases"][key]["started_at"] = _now()
    state["phases"][key]["last_error"] = None
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
    if output_file and not (ROOT / output_file).exists():
        print(
            f"WARNING: output file {output_file} does not exist -- completing anyway",
            file=sys.stderr,
        )

    archive_path = _copy_phase_output(phase, state)
    if archive_path:
        print(f"Output archived: {archive_path}")

    state["phases"][key]["status"]       = "completed"
    state["phases"][key]["completed_at"] = _now()
    state["phases"][key]["last_error"]   = None

    next_phase = phase + 1
    if str(next_phase) in state["phases"]:
        state["current_phase"] = next_phase
    _save(state)
    print(f"Phase {phase} ({state['phases'][key]['name']}) completed.")
    if str(next_phase) in state["phases"]:
        print(f"Next: Phase {next_phase} -- {state['phases'][str(next_phase)]['name']}")
    else:
        print("All 8 phases complete! Run: python scripts/html_report.py")


def cmd_fail(state: dict, phase: int, reason: str) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    state["phases"][key]["status"]     = "failed"
    state["phases"][key]["last_error"] = reason
    state["phases"][key].setdefault("retry_count", 0)
    _save(state)
    print(f"Phase {phase} marked FAILED: {reason}")
    retries_used = state["phases"][key]["retry_count"]
    if retries_used < MAX_RETRIES:
        print(f"  Retry available: python scripts/state_manager.py retry {phase}")
    else:
        print(f"  Max retries ({MAX_RETRIES}) reached -- manual intervention required.")


def cmd_retry(state: dict, phase: int) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    current_retries = state["phases"][key].get("retry_count", 0)
    if current_retries >= MAX_RETRIES:
        print(
            f"ERROR: Phase {phase} has exhausted {MAX_RETRIES} retries. "
            f"Use 'reset' to clear and start fresh.",
            file=sys.stderr,
        )
        sys.exit(1)
    state["phases"][key]["retry_count"] = current_retries + 1
    state["phases"][key]["status"]      = "in_progress"
    state["phases"][key]["started_at"]  = _now()
    state["current_phase"]              = phase
    _save(state)
    print(
        f"Phase {phase} retry {current_retries + 1}/{MAX_RETRIES}. "
        f"Re-activate the agent to run again."
    )


def cmd_reset(state: dict, phase: int) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    state["phases"][key]["status"]               = "pending"
    state["phases"][key]["started_at"]           = None
    state["phases"][key]["completed_at"]         = None
    state["phases"][key]["retry_count"]          = 0
    state["phases"][key]["last_error"]           = None
    state["phases"][key]["phase_output_archive"] = None
    state["current_phase"]                       = phase
    _save(state)
    print(f"Phase {phase} reset to pending (retry count cleared).")


def cmd_task_complete(state: dict, task_id: str) -> None:
    if "tasks" not in state:
        state["tasks"] = {}
    if task_id not in state["tasks"]:
        state["tasks"][task_id] = {"name": task_id}
    state["tasks"][task_id]["completed"]    = True
    state["tasks"][task_id]["completed_at"] = _now()
    _save(state)
    print(f"Task {task_id} marked complete.")


def cmd_phase_output(state: dict, phase: int) -> None:
    key = str(phase)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase} does not exist", file=sys.stderr)
        sys.exit(1)
    archive_path = _copy_phase_output(phase, state)
    if archive_path:
        _save(state)
        print(f"Phase {phase} output archived to: {archive_path}")
    else:
        print(f"WARNING: nothing to archive for Phase {phase} (no output file or file missing)")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    state   = _load()
    command = args[0]

    if command == "status":
        cmd_status(state)
    elif command == "start" and len(args) >= 2:
        cmd_start(state, int(args[1]))
    elif command == "complete" and len(args) >= 2:
        cmd_complete(state, int(args[1]))
    elif command == "fail" and len(args) >= 3:
        cmd_fail(state, int(args[1]), args[2])
    elif command == "retry" and len(args) >= 2:
        cmd_retry(state, int(args[1]))
    elif command == "reset" and len(args) >= 2:
        cmd_reset(state, int(args[1]))
    elif command == "task-complete" and len(args) >= 2:
        cmd_task_complete(state, args[1])
    elif command == "phase-output" and len(args) >= 2:
        cmd_phase_output(state, int(args[1]))
    else:
        print(f"ERROR: unknown command or missing arguments: {args}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
