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
| `.claude/agents/orchestrator.md` | — | Drives Phases 1–8, manages state.json, handles phase returns |
| `.claude/agents/01-requirements.md` | 1 | Reads JIRA ticket → asks questions → writes requirements.md |
| `.claude/agents/02-architecture.md` | 2 | Reads requirements + codebase → writes architecture.md |
| `.claude/agents/03-design-review.md` | 3 | Reviews architecture → writes design-review.md |
| `.claude/agents/04-impl-planning.md` | 4 | Breaks architecture into tasks → writes impl-plan.md |
| `.claude/agents/05-implementation.md` | 5 | Executes impl-plan → writes/modifies all source files |
| `.claude/agents/06-code-review.md` | 6 | Reviews code against checklist → writes review_report.md |
| `.claude/agents/07a-test-strategy.md` | 7.1 | Designs test approach → writes test-strategy.md → Confluence |
| `.claude/agents/07b-test-plan.md` | 7.2 | Writes test plan with entry/exit criteria → Confluence |
| `.claude/agents/07c-test-cases.md` | 7.3 | Writes test cases, deduplicates → Confluence + JIRA comment |
| `.claude/agents/07d-test-execution.md` | 7.4 | Runs pytest + Playwright → HTML reports → Confluence + JIRA |
| `.claude/agents/07-verification.md` | 7.5 | Maps ACs to results → verification_report.md → Confluence + JIRA |
| `.claude/agents/08-pr.md` | 8 | Commits artifacts → creates GitHub PR |

## Phase 7 — Testing sub-pipeline

Phase 7 runs as 5 sequential sub-phases, each producing a real artifact and updating Confluence:

| Sub-phase | Agent | Output | Confluence |
|-----------|-------|--------|------------|
| 7.1 Test Strategy | `07a-test-strategy` | `test-strategy.md` | Created |
| 7.2 Test Plan | `07b-test-plan` | `test-plan.md` | Created |
| 7.3 Test Cases | `07c-test-cases` | `test-cases.md` + new test files | Created + JIRA comment |
| 7.4 Test Execution | `07d-test-execution` | HTML reports in `reports/<TICKET-ID>/` | Updated + JIRA comment |
| 7.5 Verification | `07-verification` | `verification_report.md` | Updated + JIRA transition |

### HTML reports
```bash
python scripts/generate_html_report.py --ticket <TICKET-ID>
# writes: reports/<TICKET-ID>/index.html
```
Opens as a standalone page with links to unit / integration / E2E sub-reports.

### Test case deduplication
Phase 7.3 always checks existing tests before writing new ones.
Use skill: `review-test-cases` to review for duplicates.

---

## MCP servers

| Server | Package | Handles |
|--------|---------|---------|
| `atlassian` | `@sooperset/mcp-atlassian` | JIRA (stories, comments, transitions) + Confluence (pages) |
| `playwright` | `@playwright/mcp` | Browser navigation + visual verification |

Credentials live in `.env` (not committed). Both servers start automatically in VS Code.

Manual start:
```powershell
.\scripts\start-jira-mcp.ps1    # starts atlassian MCP
npx @playwright/mcp@latest      # starts playwright MCP
```

## State management

Pipeline state is tracked in `.sdlc/state.json` (auto-created, phase sub-keys: `7.1` through `7.5`).
Phase artifacts are written to `docs/artifacts/<TICKET-ID>/`.
HTML reports are written to `reports/<TICKET-ID>/`.
Confluence URLs are stored in `state.json` per phase.

## Skills reference

| Skill | When to use |
|-------|-------------|
| `analyze-codebase` | Before Phase 2 and Phase 5 |
| `write-test-cases` | Phase 7.3 — designing new test cases |
| `review-test-cases` | Phase 7.3 — deduplication + quality check |
| `confluence-sync` | Phases 7.1–7.5 — push/update Confluence pages |
| `playwright-execution` | Phase 7.4 — run E2E tests or visual verification |
| `html-reports` | Phase 7.4 — generate combined index.html |
| `git-operations` | All phases — commit artifacts, create PR |
| `run-tests` | Phases 5 and 7.4 — run test suite |
| `sdlc-state` | All phases — read/write state.json |
| `jira-fetch` | Phase 0 — fetch and rank the backlog |

## Feedback loop

If any phase is blocked, the orchestrator returns to the earliest affected phase:
- Requirements gap → Phase 1
- Architecture flaw → Phase 2/3
- Code bug → Phase 5
- Test failure (unit/integration) → Phase 5
- E2E infrastructure failure → fix and retry Phase 7.4
- Regression found in Phase 7.5 → Phase 5
