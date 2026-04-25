# Installation Guide

> Complete installation reference for all AI/agentic systems

---

## Quick Start (5 minutes)

```bash
# 1. Clone or copy this repo to a local path
# 2. Install dependencies
pip install -r requirements.txt

# 3. Choose your integration method below
```

---

## Integration Methods Quick Table

| System | Method | Difficulty | Setup Time |
|--------|--------|-------------|------------|
| Claude Desktop | MCP config | Easy | 2 min |
| Claude Code | Tool config | Easy | 2 min |
| OpenCode | Skill file | Easy | 1 min |
| Aider | Script | Easy | 2 min |
| Cursor/Windsurf | Rules | Easy | 2 min |
| Codex | Rules/script | Easy | 2 min |
| GitHub Copilot | Custom instructions | Easy | 2 min |
| Codeium | Rules file | Easy | 2 min |
| Tabnine | Rules file | Easy | 2 min |
| Cody (Sourcegraph) | Rules file | Easy | 2 min |
| Continue | MCP config | Easy | 2 min |
| Raycast | Script command | Medium | 3 min |
| Mint CLI | Tool config | Medium | 3 min |
| gptme | Commands | Medium | 3 min |
| Amazon Q | Custom instructions | Easy | 2 min |
| Any AI | HTTP API | Medium | 3 min |

---

## System-Specific Guides

### Claude Desktop
📄 [`docs/install/claude_desktop.md`](docs/install/claude_desktop.md)

```bash
mkdir -p ~/Library/Application\ Support/Claude/mcp_servers
cp file_org_wiz_mcp.json ~/Library/Application\ Support/Claude/mcp_servers/
# Restart Claude Desktop
```

### OpenCode 
📄 [`docs/install/opencode.md`](docs/install/opencode.md)

```bash
mkdir -p ~/.opencode/skills/file-org-wiz
cp SKILL.md ~/.opencode/skills/file-org-wiz/SKILL.md
```

### Aider
📄 [`docs/install/aider.md`](docs/install/aider.md)

```bash
# Simple: run script in Aider terminal
./file-org-wiz-aider.sh

# Advanced: MCP server
python src/mcp_server.py --port 5001 &
```

### Cursor/Windsurf
📄 [`docs/install/cursor_windsurf.md`](docs/install/cursor_windsurf.md)

```json
// Add to .cursorrules
{"rules": [...]}
```

### Codex
📄 [`docs/install/codex.md`](docs/install/codex.md)

```markdown
# Add to .codex/rules
```

### Any (HTTP)
📄 [`docs/install/mcp_generic.md`](docs/install/mcp_generic.md)

```bash
python src/mcp_server.py --port 5000 &
curl -X POST localhost:5000/organize ...
```

---

## Requirements

| Requirement | Version | Install |
|-------------|---------|---------|
| Python | 3.8+ | `python --version` |
| Flask | >= 2.3.2 | `pip install -r requirements.txt` |

---

## Default Paths

Edit in `src/mcp_server.py` or use environment variables:

```bash
export FILE_ORG_WIZ_MOUNT=/your/mount
export FILE_ORG_WIZ_BACKUP=/your/backup
export FILE_ORG_WIZ_VAULT=/your/vault
```

---

## Testing All Systems

### Test 1: MCP Server

```bash
cd /path/to/file-org-wiz
pip install -r requirements.txt
python src/mcp_server.py --port 5000 --mount /tmp/test --backup /tmp/backup &
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
  -d '{"mount_path": "/tmp/test", "backup_path": "/tmp/backup", "do_backup": false}'

# Check structure
ls -la /tmp/test/
# Should show: 00_INBOX 01_PROJECTS 02_AREAS 03_RESOURCES 04_ARCHIVE 90_TEMPLATES 99_SYSTEM
```

### Test 3: Files Created

```bash
ls /tmp/test/99_SYSTEM/
# Should have: File Naming Rules.md Tag Rules.md Vault Rules.md
```

### Test 4: Run Test Suite

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :5000

# Kill and restart
kill $(lsof -ti:5000)
python src/mcp_server.py --port 5001 &
```

### Permission Denied

```bash
chmod +x src/mcp_server.py
```

### Path Not Found

Use absolute paths, not relative:
- ❌ `./data`
- ✅ `/home/user/data`

---

## Advanced: MCP Server Options

### Custom Port

```bash
python src/mcp_server.py --port 5001
```

### Environment Variables

```bash
export MOUNT_PATH=/your/mount
export BACKUP_PATH=/your/backup  
export VAULT_PATH=/your/vault

python src/mcp_server.py
```

### Production (gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 "src.mcp_server:app"
```

### Production with Nginx

```nginx
# /etc/nginx/conf.d/file-org-wiz.conf
upstream file_org_wiz {
    server 127.0.0.1:5000;
}

server {
    listen 443 ssl;
    server_name file-org-wiz.example.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://file_org_wiz;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
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

## Security Notes

- Server binds to `localhost` by default
- CORS is disabled by default
- All paths are validated to prevent traversal attacks
- For production, use behind a reverse proxy with authentication

See [SECURITY.md](SECURITY.md) for full security documentation.

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
- `src/mcp_server.py` - MCP server code
- `AI_File_Organization_Agent_Prompt.md` - Full prompt
- `Why_PARA_Zettelkasten.md` - Methodology explanation
- `docs/research/` - Source documentation
- `docs/templates/` - Note templates