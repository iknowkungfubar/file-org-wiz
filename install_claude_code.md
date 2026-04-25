# Claude Code Integration

## Using file-org-wiz with Claude Code CLI

Claude Code is the CLI version (different from Claude Desktop app).

### Method 1: Tool/Function Registration

Claude Code can use custom tools. Create a config:

```bash
mkdir -p ~/.claude
```

Create `~/.claude/tools.json`:

```json
{
  "tools": [
    {
      "name": "file_org_wiz",
      "description": "Organize files using PARA methodology",
      "command": "python",
      "args": [
        "/path/to/file-org-wiz/mcp_server.py",
        "--mount", "${MOUNT_PATH}",
        "--backup", "${BACKUP_PATH}"
      ]
    }
  ]
}
```

### Method 2: Bash Integration

Add to your Claude Code config:

```yaml
# In your claude-code.yaml or settings
customCommands:
  - name: organize
    command: python /path/to/file-org-wiz/mcp_server.py
    args: ["--mount", "{{path}}"]
```

### Method 3: Quick Script

Create an executable script Claude Code can call:

```bash
#!/bin/bash
# claude-code-file-org-wiz.sh

# Check if MCP server is running
pgrep -f "mcp_server.py" || {
    echo "Starting MCP server..."
    cd /path/to/file-org-wiz
    pip install -q flask
    python mcp_server.py --port 5000 --mount /data --backup /data/backup &
    sleep 2
}

# Call organize endpoint
curl -s -X POST http://localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d "{\"mount_path\": \"$1\", \"backup_path\": \"$2\"}"
```

```bash
chmod +x claude-code-file-org-wiz.sh
```

### Method 4: Prompt Library

Add to your Claude Code prompt library:

```markdown
# file-org-wiz
You have access to file-org-wiz for file organization.

To organize files:
1. Ask for the mount path
2. Ask for backup path
3. Call the organize endpoint

PARA Structure:
- 00_INBOX/ - Drop zone
- 01_PROJECTS/ - Time-bound work
- 02_AREAS/ - Ongoing responsibilities
- 03_RESOURCES/ - Reference
- 04_ARCHIVE/ - Completed

Naming: YYYY-MM-DD__context__description__vNN.ext
```

Save to `~/.claude/prompts/file-org-wiz.md`

### Using in Claude Code

In your conversation:

```
@file-org-wiz reorganize files at /path/to/mount
```

Or use the custom command:

```
/organize /path/to/mount /path/to/backup
```

### Method 5: MCP Integration

If Claude Code supports MCP servers:

```json
// In Claude Code config
{
  "mcpServers": {
    "file-org-wiz": {
      "command": "python",
      "args": ["/path/to/file-org-wiz/mcp_server.py", "--port", "5001"]
    }
  }
}
```

Then use MCP tools directly.

---

## Installation

```bash
# Create config directories
mkdir -p ~/.claude/prompts

# Copy prompt
cp install_claude_code.md ~/.claude/prompts/file-org-wiz.md

# Make script executable
chmod +x claude-code-file-org-wiz.sh
```

---

## Troubleshooting

### Tools not loading

Check config location: `~/.claude/tools.json`
Check JSON validity: `python -m json.tool ~/.claude/tools.json`

### Server not responding

Check port: `curl localhost:5000/health`
Restart server: `pkill -f mcp_server.py; python mcp_server.py &`