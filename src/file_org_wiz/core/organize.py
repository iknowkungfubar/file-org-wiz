"""File organization engine for file-org-wiz.

Moves categorized files into the appropriate PARA subfolder structure
based on category, filename keywords, and extension heuristics.
"""

from __future__ import annotations

import os
import shutil
from typing import Any

from file_org_wiz.core.operations import PARA_FOLDERS
from file_org_wiz.core.security import validate_path


def organize_files(
    base_path: str,
    categorized_files: list[dict[str, Any]],
    dry_run: bool = False,
) -> dict[str, Any]:
    """Move categorized files to appropriate PARA subfolders.

    Takes a directory path and a list of categorized file dicts (from
    scan_and_categorize), determines the correct PARA subfolder for each
    file based on its category, and moves it there.

    Args:
        base_path: Root directory for the PARA structure.
        categorized_files: List of file info dicts from scan_and_categorize.
        dry_run: If True, preview only without moving files.

    Returns:
        Manifest dict with:
          - moved:    list of {source, destination[, dry_run]}
          - errors:   list of {source, error}
          - skipped:  list of {source, reason}
          - total_moved / total_errors / total_skipped
    """
    valid, error = validate_path(base_path)
    if not valid:
        return {
            "moved": [],
            "errors": [{"source": base_path, "error": error}],
            "skipped": [],
            "total_moved": 0,
            "total_errors": 1,
            "total_skipped": 0,
        }

    manifest: dict[str, Any] = {
        "moved": [],
        "errors": [],
        "skipped": [],
    }

    for file_info in categorized_files:
        file_path = file_info.get("path", "")

        # Skip files that no longer exist on disk
        if not os.path.isfile(file_path):
            manifest["errors"].append(
                {"source": file_path, "error": "File does not exist"}
            )
            continue

        # Skip files already inside a PARA folder
        rel_path = os.path.relpath(file_path, base_path)
        top_level = rel_path.split(os.sep, 1)[0] if rel_path and rel_path != "." else ""
        if top_level in PARA_FOLDERS:
            manifest["skipped"].append(
                {
                    "source": file_path,
                    "reason": f"Already in PARA folder: {top_level}",
                }
            )
            continue

        category = file_info.get("category", "00_INBOX")
        dest_dir = _resolve_dest_dir(base_path, file_info, category)

        if dry_run:
            manifest["moved"].append(
                {
                    "source": file_path,
                    "destination": os.path.join(dest_dir, os.path.basename(file_path)),
                    "dry_run": True,
                }
            )
            continue

        try:
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = shutil.move(file_path, dest_dir)
            manifest["moved"].append({"source": file_path, "destination": dest_path})
        except OSError as e:
            manifest["errors"].append({"source": file_path, "error": str(e)})

    manifest["total_moved"] = len(manifest["moved"])
    manifest["total_errors"] = len(manifest["errors"])
    manifest["total_skipped"] = len(manifest["skipped"])

    return manifest


def _resolve_dest_dir(
    base_path: str,
    file_info: dict[str, Any],
    category: str,
) -> str:
    """Resolve the target subdirectory for a categorized file.

    Uses filename keywords and extension heuristics to route files into
    the appropriate subfolder within the top-level PARA directory.
    """
    name = file_info.get("name", "")
    ext = file_info.get("extension", "")
    name_lower = name.lower()

    if category == "01_PROJECTS":
        return os.path.join(base_path, "01_PROJECTS")

    if category == "02_AREAS":
        sub = _match_area_subdir(name_lower, ext)
        if sub:
            return os.path.join(base_path, "02_AREAS", sub)
        return os.path.join(base_path, "02_AREAS")

    if category == "04_ARCHIVE":
        return os.path.join(base_path, "04_ARCHIVE")

    # Default for 03_RESOURCES and any unknown category
    if category == "03_RESOURCES":
        sub = _match_resource_subdir(name_lower, ext)
        if sub:
            return os.path.join(base_path, "03_RESOURCES", sub)
        return os.path.join(base_path, "03_RESOURCES")

    # Fallback -- uncategorised files land in INBOX
    return os.path.join(base_path, "00_INBOX")


def _match_area_subdir(name_lower: str, ext: str) -> str | None:
    """Match an Areas subfolder based on filename keywords or extension."""
    for keyword, subdir in [
        ("health", "Health"),
        ("fitness", "Health"),
        ("medical", "Health"),
        ("doctor", "Health"),
        ("wellness", "Health"),
        ("invoice", "Finance"),
        ("tax", "Finance"),
        ("budget", "Finance"),
        ("receipt", "Finance"),
        ("payment", "Finance"),
        ("salary", "Finance"),
        ("bank", "Finance"),
        ("home", "Home"),
        ("house", "Home"),
        ("repair", "Home"),
        ("lease", "Home"),
        ("rent", "Home"),
        ("learning", "Learning"),
        ("course", "Learning"),
        ("study", "Learning"),
        ("class", "Learning"),
        ("lesson", "Learning"),
        ("tutorial", "Learning"),
        ("education", "Learning"),
        ("personal", "Personal"),
        ("private", "Personal"),
        ("journal", "Personal"),
        ("diary", "Personal"),
        ("resume", "Personal"),
    ]:
        if keyword in name_lower:
            return subdir

    # Extension fallback: spreadsheet-like files go to Finance
    if ext in ("xlsx", "csv", "numbers"):
        return "Finance"

    return None


def _match_resource_subdir(name_lower: str, ext: str) -> str | None:
    """Match a Resources subfolder based on filename keywords or extension."""
    for keyword, subdir in [
        ("ai", "AI"),
        ("machine learning", "AI"),
        ("neural", "AI"),
        ("gpt", "AI"),
        ("llm", "AI"),
        ("tech", "Tech"),
        ("software", "Tech"),
        ("code", "Tech"),
        ("api", "Tech"),
        ("docker", "Tech"),
        ("git", "Tech"),
        ("linux", "Tech"),
        ("career", "Career"),
        ("job", "Career"),
        ("interview", "Career"),
        ("development", "Development"),
        ("dev", "Development"),
        ("sprint", "Development"),
        ("roadmap", "Development"),
        ("media", "Media"),
        ("reading", "Reading"),
        ("book", "Reading"),
        ("article", "Reading"),
        ("paper", "Reading"),
        ("research", "Reading"),
        ("tools", "Tools"),
        ("tool", "Tools"),
        ("utility", "Tools"),
        ("plugin", "Tools"),
    ]:
        if keyword in name_lower:
            return subdir

    # Extension-based matching
    image_exts = {"png", "jpg", "jpeg", "gif", "svg", "webp", "ico", "bmp", "tiff"}
    video_exts = {"mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"}
    audio_exts = {"mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"}
    reading_exts = {"pdf", "epub", "mobi"}

    if ext in image_exts | video_exts | audio_exts:
        return "Media"
    if ext in reading_exts:
        return "Reading"

    return None
