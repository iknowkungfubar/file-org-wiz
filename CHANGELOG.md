# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security
- Pin all CI actions to immutable commit SHAs (supply chain hardening)

### Added
- `.gitattributes` with language-specific text/binary classification

## [1.2.0] — 2026-06-18

### Added
- AGENTS.md for agentic coding context
- Social preview image and docs deployment workflow
- Gitleaks secret scanning in CI pipeline
- CI/CD hardening — permissions, dependabot, SECURITY.md
- Community infrastructure: CODE_OF_CONDUCT, issue/PR templates

### Changed
- Refactored `mcp_server.py` (1158 lines) into 3 focused modules
- README scope claims reduced to match actual implementation

### Fixed
- ruff E402 import violations (noqa annotations)
- API test compatibility — phases format, backup status, NLP skipif
- Backward-compatible error format in `create_backup`
- Re-exports restored in `mcp_server.py` for test compatibility
- Ruff formatting and lint

## [1.1.0] — 2026-06-03

### Added
- Proper pyproject.toml packaging
- `src/file_org_wiz/` package structure

### Changed
- Restructured from flat layout to `src/file_org_wiz/` package
- Standardized CONTRIBUTING.md and README contributing/license sections

### Fixed
- Dev extras and test imports for packaging restructure
- Stale version in CONTRIBUTING.md health example
- All open issues resolved

## [1.0.0] — 2026-04-25

### Added
- AI-powered file organization system (PARA + Zettelkasten methodology)
- MCP server (Flask-based HTTP API)
- File intelligence: auto-tagging, semantic analysis, filename suggestion
- NLP processor: natural language command parsing
- Recursive file scanning and categorization
- Duplicate detection (content hash + name similarity)
- Dry-run mode, analytics dashboard, backup integration
