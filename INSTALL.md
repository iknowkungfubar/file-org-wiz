# file-org-wiz Installation Guide

> Complete installation reference for all AI/agentic systems

---

## Quick Start (5 minutes)

```bash
# 1. Clone or copy this repo to a local path
# 2. Install dependencies
pip install flask

# 3. Choose your integration method below
```

---

## Integration Methods Quick Table

| System | Method | Difficulty | Setup Time |
|--------|--------|-------------|------------|
| Claude Desktop | MCP config | Easy | 2 min |
| OpenCode | Skill file | Easy | 1 min |
| Aider | Script | Easy | 2 min |
| Cursor/Windsurf | Rules | Easy | 2 min |
| Codex | Rules/script | Easy | 2 min |
| Any AI | HTTP API | Medium | 3 min |

---

## System-Specific Guides

### Claude Desktop
📄 `install_claude_desktop.md`

```bash
mkdir -p ~/Library/Application\ Support/Claude/mcp_servers
cp file_org_wiz_mcp.json ~/Library/Application\ Support/Claude/mcp_servers/
# Restart Claude Desktop
```

### OpenCode 
📄 `install_opencode.md`

```bash
mkdir -p ~/.opencode/skills/file-org-wiz
cp SKILL.md ~/.opencode/skills/file-org-wiz/SKILL.md
```

### Aider
📄 `install_aider.md`

```bash
# Simple: run script in Aider terminal
./file-org-wiz-aider.sh

# Advanced: MCP server
python mcp_server.py --port 5001 &
```

### Cursor/Windsurf
📄 `install_cursor_windsurf.md`

```json
// Add to .cursorrules
{"rules": [...]}
```

### Codex
📄 `install_codex.md`

```markdown
# Add to .codex/rules
```

### Any (HTTP)
📄 `install_mcp_generic.md`

```bash
python mcp_server.py --port 5000 &
curl -X POST localhost:5000/organize ...
```

---

## Requirements

| Requirement | Version | Install |
|-------------|---------|---------|
| Python | 3.8+ | `python --version` |
| Flask | Latest | `pip install flask` |

---

## Default Paths

Edit in `mcp_server.py`:

```python
MOUNT_PATH = "/data"           # Your cloud mount
DOCUMENTS_PATH = "/home/user/Documents"
DOWNLOADS_PATH = "/home/user/Downloads"
VAULT_PATH = ""              # Obsidian vault (optional)
BACKUP_PATH = "/data/backup" # Backup location
```

---

## Testing All Systems

### Test 1: MCP Server

```bash
cd /path/to/file-org-wiz
pip install flask
python mcp_server.py --port 5000 --mount /tmp/test --backup /tmp/backup &
sleep 2

# Health check
curl localhost:5000/health

# Should return:
# {"status": "healthy", "service": "file-org-wiz-mcp", "version": "1.0.0"}
```

### Test 2: Organization

```bash
curl -X POST localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{"mount_path": "/tmp/test", "backup_path": "/tmp/backup", "do_backup": true}'

# Check structure
ls -la /tmp/test/
# Should show: 00_INBOX 01_PROJECTS 02_AREAS 03_RESOURCES 04_ARCHIVE 90_TEMPLATES 99_SYSTEM
```

### Test 3: Files Created

```bash
ls /tmp/test/99_SYSTEM/
# Should have: File Naming Rules.md Tag Rules.md Vault Rules.md
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :5000

# Kill and restart
kill $(lsof -ti:5000)
python mcp_server.py --port 5001 &
```

### Permission Denied

```bash
chmod +x mcp_server.py
chmod +x *.sh
```

### Path Not Found

Use absolute paths, not relative:
- ❌ `./data`
- ✅ `/home/user/data`

---

## Advanced: MCP Server Options

### Custom Port

```bash
python mcp_server.py --port 5001
```

### Environment Variables

```bash
export MOUNT_PATH=/your/mount
export BACKUP_PATH=/your/backup  
export VAULT_PATH=/your/vault

python mcp_server.py
```

### Production (gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 mcp_server:app
```

---

## Support Matrix

| Feature | Claude Desktop | OpenCode | Aider | Cursor | Any |
|---------|---------------|----------|-------|--------|-----|
| MCP | ✅ | ❌ | ❌ | ✅ | ✅ |
| Skill | N/A | ✅ | ❌ | ❌ | ❌ |
| Rules | ❌ | ❌ | ❌ | ✅ | ❌ |
| Script | N/A | N/A | ✅ | ✅ | N/A |
| HTTP | ❌ | ❌ | ✅ | ✅ | ✅ |

---

## Next Steps

1. Choose your system above
2. Follow the specific guide
3. Test with `/tmp` paths first
4. Configure production paths
5. Use daily!

---

## Also See

- `README.md` - Main overview
- `SKILL.md` - OpenCode skill
- `mcp_server.py` - MCP server code
- `AI_File_Organization_Agent_Prompt.md` - Full prompt
- `Why_PARA_Zettelkasten.md` - Methodology explanation
- `research/` - Source documentation