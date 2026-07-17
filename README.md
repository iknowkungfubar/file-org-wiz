# file-org-wiz

> An AI-powered file organization system using the PARA + Zettelkasten methodology.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/file-org-wiz)](https://pypi.org/project/file-org-wiz/)
[![CI](https://github.com/iknowkungfubar/file-org-wiz/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/iknowkungfubar/file-org-wiz/actions/workflows/ci.yml)
[![CodeQL](https://github.com/iknowkungfubar/file-org-wiz/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/iknowkungfubar/file-org-wiz/actions/workflows/codeql.yml)
[![Tests](https://img.shields.io/badge/tests-96%20passed-green)](tests/)

A complete file organization system that provides tools to reorganize any computer's files with consistent structure, naming conventions, and documentation using the PARA (Projects, Areas, Resources, Archive) methodology combined with Zettelkasten principles.

## Features

- **PARA Folder Structure**: Action-oriented organization by Projects, Areas, Resources, and Archive
- **Deep File Scanning**: Recursive analysis and intelligent categorization
- **Duplicate Detection**: Content hash + name similarity matching
- **Zettelkasten Integration**: MOCs, atomic notes, bidirectional links for Obsidian vaults
- **MCP Server**: HTTP API for integration with AI coding assistants
- **Natural Language Commands**: Parse requests like "organize my downloads folder"
- **Auto-Tagging**: Generate semantic tags from filenames and readable file content
- **Smart Renaming**: Infer better filenames from content with `auto_describe`
- **Templates**: Apply finance, research, and media folder templates instantly
- **Analytics Dashboard API**: Inspect file types, categories, duplicate waste, tags, and largest files
- **dry-Run Mode**: Preview changes before applying
- **Safe by Design**: Path validation, backup-first execution, no data deletion without confirmation

> **Integration status**: MCP server is the primary interface. Direct integration docs are available for [Claude Desktop](docs/install/claude_desktop.md), [Aider](docs/install/aider.md), and [OpenCode](docs/install/opencode.md). Generic HTTP/MCP integration works with any AI coding assistant — see [MCP generic guide](docs/install/mcp_generic.md).

## Quick Start

### Install

```bash
# Install from source
pip install -e .

# Or install with pipx (recommended for CLI tools)
pipx install .
```

### Start the MCP server:

```bash
file-org-wiz --port 5000 --mount /YOUR/MOUNT --backup /YOUR/BACKUP
# Portfolio alias (both commands work identically)
turintech-file-org-wiz --port 5000 --mount /YOUR/MOUNT --backup /YOUR/BACKUP
```

### Examples

Try the [examples/](examples/) directory:

- **`examples/organize_downloads.py`** — Scan, analyze, and organize a directory of files using PARA + Zettelkasten methodology

```bash
python examples/organize_downloads.py /path/to/your/folder
```

### Test:

```bash
curl http://localhost:5000/health
```

### Preview (dry-run):

```bash
curl -X POST http://localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{"mount_path": "/YOUR/MOUNT", "dry_run": true}'
```

### Organize (for real):

```bash
curl -X POST http://localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{"mount_path": "/YOUR/MOUNT", "backup_path": "/YOUR/BACKUP", "do_backup": true}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|------------|
| `/health` | GET | Health check |
| `/organize` | POST | Execute reorganization |
| `/backup` | POST | Create backup |
| `/structure` | GET | Get directory structure |
| `/analytics` | GET | Get organization analytics |
| `/apply-names` | POST | Apply naming convention |
| `/analyze-file` | POST | Generate tags and smart filename suggestion |
| `/nlp-command` | POST | Parse or execute natural language requests |
| `/mcp-manifest` | GET | List available tools |

### Organize Options

```json
{
  "mount_path": "/path/to/mount",
  "backup_path": "/path/to/backup",
  "do_backup": true,
  "template": "finance",
  "dry_run": true,
  "create_vault": false,
  "vault_path": "/path/to/vault"
}
```

With `dry_run: true`, the response includes `suggested_actions` preview.

### Smart Naming

```json
{
  "file_path": "/path/to/file.txt",
  "auto_describe": true,
  "version": 1
}
```

### Natural Language Commands

```bash
curl -X POST http://localhost:5000/nlp-command \
  -H "Content-Type: application/json" \
  -d '{"command": "preview organize my downloads folder"}'
```

### Analytics

```bash
curl "http://localhost:5000/analytics?path=/YOUR/MOUNT"
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
| `docs/templates/01_meeting.md` | Meeting notes |
| `docs/templates/02_daily.md` | Daily logging |
| `docs/templates/03_project_moc.md` | Project hub |
| `docs/templates/04_area_dashboard.md` | Area dashboard |
| `docs/templates/05_project_note.md` | Project notes |

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

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on our development process, coding standards, PR workflow, and code of conduct.

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Your digital life is an extension of your mind. Organize it.*
