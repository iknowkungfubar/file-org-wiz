# file-org-wiz

> An AI-powered file organization system using the PARA + Zettelkasten methodology.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)

A complete file organization system that provides tools to reorganize any computer's files with consistent structure, naming conventions, and documentation using the PARA (Projects, Areas, Resources, Archive) methodology combined with Zettelkasten principles.

## Features

- **PARA Folder Structure**: Action-oriented organization by Projects, Areas, Resources, and Archive
- **Zettelkasten Integration**: MOCs, atomic notes, bidirectional links for Obsidian vaults
- **MCP Server**: HTTP API for integration with AI coding assistants
- **Skill System**: Direct integration with OpenCode and other AI tools
- **Multi-System Support**: Works with Claude, Copilot, Cursor, Codex, and 15+ other AI systems
- **Safe by Design**: Path validation, backup-first execution, no data deletion without confirmation

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the MCP server**:
   ```bash
   python mcp_server.py --port 5000 --mount /YOUR/MOUNT --backup /YOUR/BACKUP &
   ```

3. **Test**:
   ```bash
   curl http://localhost:5000/health
   ```

4. **Organize your files**:
   ```bash
   curl -X POST http://localhost:5000/organize \
     -H "Content-Type: application/json" \
     -d '{"mount_path": "/YOUR/MOUNT", "backup_path": "/YOUR/BACKUP", "do_backup": true}'
   ```

## Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | Get started in 5 minutes |
| [USER_GUIDE.md](USER_GUIDE.md) | Complete user guide |
| [FAQ.md](FAQ.md) | Frequently asked questions |
| [REFERENCE_CARD.md](REFERENCE_CARD.md) | Print-ready reference |
| [CHEATSHEET.md](CHEATSHEET.md) | All commands |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [Why_PARA_Zettelkasten.md](Why_PARA_Zettelkasten.md) | Methodology explanation |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/01_meeting.md` | Meeting notes |
| `templates/02_daily.md` | Daily logging |
| `templates/03_project_moc.md` | Project hub |
| `templates/04_area_dashboard.md` | Area dashboard |
| `templates/05_project_note.md` | Project notes |

## Installation by System

Choose your AI system below:

| System | Installation |
|--------|--------------|
| Claude Desktop | [`docs/install/claude_desktop.md`](docs/install/claude_desktop.md) |
| Claude Code | [`docs/install/claude_code.md`](docs/install/claude_code.md) |
| GitHub Copilot | [`docs/install/copilot.md`](docs/install/copilot.md) |
| OpenAI Codex | [`docs/install/codex.md`](docs/install/codex.md) |
| Codeium | [`docs/install/codeium.md`](docs/install/codeium.md) |
| Tabnine | [`docs/install/tabnine.md`](docs/install/tabnine.md) |
| Cody | [`docs/install/cody.md`](docs/install/cody.md) |
| Continue | [`docs/install/continue.md`](docs/install/continue.md) |
| Cursor/Windsurf | [`docs/install/cursor_windsurf.md`](docs/install/cursor_windsurf.md) |
| Aider | [`docs/install/aider.md`](docs/install/aider.md) |
| OpenCode | [`docs/install/opencode.md`](docs/install/opencode.md) |
| Raycast | [`docs/install/raycast.md`](docs/install/raycast.md) |
| Mint CLI | [`docs/install/mint.md`](docs/install/mint.md) |
| gptme | [`docs/install/gptme.md`](docs/install/gptme.md) |
| Amazon Q | [`docs/install/amazonq.md`](docs/install/amazonq.md) |
| Any (HTTP) | [`docs/install/mcp_generic.md`](docs/install/mcp_generic.md) |

## Folder Structure Created

```
MOUNT_PATH/
├── 00_INBOX/                    # Drop zone - process daily
├── 01_PROJECTS/               # Time-bound deliverables
│   ├── Projects/
│   ├── Client-Work/
│   └── Personal/
├── 02_AREAS/                  # Ongoing responsibilities
│   ├── Health/
│   ├── Finance/
│   ├── Home/
│   ├── Learning/
│   └── Personal/
├── 03_RESOURCES/              # Reference material
│   ├── AI/
│   ├── Tech/
│   ├── Career/
│   ├── Development/
│   ├── Media/
│   ├── Reading/
│   └── Tools/
├── 04_ARCHIVE/               # Completed items
├── 90_TEMPLATES/             # Reusable templates
└── 99_SYSTEM/                # Rules & documentation
    ├── File Naming Rules.md
    ├── Tag Rules.md
    ├── Vault Rules.md
    └── File_System_User_Guide.md
```

## File Naming Convention

Pattern: `YYYY-MM-DD__context__description__vNN.ext`

| Before | After |
|--------|-------|
| `final.docx` | `2026-04-25__career__resume__v01.docx` |
| `Meeting Notes.docx` | `2026-04-24__turin-tech__client-meeting__v01.docx` |

## Requirements

- Python 3.8+
- Flask >= 2.3.2
- An AI agent that can execute bash commands, read/write files, and navigate directory structure

## Security

See [SECURITY.md](SECURITY.md) for our security policy and reporting guidelines.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## License

See [LICENSE](LICENSE) for licensing details.

---

*Your digital life is an extension of your mind. Organize it.*