# Mint CLI Integration

## Using file-org-wiz with Mint

Mint is a fast Go-based AI CLI.

### Method 1: Mint Tools

Create `~/.mint/tools/file_org_wiz.py`:

```python
#!/usr/bin/env python3
"""File Org Wiz tool for Mint CLI"""
import sys
import requests
import json

def organize(files_arg: str = "") -> str:
    """Organize files using PARA methodology"""
    mount = sys.argv[1] if len(sys.argv) > 1 else "/data"
    backup = sys.argv[2] if len(sys.argv) > 2 else "/data/backup"
    
    try:
        r = requests.post(
            "http://localhost:5007/organize",
            json={"mount_path": mount, "backup_path": backup}
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(json.dumps(organize()))
```

### Method 2: Mint Config

Create `~/.mint/config.yaml`:

```yaml
tools:
  - name: organize-files
    description: Organize files using PARA
    command: python /path/to/file-org-wiz/mcp_server.py
    args: ["--port", "5007"]

context:
  - type: file
    pattern: "**/*.md"
    content: |
      # file-org-wiz rules
      # PARA folders: 00_INBOX, 01_PROJECTS, 02_AREAS, 03_RESOURCES
      # Naming: YYYY-MM-DD__context__description__vNN.ext
```

### Method 3: Shell Tool

Create `/usr/local/bin/file-org-wiz`:

```bash
#!/bin/bash
# file-org-wiz tool for any CLI

MOUNT="${1:-/data}"
BACKUP="${2:-/data/backup}"

cd /path/to/file-org-wiz

# Start server if not running
pgrep -f "mcp_server.py" > /dev/null || {
    pip install -q flask
    python mcp_server.py --port 5007 --mount "$MOUNT" --backup "$BACKUP" &
    sleep 2
}

# Organize
curl -s -X POST http://localhost:5007/organize \
  -H "Content-Type: application/json" \
  -d "{\"mount_path\": \"$MOUNT\", \"backup_path\": \"$BACKUP\"}"
```

```bash
chmod +x /usr/local/bin/file-org-wiz
```

### Using Mint

```
$ mint organize-files /path/to/mount /path/to/backup
$ mint file-org-wiz organize
```

Or use tool:

```
> Use files-organize on ~/Documents
```

---

## Installation

```bash
# Install tool
sudo cp file-org-wiz-tool /usr/local/bin/file-org-wiz
chmod +x /usr/local/bin/file-org-wiz

# Test
file-org-wiz ~/Documents ~/Backups
```

---

## Troubleshooting

### Tool not found

Add to PATH: `export PATH="$PATH:/usr/local/bin"`

### Port conflict

Change port: `mint config set port 5008`