"""Analytics, directory structure, and naming conventions for file-org-wiz.

Generates analytics reports for directory trees, walks directory structures,
and applies naming conventions to individual files.
"""

from __future__ import annotations

import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from file_org_wiz.core.operations import PARA_FOLDERS
from file_org_wiz.core.security import validate_path

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
