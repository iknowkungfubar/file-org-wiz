#!/usr/bin/env python3
"""
File Organization Wizard MCP Server

An MCP (Model Context Protocol) server that provides file organization
capabilities using the PARA + Zettelkasten methodology.

Run: python src/mcp_server.py
Endpoints:
  - GET  /health          - Health check
  - POST /organize        - Execute reorganization
  - POST /backup          - Create backup
  - GET  /structure       - Get current structure
  - GET  /analytics       - Get organization analytics
  - POST /apply-names     - Apply naming conventions
  - GET  /mcp-manifest    - List available tools

SECURITY: Default binding is localhost only. Use --host 0.0.0.0 with caution.
For production: Use behind a reverse proxy with auth and rate limiting.
"""

from __future__ import annotations

import os
import re
import shutil
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

# Import scanner and duplicates modules
try:
    from scanner import scan_and_categorize, suggest_category
except ImportError:
    scan_and_categorize = None
    suggest_category = None

try:
    from duplicates import find_all_duplicates, merge_all_duplicates
except ImportError:
    find_all_duplicates = None
    merge_all_duplicates = None

# Import NLP processor
try:
    from nlp_processor import parse_organization_command, generate_mcp_payload
except ImportError:
    parse_organization_command = None
    generate_mcp_payload = None

try:
    from file_intelligence import infer_context_description, generate_content_tags
except ImportError:
    infer_context_description = None
    generate_content_tags = None

app = Flask(__name__)

# =============================================================================
# Configuration
# =============================================================================

# Enable CORS only if explicitly requested (security)
ENABLE_CORS = os.environ.get("FILE_ORG_WIZ_CORS", "false").lower() == "true"
if ENABLE_CORS:
    CORS(app)

# Default paths (can be overridden via config or CLI args)
MOUNT_PATH = os.environ.get("FILE_ORG_WIZ_MOUNT", "/data")
DOCUMENTS_PATH = os.environ.get("FILE_ORG_WIZ_DOCUMENTS", "/home/user/Documents")
DOWNLOADS_PATH = os.environ.get("FILE_ORG_WIZ_DOWNLOADS", "/home/user/Downloads")
VAULT_PATH = os.environ.get("FILE_ORG_WIZ_VAULT", "")
BACKUP_PATH = os.environ.get("FILE_ORG_WIZ_BACKUP", "/data/backup")

# =============================================================================
# Constants
# =============================================================================

# PARA folders
PARA_FOLDERS: list[str] = [
    "00_INBOX",
    "01_PROJECTS",
    "02_AREAS",
    "03_RESOURCES",
    "04_ARCHIVE",
    "90_TEMPLATES",
    "99_SYSTEM"
]

# Sub-folders by category
PROJECT_SUBDIRS: list[str] = ["01_Projects", "02_Client-Work", "03_Personal"]
AREA_SUBDIRS: list[str] = ["Health", "Finance", "Home", "Learning", "Personal"]
RESOURCE_SUBDIRS: list[str] = [
    "AI", "Tech", "Career", "Development", "Media", "Reading", "Tools"
]

TEMPLATE_STRUCTURES: dict[str, list[str]] = {
    "finance": [
        "02_AREAS/Finance/Invoices",
        "02_AREAS/Finance/Taxes",
        "02_AREAS/Finance/Receipts",
        "03_RESOURCES/Finance/Statements",
    ],
    "research": [
        "03_RESOURCES/Research/Papers",
        "03_RESOURCES/Research/Notes",
        "03_RESOURCES/Research/Datasets",
    ],
    "media": [
        "03_RESOURCES/Media/Images",
        "03_RESOURCES/Media/Video",
        "03_RESOURCES/Media/Audio",
    ],
}

# Dangerous paths that should never be accessible
DANGEROUS_PATHS: set[str] = {
    "/etc/passwd", "/etc/shadow", "/etc/ssh", "/.ssh", "/.aws",
    "/etc/gshadow", "/etc/group", "/etc/shadow", "/etc/security",
    "/proc", "/sys"
}

# =============================================================================
# Security Functions
# =============================================================================

def validate_path(path: str, allow_absolute: bool = True) -> tuple[bool, str]:
    """
    Validate path to prevent path traversal and access to dangerous paths.

    Returns: (is_valid, error_message)
    """
    if not path:
        return False, "Path cannot be empty"

    # Get absolute path
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
    except (ValueError, OSError) as e:
        return False, f"Invalid path: {str(e)}"

    # Check for path traversal attempts in original input
    if ".." in path:
        return False, "Path traversal not allowed"

    # Check for dangerous paths
    for dangerous in DANGEROUS_PATHS:
        if abs_path.startswith(dangerous):
            return False, f"Access to {dangerous} is not allowed"

    # Additional security: reject paths that start with sensitive prefixes
    sensitive_prefixes = ["/etc/", "/sys/", "/proc/", "/dev/"]
    for prefix in sensitive_prefixes:
        if abs_path.startswith(prefix) and not abs_path.startswith("/etc/passwd") == abs_path == "/etc/passwd":
            # Allow /etc by itself but not subdirectories
            if abs_path == prefix.rstrip("/"):
                continue
            if abs_path.startswith(prefix):
                return False, f"Access to {prefix.rstrip('/')} is restricted"

    return True, ""


def safe_join_path(base: str, *paths: str) -> Optional[str]:
    """
    Safely join paths and ensure result is within base directory.

    Returns None if the path would escape the base directory.
    """
    try:
        joined = os.path.abspath(os.path.join(base, *paths))
        base_abs = os.path.abspath(base)

        # Ensure the joined path is within base
        if not joined.startswith(base_abs + os.sep) and joined != base_abs:
            return None
        return joined
    except (ValueError, OSError):
        return None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent injection attacks.

    Only allows alphanumeric, hyphens, underscores, and dots.
    """
    # Remove any path components
    filename = os.path.basename(filename)
    # Only allow safe characters
    sanitized = re.sub(r'[^a-zA-Z0-9\-_.]', '', filename)
    return sanitized or "unnamed"


# =============================================================================
# Core Functions
# =============================================================================

def create_folder_structure(base_path: str) -> dict[str, list[str]]:
    """Create PARA folder structure."""
    # Validate path
    valid, error = validate_path(base_path)
    if not valid:
        return {"created": [], "errors": [error]}

    created: list[str] = []
    errors: list[str] = []

    # Main folders
    for folder in PARA_FOLDERS:
        path = os.path.join(base_path, folder)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except OSError as e:
            errors.append(f"{path}: {str(e)}")

    # Project sub-folders
    projects_path = os.path.join(base_path, "01_PROJECTS")
    for sub in PROJECT_SUBDIRS:
        path = os.path.join(projects_path, sub)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except OSError as e:
            errors.append(f"{path}: {str(e)}")

    # Area sub-folders
    areas_path = os.path.join(base_path, "02_AREAS")
    for sub in AREA_SUBDIRS:
        path = os.path.join(areas_path, sub)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except OSError as e:
            errors.append(f"{path}: {str(e)}")

    # Resource sub-folders
    resources_path = os.path.join(base_path, "03_RESOURCES")
    for sub in RESOURCE_SUBDIRS:
        path = os.path.join(resources_path, sub)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except OSError as e:
            errors.append(f"{path}: {str(e)}")

    return {"created": created, "errors": errors}


def create_backup(source_path: str, backup_path: str) -> dict[str, Any]:
    """Create timestamped backup of source to destination."""
    # Validate paths
    valid, error = validate_path(source_path)
    if not valid:
        return {"backup_path": "", "files_copied": [], "errors": [error]}

    valid, error = validate_path(backup_path)
    if not valid:
        return {"backup_path": "", "files_copied": [], "errors": [error]}

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup__{timestamp}"
    dest_path = os.path.join(backup_path, backup_name)

    created: list[str] = []
    errors: list[str] = []

    try:
        os.makedirs(dest_path, exist_ok=True)

        # Copy contents - only first level
        for item in os.listdir(source_path):
            src = os.path.join(source_path, item)
            dst = os.path.join(dest_path, item)

            if os.path.isdir(src):
                try:
                    shutil.copytree(src, dst, symlinks=True,
                                   ignore_dangling_symlinks=True)
                    created.append(f"{item}/")
                except OSError as e:
                    errors.append(f"{item}/: {str(e)}")
            else:
                try:
                    shutil.copy2(src, dst)
                    created.append(item)
                except OSError as e:
                    errors.append(f"{item}: {str(e)}")

    except OSError as e:
        errors.append(f"Backup failed: {str(e)}")

    return {
        "backup_path": dest_path,
        "files_copied": created,
        "errors": errors
    }


def create_template_structure(base_path: str, template: str) -> dict[str, list[str]]:
    """Create additional folders for a named organization template."""
    valid, error = validate_path(base_path)
    if not valid:
        return {"created": [], "errors": [error]}

    template_paths = TEMPLATE_STRUCTURES.get(template.lower())
    if not template_paths:
        return {"created": [], "errors": [f"Unknown template: {template}"]}

    created: list[str] = []
    errors: list[str] = []
    for relative_path in template_paths:
        path = os.path.join(base_path, relative_path)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except OSError as exc:
            errors.append(f"{path}: {str(exc)}")

    return {"created": created, "errors": errors}


def create_analytics_report(base_path: str) -> dict[str, Any]:
    """Generate analytics for a directory tree."""
    valid, error = validate_path(base_path)
    if not valid:
        return {"error": error}

    file_types: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    largest_files: list[dict[str, Any]] = []
    para_files = 0
    total_size_bytes = 0

    categorized = {"files": [], "summary": {}}
    if scan_and_categorize:
        categorized = scan_and_categorize(base_path, use_date=True)

    for file_info in categorized.get("files", []):
        extension = file_info.get("extension", "") or "no_extension"
        file_types[extension] += 1
        total_size_bytes += int(file_info.get("size", 0))
        relative_path = os.path.relpath(file_info.get("path", ""), base_path)
        top_level = relative_path.split(os.sep, 1)[0] if relative_path else ""
        if top_level in PARA_FOLDERS:
            para_files += 1
        for tag in file_info.get("tags", []):
            tag_counts[tag] += 1
        largest_files.append({
            "path": file_info.get("path", ""),
            "size": file_info.get("size", 0),
            "category": file_info.get("category", ""),
        })

    largest_files.sort(key=lambda item: item["size"], reverse=True)

    duplicate_summary = {
        "duplicate_groups": 0,
        "total_duplicates": 0,
        "total_wasted_bytes": 0,
    }
    if find_all_duplicates:
        duplicates = find_all_duplicates(base_path, by_content=True, by_name=True)
        duplicate_summary = {
            "duplicate_groups": duplicates.get("duplicate_groups", 0),
            "total_duplicates": duplicates.get("total_duplicates", 0),
            "total_wasted_bytes": duplicates.get("total_wasted_bytes", 0),
        }

    total_files = categorized.get("total_files", 0)
    organization_percentage = round((para_files / total_files) * 100, 2) if total_files else 0.0

    return {
        "path": base_path,
        "total_files": total_files,
        "total_size_bytes": total_size_bytes,
        "file_types": dict(file_types),
        "category_distribution": categorized.get("summary", {}),
        "top_tags": [{"tag": tag, "count": count} for tag, count in tag_counts.most_common(10)],
        "largest_files": largest_files[:5],
        "organization_percentage": organization_percentage,
        "duplicates": duplicate_summary,
        "generated_at": datetime.now().isoformat(),
    }


def get_directory_structure(path: str, max_depth: int = 3) -> dict[str, Any]:
    """Get current directory structure with depth limit."""
    # Validate path
    valid, error = validate_path(path)
    if not valid:
        return {"error": error}

    structure: list[str] = []

    try:
        # Limit depth to prevent infinite recursion
        for root, dirs, files in os.walk(path):
            # Calculate depth
            rel_root = os.path.relpath(root, path)
            depth = rel_root.count(os.sep) if rel_root != '.' else 0

            if depth >= max_depth:
                dirs.clear()  # Don't descend further
                continue

            level = depth
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root) or path
            structure.append(f"{indent}{folder_name}/")

            subindent = ' ' * 2 * (level + 1)
            # Limit files per directory
            for file in sorted(files)[:10]:
                structure.append(f"{subindent}{file}")
            if len(files) > 10:
                structure.append(f"{subindent}... and {len(files) - 10} more")
    except OSError as e:
        return {"error": str(e)}

    return {"structure": structure, "path": path}


def apply_naming_convention(
    file_path: str,
    context: str,
    description: str,
    version: int = 1
) -> dict[str, Any]:
    """Apply naming convention to a file."""
    # Validate path
    valid, error = validate_path(file_path)
    if not valid:
        return {"original": file_path, "error": error, "success": False}

    # Sanitize inputs - only allow safe characters
    context = re.sub(r'[^a-z0-9\-]', '', context.lower().replace(' ', '-'))
    description = re.sub(r'[^a-z0-9\-]', '', description.lower().replace(' ', '-'))

    # Validate version is a positive integer
    if version < 1:
        version = 1

    try:
        ext = Path(file_path).suffix
        date = datetime.now().strftime("%Y-%m-%d")
        new_name = f"{date}__{context}__{description}__{version:02d}{ext}"
        dir_path = os.path.dirname(file_path)
        new_path = os.path.join(dir_path, new_name)

        os.rename(file_path, new_path)

        return {
            "original": file_path,
            "renamed": new_path,
            "success": True
        }
    except OSError as e:
        return {
            "original": file_path,
            "error": str(e),
            "success": False
        }


# =============================================================================
# MCP Endpoints
# =============================================================================

@app.route("/health", methods=["GET"])
def health_check() -> Response:
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "file-org-wiz-mcp",
        "version": "1.3.0"
    })


@app.route("/organize", methods=["POST"])
def organize() -> tuple[Response, int]:
    """
    Execute full reorganization.

    POST body:
    {
        "mount_path": "/path/to/mount",
        "backup_path": "/path/to/backup",
        "create_vault": true/false,
        "vault_path": "/path/to/vault",
        "do_backup": true/false,
        "template": "finance|research|media",
        "dry_run": true/false
    }
    """
    data: dict[str, Any] = request.json or {}

    # Get paths from request
    mount = data.get("mount_path", MOUNT_PATH)
    backup = data.get("backup_path", BACKUP_PATH)
    create_vault = bool(data.get("create_vault", False))
    vault = data.get("vault_path", VAULT_PATH)
    do_backup = bool(data.get("do_backup", True))
    dry_run = bool(data.get("dry_run", False))
    template = data.get("template")

    # Validate paths
    valid, error = validate_path(mount)
    if not valid:
        return jsonify({"error": f"Invalid mount_path: {error}"}), 400

    valid, error = validate_path(backup)
    if not valid:
        return jsonify({"error": f"Invalid backup_path: {error}"}), 400

    result: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "mount_path": mount,
        "dry_run": dry_run,
        "phases": [],
        "suggested_actions": []
    }

    # Phase 1: Backup (optional, skip in dry-run)
    if do_backup and not dry_run:
        backup_result = create_backup(mount, backup)
        result["phases"].append({
            "name": "backup",
            "status": "complete",
            "backup_path": backup_result["backup_path"],
            "files_copied": len(backup_result["files_copied"]),
            "errors": backup_result.get("errors", [])
        })

    # Phase 2: Scan and Categorize (if dry_run, this is the main phase)
    categorize_result = {"files_scanned": 0, "categorized": [], "summary": {}}
    if scan_and_categorize:
        categorize_result = scan_and_categorize(mount, use_date=False)
        result["phases"].append({
            "name": "scan_and_categorize",
            "status": "complete",
            "files_scanned": categorize_result["total_files"],
            "summary": categorize_result["summary"]
        })
        
        # Generate suggested actions for dry-run
        if dry_run:
            for f in categorize_result["files"]:
                fpath = f.get("path", "")
                fcategory = f.get("category", "")
                result["suggested_actions"].append({
                    "action": "categorize",
                    "from": fpath,
                    "to": os.path.join(mount, fcategory),
                    "reason": f.get("reason", ""),
                    "confidence": f.get("confidence", ""),
                    "tags": f.get("tags", []),
                    "suggested_name": f.get("suggested_name", "")
                })
    
    # Phase 3: Structure (skip in dry-run as it's just folder creation)
    if not dry_run:
        structure_result = create_folder_structure(mount)
        result["phases"].append({
            "name": "create_structure",
            "status": "complete",
            "folders_created": len(structure_result["created"]),
            "errors": structure_result.get("errors", [])
        })

        if template:
            template_result = create_template_structure(mount, template)
            result["phases"].append({
                "name": "apply_template",
                "status": "complete" if not template_result.get("errors") else "failed",
                "template": template,
                "folders_created": len(template_result["created"]),
                "errors": template_result.get("errors", []),
            })

    # Phase 3: Vault (optional, skip in dry-run)
    if create_vault and vault and not dry_run:
        valid, error = validate_path(vault)
        if valid:
            vault_result = create_folder_structure(vault)
            result["phases"].append({
                "name": "create_vault",
                "status": "complete",
                "vault_path": vault,
                "folders_created": len(vault_result["created"])
            })
        else:
            result["phases"].append({
                "name": "create_vault",
                "status": "failed",
                "error": error
            })

    # Phase 4: Duplicate Detection (optional)
    if find_all_duplicates and not dry_run:
        dup_result = find_all_duplicates(mount, by_content=True, by_name=True)
        result["phases"].append({
            "name": "find_duplicates",
            "status": "complete",
            "duplicate_groups": dup_result.get("duplicate_groups", 0),
            "total_duplicates": dup_result.get("total_duplicates", 0),
            "total_wasted_bytes": dup_result.get("total_wasted_bytes", 0),
            "errors": dup_result.get("errors", [])
        })
        
        # Generate suggested actions for duplicates (dry_run simulation)
        if dry_run:
            for group in dup_result.get("duplicates", []):
                result["suggested_actions"].append({
                    "action": "merge_duplicates",
                    "from": [f.get("path") for f in group],
                    "to": group[0].get("path"),  # Keep newest
                    "reason": "content duplicate - keep newest",
                })

    result["status"] = "complete"
    return jsonify(result), 200


@app.route("/backup", methods=["POST"])
def create_backup_endpoint() -> tuple[Response, int]:
    """Create backup endpoint."""
    data = request.json or {}

    source = data.get("source_path", MOUNT_PATH)
    dest = data.get("backup_path", BACKUP_PATH)

    # Validate paths
    valid, error = validate_path(source)
    if not valid:
        return jsonify({"error": f"Invalid source_path: {error}"}), 400

    valid, error = validate_path(dest)
    if not valid:
        return jsonify({"error": f"Invalid backup_path: {error}"}), 400

    result = create_backup(source, dest)
    return jsonify(result), 200


@app.route("/structure", methods=["GET"])
def structure_endpoint() -> tuple[Response, int]:
    """Get current structure."""
    path = request.args.get("path", MOUNT_PATH)
    depth = request.args.get("max_depth", "3")

    # Validate path
    valid, error = validate_path(path)
    if not valid:
        return jsonify({"error": f"Invalid path: {error}"}), 400

    try:
        max_depth = min(int(depth), 5)  # Cap at 5
    except ValueError:
        max_depth = 3

    return jsonify(get_directory_structure(path, max_depth)), 200


@app.route("/analytics", methods=["GET"])
def analytics_endpoint() -> tuple[Response, int]:
    """Get file organization analytics for a directory."""
    path = request.args.get("path", MOUNT_PATH)

    valid, error = validate_path(path)
    if not valid:
        return jsonify({"error": f"Invalid path: {error}"}), 400

    return jsonify(create_analytics_report(path)), 200


@app.route("/apply-names", methods=["POST"])
def apply_names_endpoint() -> tuple[Response, int]:
    """
    Apply naming convention.
    
    POST body:
    {
        "file_path": "/path/to/file",
        "context": "project-name",
        "description": "what-it-is",
        "version": 1
    }
    """
    data = request.json or {}

    file_path = data.get("file_path")
    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    # Validate path
    valid, error = validate_path(file_path)
    if not valid:
        return jsonify({"error": f"Invalid file_path: {error}"}), 400

    # Check file exists
    if not os.path.isfile(file_path):
        return jsonify({"error": "File does not exist"}), 400

    # Get version and ensure it's an integer
    version = data.get("version", 1)
    try:
        version = int(version)
    except (ValueError, TypeError):
        version = 1

    context = data.get("context", "file")
    description = data.get("description", "document")

    if bool(data.get("auto_describe", False)) and infer_context_description:
        inferred_context, inferred_description = infer_context_description(file_path)
        context = inferred_context or context
        description = inferred_description or description

    result = apply_naming_convention(
        file_path,
        context,
        description,
        version
    )

    if result.get("success") and generate_content_tags:
        result["tags"] = generate_content_tags(result["renamed"])

    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/analyze-file", methods=["POST"])
def analyze_file_endpoint() -> tuple[Response, int]:
    """Return auto-generated tags and a suggested smart filename for a file."""
    data = request.json or {}
    file_path = data.get("file_path")
    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    valid, error = validate_path(file_path)
    if not valid:
        return jsonify({"error": f"Invalid file_path: {error}"}), 400

    if not os.path.isfile(file_path):
        return jsonify({"error": "File does not exist"}), 400

    context = "file"
    description = Path(file_path).stem
    if infer_context_description:
        context, description = infer_context_description(file_path)

    suggested_name = ""
    if generate_content_tags:
        tags = generate_content_tags(file_path)
    else:
        tags = []

    try:
        from file_intelligence import suggest_smart_filename
        suggested_name = suggest_smart_filename(file_path)
    except ImportError:
        suggested_name = Path(file_path).name

    return jsonify({
        "file_path": file_path,
        "context": context,
        "description": description,
        "tags": tags,
        "suggested_name": suggested_name,
    }), 200


@app.route("/nlp-command", methods=["POST"])
def nlp_command_endpoint() -> tuple[Response, int]:
    """
    Process natural language file organization commands.
    
    POST body:
    {
        "command": "organize my downloads folder"
    }
    """
    if not parse_organization_command:
        return jsonify({"error": "NLP processing not available"}), 503
    
    data = request.json or {}
    command = data.get("command", "")
    
    if not command:
        return jsonify({"error": "command is required"}), 400
    
    # Parse the natural language command
    parsed = parse_organization_command(command)
    
    # Generate MCP payload
    payload = generate_mcp_payload(parsed)
    
    # If this is an organize command, we can execute it directly
    if parsed.get("action") == "organize" and payload.get("mount_path"):
        # Execute the organize function with our parsed parameters
        # We'll reuse the organize endpoint logic but with our parsed data
        
        # Get paths from parsed payload
        mount = payload.get("mount_path", MOUNT_PATH)
        backup = data.get("backup_path", BACKUP_PATH)  # Still allow override
        create_vault = bool(data.get("create_vault", False))
        vault = data.get("vault_path", VAULT_PATH)
        do_backup = bool(data.get("do_backup", True))
        dry_run = payload.get("dry_run", False)
        template = data.get("template")
        
        # Validate paths
        valid, error = validate_path(mount)
        if not valid:
            return jsonify({"error": f"Invalid mount_path: {error}"}), 400
        
        valid, error = validate_path(backup)
        if not valid:
            return jsonify({"error": f"Invalid backup_path: {error}"}), 400
        
        result: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "mount_path": mount,
            "original_command": command,
            "parsed_command": parsed,
            "dry_run": dry_run,
            "phases": [],
            "suggested_actions": []
        }
        
        # Phase 1: Backup (optional, skip in dry-run)
        if do_backup and not dry_run:
            backup_result = create_backup(mount, backup)
            result["phases"].append({
                "name": "backup",
                "status": "complete",
                "backup_path": backup_result["backup_path"],
                "files_copied": len(backup_result["files_copied"]),
                "errors": backup_result.get("errors", [])
            })
        
        # Phase 2: Scan and Categorize (if dry_run, this is the main phase)
        categorize_result = {"files_scanned": 0, "categorized": [], "summary": {}}
        if scan_and_categorize:
            # Apply filters from parsed command if any
            use_date = True  # Default
            if parsed.get("filters", {}).get("date_range"):
                use_date = True  # We'll use date filtering if specified
            
            categorize_result = scan_and_categorize(mount, use_date=use_date)
            result["phases"].append({
                "name": "scan_and_categorize",
                "status": "complete",
                "files_scanned": categorize_result["total_files"],
                "summary": categorize_result["summary"]
            })
            
            # Generate suggested actions for dry-run
            if dry_run:
                for f in categorize_result["files"]:
                    fpath = f.get("path", "")
                    fcategory = f.get("category", "")
                    result["suggested_actions"].append({
                        "action": "categorize",
                        "from": fpath,
                        "to": os.path.join(mount, fcategory),
                        "reason": f.get("reason", ""),
                        "confidence": f.get("confidence", ""),
                        "tags": f.get("tags", []),
                        "suggested_name": f.get("suggested_name", "")
                    })
        
        # Phase 3: Structure (skip in dry-run as it's just folder creation)
        if not dry_run:
            structure_result = create_folder_structure(mount)
            result["phases"].append({
                "name": "create_structure",
                "status": "complete",
                "folders_created": len(structure_result["created"]),
                "errors": structure_result.get("errors", [])
            })

            if template:
                template_result = create_template_structure(mount, template)
                result["phases"].append({
                    "name": "apply_template",
                    "status": "complete" if not template_result.get("errors") else "failed",
                    "template": template,
                    "folders_created": len(template_result["created"]),
                    "errors": template_result.get("errors", []),
                })
        
        # Phase 3: Vault (optional, skip in dry-run)
        if create_vault and vault and not dry_run:
            valid, error = validate_path(vault)
            if valid:
                vault_result = create_folder_structure(vault)
                result["phases"].append({
                    "name": "create_vault",
                    "status": "complete",
                    "vault_path": vault,
                    "folders_created": len(vault_result["created"])
                })
            else:
                result["phases"].append({
                    "name": "create_vault",
                    "status": "failed",
                    "error": error
                })
        
        # Phase 4: Duplicate Detection (optional)
        if find_all_duplicates and not dry_run:
            dup_result = find_all_duplicates(mount, by_content=True, by_name=True)
            result["phases"].append({
                "name": "find_duplicates",
                "status": "complete",
                "duplicate_groups": dup_result.get("duplicate_groups", 0),
                "total_duplicates": dup_result.get("total_duplicates", 0),
                "total_wasted_bytes": dup_result.get("total_wasted_bytes", 0),
                "errors": dup_result.get("errors", [])
            })
            
            # Generate suggested actions for duplicates (dry_run simulation)
            if dry_run:
                for group in dup_result.get("duplicates", []):
                    result["suggested_actions"].append({
                        "action": "merge_duplicates",
                        "from": [f.get("path") for f in group],
                        "to": group[0].get("path"),  # Keep newest
                        "reason": "content duplicate - keep newest",
                    })
        
        result["status"] = "complete"
        return jsonify(result), 200
    
    # For other actions or if we can't execute directly, return the parsed command
    return jsonify({
        "status": "parsed",
        "original_command": command,
        "parsed_command": parsed,
        "suggested_mcp_payload": payload,
        "message": "Command parsed successfully. Use the organize endpoint to execute."
    }), 200


@app.route("/mcp-manifest", methods=["GET"])
def mcp_manifest() -> Response:
    """MCP manifest - tools available."""
    return jsonify({
        "name": "file-org-wiz",
        "version": "1.3.0",
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
                        "vault_path": {"type": "string"},
                        "do_backup": {"type": "boolean"},
                        "template": {"type": "string"}
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
                        "path": {"type": "string"},
                        "max_depth": {"type": "integer"}
                    }
                }
            },
            {
                "name": "analytics",
                "description": "Get file organization analytics and dashboard metrics",
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
                        "version": {"type": "integer"},
                        "auto_describe": {"type": "boolean"}
                    }
                }
            },
            {
                "name": "analyze_file",
                "description": "Generate tags and a smart filename suggestion for a file",
                "input": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"}
                    }
                }
            },
            {
                "name": "nlp_command",
                "description": "Process natural language file organization commands",
                "input": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"}
                    }
                }
            }
        ]
    })


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="File Org Wiz MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Security Notes:
  - Default binding is localhost only (127.0.0.1)
  - CORS is disabled by default
  - All paths are validated to prevent traversal attacks

For Production:
  - Use behind a reverse proxy (nginx, etc.)
  - Add authentication at the proxy level
  - Enable rate limiting at the proxy level
  - Use HTTPS in production
        """
    )
    parser.add_argument(
        "--port", type=int, default=5000,
        help="Port to run server (default: 5000)"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1",
        help="Host to bind (default: 127.0.0.1 for security)"
    )
    parser.add_argument(
        "--mount", type=str, default=MOUNT_PATH,
        help="Default mount path"
    )
    parser.add_argument(
        "--backup", type=str, default=BACKUP_PATH,
        help="Default backup path"
    )
    parser.add_argument(
        "--vault", type=str, default=VAULT_PATH,
        help="Default vault path"
    )
    parser.add_argument(
        "--cors", action="store_true",
        help="Enable CORS (use with caution - security risk)"
    )

    args = parser.parse_args()

    # Enable CORS if requested
    if args.cors:
        CORS(app)
        print("WARNING: CORS is enabled. This is a security risk for production.")

    # Override defaults
    MOUNT_PATH = args.mount
    BACKUP_PATH = args.backup
    VAULT_PATH = args.vault

    print("=" * 60)
    print("File Org Wiz MCP Server")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Mount path: {MOUNT_PATH}")
    print(f"Backup path: {BACKUP_PATH}")
    print(f"Vault path: {VAULT_PATH or '(not set)'}")
    print(f"CORS: {'ENABLED (WARNING)' if args.cors else 'disabled'}")
    print("=" * 60)
    print()
    print("SECURITY: Server binds to localhost by default.")
    print("Use --host 0.0.0.0 only if you need network access.")
    print("For production, use behind a reverse proxy with auth.")
    print()

    # Security: Disable debug mode in production
    app.run(
        host=args.host,
        port=args.port,
        debug=False
    )
