# Claude Desktop Integration

## Using file-org-wiz with Claude Desktop (macOS/Windows)

Claude Desktop supports MCP servers. Here's how to integrate file-org-wiz:

### Method 1: Direct MCP Connection

Create the MCP config file:

**macOS:**
```bash
mkdir -p ~/Library/Application\ Support/Claude/mcp_servers
```

**Windows:**
```cmd
mkdir "%APPDATA%\Claude\mcp_servers"
```

### Create the Server Config

Create `file_org_wiz_mcp.json`:

```json
{
  "mcpServers": {
    "file-org-wiz": {
      "command": "python",
      "args": [
        "/path/to/file-org-wiz/mcp_server.py",
        "--mount", "/your/mount/path",
        "--backup", "/your/backup/path"
      ],
      "env": {},
      "description": "File Organization with PARA methodology"
    }
  }
}
```

Save to the correct location:

**macOS:** `~/Library/Application Support/Claude/mcp_servers/file_org_wiz_mcp.json`

**Windows:** `%APPDATA%\Claude\mcp_servers\file_org_wiz_mcp.json`

### Restart Claude Desktop

Close and reopen Claude Desktop. The tool should be available.

### Using the Tools

Say to Claude:

```
Use file-org-wiz to reorganize my files at /path/to/mount
```

### Alternative: Quick Script

Create a wrapper script for easier configuration:

```bash
#!/bin/bash
# claude-file-org-wiz-setup.sh

MOUNT_PATH="${1:-/data}"
BACKUP_PATH="${2:-/data/backup}"

cat > ~/Library/Application\ Support/Claude/mcp_servers/file_org_wiz_mcp.json << EOF
{
  "mcpServers": {
    "file-org-wiz": {
      "command": "python",
      "args": [
        "$(pwd)/mcp_server.py",
        "--mount", "$MOUNT_PATH",
        "--backup", "$BACKUP_PATH"
      ]
    }
  }
}
EOF

echo "Setup complete. Restart Claude Desktop."
```

---

## Available Tools in Claude Desktop

Once configured, you can use:

| Tool | Description |
|------|------------|
| `organize` | Execute full PARA reorganization |
| `backup` | Create timestamped backup |
| `structure` | View current directory structure |
| `apply_names` | Apply naming convention to file |

### Example Usage

```
Hey Claude, use file-org-wiz to:
- Backup my files at /run/media/turin/Data/rclone/gdrive-mount/
- Create the PARA folder structure
- Set up my Obsidian vault at /path/to/vault
```

---

## Troubleshooting

### Server won't start

1. Check Python is installed: `python --version`
2. Install Flask: `pip install flask`
3. Check path: Verify the path to mcp_server.py is absolute

### Tools not showing

1. Restart Claude Desktop completely
2. Check config file exists
3. Check for errors in logs

### Path issues

Use absolute paths in the config. The tilde (~) doesn't work - use full paths: