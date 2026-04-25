# Amazon Q Integration

## Using file-org-wiz with Amazon Q

Amazon Q is AWS's AI developer assistant.

### Method 1: Amazon Q Custom Instructions

Create configuration file:

```bash
mkdir -p ~/.aws/amazonq
```

Create `~/.aws/amazonq/custom-instructions.md`:

```markdown
# Amazon Q - file-org-wiz Instructions

You have access to file-org-wiz for organizing files.

When asked to organize:
1. ALWAYS backup first (CRITICAL!)
2. Create PARA folder structure:
   - 00_INBOX/ (drop zone)
   - 01_PROJECTS/ (active work)
   - 02_AREAS/ (ongoing)
   - 03_RESOURCES/ (reference)
   - 04_ARCHIVE/ (completed)
3. Apply naming: YYYY-MM-DD__context__description__vNN.ext

Context slugs: lowercase, hyphens for spaces

Examples:
- 2026-04-25__project__document__v01.pdf
- 2026-04-24__career__resume__v01.docx

Never delete files without permission.
```

### Method 2: Amazon Q Extension (VSCode)

In VSCode with Amazon Q extension:

```bash
# Amazon Q looks for . amazonq extension points
mkdir -p .amazonq/commands
```

Create `.amazonq/commands/organize.json`:

```json
{
  "name": "organize",
  "description": "Organize files using PARA methodology",
  "command": {
    "type": "shell",
    "command": "python /path/to/file-org-wiz/mcp_server.py"
  }
}
```

### Method 3: AWS CLI Integration

```bash
# Create alias
alias q-organize='python /path/to/file-org-wiz/mcp_server.py --port 5010 && curl -X POST http://localhost:5010/organize'
```

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# file-org-wiz alias
organize-files() {
    python /path/to/file-org-wiz/mcp_server.py --port 5010 &
    sleep 2
    curl -X POST http://localhost:5010/organize \
        -H "Content-Type: application/json" \
        -d "{\"mount_path\": \"$1\", \"backup_path\": \"$2\"}"
}
```

### Method 4: Chat Command

In Amazon Q chat:

```
organize my code at /workspace using PARA structure
```

### Method 5: Amazon Q CLI

If using `q` CLI:

```
$ q chat "organize files at /workspace"
```

---

## Installation

```bash
# Copy custom instructions
mkdir -p ~/.aws/amazonq
cp install_amazonq.md ~/.aws/amazonq/custom-instructions.md
```

---

## Troubleshooting

### Custom instructions not loading

- Check file: `cat ~/.aws/amazonq/custom-instructions.md`
- Restart VSCode/IDE
- Check Amazon Q settings

### Permissions

Ensure Python path is correct: `which python`