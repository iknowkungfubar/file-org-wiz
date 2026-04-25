# Tabnine Integration

## Using file-org-wiz with Tabnine

Tabnine is an AI code completion tool with local model option.

### Method 1: Tabnine Rules

Create `.tabnine/rules.md`:

```markdown
# file-org-wiz - File Organization

When asked to organize files in the workspace:
1. Create backup first
2. Use PARA folder structure
3. Apply naming: YYYY-MM-DD__context__description__vNN.ext

PARA: 00_INBOX, 01_PROJECTS, 02_AREAS, 03_RESOURCES, 04_ARCHIVE
```

### Method 2: Tabnine Config

Add to `.tabnine/config.json`:

```json
{
  "preferences": {
    "disabled": false,
    "ai_max_tokens": 2048
  },
  "rules": {
    "enabled": true,
    "file": ".tabnine/rules.md"
  }
}
```

### Method 3: Custom Context

Tabnine reads `.tabnine/userContext.md`:

```markdown
# workspace: organize using file-org-wiz PARA structure
# backup: always required before changes
```

### Using Tabnine

Type naturally in your editor:

```
organize my workspace files
```

Tabnine will suggest organization based on rules.

---

## Installation

```bash
mkdir -p .tabnine
cp install_tabnine.md .tabnine/rules.md
```