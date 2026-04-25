# file-org-wiz Command Cheatsheet

> All the commands in one place.

---

## MCP Server Commands

### Start Server

```bash
# Basic
python mcp_server.py --port 5000 --mount /mount/path --backup /backup/path

# With vault
python mcp_server.py --port 5000 --mount /mount --backup /backup --vault /vault/path

# Custom port
python mcp_server.py --port 5001

# Background
python mcp_server.py &>/dev/null &
nohup python mcp_server.py &
```

### Server Health

```bash
# Check health
curl http://localhost:5000/health

# Get structure
curl http://localhost:5000/structure?path=/mount/path

# Get MCP manifest
curl http://localhost:5000/mcp-manifest
```

### Organization

```bash
# Full organize (with backup)
curl -X POST http://localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{
    "mount_path": "/mount/path",
    "backup_path": "/backup/path",
    "do_backup": true,
    "create_vault": false
  }'

# Just structure
curl -X POST http://localhost:5000/organize \
  -d '{"mount_path": "/mount", "do_backup": false}'

# With vault
curl -X POST localhost:5000/organize \
  -d '{"mount_path": "/mount", "create_vault": true, "vault_path": "/vault"}'
```

### Backup

```bash
# Create backup
curl -X POST http://localhost:5000/backup \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "/mount/path",
    "backup_path": "/backup/path"
  }'
```

### Naming

```bash
# Apply naming convention
curl -X POST http://localhost:5000/apply-names \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/mount/file.pdf",
    "context": "project",
    "description": "my-document",
    "version": 1
  }'
```

---

## File Commands

### Create Structure Manually

```bash
cd /mount/path
mkdir -p 00_INBOX 01_PROJECTS 02_AREAS 03_RESOURCES 04_ARCHIVE 90_TEMPLATES 99_SYSTEM
mkdir -p 01_PROJECTS/Projects 01_PROJECTS/Client-Work
mkdir -p 02_AREAS/Health 02_AREAS/Finance 02_AREAS/Home 02_AREAS/Learning 02_AREAS/Personal
mkdir -p 03_RESOURCES/AI 03_RESOURCES/Tech 03_RESOURCES/Career 03_RESOURCES/Development 03_RESOURCES/Media 03_RESOURCES/Reading 03_RESOURCES/Tools
```

### Rename Files

```bash
# Single file
mv old-name.pdf 2026-04-25__context__description__v01.pdf

# Batch (by date)
for f in *.pdf; do mv "$f" "$(date +%Y-%m-%d)__project__${f}"; done
```

### Backup

```bash
# Manual backup
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
mkdir -p /backup/backup__$TIMESTAMP
cp -r /mount/* /backup/backup__$TIMESTAMP/
```

---

## System-Specific

### Claude Desktop

```bash
# Check config
ls -la ~/Library/Application\ Support/Claude/mcp_servers/
```

### Aider

```bash
# In Aider, just type:
/organize /path /backup
```

### Raycast

```
# Type in Raycast:
organize files
```

### OpenCode

```
# Say to OpenCode:
Use file-org-wiz to reorganize files at /path
```

---

## Quick Reference

### Daily Commands

```bash
# 1. Check structure
curl localhost:5000/structure?path=/mount

# 2. Process inbox
ls /mount/00_INBOX/

# 3. Organize
curl -X POST localhost:5000/organize -d '{"mount_path": "/mount"}'
```

### Maintenance

```bash
# Weekly: Check structure
curl localhost:5000/structure?path=/mount | head -20

# Monthly: Full organize
curl -X POST localhost:5000/organize \
  -d '{"mount_path": "/mount", "backup_path": "/backup", "do_backup": true}'
```

---

## Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# file-org-wiz aliases
organize() {
  curl -X POST localhost:5000/organize \
    -d "{\"mount_path\": \"$1\", \"backup_path\": \"$2\"}"
}

backup() {
  curl -X POST localhost:5000/backup \
    -d "{\"source_path\": \"$1\", \"backup_path\": \"$2\"}"
}

structure() {
  curl "localhost:5000/structure?path=$1"
}

healthcheck() {
  curl localhost:5000/health
}
```

Then use:
```bash
organize /mount /backup
structure /mount
healthcheck
```

---

## Port Reference

| Port | Typical Use |
|------|-------------|
| 5000 | Default |
| 5001 | Claude Desktop |
| 5002 | Cursor/Windsurf |
| 5003 | Codex |
| 5004 | Cody |
| 5005 | Continue |
| 5006 | Raycast |
| 5007 | Mint |
| 5008 | gptme |
| 5009 | Amazon Q |
| 5010 |备用 |

---

## Environment Variables

```bash
export MOUNT_PATH=/your/mount
export BACKUP_PATH=/your/backup
export VAULT_PATH=/your/vault
export PORT=5000
```

---

## Troubleshooting Commands

```bash
# Check if server running
lsof -i :5000

# Check server logs
tail -f /var/log/mcp_server.log

# Kill server
kill $(pgrep -f mcp_server.py)

# Restart server
pkill -f mcp_server.py; python mcp_server.py &

# Check permissions
ls -la /mount/
```

---

*Keep this cheatsheet handy!*