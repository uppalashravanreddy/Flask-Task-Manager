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

## Constraints
- NEVER infer or guess — every gap must be marked `TBD — awaiting clarification`
- NEVER write to any file outside `docs/artifacts/FLASK-001/`
- NEVER advance pipeline state before the output file is written and reviewed
- Do NOT include PII, secrets, or references to internal systems not in the repository
- Output file must be at least 500 bytes

---

## Step 0 — Fetch the JIRA Story (REQUIRED FIRST STEP)

Read the skill: `#file:.github/skills/fetch-jira-story.md`

Then call the JIRA MCP tool to fetch the story:
```
Tool: get_issue
Arguments:
  issue_key: "FLASK-001"
```

Write the raw JIRA response to `docs/artifacts/FLASK-001/jira-story-raw.md` using the
format defined in the fetch-jira-story skill.

**If the JIRA call fails:**
- Log the error in the output document under "## JIRA Fetch Error"
- Fall back to reading `#file:docs/artifacts/FLASK-001/problem_spec.md`
- If that file also doesn't exist, HALT and tell the developer to provide the user story

---

## Step 1 — Clarify

Using the JIRA story content (or fallback spec) as context, ask the developer these
questions and wait for answers before writing requirements.md:

1. Does the JIRA story description capture all the expected functionality, or are there
   details discussed elsewhere (Confluence, Slack, emails) that should be included?
2. Should the pipeline support output formats other than Markdown (HTML, Confluence wiki)?
3. Should "Not Specified" fields be omitted or included with the placeholder text?
4. Should the CLI accept `--repo-path` and `--output-path` arguments or use hardcoded defaults?
5. Is there a maximum file size limit for the generated technical profile?
6. Are there additional repository files beyond the six listed that should be scanned?

---

## Step 2 — Write `docs/artifacts/FLASK-001/requirements.md`

Use the JIRA story (from `jira-story-raw.md`) and the developer's clarification answers
as the sole inputs. Do not invent content.

```markdown
# Requirements — FLASK-001: Automated Documentation Sync

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| JIRA Summary | (verbatim from JIRA summary field) |
| JIRA Status | (verbatim from JIRA status field) |
| Feature | Automated Documentation Sync |
| Phase | 1 — Requirements |
| Status | Draft |
| Author | GitHub Copilot (requirements agent) |
| Date | YYYY-MM-DD |
| Source | JIRA ticket FLASK-001 fetched via MCP |

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
(explicit exclusion list)

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
- `docs/artifacts/FLASK-001/jira-story-raw.md` written from live JIRA fetch (or fallback logged)
- `docs/artifacts/FLASK-001/requirements.md` exists and is > 500 bytes
- User story section contains verbatim JIRA text
- All clarification questions answered and logged

## On Failure
If the developer does not answer the clarifying questions within the session:
- Mark unanswered items as `TBD — awaiting developer input`
- Write the document with TBD placeholders
- Do NOT block pipeline progress — mark the TBDs as open items in section 7

## State Transition
When output file is written and verified: `python scripts/state_manager.py complete 1`
${input:additional_context:No additional context provided}
