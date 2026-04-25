# Raycast AI Integration

## Using file-org-wiz with Raycast

Raycast is a popular macOS launcher with AI features.

### Method 1: Raycast Script Command

Create a Raycast script command:

```bash
#!/bin/bash
# file-org-wiz.sh
# Required visibility: global

# Parameters
MOUNT_PATH="${1:-$HOME/Documents}"
BACKUP_PATH="${2:-$HOME/Desktop/Backups}"

# Run organization
cd /path/to/file-org-wiz
pip install -q flask

# Check if server running
pgrep -f "mcp_server.py" || python mcp_server.py --port 5006 &

sleep 1

# Call organize
curl -s -X POST http://localhost:5006/organize \
  -H "Content-Type: application/json" \
  -d "{\"mount_path\": \"$MOUNT_PATH\", \"backup_path\": \"$BACKUP_PATH\"}"
```

### Method 2: Raycast Extension

Create directory: `~/.raycast/extensions/file-org-wiz/`

File: `extension.json`:

```json
{
  "name": "file-org-wiz",
  "description": "Organize files using PARA methodology",
  "icon": "folder",
  "commands": [
    {
      "name": "organize",
      "title": "Organize Files",
      "description": "Organize files using PARA structure",
      "script": "file-org-wiz.sh",
      "arguments": [
        {
          "name": "mount",
          "placeholder": "Mount path"
        }
      ]
    }
  ]
}
```

### Using Raycast

Type in Raycast:

```
organize files
```

Or use the extension command:

```
/file-org-wiz organize at ~/Documents
```

### Method 3: Quick Action

Create Quick Action in Raycast:

```bash
# Raycast > Settings > Quick Actions > Create New
# Name: Organize Files
# Script:
python /path/to/file-org-wiz/mcp_server.py --port 5006
```

---

## Installation

```bash
# Install script command
mkdir -p ~/.raycast/extensions/file-org-wiz
cp file-org-wiz.sh ~/.raycast/extensions/file-org-wiz/file-org-wiz.sh
chmod +x ~/.raycast/extensions/file-org-wiz/file-org-wiz.sh
```

Restart Raycast to load new command.

---

## Troubleshooting

### Script not appearing

- Restart Raycast: `killall Raycast`
- Check script: `cat ~/.raycast/extensions/file-org-wiz/file-org-wiz.sh`
- View errors: `~/.raycast/logs/`

### Permission denied

```bash
chmod +x ~/.raycast/extensions/file-org-wiz/file-org-wiz.sh
```