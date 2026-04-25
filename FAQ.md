# file-org-wiz FAQ

> Frequently asked questions about file-org-wiz.

---

## General Questions

### Q: What is file-org-wiz?

file-org-wiz is a complete file organization system using the PARA methodology. It provides tools to organize any computer's files with consistent structure, naming, and documentation.

### Q: Why PARA instead of topic folders?

PARA organizes by *action* (what you're doing), not *topic* (what it is). This aligns with how you actually live - active projects vs. ongoing areas vs. reference material.

### Q: Does this work on Windows/macOS/Linux?

Yes! The MCP server and file structure work on any OS. Path separators auto-adjust.

### Q: Is this free?

Yes, fully open source. Use, modify, share freely.

---

## Getting Started

### Q: Which system should I install first?

Start simple:
1. **Quick**: Use MCP server + HTTP API
2. **VSCode users**: Codeium, Copilot, or Continue
3. **macOS users**: Raycast
4. **Power users**: Claude Desktop or OpenCode

### Q: How long does installation take?

- MCP server: 2 minutes
- System-specific: 2-5 minutes
- Full setup: 5-10 minutes

### Q: Do I need Python?

Yes for MCP server. Install:
```bash
pip install flask
```

---

## Usage Questions

### Q: How do I organize new files?

1. Determine: Project? Area? Resource? Archive?
2. Apply naming: `YYYY-MM-DD__context__description__vNN.ext`
3. Move to correct folder

### Q: Can I use this with Obsidian?

Yes! Vault should mirror file system. See [USER_GUIDE.md](./USER_GUIDE.md).

### Q: How often should I organize?

**Daily**: Check 00_INBOX (2 minutes)
**Weekly**: Full review (30 minutes)
**Monthly**: Maintenance (60 minutes)

### Q: What about sensitive files?

The system creates backups before changes. Keep backups in secure location.

---

## Technical Questions

### Q: Server won't start

1. Check Python: `python --version`
2. Install Flask: `pip install flask`
3. Check port: `lsof -i :5000`

### Q: Port already in use

```bash
# Find process
lsof -i :5000

# Kill or use different port
python mcp_server.py --port 5001
```

### Q: Paths not working

Use absolute paths:
- ✅ `/home/user/Documents`
- ❌ `~/Documents`

### Q: MCP server vs skill - which to use?

| Server | Skill |
|--------|--------|
| HTTP API | Direct integration |
| Programmatic | Natural language |
| Custom tools | AI chat |
| 16 systems | OpenCode only |

---

## PARAS Questions

### Q: What's a "context slug"?

Part of filename: `YYYY-MM-DD__SLUG__description`

Examples: `turin-tech`, `career`, `health`, `game-symbiosis`

Create slugs for your main projects/areas.

### Q: Can I rename existing files?

Yes, but:
1. Keep backup first
2. Use consistent pattern
3. Tools will auto-suggest new names

### Q: What about duplicate files?

Check both:
- 00_INBOX (temporary)
- 04_ARCHIVE (old versions)

### Q: How deep should folders go?

Max 3-4 levels:
```
01_PROJECTS/my-project/
├── 01_admin/
├── 02_notes/
└── etc
```

---

## Backup & Restore

### Q: Where are backups?

Timestamped:
```
/backup/backup__2026-04-25_15-30-00/
```

### Q: How to restore?

```bash
cp -r /backup/backup__2026-04-25_*/* /mount/
```

### Q: Can I auto-backup?

Yes, MCP server does this automatically when organized with `do_backup: true`.

---

## Integrations

### Q: Which integration for my AI?

| Use | Integration |
|-----|-------------|
| Claude Desktop | MCP |
| VSCode | Copilot/Codeium |
| Terminal | Aider/Mint |
| Browser | MCP HTTP |
| Chat only | Rules file |

### Q: Multiple integrations at once?

Yes! Use different ports:
```bash
python mcp_server.py --port 5000  # Claude
python mcp_server.py --port 5001  # Aider
```

---

## Troubleshooting

### Q: "file not found"

- Check path exists: `ls /mount/00_INBOX/`
- Use absolute path
- Check server running

### Q: "permission denied"

```bash
chmod +x mcp_server.py
# or
sudo chown $USER:$USER /mount
```

### Q: "JSON error"

Validate MCP requests:
```python
python -m json.tool request.json
```

### Q: Still stuck?

1. Check MCP server running: `curl localhost:5000/health`
2. Check file exists: `ls /mount/99_SYSTEM/`
3. Re-read QUICKSTART.md
4. Submit issue

---

## Contributing

### Q: How to contribute?

1. Fork repo
2. Add system guide
3. Submit PR

### Q: Can I translate?

Yes! Create `install_*.md` in your language.

---

## More Questions?

- Check [USER_GUIDE.md](./USER_GUIDE.md)
- Check [QUICKSTART.md](./QUICKSTART.md)
- Read [AI_File_Organization_Agent_Prompt.md](./AI_File_Organization_Agent_Prompt.md)