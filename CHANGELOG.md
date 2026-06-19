# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-03-28

### Added

- Community infrastructure: CODE_OF_CONDUCT, issue/PR templates, SECURITY.md
- Social preview image and docs deployment workflow (gh-pages)
- AGENTS.md for agentic coding context
- Gitleaks secret scanning in CI pipeline

### Changed

- Refactored 1158-line `mcp_server.py` into 3 focused modules (file_intelligence.py, nlp_processor.py, scanner/)
- README scope claims reduced to match actual implementation
- Community health files added for open-source sustainability

### Fixed

- REST API test compatibility — phases format, backup status endpoint, NLP skipif condition
- Backward-compatible error format in `create_backup`
- Re-exports in `mcp_server.py` restored for test compatibility
- Ruff lint/formatting issues across the codebase
- E402 import violations with noqa annotations

## [1.2.0] - 2025-03-10

### Added

- Initial release with PARA + Zettelkasten methodology
- MCP server with Flask HTTP API
- File scanning and categorization engine
- Duplicate detection (content hash + name similarity)
- Zettelkasten integration: MOCs, atomic notes, bidirectional links
- Natural language command parsing
- Auto-tagging and smart renaming
- Analytics dashboard API
- Template system (finance, research, media)
- Dry-run mode for preview before applying changes
- Path validation and security hardening

[1.3.0]: https://github.com/iknowkungfubar/file-org-wiz/releases/tag/v1.3.0
[1.2.0]: https://github.com/iknowkungfubar/file-org-wiz/releases/tag/v1.2.0
