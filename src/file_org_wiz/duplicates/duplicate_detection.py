"""Duplicate detection functions for file-org-wiz.

This module contains functions for finding duplicate files based on
various criteria including size, content hash, and filename similarity.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def find_duplicates_by_size(files):
    """Initial filtering by file size - only same size can be duplicates."""
    size_groups = defaultdict(list)

    for f in files:
        size = f.get("size", 0)
        if size > 0:  # Exclude empty files
            size_groups[size].append(f)

    # Return only groups with potential duplicates
    return {
        size: file_list for size, file_list in size_groups.items() if len(file_list) > 1
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
    except OSError:
        return ""


def full_hash_file(file_path, algorithm="sha256"):
    """Full content hash for accurate duplicate detection."""
    try:
        hash_func = hashlib.new(algorithm)

        with open(file_path, "rb") as f:
            while chunk := f.read(131072):  # 128KB chunks
                hash_func.update(chunk)

        return hash_func.hexdigest()
    except OSError:
        return ""


def find_duplicates_by_hash(file_group):
    """Find true duplicates by content hash."""
    # Quick hash groups
    qgroups = defaultdict(list)

    for f in file_group:
        path = f.get("path", "")
        if path:
            qhash = quick_hash_file(path)
            if qhash:
                qgroups[qhash].append(f)

    # Verify with full hash
    duplicates = []

    for qhash, candidates in qgroups.items():
        if len(candidates) > 1:
            # Full hash check
            fgroups = defaultdict(list)

            for f in candidates:
                path = f.get("path", "")
                if path:
                    fhash = full_hash_file(path)
                    if fhash:
                        fgroups[fhash].append(f)

            # Add confirmed duplicate groups
            for fhash, files in fgroups.items():
                if len(files) > 1:
                    duplicates.append(files)

    return duplicates


def find_duplicates_by_name_similarity(file_list, threshold=0.8):
    """Find duplicates by filename similarity."""

    def normalize(name):
        """Remove dates, versions for comparison."""
        # Remove YYYY-MM-DD dates
        name = re.sub(r"\d{4}-\d{2}-\d{2}", "", name)
        # Remove vNN version
        name = re.sub(r"v\d+", "", name)
        # Remove case differences
        name = name.lower()
        # Remove extensions
        name = Path(name).stem
        # Remove special chars
        name = re.sub(r"[^a-z0-9]", "", name)
        return name

    name_groups = defaultdict(list)

    for f in file_list:
        name = f.get("name", "")
        normalized = normalize(name)
        if named:
            name_groups[normalized].append(f)

    # Return groups with potential matches
    return [files for files in name_groups.values() if len(files) > 1]


def normalize(name):
    """Remove dates, versions for comparison."""
    # Remove YYYY-MM-DD dates
    name = re.sub(r"\d{4}-\d{2}-\d{2}", "", name)
    # Remove vNN version
    name = re.sub(r"v\d+", "", name)
    # Remove case differences
    name = name.lower()
    # Remove extensions
    name = Path(name).stem
    # Remove special chars
    name = re.sub(r"[^a-z0-9]", "", name)
    return name


def find_all_duplicates(base_path, by_content=True, by_name=True):
    """Find all duplicates in a directory."""
    from file_org_wiz.scanner import scan_files_recursive

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
