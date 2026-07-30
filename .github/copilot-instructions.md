# GitHub Copilot Instructions — Flask Task Manager

## What This Repository Is
Flask Task Manager is a CRUD web application (Flask + SQLAlchemy + Flask-WTF) with an Automated Documentation Sync pipeline (FLASK-001) and a full Agentic SDLC pipeline managed through GitHub Copilot agents.

## Pipeline Entry Point
- State file: `.sdlc/state.json` — always read this first
- Orchestrator: `python scripts/orchestrator.py` — shows current phase and Copilot invocation
- Resume: `python scripts/orchestrator.py --resume` — resumes from the interrupted phase
- HTML dashboard: `reports/sdlc-summary.html` — visual pipeline status

## Instruction Files (load before any phase)
| File | Purpose |
|---|---|
| `#file:.github/instructions/00-project-context.md` | Project facts, repo map, known bugs |
| `#file:.github/instructions/01-coding-standards.md` | Python code rules |
| `#file:.github/instructions/02-testing-standards.md` | Test writing and running rules |
| `#file:.github/instructions/03-security-standards.md` | Secrets, protected files, output rules |
| `#file:.github/instructions/04-failure-handling.md` | Retry policy, resume logic, escalation |

## Available Agents
`@orchestrator` — master agent, runs the whole pipeline. All other agents are invoked by it.

Sub-agents (also invokable directly): `@requirements`, `@architecture`, `@design-review`, `@impl-planning`, `@implementation`, `@code-review`, `@verification`, `@pr`

## Skills
`#file:.github/skills/analyze-codebase.md` | `#file:.github/skills/generate-docs.md` | `#file:.github/skills/run-tests.md` | `#file:.github/skills/git-operations.md` | `#file:.github/skills/sdlc-state.md`
