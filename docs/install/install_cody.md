# Cody (Sourcegraph) Integration

## Using file-org-wiz with Cody

Cody is Sourcegraph's AI coding assistant.

### Method 1: Cody Custom Rules

Create `.cody/rules.md`:

```markdown
# file-org-wiz - File Organization Rules

You have access to file-org-wiz for organizing workspace files.

When asked to organize files:
1. ALWAYS backup before any changes
2. Create PARA folder structure
3. Apply naming: YYYY-MM-DD__context__description__vNN.ext

PARA Folders:
- 00_INBOX/ (drop zone)
- 01_PROJECTS/ (time-bound work)
- 02_AREAS/ (ongoing)
- 03_RESOURCES/ (reference)
- 04_ARCHIVE/ (completed)

Context slugs: always lowercase (project, career, health, home)
```

### Method 2: Cody Config

Create `.cody/config.json`:

```json
{
  "organization": {
    "enabled": true,
    "rules_file": ".cody/rules.md"
  }
}
```

### Method 3: Chat Command

In Cody Chat:

```
/organization add file-org-wiz rules to workspace
```

Then ask naturally:

```
@workspace organize my files using PARA
```

### Method 4: Execute MCP

Start MCP server:

```bash
python /path/to/file-org-wiz/mcp_server.py --port 5004 &
```

In Cody, connect via MCP if supported:

```json
{
  "mcp": {
    "file-org-wiz": "localhost:5004"
  }
}
```

### Using Cody

Cody will understand organization when you say:

```
organize files at /workspace using PARA methodology
backup first then create the folder structure
```

---

## Installation

```bash
mkdir -p .cody
cp install_cody.md .cody/rules.md
```

---

## Troubleshooting

### Rules not found

Cody looks in:
- Project root
- Home directory
- `~/.cody/rules.md`

### Commands not working

Enable in Cody settings: Settings > Cody > Custom Commands