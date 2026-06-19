# file-org-wiz — Agent Context

## Overview

file-org-wiz is an AI-powered file organization system using the PARA + Zettelkasten methodology.

## Tech Stack

- **Language:** Python 3.8+
- **Build System:** setuptools
- **Framework:** Flask (MCP server)
- **Testing:** pytest

## Repository Structure

```
src/file_org_wiz/
├── __init__.py          # Package init
├── mcp_server.py        # Flask MCP server (main entry point)
├── file_intelligence.py # File analysis, tagging, content inference
├── nlp_processor.py     # Natural language command parsing
├── scanner/             # File scanning module
│   └── __init__.py
└── duplicates/          # Duplicate detection
    └── __init__.py
```

## Architecture

- **MCP Server** (mcp_server.py): Flask-based HTTP API with routes for organize, backup, structure, analytics, naming
- **File Intelligence** (file_intelligence.py): Auto-tagging, semantic analysis, filename suggestion
- **NLP Processor** (nlp_processor.py): Parse natural language commands like "organize my downloads folder"
- **Scanner** (scanner/): Recursive file scanning and categorization
- **Duplicates** (duplicates/): Content hash + name similarity duplicate detection

## Conventions

- Type hints preferred
- Flask routes in mcp_server.py
- Tests mirror source structure

## Quality Gates

- `ruff check src/ tests/`
- `pytest tests/ -v`
