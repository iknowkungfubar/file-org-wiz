# OpenAI Codex Integration

## Using file-org-wiz with OpenAI Codex

OpenAI Codex (formerly Canvas) supports MCP and custom configurations:

### Method 1: Codex Project Rules

Create a `.codex/rules` file in the root of your Codex projects:

```markdown
# file-org-wiz - File Organization Rules

You are a file organization expert using PARA methodology.

## Core Principles

1. ALWAYS backup before any changes (CRITICAL!)
2. Ask for paths before executing
3. Use PARA folder structure
4. Apply consistent naming

## PARA Structure

- 00_INBOX/ - Drop zone, process daily
- 01_PROJECTS/ - Active time-bound deliverables
- 02_AREAS/ - Ongoing responsibilities  
- 03_RESOURCES/ - Reference material
- 04_ARCHIVE/ - Completed/obsolete
- 90_TEMPLATES/ - Reusable templates
- 99_SYSTEM/ - Rules and documentation

## Naming Convention

Pattern: `YYYY-MM-DD__context__description__vNN.ext`

Examples:
- 2026-04-25__turin-tech__pitch-deck__v01.pdf
- 2026-04-24__career__resume__v01.docx
- 2026-04-20__project__meeting-notes__v01.md

## Context Slugs

Use consistent lowercase slugs:
- `turin-tech` - Business
- `career` - Job search
- `health` - Health info
- `home` - Household
- `learning` - Education
- `project-name` - Active projects

## Workflow

When asked to organize:
1. Confirm paths
2. Create backup first
3. Execute changes
4. Document what was done
```

Save as `.codex/rules` or add to project rules.

### Method 2: Codex MCP Config

Create a `.codex/mcp.json`:

```json
{
  "mcpServers": {
    "file-org-wiz": {
      "command": "python",
      "args": [
        "/path/to/file-org-wiz/mcp_server.py",
        "--mount", "/data",
        "--backup", "/data/backup"
      ]
    }
  }
}
```

### Method 3: Codex Startup Script

Create a script Codex can run:

```bash
#!/bin/bash
# codex-file-org-wiz.sh

echo "=== File Org Wizard ==="
read -p "Mount path: " MOUNT
read -p "Backup path: " BACKUP

cd /path/to/file-org-wiz

echo "[1/3] Creating backup..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP/backup__$TIMESTAMP"
cp -r "$MOUNT/"* "$BACKUP/backup__$TIMESTAMP/"

echo "[2/3] Creating PARA structure..."
cd "$MOUNT"
mkdir -p 00_INBOX 01_PROJECTS 02_AREAS 03_RESOURCES 04_ARCHIVE 90_TEMPLATES 99_SYSTEM
mkdir -p 01_PROJECTS/Projects 01_PROJECTS/Client-Work
mkdir -p 02_AREAS/Health 02_AREAS/Finance 02_AREAS/Home 02_AREAS/Learning 02_AREAS/Personal
mkdir -p 03_RESOURCES/AI 03_RESOURCES/Tech 03_RESOURCES/Career 03_RESOURCES/Development

echo "[3/3] Creating system docs..."
cd "$MOUNT/99_SYSTEM"
cat > File_Naming_Rules.md << 'EOF'
# File Naming Rules
Pattern: YYYY-MM-DD__context__description__vNN.ext
EOF

cat > README.md << 'EOF'
# Organization Complete
Created: $(date)
Mount: $MOUNT
Backup: $BACKUP/backup__$TIMESTAMP
EOF

echo "Done! Structure created at $MOUNT"
```

### Method 4: Codex Function (Python)

If Codex supports Python functions:

```python
import os
import shutil
from datetime import datetime

def organize_files(mount_path: str, backup_path: str) -> dict:
    """Execute PARA file organization"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Backup
    backup_dir = os.path.join(backup_path, f"backup__{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create structure
    for folder in ["00_INBOX", "01_PROJECTS", "02_AREAS", "03_RESOURCES", 
                "04_ARCHIVE", "90_TEMPLATES", "99_SYSTEM"]:
        os.makedirs(os.path.join(mount_path, folder), exist_ok=True)
    
    return {"status": "complete", "backup": backup_dir}
```

### Using in Codex

Ask Codex:

```
organize my files at /path/to/mount using PARA structure
```

Or use the custom function:

```python
organize_files("/path/to/mount", "/path/to/backup")
```

---

## Troubleshooting

### Rules Not Applied

1. Check file is named exactly `.codex/rules`
2. Restart Codex session
3. Check rules file is valid Markdown

### MCP Server Issues

1. Check Python path: `which python`
2. Install Flask: `pip install flask`
3. Test server: `python mcp_server.py --help`