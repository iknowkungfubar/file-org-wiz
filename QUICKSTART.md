# file-org-wiz Quick Start Guide

> Get organized in 5 minutes.

---

## Step 1: Choose Your System

| You Use | Follow Guide |
|--------|-------------|
| Claude Desktop | [install_claude_desktop.md](#claude-desktop) |
| Claude Code | [install_claude_code.md](#claude-code) |
| GitHub Copilot | [install_copilot.md](#github-copilot) |
| OpenAI Codex | [install_codex.md](#codex) |
| Codeium | [install_codeium.md](#codeium) |
| Tabnine | [install_tabnine.md](#tabnine) |
| Cody | [install_cody.md](#cody) |
| Continue | [install_continue.md](#continue) |
| Cursor/Windsurf | [install_cursor_windsurf.md](#cursor) |
| Aider | [install_aider.md](#aider) |
| OpenCode | [install_opencode.md](#opencode) |
| Raycast | [install_raycast.md](#raycast) |
| Mint CLI | [install_mint.md](#mint) |
| gptme | [install_gptme.md](#gptme) |
| Amazon Q | [install_amazonq.md](#amazon-q) |
| Any other AI | [install_mcp_generic.md](#any-ai) |

---

## Step 2: Install (2-3 minutes)

### Option A: Quick MCP Server

```bash
# 1. Navigate to file-org-wiz
cd /path/to/file-org-wiz

# 2. Install Flask
pip install flask

# 3. Start server
python mcp_server.py --port 5000 --mount /YOUR/MOUNT --backup /YOUR/BACKUP &

# 4. Test
curl http://localhost:5000/health
```

### Option B: System-Specific

Check your system guide:
- **Claude Desktop**: Copy MCP config to `~/Library/Application Support/Claude/mcp_servers/`
- **OpenCode**: Copy `SKILL.md` to `~/.opencode/skills/file-org-wiz/`
- **Aider**: Use the provided script
- See `INSTALL.md` for all systems

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
organize /your/mount /your/backup

# Check structure
curl http://localhost:5000/structure?path=/your/mount
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

1. **Read the User Guide**: [USER_GUIDE.md](./USER_GUIDE.md)
2. **Check the FAQ**: [FAQ.md](./FAQ.md)
3. **Daily Use**: Say "organize files at [path]" anytime

---

## Quick Reference

| Task | Command |
|------|---------|
| Organize | `curl -X POST localhost:5000/organize -d {...}` |
| Backup | `curl -X POST localhost:5000/backup -d {...}` |
| Check structure | `curl localhost:5000/structure?path=X` |
| Apply naming | `curl -X POST localhost:5000/apply-names -d {...}` |
| Health check | `curl localhost:5000/health` |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | `pip install flask` |
| Port in use | Change port: `python mcp_server.py --port 5001` |
| Files not found | Check path is absolute, not `~` |
| AI doesn't understand | Use system prompt: see `WHY_PARA_ZETTELKASTEN.md` |