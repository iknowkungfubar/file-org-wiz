# Continue Integration

## Using file-org-wiz with Continue

Continue is an open-source VSCode extension with MCP support.

### Method 1: Continue Config

Create/edit `~/.continue/config.yaml`:

```yaml
mcpServers:
  file-org-wiz:
    command: python
    args:
      - /path/to/file-org-wiz/mcp_server.py
      - --port
      - "5005"
      - --mount
      - /your/mount/path
      - --backup
      - /your/backup/path
```

### Method 2: Continue Rules

Create `~/.continue/rules.md`:

```markdown
# file-org-wiz Rules

You have access to file-org-wiz MCP server.

Organization rules:
1. Always backup first
2. Use PARA: 00_INBOX, 01_PROJECTS, 02_AREAS, 03_RESOURCES, 04_ARCHIVE
3. Naming: YYYY-MM-DD__context__description__vNN.ext

Context slugs: lowercase, hyphens for spaces
```

### Method 3: Continue Commands

Add custom slash commands:

```yaml
slashCommands:
  - name: /organize
    description: Organize files using PARA
    ...
```

### Using Continue

Start MCP server:

```bash
python /path/to/file-org-wiz/mcp_server.py --port 5005 &
```

In VSCode with Continue:

```
@file-org-wiz organize files at /workspace
```

Or use:

```
/organize /path/to/mount /path/to/backup
```

---

## Installation

```bash
# Create config directory
mkdir -p ~/.continue

# Copy config and rules
cp install_continue.md ~/.continue/rules.md
```

Edit `~/.continue/config.yaml` to add MCP server.

---

## Troubleshooting

### MCP not connecting

Check server: `curl localhost:5005/health`
Verify config YAML syntax: `python -c "import yaml; yaml.safe_load(open('~/.continue/config.yaml'))"`

### Tools not appearing

Restart VSCode
Check Continue output panel for errors