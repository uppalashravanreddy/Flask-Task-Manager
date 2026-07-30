"""Agentic SDLC Orchestrator for Flask Task Manager -- FLASK-001.

Reads pipeline state, resumes from any interruption, drives all 8 phase
sub-agents in order, handles failures with retry, and generates HTML
reports after each phase.

Usage:
    python scripts/orchestrator.py              # show current phase + Copilot instructions
    python scripts/orchestrator.py --resume     # resume from interrupted phase
    python scripts/orchestrator.py --run-all    # walk through all phases (dry-run mode)
    python scripts/orchestrator.py --phase N    # show instructions for a specific phase
    python scripts/orchestrator.py --report     # generate pipeline HTML report
    python scripts/orchestrator.py --status     # show phase status table
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
STATE_FILE = ROOT / ".sdlc" / "state.json"
PHASE_OUTPUTS_ROOT = ROOT / ".sdlc" / "phase-outputs"

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


def _load_state() -> dict:
    if not STATE_FILE.exists():
        print("ERROR: state file not found -- run from repo root", file=sys.stderr)
        sys.exit(1)
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    state["last_updated"] = _now()
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _generate_html() -> None:
    try:
        subprocess.run(
            [sys.executable, "scripts/html_report.py"],
            cwd=ROOT, check=False,
        )
    except Exception:
        pass


def _find_resume_phase(state: dict) -> int:
    """Return the phase number to resume from.

    Rules:
    - If a phase is 'in_progress': resume there (re-run it).
    - Else find the first phase where status != 'completed'.
    - Never restart from Phase 1 if later phases show completed.
    """
    phases = state["phases"]
    for num_str in sorted(phases.keys(), key=int):
        phase = phases[num_str]
        if phase["status"] == "in_progress":
            return int(num_str)
    for num_str in sorted(phases.keys(), key=int):
        phase = phases[num_str]
        if phase["status"] != "completed":
            return int(num_str)
    return -1


def _phase_summary(state: dict) -> list[dict]:
    rows = []
    for num_str, phase in state["phases"].items():
        output = phase.get("output_file")
        output_exists = (ROOT / output).exists() if output else None
        rows.append({
            "num":          int(num_str),
            "name":         phase["name"],
            "status":       phase["status"],
            "agent":        phase["agent"],
            "output_file":  output,
            "output_exists": output_exists,
            "retry_count":  phase.get("retry_count", 0),
        })
    return sorted(rows, key=lambda r: r["num"])


def _print_status_table(state: dict) -> None:
    print()
    print(f"  Flask Task Manager -- Agentic SDLC Pipeline")
    print(f"  Project: {state['project']} | {state['feature']}")
    print()
    rows = _phase_summary(state)
    completed = sum(1 for r in rows if r["status"] == "completed")
    failed    = sum(1 for r in rows if r["status"] == "failed")
    print(f"  Progress: {completed}/8 phases completed | {failed} failed")
    print()
    current = state["current_phase"]
    for row in rows:
        icon = {
            "pending":     "[ ]",
            "in_progress": "[>]",
            "completed":   "[x]",
            "failed":      "[!]",
            "skipped":     "[-]",
        }.get(row["status"], "[?]")
        active  = " <== CURRENT" if row["num"] == current else ""
        retries = f" (retries:{row['retry_count']})" if row["retry_count"] > 0 else ""
        print(f"    {icon}  Phase {row['num']}: {row['name']:30s} [{row['status']}]{retries}{active}")
    print()


def _print_phase_instructions(phase_num: int, state: dict) -> None:
    key = str(phase_num)
    if key not in state["phases"]:
        print(f"ERROR: phase {phase_num} not found", file=sys.stderr)
        return
    phase = state["phases"][key]
    agent_name  = phase["agent"]
    prompt_file = phase["prompt"]
    agent_file  = f".github/agents/{phase_num:02d}-{agent_name}.md"

    print("=" * 70)
    print(f"  SDLC Phase {phase_num}: {phase['name']}")
    print("=" * 70)
    print()
    print(f"  Status      : {phase['status']}")
    print(f"  Retry Count : {phase.get('retry_count', 0)} / {MAX_RETRIES}")
    print(f"  Agent       : @{agent_name}")
    print(f"  Agent file  : {agent_file}")
    print(f"  Prompt file : {prompt_file}")
    if phase.get("output_file"):
        exists = (ROOT / phase["output_file"]).exists()
        marker = "EXISTS" if exists else "NOT YET CREATED"
        print(f"  Output file : {phase['output_file']}  [{marker}]")
    if phase.get("last_error"):
        print(f"  Last Error  : {phase['last_error']}")
    print()
    print("  GitHub Copilot Chat activation (VS Code):")
    print(f"    @{agent_name}  (or open prompt: {prompt_file})")
    print()
    print("  After the agent completes:")
    print(f"    python scripts/state_manager.py complete {phase_num}")
    print()


def _copy_phase_output(phase_num: int, state: dict) -> str | None:
    """Archive the canonical output to .sdlc/phase-outputs/<dir>/ with timestamp header."""
    phase = state["phases"][str(phase_num)]
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

    ts = _now().replace(":", "-")
    dest = dest_dir / f"{ts}_{src.name}"
    header = (
        f"<!-- phase-output-archive\n"
        f"     phase: {phase_num}\n"
        f"     name: {phase['name']}\n"
        f"     archived_at: {_now()}\n"
        f"     source: {out_file}\n"
        f"-->\n"
    )
    original = src.read_text(encoding="utf-8")
    dest.write_text(header + original, encoding="utf-8")
    return str(dest.relative_to(ROOT))


def _validate_output(phase_num: int, state: dict) -> bool:
    """Return True if the phase output file exists and is > 500 bytes."""
    out_file = state["phases"][str(phase_num)].get("output_file")
    if not out_file:
        return True
    p = ROOT / out_file
    return p.exists() and p.stat().st_size > 500


def cmd_resume(state: dict) -> None:
    resume_phase = _find_resume_phase(state)
    if resume_phase == -1:
        print("  All 8 phases are completed! Pipeline is done.")
        _generate_html()
        return

    print()
    print(f"  Resuming pipeline from Phase {resume_phase}.")
    print()

    phase_status = state["phases"][str(resume_phase)]["status"]
    if phase_status == "in_progress":
        print(f"  Phase {resume_phase} was interrupted (in_progress). Re-running.")
    elif phase_status == "failed":
        retry_count = state["phases"][str(resume_phase)].get("retry_count", 0)
        if retry_count >= MAX_RETRIES:
            print(f"  Phase {resume_phase} has exhausted {MAX_RETRIES} retries.")
            print(f"  Manual intervention required. Reset with:")
            print(f"    python scripts/state_manager.py reset {resume_phase}")
            return
        print(f"  Phase {resume_phase} previously failed. Retry {retry_count + 1}/{MAX_RETRIES}.")
        state["phases"][str(resume_phase)]["retry_count"] = retry_count + 1
        _save_state(state)

    _print_phase_instructions(resume_phase, state)

    if not _validate_output(resume_phase, state):
        print(f"  WARNING: output file for Phase {resume_phase} does not yet exist.")
        print(f"  Run the agent shown above, then:")
        print(f"    python scripts/state_manager.py complete {resume_phase}")
    else:
        archive_path = _copy_phase_output(resume_phase, state)
        if archive_path:
            print(f"  Output archived to: {archive_path}")
        _generate_html()


def cmd_show_current(state: dict) -> None:
    _print_status_table(state)
    resume_phase = _find_resume_phase(state)
    if resume_phase == -1:
        print("  All 8 phases completed!")
        return
    _print_phase_instructions(resume_phase, state)


def cmd_show_phase(phase_num: int, state: dict) -> None:
    _print_phase_instructions(phase_num, state)


def cmd_run_all(state: dict) -> None:
    print("  Dry-run mode -- showing all phase instructions in sequence")
    print()
    for phase_num in range(1, 9):
        _print_phase_instructions(phase_num, state)


def cmd_report(state: dict) -> None:
    _generate_html()
    out = ROOT / "reports" / "sdlc-summary.html"
    print(f"HTML report: {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume", action="store_true",
                        help="Resume pipeline from last interrupted phase")
    parser.add_argument("--run-all", action="store_true",
                        help="Show instructions for all 8 phases (dry-run)")
    parser.add_argument("--phase", type=int, metavar="N",
                        help="Show instructions for a specific phase")
    parser.add_argument("--report", action="store_true",
                        help="Generate the SDLC pipeline HTML report")
    parser.add_argument("--status", action="store_true",
                        help="Show phase status table only")
    args = parser.parse_args()

    state = _load_state()

    if args.report:
        cmd_report(state)
    elif args.status:
        _print_status_table(state)
    elif args.run_all:
        cmd_run_all(state)
    elif args.phase:
        cmd_show_phase(args.phase, state)
    elif args.resume:
        cmd_resume(state)
    else:
        cmd_show_current(state)


if __name__ == "__main__":
    main()
