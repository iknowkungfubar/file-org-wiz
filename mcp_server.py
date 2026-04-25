#!/usr/bin/env python3
"""
File Organization Wizard MCP Server

An MCP (Model Context Protocol) server that provides file organization
capabilities using the PARA + Zettelkasten methodology.

Run: python mcp_server.py
Endpoints:
  - GET  /health          - Health check
  - POST /organize       - Execute reorganization
  - POST /backup       - Create backup
  - GET  /structure    - Get current structure
  - POST /apply-names  - Apply naming conventions
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from flask import Flask, request, jsonify

app = Flask(__name__)

# Default paths (can be overridden via config)
MOUNT_PATH = os.environ.get("MOUNT_PATH", "/data")
DOCUMENTS_PATH = os.environ.get("DOCUMENTS_PATH", "/home/user/Documents")
DOWNLOADS_PATH = os.environ.get("DOWNLOADS_PATH", "/home/user/Downloads")
VAULT_PATH = os.environ.get("VAULT_PATH", "")
BACKUP_PATH = os.environ.get("BACKUP_PATH", "/data/backup")

# PARA folders
PARA_FOLDERS = [
    "00_INBOX",
    "01_PROJECTS", 
    "02_AREAS",
    "03_RESOURCES",
    "04_ARCHIVE",
    "90_TEMPLATES",
    "99_SYSTEM"
]

# Sub-folders by category
PROJECT_SUBDIRS = ["01_Projects", "02_Client-Work", "03_Personal"]
AREA_SUBDIRS = ["Health", "Finance", "Home", "Learning", "Personal"]
RESOURCE_SUBDIRS = ["AI", "Tech", "Career", "Development", "Media", "Reading", "Tools"]


def create_folder_structure(base_path: str) -> dict:
    """Create PARA folder structure"""
    created = []
    errors = []
    
    # Main folders
    for folder in PARA_FOLDERS:
        path = os.path.join(base_path, folder)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except Exception as e:
            errors.append(f"{path}: {str(e)}")
    
    # Project sub-folders
    projects_path = os.path.join(base_path, "01_PROJECTS")
    for sub in PROJECT_SUBDIRS:
        path = os.path.join(projects_path, sub)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except Exception as e:
            errors.append(f"{path}: {str(e)}")
    
    # Area sub-folders
    areas_path = os.path.join(base_path, "02_AREAS")
    for sub in AREA_SUBDIRS:
        path = os.path.join(areas_path, sub)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except Exception as e:
            errors.append(f"{path}: {str(e)}")
    
    # Resource sub-folders
    resources_path = os.path.join(base_path, "03_RESOURCES")
    for sub in RESOURCE_SUBDIRS:
        path = os.path.join(resources_path, sub)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except Exception as e:
            errors.append(f"{path}: {str(e)}")
    
    return {"created": created, "errors": errors}


def create_backup(source_path: str, backup_path: str) -> dict:
    """Create timestamped backup"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup__{timestamp}"
    dest_path = os.path.join(backup_path, backup_name)
    
    created = []
    errors = []
    
    try:
        os.makedirs(dest_path, exist_ok=True)
        
        # Copy contents
        for item in os.listdir(source_path):
            src = os.path.join(source_path, item)
            dst = os.path.join(dest_path, item)
            
            if os.path.isdir(src):
                try:
                    shutil.copytree(src, dst)
                    created.append(f"{item}/")
                except Exception as e:
                    errors.append(f"{item}/: {str(e)}")
            else:
                try:
                    shutil.copy2(src, dst)
                    created.append(item)
                except Exception as e:
                    errors.append(f"{item}: {str(e)}")
                    
    except Exception as e:
        errors.append(f"Backup failed: {str(e)}")
    
    return {
        "backup_path": dest_path,
        "files_copied": created,
        "errors": errors
    }


def get_directory_structure(path: str) -> dict:
    """Get current directory structure"""
    structure = []
    
    try:
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root) or path
            structure.append(f"{indent}{folder_name}/")
            
            subindent = ' ' * 2 * (level + 1)
            for file in sorted(files)[:10]:  # Limit files shown
                structure.append(f"{subindent}{file}")
            if len(files) > 10:
                structure.append(f"{subindent}... and {len(files) - 10} more")
    except Exception as e:
        return {"error": str(e)}
    
    return {"structure": structure, "path": path}


def apply_naming_convention(
    file_path: str, 
    context: str, 
    description: str,
    version: int = 1
) -> dict:
    """Apply naming convention to a file"""
    try:
        ext = Path(file_path).suffix
        date = datetime.now().strftime("%Y-%m-%d")
        new_name = f"{date}__{context}__{description}__v{version:02d}{ext}"
        dir_path = os.path.dirname(file_path)
        new_path = os.path.join(dir_path, new_name)
        
        os.rename(file_path, new_path)
        
        return {
            "original": file_path,
            "renamed": new_path,
            "success": True
        }
    except Exception as e:
        return {
            "original": file_path,
            "error": str(e),
            "success": False
        }


# ============ MCP Endpoints ============

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "file-org-wiz-mcp",
        "version": "1.0.0"
    })


@app.route("/organize", methods=["POST"])
def organize():
    """
    Execute full reorganization
    
    POST body:
    {
        "mount_path": "/path/to/mount",
        "backup_path": "/path/to/backup",
        "create_vault": true/false,
        "vault_path": "/path/to/vault",
        "migrate_files": true/false
    }
    """
    data = request.json or {}
    
    mount = data.get("mount_path", MOUNT_PATH)
    backup = data.get("backup_path", BACKUP_PATH)
    create_vault = data.get("create_vault", False)
    vault = data.get("vault_path", VAULT_PATH)
    migrate = data.get("migrate_files", False)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "mount_path": mount,
        "phases": []
    }
    
    # Phase 1: Backup
    if data.get("do_backup", True):
        backup_result = create_backup(mount, backup)
        result["phases"].append({
            "name": "backup",
            "status": "complete",
            "backup_path": backup_result["backup_path"],
            "files_copied": len(backup_result["files_copied"]),
            "errors": backup_result.get("errors", [])
        })
    
    # Phase 2: Structure
    structure_result = create_folder_structure(mount)
    result["phases"].append({
        "name": "create_structure",
        "status": "complete",
        "folders_created": len(structure_result["created"]),
        "errors": structure_result.get("errors", [])
    })
    
    # Phase 3: Vault (optional)
    if create_vault and vault:
        vault_result = create_folder_structure(vault)
        result["phases"].append({
            "name": "create_vault",
            "status": "complete",
            "vault_path": vault,
            "folders_created": len(vault_result["created"])
        })
    
    result["status"] = "complete"
    return jsonify(result)


@app.route("/backup", methods=["POST"])
def create_backup_endpoint():
    """Create backup endpoint"""
    data = request.json or {}
    
    source = data.get("source_path", MOUNT_PATH)
    dest = data.get("backup_path", BACKUP_PATH)
    
    result = create_backup(source, dest)
    return jsonify(result)


@app.route("/structure", methods=["GET"])
def structure_endpoint():
    """Get current structure"""
    path = request.args.get("path", MOUNT_PATH)
    return jsonify(get_directory_structure(path))


@app.route("/apply-names", methods=["POST"])
def apply_names_endpoint():
    """
    Apply naming convention
    
    POST body:
    {
        "file_path": "/path/to/file",
        "context": "project-name",
        "description": "what-it-is",
        "version": 1
    }
    """
    data = request.json or {}
    
    result = apply_naming_convention(
        data["file_path"],
        data.get("context", "file"),
        data.get("description", "document"),
        data.get("version", 1)
    )
    
    return jsonify(result)


@app.route("/mcp-manifest", methods=["GET"])
def mcp_manifest():
    """MCP manifest - tools available"""
    return jsonify({
        "name": "file-org-wiz",
        "version": "1.0.0",
        "tools": [
            {
                "name": "organize",
                "description": "Execute full file reorganization with PARA structure",
                "input": {
                    "type": "object",
                    "properties": {
                        "mount_path": {"type": "string"},
                        "backup_path": {"type": "string"},
                        "create_vault": {"type": "boolean"},
                        "vault_path": {"type": "string"}
                    }
                }
            },
            {
                "name": "backup",
                "description": "Create timestamped backup of directory",
                "input": {
                    "type": "object", 
                    "properties": {
                        "source_path": {"type": "string"},
                        "backup_path": {"type": "string"}
                    }
                }
            },
            {
                "name": "structure",
                "description": "Get current directory structure",
                "input": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    }
                }
            },
            {
                "name": "apply_names",
                "description": "Apply naming convention to file",
                "input": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"},
                        "context": {"type": "string"},
                        "description": {"type": "string"},
                        "version": {"type": "integer"}
                    }
                }
            }
        ]
    })


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="File Org Wiz MCP Server")
    parser.add_argument("--port", type=int, default=5000, help="Port to run server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind")
    parser.add_argument("--mount", type=str, default=MOUNT_PATH, help="Default mount path")
    parser.add_argument("--backup", type=str, default=BACKUP_PATH, help="Default backup path")
    parser.add_argument("--vault", type=str, default=VAULT_PATH, help="Default vault path")
    
    args = parser.parse_args()
    
    # Override defaults
    MOUNT_PATH = args.mount
    BACKUP_PATH = args.backup
    VAULT_PATH = args.vault
    
    print(f"Starting File Org Wiz MCP Server...")
    print(f"Mount path: {MOUNT_PATH}")
    print(f"Backup path: {BACKUP_PATH}")
    print(f"Vault path: {VAULT_PATH or '(not set)'}")
    
    app.run(host=args.host, port=args.port)