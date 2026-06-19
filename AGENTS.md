# AGENTS.md — File Org Wiz

> Operating context for AI agents working on this repository. Load at session start.

## Project Identity

**File Org Wiz** is an AI-powered file organization system using the PARA + Zettelkasten methodology. It automatically classifies, categorizes, and organizes files into structured hierarchies based on content analysis and user-defined rules.

## Tech Stack

- **Language:** Python 3.10+
- **Build:** setuptools (pyproject.toml)
- **Linting:** ruff
- **Testing:** pytest
- **MCP Integration:** Model Context Protocol for AI assistant integration
- **Published:** PyPI as `file-org-wiz`

## Repository Structure

```
├── src/file_org_wiz/          # Main package
│   ├── core/                  # Classification engine, rules engine
│   ├── para/                  # PARA methodology implementation
│   ├── zettelkasten/          # Zettelkasten methodology implementation
│   ├── watcher/               # File system watcher service
│   ├── mcp/                   # MCP server integration
│   └── config.py              # Configuration management
├── tests/                     # Test suite
├── docs/                      # Documentation (25+ files)
├── AGENTS.md                  # This file
├── LICENSE                    # MIT
└── README.md                  # Project documentation
```

## Conventions

- **Commits:** `feat:|fix:|refactor:|test:|docs:|chore: — [message]`
- **Type annotations** on all public functions
- **Docstrings** for all public modules and classes

## Quality Gates

- `ruff check src/` — 0 errors
- `pytest tests/` — all tests pass

## Agent Workflow

1. **Understand the methodology** — Read `docs/` — PARA and Zettelkasten are the core paradigms
2. **Classification pipeline** — File classification lives in `src/core/`
3. **Watcher service** — Real-time file monitoring in `src/watcher/`
4. **Tests first** — New classification rules need test coverage
5. **Verify** — Run full test suite before claiming done
