# Skill: SDLC State Management

Use this skill whenever you need to read, update, or query the SDLC pipeline state.

## State File Location

`.sdlc/state.json` — the single source of truth for pipeline progress.

## Reading State

```bash
python scripts/state_manager.py status
```

Or read the file directly:
```bash
cat .sdlc/state.json
```

## State Schema

```json
{
  "project": "FLASK-001",
  "feature": "Automated Documentation Sync",
  "started_at": "YYYY-MM-DDTHH:MM:SSZ",
  "current_phase": 1,
  "phases": {
    "1": {
      "name": "Requirements",
      "status": "pending|in_progress|completed|failed",
      "started_at": null,
      "completed_at": null,
      "retry_count": 0,
      "last_error": null,
      "phase_output_archive": null,
      "output_file": "docs/artifacts/FLASK-001/requirements.md",
      "agent": "requirements",
      "prompt": ".github/prompts/01-requirements.prompt.md"
    }
  },
  "tasks": {},
  "last_updated": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## State Transition Commands

| Action | Command |
|---|---|
| Start a phase | `python scripts/state_manager.py start <phase_number>` |
| Complete a phase | `python scripts/state_manager.py complete <phase_number>` |
| Fail a phase | `python scripts/state_manager.py fail <phase_number> "<reason>"` |
| Retry a failed phase | `python scripts/state_manager.py retry <phase_number>` |
| Archive phase output | `python scripts/state_manager.py phase-output <phase_number>` |
| Complete an impl task | `python scripts/state_manager.py task-complete <TASK-ID>` |
| Show current status | `python scripts/state_manager.py status` |
| Reset a phase | `python scripts/state_manager.py reset <phase_number>` |

## Resume After Interruption

If the pipeline was interrupted, resume from the correct phase:
```bash
python scripts/orchestrator.py --resume
```

This reads `state.json`, finds the first phase where `status != "completed"`, and prints instructions for that phase. It NEVER restarts from Phase 1 if later phases show completed.

## Phase Output Archiving

When a phase is completed, `state_manager.py complete N` automatically:
1. Copies the output file to `.sdlc/phase-outputs/<phase-dir>/`
2. Prepends a metadata header with timestamp, phase number, and source path
3. Records the archive path in `state.json` under `phase_output_archive`

Manual copy:
```bash
python scripts/state_manager.py phase-output <phase_number>
```

## Status Values

| Status | Meaning |
|---|---|
| `pending` | Not yet started |
| `in_progress` | Currently active |
| `completed` | Successfully finished |
| `failed` | Stopped due to an error or failing gate |
| `skipped` | Intentionally skipped (pre-existing output) |

## Rules

- Never edit `.sdlc/state.json` directly — always use `state_manager.py`.
- A phase can only be marked `completed` if its output file exists.
- A phase cannot start if the previous phase is not `completed`.
- The orchestrator reads state to determine which phase to run next.
