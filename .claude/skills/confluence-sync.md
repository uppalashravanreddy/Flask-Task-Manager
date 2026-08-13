# Skill: confluence-sync

## Purpose
Create and update Confluence pages during the SDLC pipeline using the `@sooperset/mcp-atlassian` MCP server (which handles both JIRA and Confluence via the same connection).

## MCP server
The Confluence MCP is provided by the same `atlassian` server in `.vscode/mcp.json`.
Credentials: `JIRA_INSTANCE_URL`, `JIRA_USER_EMAIL`, `JIRA_API_KEY` from `.env`.

## Available MCP tools
- `confluence_search` — search for existing pages
- `confluence_get_page` — read a page by ID
- `confluence_create_page` — create a new page
- `confluence_update_page` — update an existing page
- `confluence_get_spaces` — list available spaces

## Page hierarchy for this project

```
Confluence Space: <your space>
└── Flask Task Manager
    └── QA
        └── <TICKET-ID> Test Strategy      ← Phase 7.1
            └── <TICKET-ID> Test Plan       ← Phase 7.2
                └── <TICKET-ID> Test Cases  ← Phase 7.3
                    └── <TICKET-ID> Test Results  ← Phase 7.4
                        └── <TICKET-ID> Verification Report  ← Phase 7.5
```

## Create a page (Phase 7.1 example)
```
Use confluence_create_page with:
  space_key: <found via confluence_get_spaces>
  title: "FLASK-002 Test Strategy"
  parent_title: "QA"
  content: <markdown or HTML content>
```

## Update a page (idempotent pattern)
1. `confluence_search` for the title to get the page ID.
2. If found → `confluence_update_page` with the new content.
3. If not found → `confluence_create_page`.

## Content format
`@sooperset/mcp-atlassian` accepts Markdown. For tables, use standard Markdown table syntax. The MCP converts to Confluence storage format automatically.

## Storing the URL
After every create/update call, save the returned page URL:
```json
// .sdlc/state.json
"phases": {
  "7.1": {"confluence_url": "https://<instance>.atlassian.net/wiki/spaces/<space>/pages/<id>"}
}
```

## Error handling
- `403 Forbidden` → check JIRA_API_KEY in `.env`; may have expired
- `404 Not Found` on parent page → create the parent first (e.g. "QA" page)
- `title already exists` → switch to `confluence_update_page`

## Troubleshooting
Start the MCP server manually to test:
```powershell
.\scripts\start-jira-mcp.ps1
```
Then call a tool directly in the Claude Code session.
