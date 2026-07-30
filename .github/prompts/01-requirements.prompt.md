---
mode: agent
description: "Phase 1 — Elicit requirements from the FLASK-001 user story and produce requirements.md"
tools:
  - read_file
  - write_file
  - run_in_terminal
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/03-security-standards.md
#file:.github/skills/generate-docs.md

## Constraints
- NEVER infer or guess — every gap must be marked `TBD — awaiting clarification`
- NEVER write to any file outside `docs/artifacts/FLASK-001/`
- NEVER advance pipeline state before the output file is written and reviewed
- Do NOT include PII, secrets, or references to internal systems not in the repository
- Output file must be at least 500 bytes

## Input
Read these files before writing anything:
- #file:docs/artifacts/FLASK-001/problem_spec.md
- #file:docs/artifacts/FLASK-001/design_spec.md

## Task

**Step 1 — Clarify**
Ask the developer these questions and wait for answers before proceeding:
1. Should the pipeline support output formats other than Markdown (HTML, Confluence wiki)?
2. Should "Not Specified" fields be omitted or included with the placeholder text?
3. Should the CLI accept `--repo-path` and `--output-path` arguments or use hardcoded defaults?
4. Is there a maximum file size limit for the generated technical profile?
5. Are there additional repository files beyond the six listed that should be scanned?

**Step 2 — Write `docs/artifacts/FLASK-001/requirements.md`**

## Output Specification

```markdown
# Requirements — FLASK-001: Automated Documentation Sync

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Feature | Automated Documentation Sync |
| Phase | 1 — Requirements |
| Status | Draft |
| Author | GitHub Copilot (requirements agent) |
| Date | YYYY-MM-DD |

## 1. User Story
(verbatim from problem_spec.md)

## 2. Clarifications Log
| # | Question | Answer |
|---|---|---|
| Q1 | ... | ... |

## 3. Functional Requirements
| ID | Requirement | Acceptance Criteria | Priority |
|---|---|---|---|
| FR-01 | ... | ... | Must Have |

## 4. Non-Functional Requirements
| ID | Category | Requirement | Metric |
|---|---|---|---|
| NFR-01 | Performance | ... | < X seconds |

## 5. Out of Scope
(explicit exclusion list)

## 6. Assumptions and Dependencies

## 7. Sign-Off Checklist
- [ ] All FRs traceable to the user story
- [ ] All NFRs have measurable metrics
- [ ] Out-of-scope items explicitly listed
- [ ] No inferred values — only repository evidence or developer answers
```

## Success Criteria
- File `docs/artifacts/FLASK-001/requirements.md` exists and is > 500 bytes
- All clarification questions answered and logged
- Every FR has an acceptance criterion
- Every NFR has a measurable metric

## On Failure
If the developer does not answer the clarifying questions within the session:
- Mark unanswered items as `TBD — awaiting developer input`
- Write the document with TBD placeholders
- Do NOT block pipeline progress — mark the TBDs as open items in section 6

## State Transition
When output file is written and verified: `python scripts/state_manager.py complete 1`
${input:additional_context:No additional context provided}
