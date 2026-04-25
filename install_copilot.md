# GitHub Copilot Integration

## Using file-org-wiz with GitHub Copilot in VSCode

Copilot doesn't have MCP but can use custom instructions. Here's how:

### Method 1: VSCode Workspace Rules

Create `.vscode/file-org-wiz.code-workspace` or add to existing:

```json
{
  "settings": {
    "files.associations": {
      "*.md": "markdown"
    }
  }
}
```

### Method 2: Copilot Chat Instructions

Create a custom instruction file:

```markdown
<!-- .copilot/file-org-wiz.md -->
# file-org-wiz Instructions

You are a file organization expert using PARA methodology.

When asked to organize files:
1. ALWAYS create backup first (CRITICAL!)
2. Create PARA folder structure:
   - 00_INBOX/ (drop zone)
   - 01_PROJECTS/ (active work)
   - 02_AREAS/ (ongoing)
   - 03_RESOURCES/ (reference)
   - 04_ARCHIVE/ (completed)
   - 90_TEMPLATES/ (templates)
   - 99_SYSTEM/ (rules)
3. Apply naming: YYYY-MM-DD__context__description__vNN.ext

Example:
- 2026-04-25__project__pitch-deck__v01.pdf
- 2026-04-24__career__resume__v01.docx

Always confirm paths before executing.
```

### Method 3: VSCode Task

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "file-org-wiz: Organize",
      "type": "shell",
      "command": "python /path/to/file-org-wiz/mcp_server.py",
      "args": ["--mount", "${workspaceFolder}"],
      "problemMatcher": []
    }
  ]
}
```

### Method 4: Shell Command

Create a shell command Copilot can suggest:

```bash
#!/bin/bash
# file-org-wiz-copilot.sh

organize_files() {
    MOUNT="$1"
    BACKUP="$2"
    
    cd /path/to/file-org-wiz
    pip install -q flask
    python mcp_server.py --port 5001 --mount "$MOUNT" --backup "$BACKUP"
}
```

### Method 5: Inline Prompt (Chat)

In Copilot Chat, say:

```
@workspace You are a file-org-wiz expert. Organize files using PARA. 
Create folders: 00_INBOX, 01_PROJECTS, 02_AREAS, 03_RESOURCES, 04_ARCHIVE.
Naming: YYYY-MM-DD__context__desc__vNN.ext
```

---

## Using the Copilot Chat

Type in VSCode Copilot Chat:

```
organize my project files using PARA at /path/to/workspace
```

Copilot will suggest the organization command.

---

## Installation

```bash
# Create .copilot directory
mkdir -p .copilot

# Copy instructions
cp install_copilot.md .copilot/file-org-wiz.md
```

---

## Troubleshooting

### Rules not applied

Restart VSCode
Check file encoding: UTF-8

### Suggestions not showing

Type in @workspace context first
Reload window: Cmd+Shift+P > Reload Window