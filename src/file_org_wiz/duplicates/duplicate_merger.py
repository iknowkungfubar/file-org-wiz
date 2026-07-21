"""Duplicate merging functions for file-org-wiz.

This module contains functions for merging duplicate files by
selecting which files to keep and handling the rest according to
a specified strategy.
"""

from __future__ import annotations

import os
import shutil
from datetime import datetime


def get_newest_file(file_list):
    """Get the newest file from a duplicate set based on modification time."""
    newest = None
    newest_time = None

    for f in file_list:
        mod_time = f.get("modified", "")
        if mod_time:
            try:
                dt = datetime.fromisoformat(mod_time)
                if newest_time is None or dt > newest_time:
                    newest = f
                    newest_time = dt
            except (ValueError, OSError):
                continue

    # Fallback to first if no times
    return newest or file_list[0]


def get_oldest_file(file_list):
    """Get the oldest file from a duplicate set."""
    oldest = None
    oldest_time = None

    for f in file_list:
        mod_time = f.get("modified", "")
        if mod_time:
            try:
                dt = datetime.fromisoformat(mod_time)
                if oldest_time is None or dt < oldest_time:
                    oldest = f
                    oldest_time = dt
            except (ValueError, OSError):
                continue

    return oldest or file_list[0]


def merge_duplicates(
    duplicate_group, keep_strategy="newest", archive_path="", dry_run=True
):
    """
    Merge a duplicate file group.

    Args:
        duplicate_group: List of file dictionaries representing duplicates
        keep_strategy: "newest", "oldest", or "first" - which file to keep
        archive_path: Directory to move duplicates to (if empty, delete files)
        dry_run: If True, only preview changes without making them

    Returns:
        dict with keys: kept, archived, deleted, saved_bytes
    """
    if len(duplicate_group) < 2:
        return {
            "kept": None,
            "archived": [],
            "deleted": [],
            "saved_bytes": 0,
        }

    # Determine which to keep
    if keep_strategy == "newest":
        keep = get_newest_file(duplicate_group)
    elif keep_strategy == "oldest":
        keep = get_oldest_file(duplicate_group)
    else:  # "first"
        keep = duplicate_group[0]

    keep_path = getattr(keep, 'get', lambda k, d: None)("path", "")

    archived = []
    deleted = []
    saved_bytes = 0

    for f in duplicate_group:
        path = f.get("path", "")

        if path == keep_path:
            continue

        if archive_path and not dry_run:
            # Move to archive
            try:
                # Handle filename conflicts
                filename = os.path.basename(path)
                counter = 0
                while True:
                    if counter == 0:
                        candidate_path = os.path.join(archive_path, filename)
                    else:
                        name, ext = os.path.splitext(filename)
                        candidate_path = os.path.join(archive_path, f"{name}_dup_{counter}{ext}")
                    
                    if not os.path.exists(candidate_path):
                        break
                    counter += 1
                
                shutil.move(path, candidate_path)
                archived.append(path)
                saved_bytes += f.get("size", 0)
            except OSError:
                # If move fails, try to delete instead
                try:
                    os.remove(path)
                    deleted.append(path)
                    saved_bytes += f.get("size", 0)
                except OSError:
                    pass  # Give up on this file
        else:
            # Just delete (or simulate deletion)
            if dry_run:
                deleted.append(path)  # Preview only
            else:
                try:
                    os.remove(path)
                    deleted.append(path)
                    saved_bytes += f.get("size", 0)
                except OSError:
                    pass  # File might already be gone

    return {
        "kept": getattr(keep, 'get', lambda k, d: None)("path", ""),
        "archived": [],
        "deleted": [],
        "saved_bytes": 0,
    }


def merge_all_duplicates(
    base_path,
    keep_strategy="newest",
    archive_path="",
    by_content=True,
    by_name=True,
    dry_run=True,
):
    """Find and merge all duplicates in a directory."""
    # Import here to avoid circular imports
    from file_org_wiz.duplicates.duplicate_detection import find_all_duplicates

    # Find all duplicate groups
    dup_info = find_all_duplicates(
        base_path, by_content=by_content, by_name=by_name
    )
    
    duplicate_groups = dup_info.get("duplicates", [])

    # Prepare results structure
    results = {
        "base_path": base_path,
        "keep_strategy": keep_strategy,
        "dry_run": dry_run,
        "duplicate_groups": len(duplicate_groups),
        "total_duplicates": sum(len(g) for g in duplicate_groups),
        "merges": [],
        "total_saved_bytes": 0,
    }

    # Process each duplicate group
    for group in duplicate_groups:
        merge_result = merge_duplicates(
            group,
            keep_strategy=keep_strategy,
            archive_path=archive_path,
            dry_run=dry_run,
        )
        results["merges"].append(merge_result)
        results["total_saved_bytes"] += merge_result.get("saved_bytes", 0)

    return results
