---
mode: agent
description: "Phase 3 — Structured design review of architecture.md. Identify risks, gaps, and blocking issues before any code is written."
tools:
  - read_file
  - write_file
  - run_in_terminal
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/03-security-standards.md
#file:.github/instructions/04-failure-handling.md
#file:.github/skills/generate-docs.md

## Constraints
- Review every dimension below — never skip one; write "No issues identified" if clean
- Only Blocking findings may modify `architecture.md` — and only after developer approval
- Do NOT write to any file outside `docs/artifacts/FLASK-001/`
- All findings must be actionable — no vague "consider improving X"

## Input
Read before reviewing:
- #file:docs/artifacts/FLASK-001/architecture.md  ← subject of this review
- #file:docs/artifacts/FLASK-001/requirements.md  ← traceability reference

## Task
Review `architecture.md` against all 7 dimensions. For each Blocking finding: apply the correction to `architecture.md` after developer approval before advancing.

## Review Dimensions

| Dimension | Question |
|---|---|
| Requirements Traceability | Does every FR and NFR have a matching component or data flow step? |
| Security | Are secrets in `.env`? Are file write boundaries enforced? |
| Error Handling | Are scanner/extractor/page-creator failure modes addressed? |
| Scalability | Is the SQLite ADR appropriate? What breaks first as the repo grows? |
| Test Strategy | Are unit/integration test boundaries clearly defined? |
| Missing Components | Is `__init__.py` present? Is the CLI entry point correct? |
| Naming Consistency | Do architecture file names match actual code file names exactly? |

## Output Specification

```markdown
# Design Review — FLASK-001: Automated Documentation Sync

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Phase | 3 — Design Review |
| Status | Draft |
| Author | GitHub Copilot (design-review agent) |
| Architecture Version | (from architecture.md date field) |
| Date | YYYY-MM-DD |

## 1. Review Findings
| ID | Dimension | Severity | Finding | Recommendation | Resolved |
|---|---|---|---|---|---|
| DR-01 | Security | Blocking | ... | ... | Yes/No |

Severity: Blocking | Major | Minor | Suggestion

## 2. Agreed Design Decisions
(changes applied to architecture.md)

## 3. Open Items for Implementation
(items deferred to Phase 4 or Phase 5)

## 4. Sign-Off Checklist
- [ ] All Blocking findings resolved in architecture.md
- [ ] One finding per dimension logged
- [ ] architecture.md version updated if modified
```

## Success Criteria
- At least one finding logged per dimension
- All Blocking findings either resolved or noted as accepted risk
- `design-review.md` exists and is > 500 bytes

## On Failure
If `architecture.md` does not exist: stop and run Phase 2 first.
If no Blocking findings can be resolved after 2 attempts: escalate to developer and halt.

## State Transition
When complete: `python scripts/state_manager.py complete 3`
${input:review_focus:Review all dimensions equally}
