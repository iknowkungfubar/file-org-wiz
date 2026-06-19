"""Core file organization logic for file-org-wiz.

Security validation, PARA folder structure creation, backups,
analytics, naming conventions, and directory traversal.
"""

from __future__ import annotations

import os
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

# Import optional scanner and duplicates
try:
    from file_org_wiz.scanner import scan_and_categorize, suggest_category
except ImportError:
    scan_and_categorize = None
    suggest_category = None

try:
    from file_org_wiz.duplicates import find_all_duplicates, merge_all_duplicates
except ImportError:
    find_all_duplicates = None
    merge_all_duplicates = None

# ── Constants ────────────────────────────────────────────────────────────────

PARA_FOLDERS: list[str] = [
    "00_INBOX",
    "01_PROJECTS",
    "02_AREAS",
    "03_RESOURCES",
    "04_ARCHIVE",
    "90_TEMPLATES",
    "99_SYSTEM",
]

PROJECT_SUBDIRS: list[str] = ["01_Projects", "02_Client-Work", "03_Personal"]
AREA_SUBDIRS: list[str] = ["Health", "Finance", "Home", "Learning", "Personal"]
RESOURCE_SUBDIRS: list[str] = [
    "AI",
    "Tech",
    "Career",
    "Development",
    "Media",
    "Reading",
    "Tools",
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

SENSITIVE_PREFIXES: tuple[str, ...] = (
    "/etc",
    "/sys",
    "/proc",
    "/dev",
    "/boot",
    "/root",
    "/.ssh",
    "/.aws",
)


# ── Security ─────────────────────────────────────────────────────────────────


def validate_path(path: str, allow_absolute: bool = True) -> tuple[bool, str]:
    """Validate path to prevent path traversal and sensitive path access."""
    if not path:
        return False, "Path cannot be empty"
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
    except (ValueError, OSError) as e:
        return False, f"Invalid path: {e}"
    clean_path = os.path.normpath(path)
    if ".." in clean_path:
        return False, "Path traversal not allowed"
    for prefix in SENSITIVE_PREFIXES:
        if abs_path == prefix or abs_path.startswith(prefix + "/"):
            return False, f"Access to {prefix} is restricted"
    return True, ""


def safe_join_path(base: str, *paths: str) -> str | None:
    """Safely join paths, return None if result escapes base directory."""
    try:
        joined = os.path.abspath(os.path.join(base, *paths))
        base_abs = os.path.abspath(base)
        if not joined.startswith(base_abs + os.sep) and joined != base_abs:
            return None
        return joined
    except (ValueError, OSError):
        return None


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to alphanumeric, hyphens, underscores, dots only."""
    filename = os.path.basename(filename)
    sanitized = re.sub(r"[^a-zA-Z0-9\-_.]", "", filename)
    return sanitized or "unnamed"


# ── Core Operations ──────────────────────────────────────────────────────────


def create_folder_structure(base_path: str) -> dict[str, list[str]]:
    """Create PARA folder structure at base_path."""
    valid, error = validate_path(base_path)
    if not valid:
        return {"created": [], "errors": [error]}
    created: list[str] = []
    errors: list[str] = []
    for folder in PARA_FOLDERS:
        path = os.path.join(base_path, folder)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except OSError as e:
            errors.append(f"{path}: {e}")
    projects_path = os.path.join(base_path, "01_PROJECTS")
    for sub in PROJECT_SUBDIRS:
        path = os.path.join(projects_path, sub)
        try:
            os.makedirs(path, exist_ok=True)
            created.append(path)
        except OSError as e:
            errors.append(f"{path}: {e}")
    for folder, subdirs in [
        ("02_AREAS", AREA_SUBDIRS),
        ("03_RESOURCES", RESOURCE_SUBDIRS),
    ]:
        base_folder = os.path.join(base_path, folder)
        for sub in subdirs:
            path = os.path.join(base_folder, sub)
            try:
                os.makedirs(path, exist_ok=True)
                created.append(path)
            except OSError as e:
                errors.append(f"{path}: {e}")
    return {"created": created, "errors": errors}


def create_backup(source_path: str, backup_path: str) -> dict[str, Any]:
    """Create timestamped backup of source to destination."""
    valid, error = validate_path(source_path)
    if not valid:
        return {"backup_path": "", "files_copied": [], "errors": [error]}
    valid, error = validate_path(backup_path)
    if not valid:
        return {"backup_path": "", "files_copied": [], "errors": [error]}
    
    # Check that source exists
    if not os.path.isdir(source_path):
        return {"backup_path": "", "files_copied": [], "errors": [f"Source path does not exist: {source_path}"]}
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dest_path = os.path.join(backup_path, f"backup__{timestamp}")
    created: list[str] = []
    errors: list[str] = []
    try:
        os.makedirs(dest_path, exist_ok=True)
        for item in os.listdir(source_path):
            src = os.path.join(source_path, item)
            dst = os.path.join(dest_path, item)
            if os.path.isdir(src):
                try:
                    shutil.copytree(
                        src, dst, symlinks=True, ignore_dangling_symlinks=True
                    )
                    created.append(f"{item}/")
                except OSError as e:
                    errors.append(f"{item}/: {e}")
            else:
                try:
                    shutil.copy2(src, dst)
                    created.append(item)
                except OSError as e:
                    errors.append(f"{item}: {e}")
    except OSError as e:
        errors.append(f"Backup failed: {e}")
    return {"backup_path": dest_path, "files_copied": created, "errors": errors}


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
            errors.append(f"{path}: {exc}")
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
        largest_files.append(
            {
                "path": file_info.get("path", ""),
                "size": file_info.get("size", 0),
                "category": file_info.get("category", ""),
            }
        )
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
    organization_pct = (
        round((para_files / total_files) * 100, 2) if total_files else 0.0
    )
    return {
        "path": base_path,
        "total_files": total_files,
        "total_size_bytes": total_size_bytes,
        "file_types": dict(file_types),
        "category_distribution": categorized.get("summary", {}),
        "top_tags": [
            {"tag": tag, "count": count} for tag, count in tag_counts.most_common(10)
        ],
        "largest_files": largest_files[:5],
        "organization_percentage": organization_pct,
        "duplicates": duplicate_summary,
        "generated_at": datetime.now().isoformat(),
    }


def get_directory_structure(path: str, max_depth: int = 3) -> dict[str, Any]:
    """Get current directory structure with depth limit."""
    valid, error = validate_path(path)
    if not valid:
        return {"error": error}
    structure: list[str] = []
    try:
        for root, dirs, files in os.walk(path):
            rel_root = os.path.relpath(root, path)
            depth = rel_root.count(os.sep) if rel_root != "." else 0
            if depth >= max_depth:
                dirs.clear()
                continue
            indent = " " * 2 * depth
            folder_name = os.path.basename(root) or path
            structure.append(f"{indent}{folder_name}/")
            subindent = " " * 2 * (depth + 1)
            for file in sorted(files)[:10]:
                structure.append(f"{subindent}{file}")
            if len(files) > 10:
                structure.append(f"{subindent}... and {len(files) - 10} more")
    except OSError as e:
        return {"error": str(e)}
    return {"structure": structure, "path": path}


def apply_naming_convention(
    file_path: str, context: str, description: str, version: int = 1
) -> dict[str, Any]:
    """Apply naming convention to a file."""
    valid, error = validate_path(file_path)
    if not valid:
        return {"original": file_path, "error": error, "success": False}
    context = re.sub(r"[^a-z0-9\-]", "", context.lower().replace(" ", "-"))
    description = re.sub(r"[^a-z0-9\-]", "", description.lower().replace(" ", "-"))
    if version < 1:
        version = 1
    try:
        ext = Path(file_path).suffix
        date = datetime.now().strftime("%Y-%m-%d")
        new_name = f"{date}__{context}__{description}__{version:02d}{ext}"
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        return {"original": file_path, "renamed": new_path, "success": True}
    except OSError as e:
        return {"original": file_path, "error": str(e), "success": False}
