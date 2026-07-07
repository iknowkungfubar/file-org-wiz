"""Path validation and security checks for file-org-wiz.

Security validation, safe path joining, and filename sanitization
to prevent path traversal and sensitive path access.
"""

from __future__ import annotations

import os
import re

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
