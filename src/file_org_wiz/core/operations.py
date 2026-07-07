"""Folder structure creation and backup operations for file-org-wiz.

Creates PARA folder structures, timestamped backups, and template-based
organization structures.
"""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from typing import Any

from file_org_wiz.core.security import validate_path

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


# ── Operations ───────────────────────────────────────────────────────────────


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
        return {
            "backup_path": "",
            "files_copied": [],
            "errors": [f"Source path does not exist: {source_path}"],
        }
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
