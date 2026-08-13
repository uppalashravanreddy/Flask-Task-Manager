# Load .env from project root and start the GitHub MCP server.
# Same pattern as start-jira-mcp.ps1 — bridges .env into process env vars.

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

# @modelcontextprotocol/server-github reads GITHUB_PERSONAL_ACCESS_TOKEN
if (-not $env:GITHUB_PERSONAL_ACCESS_TOKEN) {
    Write-Error "GITHUB_PERSONAL_ACCESS_TOKEN is not set in .env"
    exit 1
}

npx -y @modelcontextprotocol/server-github
