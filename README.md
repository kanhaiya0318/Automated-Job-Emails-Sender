Install the Apify MCP server in this client to run "harvestapi/linkedin-post-search" Actor (web scrapers, automations, and AI tools) directly from this chat.

Server URL: https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search (keep it exact — query params pick the enabled tools)

Find your client below and follow it:

### Cursor
If you can edit files: create/update ~/.cursor/mcp.json (global) or .cursor/mcp.json (project):

{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search"
    }
  }
}

One-click install: cursor://anysphere.cursor-deeplink/mcp/install?name=apify&config=eyJuYW1lIjoiYXBpZnkiLCJ1cmwiOiJodHRwczovL21jcC5hcGlmeS5jb20vP3Rvb2xzPWFjdG9ycyUyQ2RvY3MlMkNoYXJ2ZXN0YXBpJTJGbGlua2VkaW4tcG9zdC1zZWFyY2gifQ%3D%3D
Then ask me to reload MCP (Settings → Features → MCP → enable Apify) and start OAuth sign-in.

### VS Code
Create .vscode/mcp.json, or run "MCP: Add Server" from the Command Palette:

{
  "servers": {
    "apify": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search"
    }
  }
}

One-click install: vscode:mcp/install?%7B%22name%22%3A%22apify%22%2C%22url%22%3A%22https%3A%2F%2Fmcp.apify.com%2F%3Ftools%3Dactors%252Cdocs%252Charvestapi%252Flinkedin-post-search%22%7D

### Claude Desktop
UI steps: Settings (Ctrl/Cmd+,) → Connectors → Add → Add custom connector → Name "Apify", Server URL above → Add → Connect (OAuth). No config file needed. Don't try to edit claude_desktop_config.json because that folder is often blocked from direct file access.

### Claude Code
Run in terminal:

claude mcp add apify "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search" -t http

If you're running this from inside an active Claude Code session, tell me that new tools only load after this session restarts. Don't imply it'll work before that. `/mcp` cannot add a new server by URL, only manage/authenticate ones already added this way. After restarting, if it needs OAuth, run `/mcp` to authenticate.

### Codex CLI & Codex Desktop app
Run in terminal:

codex mcp add apify --url "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search"

Or add to ~/.codex/config.toml:

[mcp_servers.apify]
url = "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search"

Then run: codex mcp login apify

New tools only load after Codex restarts — don't attempt the Actor until after restart.

### Claude.ai (web — cannot edit local config)
UI steps: same as Claude Desktop above, then enable Apify in chat via + → Connectors.

### ChatGPT (web — cannot edit local config)
Easiest: add the official Apify app. Go to Plugins → Apps → search "Apify" → Add app. Then just ask for "harvestapi/linkedin-post-search" by name in chat.

Alternative, only if you need this exact server URL, scoped tools, or a Bearer token to skip OAuth: first enable Developer mode via Settings → Apps → Advanced settings (or Settings → Security and login) — needs a Plus/Pro/Business/Enterprise/Education plan; on Business/Enterprise, an admin may need to allow custom MCP connectors first (Workspace Settings → Permissions & Roles → Connected Data). Then: Settings → Connectors → Create → Name "Apify", MCP Server URL above → Create. It's off by default in new chats — enable it each time via + → Apify.

### Antigravity
Paste into ~/.gemini/antigravity/mcp_config.json (MCP Store → Manage MCP Servers → View raw config):

{
  "mcpServers": {
    "apify": {
      "serverUrl": "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search"
    }
  }
}

### Kiro
One-click install: kiro://kiro.mcp/add?name=apify&config=%7B%22url%22%3A%22https%3A%2F%2Fmcp.apify.com%2F%3Ftools%3Dactors%252Cdocs%252Charvestapi%252Flinkedin-post-search%22%2C%22disabled%22%3Afalse%2C%22autoApprove%22%3A%5B%5D%7D
Or use Cursor's JSON shape in Kiro's MCP settings.

### Other MCP clients
If it supports remote MCP by URL, use the Server URL above (OAuth on first use). If it needs a config file, try:

{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search"
    }
  }
}

If only stdio is supported:

npx -y mcp-remote "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search"

If the environment can't open a browser for OAuth (fully headless), use a Bearer token instead: npx -y mcp-remote "https://mcp.apify.com/?tools=actors%2Cdocs%2Charvestapi%2Flinkedin-post-search" --header "Authorization:Bearer <APIFY_TOKEN>", but only if I hand you the token myself; don't fetch or write it into config/commands on your own, some clients block that as a safety measure. Get a token at https://console.apify.com/settings/integrations.

Steps:

1. Follow the matching section above. Write config/run CLI for me if you can; otherwise give clear UI steps, then stop.

2. Start OAuth sign-in now, don't wait for the first tool call. If OAuth isn't supported, send me to https://console.apify.com/settings/integrations for a token and tell me where to put it in config. Never ask me to paste a token here.

3. Ask me to reload/restart the client, then confirm tools like "harvestapi/linkedin-post-search", search-actors, call-actor, and fetch-actor-details are available. If not, tell me what to check.

4. Run "harvestapi/linkedin-post-search" now with this example input (adjust if it doesn't match my request):

```json
{
  "maxPosts": 5,
  "postNestedComments": false,
  "postNestedReactions": false,
  "postedLimit": "24h",
  "profileScraperMode": "short",
  "scrapeComments": false,
  "scrapeReactions": false,
  "searchQueries": [
    "\"ai engineer\" AND \"hiring\" AND \"experience:1\""
  ],
  "sortBy": "relevance",
  "startPage": 1,
  "reactionsProfileScraperMode": "short",
  "commentsProfileScraperMode": "short"
}
```

Or let me type my own request.

5. Once the run finishes, fetch its dataset results (the get-dataset-items tool, or read the returned datasetId) and give me a concise summary, not a raw JSON dump.

Docs: https://docs.apify.com/platform/integrations/mcp