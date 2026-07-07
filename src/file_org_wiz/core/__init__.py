"""Core file organization logic for file-org-wiz.

This package provides security validation, PARA folder structure creation,
backups, analytics, naming conventions, and directory traversal.

Sub-package split from the original monolithic organizer.py into:
  - security     -- path validation and sanitization
  - operations   -- folder structure creation and backups
  - organize     -- file organization engine
  - analytics    -- reports, directory structure, naming conventions
"""

from __future__ import annotations

from file_org_wiz.core.analytics import (
    apply_naming_convention,
    create_analytics_report,
    get_directory_structure,
)
from file_org_wiz.core.operations import (
    AREA_SUBDIRS,
    PARA_FOLDERS,
    PROJECT_SUBDIRS,
    RESOURCE_SUBDIRS,
    TEMPLATE_STRUCTURES,
    create_backup,
    create_folder_structure,
    create_template_structure,
)
from file_org_wiz.core.organize import (
    _match_area_subdir,
    _match_resource_subdir,
    _resolve_dest_dir,
    organize_files,
)
from file_org_wiz.core.security import (
    safe_join_path,
    sanitize_filename,
    validate_path,
)

__all__ = [
    "safe_join_path",
    "sanitize_filename",
    "validate_path",
    "PARA_FOLDERS",
    "PROJECT_SUBDIRS",
    "AREA_SUBDIRS",
    "RESOURCE_SUBDIRS",
    "TEMPLATE_STRUCTURES",
    "create_backup",
    "create_folder_structure",
    "create_template_structure",
    "organize_files",
    "_resolve_dest_dir",
    "_match_area_subdir",
    "_match_resource_subdir",
    "apply_naming_convention",
    "create_analytics_report",
    "get_directory_structure",
]
