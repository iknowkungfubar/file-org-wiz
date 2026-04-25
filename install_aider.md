# Aider Integration

## Using file-org-wiz with Aider (AI Editor)

Aider is a terminal-based AI code editor. Here's how to integrate file-org-wiz:

### Method 1: MCP Server (Full Integration)

Start the MCP server:

```bash
cd /path/to/file-org-wiz
pip install flask
python mcp_server.py --port 5001 --mount /your/mount --backup /your/backup &
```

### Configure Aider

Add to your `.aider.conf`:

```bash
# MCP Servers
MCP_SERVERS=file-org-wiz:5001
```

Or pass at runtime:

```bash
aider --mcp-server file-org-wiz:5001
```

### Method 2: Execute Script (Simpler)

Create an execution script:

```bash
#!/bin/bash
# file-org-wiz-aider.sh

# Default paths (edit these)
MOUNT_PATH="${MOUNT_PATH:-/data}"
BACKUP_PATH="${BACKUP_PATH:-/data/backup}"

# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${BACKUP_PATH}/backup__${TIMESTAMP}"

echo "Creating backup at ${BACKUP_DIR}..."
mkdir -p "$BACKUP_DIR"
cp -r "$MOUNT_PATH/"* "$BACKUP_DIR/" 2>/dev/null || true

# Create PARA structure
echo "Creating PARA structure..."
cd "$MOUNT_PATH"
mkdir -p 00_INBOX 01_PROJECTS 02_AREAS 03_RESOURCES 04_ARCHIVE 90_TEMPLATES 99_SYSTEM

# Create subfolders
mkdir -p 01_PROJECTS/Projects 01_PROJECTS/Client-Work
mkdir -p 02_AREAS/Health 02_AREAS/Finance 02_AREAS/Home 02_AREAS/Learning 02_AREAS/Personal
mkdir -p 03_RESOURCES/AI 03_RESOURCES/Tech 03_RESOURCES/Career 03_RESOURCES/Development 03_RESOURCES/Media 03_RESOURCES/Reading 03_RESOURCES/Tools

echo "Done! PARA structure created at ${MOUNT_PATH}"
```

Make executable:

```bash
chmod +x file-org-wiz-aider.sh
```

### Method 3: Aider GPT Config

Create a custom GPT config for Aider:

```json
{
  "name": "file-org-wiz",
  "system_prompt": "You are a file organization expert using PARA methodology. When asked to organize files:
1. Always backup first (required!)
2. Create PARA folder structure
3. Apply naming conventions
4. Document changes

PARA Folders:
- 00_INBOX/ (drop zone)
- 01_PROJECTS/ (time-bound work)
- 02_AREAS/ (ongoing responsibilities)
- 03_RESOURCES/ (reference material)
- 04_ARCHIVE/ (completed items)
- 90_TEMPLATES/ (templates)
- 99_SYSTEM/ (rules/docs)

Naming: YYYY-MM-DD__context__description__vNN.ext"
}
```

### Using in Aider

Once configured, in Aider chat:

```
organize my files using PARA structure at /path/to/mount
```

### Available Commands

```bash
# Run organization script
./file-org-wiz-aider.sh

# Custom mount
MOUNT_PATH=/your/path ./file-org-wiz-aider.sh

# Check structure
ls -la /path/to/mount/
```

---

## Troubleshooting

### MCP Connection Failed

1. Check server is running: `curl localhost:5001/health`
2. Check Firewall: Allow local connections
3. Check port: Ensure 5001 is not in use

### Permission Denied

```bash
chmod +x file-org-wiz-aider.sh
```

### Backup Failed

Ensure backup path exists:
```bash
mkdir -p /your/backup/path