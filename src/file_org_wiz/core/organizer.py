"""Core file organization logic for file-org-wiz.

Legacy re-export module -- all symbols now live in sub-modules of the
file_org_wiz.core package (security, operations, organize, analytics).

This file is kept for backward compatibility. New code should import
from file_org_wiz.core directly or from the appropriate sub-module.
"""

from __future__ import annotations

from file_org_wiz.core.analytics import (  # noqa: F401 -- legacy re-export
    apply_naming_convention,
    create_analytics_report,
    get_directory_structure,
)
from file_org_wiz.core.operations import (  # noqa: F401 -- legacy re-export
    AREA_SUBDIRS,
    PARA_FOLDERS,
    PROJECT_SUBDIRS,
    RESOURCE_SUBDIRS,
    TEMPLATE_STRUCTURES,
    create_backup,
    create_folder_structure,
    create_template_structure,
)
from file_org_wiz.core.organize import (  # noqa: F401 -- legacy re-export
    _match_area_subdir,
    _match_resource_subdir,
    _resolve_dest_dir,
    organize_files,
)
from file_org_wiz.core.security import (  # noqa: F401 -- legacy re-export
    SENSITIVE_PREFIXES,
    safe_join_path,
    sanitize_filename,
    validate_path,
)
