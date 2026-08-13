# Skill: sdlc-state

## Purpose
Read and update `.sdlc/state.json` to track the current phase of the pipeline.

## State file location
`.sdlc/state.json` — created automatically if missing.

## Schema
```json
{
  "ticket_id": "FLASK-002",
  "story": "Short human-readable story title",
  "branch": "feature/FLASK-002-task-priority",
  "current_phase": 1,
  "phases": {
    "1": "complete",
    "2": "complete",
    "3": "complete",
    "4": "in_progress",
    "5": "pending",
    "6": "pending",
    "7": "pending",
    "8": "pending"
  },
  "feedback_loops": [
    {
      "discovered_in": 3,
      "returned_to": 2,
      "reason": "Bootstrap badge class mismatch found in design review"
    }
  ]
}
```

## Operations

### Initialize (Phase 1 start)
```python
import json, os
state = {
    "ticket_id": ticket_id,
    "story": story_title,
    "branch": branch_name,
    "current_phase": 1,
    "phases": {str(i): "pending" for i in range(1, 9)},
    "feedback_loops": []
}
os.makedirs(".sdlc", exist_ok=True)
with open(".sdlc/state.json", "w") as f:
    json.dump(state, f, indent=2)
```

### Mark phase complete
```python
state["phases"][str(phase_num)] = "complete"
state["current_phase"] = phase_num + 1
```

### Record a feedback loop
```python
state["feedback_loops"].append({
    "discovered_in": discovered_phase,
    "returned_to": return_phase,
    "reason": reason_string
})
state["current_phase"] = return_phase
state["phases"][str(return_phase)] = "in_progress"
```

## When to use
- Orchestrator agent reads state.json at startup to resume an interrupted pipeline.
- Each phase agent reads state.json to confirm it is the active phase before proceeding.
- Each phase agent writes state.json after completing its work.
