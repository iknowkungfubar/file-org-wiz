"""Duplicate detection and merging utilities for file-org-wiz.

This package provides comprehensive duplicate file handling including
detection, merging, and reporting functionality.
"""

from __future__ import annotations

# Re-export all public functions from submodules for backward compatibility
from .duplicate_detection import (
    find_duplicates_by_size,
    quick_hash_file,
    full_hash_file,
    find_duplicates_by_hash,
    find_duplicates_by_name_similarity,
    normalize,
    find_all_duplicates,
)

from .duplicate_merger import (
    get_newest_file,
    get_oldest_file,
    merge_duplicates,
    merge_all_duplicates,
)

from .duplicate_utils import (
    format_bytes,
    generate_duplicate_report,
)

# Also export the submodules for advanced usage
from . import duplicate_detection
from . import duplicate_merger
from . import duplicate_utils
