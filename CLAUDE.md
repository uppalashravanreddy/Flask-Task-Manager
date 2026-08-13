# Flask Task Manager — Claude Code SDLC Pipeline

## How to start a new feature

### Step 1 — Run the prioritization agent
```
Use agent: prioritize
```
The agent fetches all stories from JIRA (KAN project), scores and ranks them,
and presents a prioritized list. Pick one story to work on.

### Step 2 — Orchestrator runs the full pipeline
```
Use agent: orchestrator
Input: the selected story from Step 1
```
The orchestrator drives all 8 phases sequentially and handles feedback loops automatically.

---

## Agent map

| Agent file | Phase | What it does |
|---|---|---|
| `.claude/agents/00-prioritize.md` | 0 | Fetches JIRA stories, ranks them, waits for user pick |
| `.claude/agents/orchestrator.md` | — | Drives Phases 1–8, manages state, handles phase returns |
| `.claude/agents/01-requirements.md` | 1 | Reads JIRA ticket → asks questions → writes requirements.md |
| `.claude/agents/02-architecture.md` | 2 | Reads requirements + codebase → writes architecture.md |
| `.claude/agents/03-design-review.md` | 3 | Reviews architecture → writes design-review.md |
| `.claude/agents/04-impl-planning.md` | 4 | Breaks architecture into tasks → writes impl-plan.md |
| `.claude/agents/05-implementation.md` | 5 | Executes impl-plan → writes/modifies all source files |
| `.claude/agents/06-code-review.md` | 6 | Reviews code against checklist → writes review_report.md |
| `.claude/agents/07-verification.md` | 7 | Runs tests → writes verification_report.md |
| `.claude/agents/08-pr.md` | 8 | Commits artifacts → creates GitHub PR |

## State management

Pipeline state is tracked in `.sdlc/state.json`.
Phase artifacts are written to `docs/artifacts/<TICKET-ID>/`.

## JIRA integration

Credentials live in `.env` (not committed). The JIRA MCP server is configured
in `.vscode/mcp.json` using `@sooperset/mcp-atlassian`.

Fetch a ticket manually:
```bash
python scripts/jira_fetch.py        # ranked backlog
```

## Feedback loop

If any phase is blocked, the orchestrator returns to the earliest affected phase:
- Requirements gap → Phase 1
- Architecture flaw → Phase 2/3
- Code bug → Phase 5
- Test failure → Phase 5
