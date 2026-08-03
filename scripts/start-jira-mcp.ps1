# Load .env from project root and start the JIRA MCP server.
# Jira Cloud (@sooperset/mcp-atlassian) uses JIRA_URL / JIRA_USERNAME / JIRA_API_TOKEN.
# Our .env uses JIRA_INSTANCE_URL / JIRA_USER_EMAIL / JIRA_API_KEY — this script bridges the gap.

$envFile = Join-Path $PSScriptRoot "..\\.env"
if (Test-Path $envFile) {
    foreach ($line in Get-Content $envFile) {
        $line = $line.Trim()
        if ($line -and !$line.StartsWith('#') -and $line -match '^([^=]+)=(.*)$') {
            $name  = $Matches[1].Trim()
            $value = $Matches[2].Trim().Trim('"')
            [System.Environment]::SetEnvironmentVariable($name, $value, 'Process')
        }
    }
}

# Map .env names → @sooperset/mcp-atlassian expected names (Jira Cloud)
$env:JIRA_URL       = $env:JIRA_INSTANCE_URL -replace '/$'   # strip trailing slash
$env:JIRA_USERNAME  = $env:JIRA_USER_EMAIL
$env:JIRA_API_TOKEN = $env:JIRA_API_KEY

Write-Host "Starting Jira MCP for: $env:JIRA_URL" -ForegroundColor Cyan

npx -y @sooperset/mcp-atlassian