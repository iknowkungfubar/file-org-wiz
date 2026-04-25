# Quick Start Guide

> Get organized in 5 minutes.

---

## Step 1: Choose Your System

| You Use | Follow Guide |
|--------|-------------|
| Claude Desktop | [docs/install/claude_desktop.md](docs/install/claude_desktop.md) |
| Claude Code | [docs/install/claude_code.md](docs/install/claude_code.md) |
| GitHub Copilot | [docs/install/copilot.md](docs/install/copilot.md) |
| OpenAI Codex | [docs/install/codex.md](docs/install/codex.md) |
| Codeium | [docs/install/codeium.md](docs/install/codeium.md) |
| Tabnine | [docs/install/tabnine.md](docs/install/tabnine.md) |
| Cody | [docs/install/cody.md](docs/install/cody.md) |
| Continue | [docs/install/continue.md](docs/install/continue.md) |
| Cursor/Windsurf | [docs/install/cursor_windsurf.md](docs/install/cursor_windsurf.md) |
| Aider | [docs/install/aider.md](docs/install/aider.md) |
| OpenCode | [docs/install/opencode.md](docs/install/opencode.md) |
| Raycast | [docs/install/raycast.md](docs/install/raycast.md) |
| Mint CLI | [docs/install/mint.md](docs/install/mint.md) |
| gptme | [docs/install/gptme.md](docs/install/gptme.md) |
| Amazon Q | [docs/install/amazonq.md](docs/install/amazonq.md) |
| Any other AI | [docs/install/mcp_generic.md](docs/install/mcp_generic.md) |

---

## Step 2: Install (2-3 minutes)

### Option A: Quick MCP Server

```bash
# 1. Navigate to file-org-wiz
cd /path/to/file-org-wiz

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start server
python src/mcp_server.py --port 5000 --mount /YOUR/MOUNT --backup /YOUR/BACKUP &

# 4. Test
curl http://localhost:5000/health
```

### Option B: System-Specific

Check your system guide:
- **Claude Desktop**: Copy MCP config to `~/Library/Application Support/Claude/mcp_servers/`
- **OpenCode**: Copy `SKILL.md` to `~/.opencode/skills/file-org-wiz/`
- **Aider**: Use the provided script
- See [INSTALL.md](INSTALL.md) for all systems

---

## Step 3: Use It

### Via AI Chat

Say to your AI:

```
Organize my files using PARA methodology at /path/to/mount
```

### Via API

```bash
# Create backup + organize
curl -X POST http://localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{
    "mount_path": "/your/mount",
    "backup_path": "/your/backup",
    "do_backup": true,
    "create_vault": false
  }'
```

### Via Command Line

```bash
# Simple organize
curl -X POST localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{"mount_path": "/your/mount"}'

# Check structure
curl "localhost:5000/structure?path=/your/mount"
```

---

## Done! Your Files Are Now Organized

### What Changed?

```
/your/mount/
├── 00_INBOX/           # Drop zone
├── 01_PROJECTS/       # Active work
│   ├── Projects/
│   └── Client-Work/
├── 02_AREAS/          # Ongoing
│   ├── Health/
│   ├── Finance/
│   ├── Home/
│   ├── Learning/
│   └── Personal/
├── 03_RESOURCES/      # Reference
│   ├── AI/
│   ├── Tech/
│   ├── Career/
│   ├── Development/
│   └── ...
├── 04_ARCHIVE/        # Completed
├── 90_TEMPLATES/     # Templates
└── 99_SYSTEM/        # Rules
    ├── File Naming Rules.md
    ├── Tag Rules.md
    ├── Vault Rules.md
    └── File_System_User_Guide.md
```

---

## File Naming

New files follow: `YYYY-MM-DD__context__description__vNN.ext`

| Before | After |
|--------|--------|
| `final.docx` | `2026-04-25__career__resume__v01.docx` |
| `Meeting Notes.docx` | `2026-04-24__turin-tech__client-meeting__v01.docx` |

---

## Next Steps

1. **Read the User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
2. **Check the FAQ**: [FAQ.md](FAQ.md)
3. **Daily Use**: Say "organize files at [path]" anytime

---

## Quick Reference

| Task | Command |
|------|---------|
| Organize | `curl -X POST localhost:5000/organize -H "Content-Type: application/json" -d '{"mount_path": "/mount"}'` |
| Backup | `curl -X POST localhost:5000/backup -H "Content-Type: application/json" -d '{"source_path": "/mount", "backup_path": "/backup"}'` |
| Check structure | `curl "localhost:5000/structure?path=/mount"` |
| Apply naming | `curl -X POST localhost:5000/apply-names -H "Content-Type: application/json" -d '{"file_path": "/file", "context": "proj", "description": "doc"}'` |
| Health check | `curl localhost:5000/health` |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | `pip install -r requirements.txt` |
| Port in use | Change port: `python src/mcp_server.py --port 5001` |
| Files not found | Check path is absolute, not `~` |
| AI doesn't understand | Use system prompt: see `Why_PARA_Zettelkasten.md` |

---

## Security

- Server binds to localhost by default
- CORS is disabled by default
- All paths are validated
- See [SECURITY.md](SECURITY.md) for details