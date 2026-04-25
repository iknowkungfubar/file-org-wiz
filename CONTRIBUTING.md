# Contributing Guide

Thank you for contributing to file-org-wiz.

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/file-org-wiz.git
cd file-org-wiz

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov
```

## Adding New Installation Guide

Create `docs/install/install_systemname.md` with:
- Setup instructions
- How to use
- Troubleshooting
- Configuration options

## Code Standards

- Python: Follow PEP 8
- Include docstrings for all functions
- Add type hints where possible
- Test before submitting

## Testing

Before submitting:

```bash
# Run tests
python -m pytest tests/ -v

# Test MCP server manually
cd /path/to/file-org-wiz
python src/mcp_server.py --port 5000 --mount /tmp/test --backup /tmp/backup &
sleep 2
curl localhost:5000/health

# Cleanup test
pkill -f mcp_server.py
rm -rf /tmp/test /tmp/backup
```

## Testing the MCP Server

### Health Check

```bash
curl http://localhost:5000/health
# Expected: {"status": "healthy", "service": "file-org-wiz-mcp", "version": "1.0.0"}
```

### Organization Endpoint

```bash
curl -X POST http://localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{"mount_path": "/tmp/test", "backup_path": "/tmp/backup", "do_backup": false}'
```

### Verify Structure Created

```bash
ls /tmp/test/
# Should show: 00_INBOX 01_PROJECTS 02_AREAS 03_RESOURCES 04_ARCHIVE 90_TEMPLATES 99_SYSTEM
```

## Reporting Issues

Open an issue with:
1. Clear description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details (OS, Python version)

## Security Issues

**DO NOT** report security vulnerabilities in public issues. See [SECURITY.md](SECURITY.md) for reporting guidelines.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.