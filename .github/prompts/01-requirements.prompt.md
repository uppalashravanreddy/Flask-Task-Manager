---
mode: agent
description: "Phase 1 — Fetch the JIRA user story via MCP, elicit clarifications, and produce requirements.md"
tools:
  - read_file
  - write_file
  - run_in_terminal
  - jira
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/03-security-standards.md
#file:.github/skills/fetch-jira-story.md
#file:.github/skills/generate-docs.md

## Inputs
- `${input:jira_issue_key}` — JIRA ticket key to use as Phase 1 input (e.g. `EPMCDMETST-56919`)
- `${input:additional_context:No additional context provided}`

## Constraints
- NEVER infer or guess — every gap must be marked `TBD — awaiting clarification`
- NEVER write to any file outside `docs/artifacts/${input:jira_issue_key}/`
- NEVER advance pipeline state before the output file is written and reviewed
- Do NOT include PII, secrets, or references to internal systems not in the repository
- Output file must be at least 500 bytes

---

## Step 0 — Fetch the JIRA Story (REQUIRED FIRST STEP)

Read the skill: `#file:.github/skills/fetch-jira-story.md`

Call the JIRA MCP tool to fetch the story provided as input:
```
Tool: get_issue
Arguments:
  issue_key: "${input:jira_issue_key}"
```

Write the raw JIRA response to `docs/artifacts/${input:jira_issue_key}/jira-story-raw.md`
using the format defined in the fetch-jira-story skill.

**If the JIRA call fails:**
- Log the error in the output document under "## JIRA Fetch Error"
- Fall back to reading `docs/artifacts/${input:jira_issue_key}/problem_spec.md` if it exists
- If that file also doesn't exist, HALT and tell the developer to provide the user story text

---

## Step 1 — Clarify

Using the JIRA story content (or fallback spec) as context, ask the developer:

1. Does the JIRA story description capture all expected functionality, or are there
   details elsewhere (Confluence, Slack, emails) that should be included?
2. What is the target output format — Markdown only, or also HTML / Confluence wiki?
3. Should "Not Specified" fields be omitted or shown as a placeholder?
4. Are there additional acceptance criteria beyond what is in the JIRA description?
5. What is the priority classification: Must Have / Should Have / Could Have?

---

## Step 2 — Write `docs/artifacts/${input:jira_issue_key}/requirements.md`

Use the JIRA story (from `jira-story-raw.md`) and the developer's clarification answers
as the sole inputs. Do not invent content.

```markdown
# Requirements — ${input:jira_issue_key}

| Field | Value |
|---|---|
| Ticket ID | ${input:jira_issue_key} |
| JIRA Summary | (verbatim from JIRA summary field) |
| JIRA Status | (verbatim from JIRA status field) |
| JIRA Type | (verbatim from JIRA issuetype field) |
| Phase | 1 — Requirements |
| Status | Draft |
| Author | GitHub Copilot (requirements agent) |
| Date | YYYY-MM-DD |
| Source | JIRA ticket fetched via MCP |

## 1. User Story
(verbatim description from JIRA — do not paraphrase)

## 2. Acceptance Criteria
(verbatim from JIRA acceptance criteria field or description checklist)

## 3. Clarifications Log
| # | Question | Answer |
|---|---|---|
| Q1 | ... | ... |

## 4. Functional Requirements
| ID | Requirement | Acceptance Criteria | Priority |
|---|---|---|---|
| FR-01 | ... | ... | Must Have |

## 5. Non-Functional Requirements
| ID | Category | Requirement | Metric |
|---|---|---|---|
| NFR-01 | Performance | ... | < X seconds |

## 6. Out of Scope

## 7. Assumptions and Dependencies

## 8. Sign-Off Checklist
- [ ] User story text is verbatim from JIRA (not paraphrased)
- [ ] All FRs traceable to the JIRA story
- [ ] All NFRs have measurable metrics
- [ ] Out-of-scope items explicitly listed
- [ ] No inferred values — only JIRA content or developer answers
```

---

## Success Criteria
- `docs/artifacts/${input:jira_issue_key}/jira-story-raw.md` written from live JIRA fetch
- `docs/artifacts/${input:jira_issue_key}/requirements.md` exists and is > 500 bytes
- User story section contains verbatim JIRA text

## On Failure
If clarifying questions are unanswered:
- Mark items as `TBD — awaiting developer input`
- Write the document with TBD placeholders
- Do NOT block pipeline progress

## State Transition
When output file is written and verified: `python scripts/state_manager.py complete 1`