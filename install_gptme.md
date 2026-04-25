# gptme Integration

## Using file-org-wiz with gptme

gptme is an interactive CLI AI.

### Method 1: gptme Configuration

Create `~/.gptme/file-org-wiz.yaml`:

```yaml
# gptme config for file organization
system_prompts:
  - role: system
    content: |
      You are a file organization expert using PARA methodology.
      
      When organizing files:
      1. ALWAYS backup first (required!)
      2. Create PARA folder structure
      3. Apply naming: YYYY-MM-DD__context__description__vNN.ext
      
      PARA Folders:
      - 00_INBOX/ (drop zone)
      - 01_PROJECTS/ (time-bound work)
      - 02_AREAS/ (ongoing responsibilities)
      - 03_RESOURCES/ (reference material)
      - 04_ARCHIVE/ (completed/obsolete)
      
      Never delete without explicit permission.
```

### Method 2: gptme Tools

If gptme supports custom tools:

```json
{
  "tools": [
    {
      "name": "organize_files",
      "description": "Organize files using PARA",
      "command": "python /path/to/file-org-wiz/mcp_server.py",
      "args": ["--port", "5009"]
    }
  ]
}
```

### Method 3: Direct Execution

In gptme session:

```
> Run: python /path/to/file-org-wiz/mcp_server.py --port 5009 &
> Call organize endpoint on localhost:5009
```

Or:

```
organize my files at /workspace using PARA
```

### Method 4: Commands File

Create `~/.gptme/commands/organize.py`:

```python
#!/usr/bin/env python3
"""organize command for gptme"""
import subprocess
import json

def run(args):
    mount = args[0] if args else "/data"
    backup = args[1] if len(args) > 1 else "/data/backup"
    
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:5009/organize",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({"mount_path": mount, "backup_path": backup})],
        capture_output=True
    )
    return result.stdout

if __name__ == "__main__":
    import sys
    print(run(sys.argv[1:]))
```

### Using gptme

In gptme interactive mode:

```
$ organize /workspace /backup
$ organize files using PARA methodology
```

---

## Installation

```bash
mkdir -p ~/.gptme/commands
cp organize.py ~/.gptme/commands/
chmod +x ~/.gptme/commands/organize.py
```

Start MCP server first: `python mcp_server.py --port 5009 &`

---

## Troubleshooting

### Command not found

Restart gptme: `gptme --restart`

### API errors

Check gptme version: `gptme --version`