# Security Policy

> Last updated: 2026-04-25

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within file-org-wiz, please follow these steps:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Send a detailed report to the maintainers via:
   - Email (if contact available)
   - Private security advisory (GitHub Security Advisories)

### What to Include

When reporting, please include:

- Type of vulnerability (e.g., path traversal, injection, etc.)
- Full paths of source file(s) that have the vulnerability
- Location of the affected source code (branch/tag/commit)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact assessment of the vulnerability

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 7 days
- **Fix Timeline**: Dependent on severity (see below)

## Security Best Practices

When using file-org-wiz:

### 1. Network Access

The MCP server binds to `localhost` by default for security. Only expose it to network access if absolutely necessary:

```bash
# Default (safe) - localhost only
python mcp_server.py --port 5000

# Only if you need network access (use with caution)
python mcp_server.py --port 5000 --host 0.0.0.0
```

### 2. Enable CORS Explicitly

CORS is disabled by default. Enable only when needed:

```bash
python mcp_server.py --port 5000 --cors
```

### 3. Use Environment Variables for Production

```bash
export FILE_ORG_WIZ_MOUNT=/secure/mount/path
export FILE_ORG_WIZ_BACKUP=/secure/backup/path
export FILE_ORG_WIZ_CORS=false  # Keep disabled in production
```

### 4. Backup Before Organization

The system creates automatic backups when `do_backup: true` is set. Always keep backups in a secure, separate location.

### 5. Restrict File Permissions

Ensure the MCP server runs with minimal required permissions:

```bash
# Create dedicated user for file operations
useradd -r -s /bin/false file-org-wiz

# Set permissions
chown -R file-org-wiz:file-org-wiz /path/to/mount
chmod -R 755 /path/to/mount  # Read/execute only where needed
```

## Known Security Considerations

### Path Validation

The MCP server includes path validation to prevent:
- Path traversal attacks (`../` sequences)
- Access to sensitive system paths (`/etc/passwd`, `/.ssh`, etc.)
- Operations outside allowed base paths

### Input Sanitization

- All user inputs are sanitized before use in file operations
- JSON request bodies are validated
- Special characters are stripped from naming conventions

### What We Don't Do (By Design)

The following are intentional design decisions:

1. **No Authentication**: The server is designed for local use behind a firewall
2. **No Encryption at Rest**: Files are not encrypted; use filesystem-level encryption
3. **No Built-in Rate Limiting**: For production, use a reverse proxy (nginx, etc.)

For production deployments, wrap the server behind a reverse proxy with authentication and rate limiting.

## Vulnerability Categories

### Critical (CVSS 9-10)

- Remote code execution
- Path traversal allowing read/write of system files
- Data exfiltration

### High (CVSS 7-8.9)

- Path traversal in user-controlled paths
- Injection vulnerabilities
- Denial of service

### Medium (CVSS 4-6.9)

- Information disclosure
- Bypass of intended restrictions
- Resource exhaustion

### Low (CVSS 0-3.9)

- Minor information leakage
- Cosmetic security issues

## Security Updates

Security updates are released as patch versions (1.0.x → 1.0.x+1). Major security issues may require minor version updates.

## Credits

Thank you to the security researchers who help improve this project.

---

*Keeping your files organized AND secure.*