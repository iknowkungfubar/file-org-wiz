# Cursor/Windsurf Extension Integration

## Using file-org-wiz with Cursor or Windsurf IDE

Cursor and Windsurf support custom rules and extensions. Here's how to integrate file-org-wiz:

### Method 1: Cursor Rules (Rules.json)

Create a `.cursorrules` file in your project or home directory:

```json
{
  "rules": [
    {
      "pattern": "**/*",
      "content": "You are a file organization expert using PARA methodology. When asked to organize files:\n\n1. Always backup first (CRITICAL!)\n2. Create PARA folder structure\n3. Apply naming conventions: YYYY-MM-DD__context__description__vNN.ext\n4. Document all changes\n\nPARA Folders:\n- 00_INBOX/ (drop zone, process daily)\n- 01_PROJECTS/ (active time-bound work)\n- 02_AREAS/ (ongoing responsibilities)\n- 03_RESOURCES/ (reference material)\n- 04_ARCHIVE/ (completed items)\n- 90_TEMPLATES/ (templates)\n- 99_SYSTEM/ (rules and docs)\n\nFile Naming Pattern:\n- 2026-04-25__project__description__v01.pdf\n- 2026-04-24__career__resume__v01.docx\n\nAlways confirm paths before executing."
    }
  ]
}
```

Save to your home or project directory.

### Method 2: Cursor Custom Command

Create a custom command in the IDE:

1. Open Cursor → Settings → Commands
2. Add new command:
   - **Name**: File Org Wiz
   - **Command**: 
   ```bash
   python /path/to/file-org-wiz/mcp_server.py --mount {{input_path}} --backup {{backup_path}}
   ```

### Method 3: Windsurf Extension (mcp.yaml)

Create `.windsurf/mcp.yaml` in your home directory:

```yaml
mcp_servers:
  file-org-wiz:
    command: python
    args:
      - /path/to/file-org-wiz/mcp_server.py
      - --port
      - 5002
      - --mount
      - /your/mount/path
      - --backup
      - /your/backup/path
```

### Method 4: Quick Action Script

Create a Cursor-friendly script:

```bash
#!/bin/bash
# cursor-file-org-wiz.sh

read -p "Mount path: " MOUNT
read -p "Backup path: " BACKUP
read -p "Create vault? (y/n): " VAULT_Q

cd /path/to/file-org-wiz
pip install -q flask

if [ "$VAULT_Q" = "y" ]; then
    read -p "Vault path: " VAULT
    python mcp_server.py --mount "$MOUNT" --backup "$BACKUP" --vault "$VAULT"
else
    python mcp_server.py --mount "$MOUNT" --backup "$BACKUP"
fi
```

### Using in Cursor

In the Cursor chat:

```
organize my files at [path] using PARA structure
```

Or use the custom command.

### Method 5: Rule-based Organization

Add to `.cursorignore` or project rules:

```
# file-org-wiz organization rules
# 
# When creating new files, use: YYYY-MM-DD__context__description__vNN.ext
#
# Context slugs:
#   - projectname for active projects
#   - career for job search
#   - health for health info
#   - home for household
#
# Archive completed projects to 04_ARCHIVE/
```

---

## Available in IDE

| Feature | Cursor | Windsurf |
|---------|--------|---------|
| Custom Rules | ✅ | ✅ |
| MCP Server | ✅ | ✅ |
| Custom Commands | ✅ | ✅ |
| Terminal | ✅ | ✅ |

---

## Troubleshooting

### Rules not Loading

1. Check file location: `~/.cursorrules` or project root
2. Check JSON validity: Use a JSON validator
3. Restart IDE

### MCP Tools Not Available

1. Ensure MCP config is in correct location
2. Restart IDE
3. Check server is running: `curl localhost:5002/health`