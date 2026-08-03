# Skill: Fetch JIRA Story

Use this skill at the start of Phase 1 to retrieve the user story directly from JIRA
instead of reading a local file.

## How to Fetch a Story

Call the JIRA MCP tool `get_issue` with the ticket key:

```
Tool: get_issue
Arguments:
  issue_key: "FLASK-001"   # or whatever the current project key is
```

Read the key fields from the response:

| JIRA field         | Maps to requirements section        |
|--------------------|-------------------------------------|
| `summary`          | User story title / feature name     |
| `description`      | User story body, acceptance criteria|
| `issuetype.name`   | Story / Epic / Bug                  |
| `priority.name`    | Initial priority signal             |
| `status.name`      | Current workflow status             |
| `assignee`         | Owner                               |
| `labels`           | Tags / functional areas             |
| `comment.comments` | Clarification thread (if any)       |

## Fallback

If the MCP call fails (network, auth, key not found):
1. Log the error: `JIRA fetch failed: <error>`
2. Fall back to reading `docs/artifacts/FLASK-001/problem_spec.md` if it exists
3. If neither is available, HALT and ask the developer to provide the user story text

## Output After Fetch

After a successful fetch, write the raw JIRA content to:
`docs/artifacts/FLASK-001/jira-story-raw.md`

Format:
```markdown
# JIRA Story — <issue_key>

| Field       | Value       |
|-------------|-------------|
| Key         | FLASK-001   |
| Summary     | ...         |
| Type        | Story       |
| Priority    | ...         |
| Status      | ...         |
| Reporter    | ...         |
| Fetched at  | YYYY-MM-DD  |

## Description
<verbatim description from JIRA>

## Acceptance Criteria
<verbatim from JIRA description or acceptance criteria field>

## Comments (latest 5)
<verbatim comment thread>
```

This raw file becomes the authoritative input for Phase 1 and is archived under `.sdlc/phase-outputs/01-requirements/`.
