# Codeium Integration

## Using file-org-wiz with Codeium

Codeium is a free AI coding assistant. Here's integration:

### Method 1: Codeium Rules

Codeium respects `.codeium` directory files.

Create `.codeium/rules.md`:

```markdown
# file-org-wiz - File Organization Rules

You are a file organization expert using PARA methodology.

When organizing files:
1. ALWAYS backup first (CRITICAL!)
2. Create PARA folder structure
3. Apply naming: YYYY-MM-DD__context__description__vNN.ext

PARA Folders:
- 00_INBOX/ - Drop zone (process daily)
- 01_PROJECTS/ - Active time-bound work
- 02_AREAS/ - Ongoing responsibilities
- 03_RESOURCES/ - Reference material
- 04_ARCHIVE/ - Completed/obsolete
- 90_TEMPLATES/ - Reusable templates
- 99_SYSTEM/ - Rules and documentation

Naming Examples:
- 2026-04-25__turin-tech__pitch-deck__v01.pdf
- 2026-04-24__career__resume__v01.docx

Context Slugs (always lowercase):
- project-name for projects
- career for job search
- health for health info
- home for household

Never delete files without explicit permission.
Always create backup before changes.
```

Save to your project root or home directory.

### Method 2: Codeium Config

Create `.codeium/config.json`:

```json
{
  "enable_rules": true,
  "rules_file": ".codeium/rules.md",
  "organization_rules": {
    "file_naming": "YYYY-MM-DD__context__description__vNN.ext",
    "backup_first": true,
    "para_structure": true
  }
}
```

### Method 3: IDE Commands

Add to `.codeium/commands.json`:

```json
{
  "commands": [
    {
      "name": "organize-files",
      "description": "Organize files using PARA",
      "script": "python /path/to/file-org-wiz/mcp_server.py --port 5003 --mount ${workspace}"
    }
  ]
}
```

### Using in Codeium

In your editor, say:

```
/organize-files /workspace
@file-org-wiz organize at /path
```

---

## Installation

```bash
mkdir -p .codeium
cp install_codeium.md .codeium/rules.md
```

---

## Troubleshooting

### Rules not loading

- Place `.codeium/rules.md` in project root
- Codeium scans up to 3 parent directories
- Enable in Codeium settings: Codeium > Enable Rules