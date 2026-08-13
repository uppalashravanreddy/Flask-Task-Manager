"""
Fetches all stories from the KAN JIRA project, scores them by priority,
complexity, and SDLC artifact status, and prints a ranked list for the
prioritization agent to present to the user.
"""
import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"
ARTIFACTS_DIR = Path(__file__).parent.parent / "docs" / "artifacts"

JIRA_PRIORITY_SCORE = {"Highest": 5, "High": 4, "Medium": 3, "Low": 2, "Lowest": 1}

COMPLEXITY_KEYWORDS = {
    "low":    ["navigation", "flash", "config", "csrf", "requirements.txt", "initialise", "database init"],
    "medium": ["view", "add", "edit", "delete", "form", "model", "validation", "unique"],
    "high":   ["pipeline", "extractor", "scanner", "page creator", "integration", "orchestrat"],
}

EPIC_KEYS = {"KAN-1", "KAN-2", "KAN-3", "KAN-4", "KAN-5", "KAN-6"}


def load_env():
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"')
    return env


def jira_get(url, b64_auth):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def fetch_stories(base_url, b64_auth):
    stories = []
    for i in range(1, 50):
        key = f"KAN-{i}"
        try:
            data = jira_get(f"{base_url}/rest/api/3/issue/{key}", b64_auth)
            fields = data["fields"]
            if key in EPIC_KEYS or fields.get("issuetype", {}).get("name") == "Epic":
                continue
            desc_text = ""
            try:
                desc_text = fields["description"]["content"][0]["content"][0]["text"]
            except Exception:
                pass
            stories.append({
                "key": key,
                "summary": fields.get("summary", ""),
                "priority": fields.get("priority", {}).get("name", "Medium"),
                "status": fields.get("status", {}).get("name", "Idea"),
                "description": desc_text,
            })
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break
        except Exception:
            continue
    return stories


def complexity_score(summary, description):
    text = (summary + " " + description).lower()
    for level, keywords in COMPLEXITY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return {"low": 3, "medium": 2, "high": 1}[level]
    return 2


def sdlc_done(key):
    ticket_id = key.replace("-", "").upper()
    artifact_dir = ARTIFACTS_DIR / ticket_id
    if artifact_dir.exists():
        return len(list(artifact_dir.glob("*.md"))) >= 3
    return False


def score_story(story):
    p = JIRA_PRIORITY_SCORE.get(story["priority"], 3)
    c = complexity_score(story["summary"], story["description"])
    done_penalty = -10 if sdlc_done(story["key"]) else 0
    return p * 2 + c + done_penalty


def main():
    env = load_env()
    base_url = env.get("JIRA_INSTANCE_URL", "").rstrip("/")
    email = env.get("JIRA_USER_EMAIL", "")
    token = env.get("JIRA_API_KEY", "")

    if not all([base_url, email, token]):
        print("ERROR: Missing JIRA credentials in .env")
        return

    b64_auth = base64.b64encode(f"{email}:{token}".encode()).decode()

    print("Fetching stories from JIRA...")
    stories = fetch_stories(base_url, b64_auth)

    for s in stories:
        s["score"] = score_story(s)
        s["sdlc_done"] = sdlc_done(s["key"])

    ranked = sorted(stories, key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 65)
    print("  PRIORITIZED STORY BACKLOG — KAN Project")
    print("=" * 65)
    print(f"{'#':<3} {'Key':<8} {'Pri':<8} {'Score':<7} {'SDLC':<6} Summary")
    print("-" * 65)

    for i, s in enumerate(ranked, 1):
        sdlc_tag = "[DONE]" if s["sdlc_done"] else "      "
        print(f"{i:<3} {s['key']:<8} {s['priority']:<8} {s['score']:<7} {sdlc_tag} {s['summary']}")

    print("=" * 65)
    print("\nScoring: JIRA priority × 2  +  complexity (3=low, 2=med, 1=high)")
    print("SDLC [DONE] = artifacts already exist in docs/artifacts/\n")

    return ranked


if __name__ == "__main__":
    main()
