"""Utility functions for duplicate handling in file-org-wiz.

This module contains helper functions for formatting and reporting
on duplicate file operations.
"""

from __future__ import annotations


def format_bytes(size):
    """Format bytes to human readable (e.g., 1024 -> '1.0 KB')."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def generate_duplicate_report(duplicate_info):
    """Generate a formatted text report of duplicate findings."""
    lines = [
        "=" * 60,
        "DUPLICATE FILE REPORT",
        "=" * 60,
        f"Base Path: {duplicate_info.get('base_path', 'Unknown')}",
        f"Total Files: {duplicate_info.get('total_files', 0)}",
        f"Duplicate Groups: {duplicate_info.get('duplicate_groups', 0)}",
        f"Total Duplicates: {duplicate_info.get('total_duplicates', 0)}",
        f"Wasted Space: {format_bytes(duplicate_info.get('total_wasted_bytes', 0))}",
        "",
    ]

    duplicates = duplicate_info.get("duplicates", [])
    for i, group in enumerate(duplicates, 1):
        lines.append(f"Group {i}:")
        for f in group:
            path = f.get("path", "Unknown")
            size = f.get("size", 0)
            mod = f.get("modified", "Unknown")
            lines.append(f"  - {path} ({format_bytes(size)}, {mod})")
        lines.append("")  # Blank line between groups

    return "
".join(lines)