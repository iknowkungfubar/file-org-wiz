# MCP Server for File Org Wiz

## Running the MCP Server

### Install Dependencies

```bash
pip install flask
```

### Run the Server

```bash
python mcp_server.py --port 5000 --mount /path/to/mount --backup /path/to/backup
```

### Options

| Flag | Default | Description |
|------|---------|-----------|
| `--port` | 5000 | Port to run server |
| `--host` | 127.0.0.1 | Host to bind (localhost for security) |
| `--mount` | /data | Default mount path |
| `--backup` | /data/backup | Backup location |
| `--vault` | (empty) | Obsidian vault path |
| `--template` | (none) | Template to apply (finance, research, media) |

## MCP Endpoints

### Health Check
```bash
GET /health
```

### Execute Reorganization
```bash
POST /organize
{
  "mount_path": "/path/to/mount",
  "backup_path": "/path/to/backup", 
  "create_vault": true,
  "vault_path": "/path/to/vault"
}
```

### Create Backup
```bash
POST /backup
{
  "source_path": "/path/to/source",
  "backup_path": "/path/to/backup"
}
```

### Get Structure
```bash
GET /structure?path=/path/to/dir&max_depth=3
```

### Get Analytics
```bash
GET /analytics?path=/path/to/mount
```

### Apply Naming Convention
```bash
POST /apply-names
{
  "file_path": "/path/to/file.pdf",
  "context": "project",
  "description": "my-document",
  "version": 1
}
```

### Auto-Describe File
```bash
POST /analyze-file
{
  "file_path": "/path/to/file.pdf"
}
```

### Natural Language Command
```bash
POST /nlp-command
{
  "command": "organize my downloads folder"
}
```

### Get MCP Manifest
```bash
GET /mcp-manifest
```

## Using with AI

To use with an AI that supports MCP:

1. Start the server: `python mcp_server.py`
2. Configure AI to connect to `http://localhost:5000`
3. Use endpoints for file operations