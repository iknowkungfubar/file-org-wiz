# Duplicate detection and merge module

from __future__ import annotations

import os
import hashlib
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict, List
from collections import defaultdict


# =============================================================================
# Duplicate Detection
# =============================================================================


def find_duplicates_by_size(files):
    """Initial filtering by file size - only same size can be duplicates."""
    size_groups = defaultdict(list)
    
    for f in files:
        size = f.get("size", 0)
        if size > 0:  # Exclude empty files
            size_groups[size].append(f)
    
    # Return only groups with potential duplicates
    return {
        size: file_list for size, file_list in size_groups.items()
        if len(file_list) > 1
    }


def quick_hash_file(file_path):
    """Quick hash - first and last 4KB for fast preliminary check."""
    try:
        file_size = os.path.getsize(file_path)
        
        hash_func = hashlib.md5()
        
        with open(file_path, "rb") as f:
            # First 4KB
            hash_func.update(f.read(4096))
            
            # Last 4KB if file is large enough
            if file_size > 8192:
                f.seek(-4096, 2)
                hash_func.update(f.read(4096))
        
        return hash_func.hexdigest()
    except (OSError, IOError):
        return ""


def full_hash_file(file_path, algorithm="sha256"):
    """Full content hash for accurate duplicate detection."""
    try:
        hash_func = hashlib.new(algorithm)
        
        with open(file_path, "rb") as f:
            while chunk := f.read(131072):  # 128KB chunks
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    except (OSError, IOError):
        return ""


def find_duplicates_by_hash(file_group):
    """Find true duplicates by content hash."""
    # Quick hash groups
    quick_groups = defaultdict(list)
    
    for f in file_group:
        path = f.get("path", "")
        if path:
            qhash = quick_hash_file(path)
            if qhash:
                quick_groups[qhash].append(f)
    
    # Verify with full hash
    duplicates = []
    
    for qhash, candidates in quick_groups.items():
        if len(candidates) > 1:
            # Full hash check
            full_groups = defaultdict(list)
            
            for f in candidates:
                path = f.get("path", "")
                if path:
                    fhash = full_hash_file(path)
                    if fhash:
                        full_groups[fhash].append(f)
            
            # Add confirmed duplicate groups
            for fhash, files in full_groups.items():
                if len(files) > 1:
                    duplicates.append(files)
    
    return duplicates


def find_duplicates_by_name_similarity(file_list, threshold=0.8):
    """Find duplicates by filename similarity."""
    def normalize(name):
        """Remove dates, versions for comparison."""
        # Remove YYYY-MM-DD dates
        name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
        # Remove vNN version
        name = re.sub(r'v\d+', '', name)
        # Remove case differences
        name = name.lower()
        # Remove extensions
        name = Path(name).stem
        # Remove special chars
        name = re.sub(r'[^a-z0-9]', '', name)
        return name
    
    name_groups = defaultdict(list)
    
    for f in file_list:
        name = f.get("name", "")
        normalized = normalize(name)
        if normalized:
            name_groups[normalized].append(f)
    
    # Return groups with potential matches
    return [files for files in name_groups.values() if len(files) > 1]


def find_all_duplicates(base_path, by_content=True, by_name=True):
    """Find all duplicates in a directory."""
    from scanner import scan_files_recursive
    
    # Scan all files
    files = scan_files_recursive(base_path)
    
    # Group by size
    size_groups = find_duplicates_by_size(files)
    
    all_duplicates = []
    total_wasted = 0
    
    if by_content:
        # For each size group, find content duplicates
        for size, file_group in size_groups.items():
            dupes = find_duplicates_by_hash(file_group)
            all_duplicates.extend(dupes)
            
            # Calculate wasted space (keep one, count others)
            for dup_set in dupes:
                total_wasted += size * (len(dup_set) - 1)
    
    if by_name:
        # Check name similarity
        name_dupes = find_duplicates_by_name_similarity(files)
        all_duplicates.extend(name_dupes)
    
    # Deduplicate groups (same files in multiple groups)
    seen_paths = set()
    unique_groups = []
    
    for group in all_duplicates:
        paths = set(f.get("path", "") for f in group)
        if not paths.intersection(seen_paths):
            unique_groups.append(group)
            seen_paths.update(paths)
    
    return {
        "base_path": base_path,
        "total_files": len(files),
        "duplicate_groups": len(unique_groups),
        "total_duplicates": sum(len(g) for g in unique_groups),
        "total_wasted_bytes": total_wasted,
        "duplicates": unique_groups,
    }


# =============================================================================
# Duplicate Merger
# =============================================================================


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


def merge_duplicates(duplicate_group, keep_strategy="newest", archive_path="", dry_run=True):
    """
    Merge a duplicate file group.
    
    keep_strategy: "newest", "oldest", "first"
    archive_path: Where to move duplicates (if empty, delete)
    dry_run: Preview without making changes
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
    else:
        keep = duplicate_group[0]
    
    keep_path = keep.get("path", "")
    
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
                arch_path = os.path.join(archive_path, os.path.basename(path))
                # Handle name conflicts
                if os.path.exists(arch_path):
                    base, ext = os.path.splitext(arch_path)
                    arch_path = f"{base}_dup_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                
                shutil.move(path, arch_path)
                archived.append(path)
                saved_bytes += f.get("size", 0)
            except (OSError, IOError):
                deleted.append(path)
        else:
            # Just delete
            if dry_run:
                deleted.append(path)  # Preview
            else:
                try:
                    os.remove(path)
                    deleted.append(path)
                    saved_bytes += f.get("size", 0)
                except OSError:
                    pass
    
    return {
        "kept": keep_path,
        "archived": archived,
        "deleted": deleted,
        "saved_bytes": saved_bytes,
    }


def merge_all_duplicates(
    base_path,
    keep_strategy="newest",
    archive_path="",
    by_content=True,
    by_name=True,
    dry_run=True
):
    """Find and merge all duplicates in a directory."""
    # Find duplicates
    dupes = find_all_duplicates(
        base_path,
        by_content=by_content,
        by_name=by_name
    )
    
    duplicate_groups = dupes.get("duplicates", [])
    
    results = {
        "base_path": base_path,
        "keep_strategy": keep_strategy,
        "dry_run": dry_run,
        "duplicate_groups": len(duplicate_groups),
        "total_duplicates": sum(len(g) for g in duplicate_groups),
        "merges": [],
        "total_saved_bytes": 0,
    }
    
    for group in duplicate_groups:
        merge_result = merge_duplicates(
            group,
            keep_strategy=keep_strategy,
            archive_path=archive_path,
            dry_run=dry_run
        )
        results["merges"].append(merge_result)
        results["total_saved_bytes"] += merge_result.get("saved_bytes", 0)
    
    return results


# =============================================================================
# Utility Functions
# =============================================================================


def format_bytes(size):
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def generate_duplicate_report(duplicate_info):
    """Generate text summary of duplicate findings."""
    lines = [
        "=" * 60,
        "DUPLICATE FILE REPORT",
        "=" * 60,
        f"Base Path: {duplicate_info.get('base_path')}",
        f"Total Files: {duplicate_info.get('total_files')}",
        f"Duplicate Groups: {duplicate_info.get('duplicate_groups')}",
        f"Total Duplicates: {duplicate_info.get('total_duplicates')}",
        f"Wasted Space: {format_bytes(duplicate_info.get('total_wasted_bytes', 0))}",
        "",
    ]
    
    for i, group in enumerate(duplicate_info.get("duplicates", []), 1):
        lines.append(f"Group {i}:")
        for f in group:
            path = f.get("path", "")
            size = f.get("size", 0)
            mod = f.get("modified", "")
            lines.append(f"  - {path} ({format_bytes(size)}, {mod})")
        lines.append("")
    
    return "\n".join(lines)