# Skill: jira-fetch

## Purpose
Fetch JIRA stories from the KAN project, score them by priority and complexity, and present a ranked list for the user to choose from.

## Script
`scripts/jira_fetch.py` — runs standalone, reads credentials from `.env`.

## Usage
```bash
python scripts/jira_fetch.py
```

## Output format
```
Rank  Ticket   Score  Priority    Title
----  -------  -----  ----------  ----------------------------------------
   1  KAN-27    6     High        US-21: Assign priority level to tasks
   2  KAN-13    5     Medium      US-18: Filter tasks by status
   ...
```

## Scoring formula
```
score = JIRA_PRIORITY_SCORE[priority] * 2 + complexity_score + done_penalty
```

Where:
- `JIRA_PRIORITY_SCORE`: Highest=5, High=4, Medium=3, Low=2, Lowest=1
- `complexity_score`: 1–3 estimated from story length
- `done_penalty`: +10 if status is Done (pushes completed stories to the bottom)

## Integration with 00-prioritize agent
The `00-prioritize` agent runs this script, shows the ranked list, waits for the user to pick a ticket (by number OR by typing a JIRA ticket ID directly), then hands off to the orchestrator with the selected ticket.

## Troubleshooting
- `410 Gone` from JIRA search endpoint: this Atlassian plan does not support JQL search. The script fetches individual tickets KAN-1…KAN-N until 404.
- `ModuleNotFoundError: dotenv`: run `pip install python-dotenv requests`.
- `401 Unauthorized`: check `JIRA_API_KEY` in `.env` — it may have expired.
