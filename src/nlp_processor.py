"""Natural language parsing for file organization requests."""

from __future__ import annotations

import os
import re
from datetime import datetime, timedelta
from typing import Any


FOLDER_PATHS = {
    "downloads": "Downloads",
    "desktop": "Desktop",
    "documents": "Documents",
    "pictures": "Pictures",
    "music": "Music",
    "videos": "Videos",
}

ACTION_PATTERNS = {
    "find": [r"\bfind\b", r"\bsearch\b", r"\blocate\b", r"\bshow\b"],
    "move": [r"\bmove\b", r"\btransfer\b", r"\brelocate\b"],
    "delete": [r"\bdelete\b", r"\bremove\b", r"\btrash\b"],
    "rename": [r"\brename\b"],
    "organize": [r"\borganize\b", r"\bsort\b", r"\barrange\b", r"clean up"],
}

FILE_TYPE_PATTERNS = {
    "pdf": [r"\.pdf", r"\bpdfs?\b"],
    "jpg": [r"\.jpe?g", r"\bimages?\b", r"\bphotos?\b"],
    "png": [r"\.png", r"\bpng\b"],
    "doc": [r"\.docx?", r"\bdocuments?\b", r"\bword files?\b"],
    "xls": [r"\.xlsx?", r"\bexcel files?\b", r"\bspreadsheets?\b"],
    "txt": [r"\.txt", r"\btext files?\b"],
    "zip": [r"\.zip", r"\barchives?\b", r"\bzipped files?\b"],
    "mp3": [r"\.mp3", r"\baudio files?\b", r"\bmusic\b"],
    "mp4": [r"\.mp4|\.mov|\.avi", r"\bvideos?\b"],
}


def _expand_folder(keyword: str) -> str:
    return os.path.join(os.path.expanduser("~"), FOLDER_PATHS[keyword])


def _extract_action(command: str) -> str:
    for action, patterns in ACTION_PATTERNS.items():
        if any(re.search(pattern, command) for pattern in patterns):
            return action
    return "organize"


def _extract_file_types(command: str) -> list[str]:
    matches: list[str] = []
    for file_type, patterns in FILE_TYPE_PATTERNS.items():
        if any(re.search(pattern, command) for pattern in patterns):
            matches.append(file_type)
    return matches


def _extract_date_filters(command: str) -> dict[str, Any]:
    now = datetime.now()
    if "last month" in command:
        last_day_prev_month = now.replace(day=1) - timedelta(days=1)
        return {
            "date_range": {
                "start": last_day_prev_month.replace(day=1).strftime("%Y-%m-%d"),
                "end": last_day_prev_month.strftime("%Y-%m-%d"),
            }
        }
    if "this month" in command:
        return {
            "date_range": {
                "start": now.replace(day=1).strftime("%Y-%m-%d"),
                "end": now.strftime("%Y-%m-%d"),
            }
        }
    if "this week" in command:
        start = now - timedelta(days=now.weekday())
        return {"date_range": {"start": start.strftime("%Y-%m-%d"), "end": now.strftime("%Y-%m-%d")}}
    if "yesterday" in command:
        return {"date": (now - timedelta(days=1)).strftime("%Y-%m-%d")}
    if "today" in command:
        return {"date": now.strftime("%Y-%m-%d")}
    return {}


def _extract_target_path(command: str) -> str | None:
    for keyword in FOLDER_PATHS:
        if re.search(rf"\b{keyword[:-1] if keyword.endswith('s') else keyword}s?\b", command):
            return _expand_folder(keyword)
    return None


def _extract_destination(command: str) -> str | None:
    match = re.search(r"(?:to|into|put in)\s+([a-zA-Z0-9_\-/ ]+)$", command)
    if not match:
        return None
    raw = match.group(1).strip().lower()
    for keyword in FOLDER_PATHS:
        if keyword in raw or keyword.rstrip("s") in raw:
            return _expand_folder(keyword)
    return raw or None


def parse_organization_command(command: str) -> dict[str, Any]:
    """Parse a natural-language request into structured intent."""
    command_lower = command.lower().strip()
    filters = _extract_date_filters(command_lower)
    file_types = _extract_file_types(command_lower)
    if file_types:
        filters["file_types"] = file_types

    return {
        "action": _extract_action(command_lower),
        "target_path": _extract_target_path(command_lower),
        "filters": filters,
        "destination": _extract_destination(command_lower),
        "dry_run": any(phrase in command_lower for phrase in ["preview", "dry run", "simulate", "test"]),
    }


def generate_mcp_payload(parsed_command: dict[str, Any]) -> dict[str, Any]:
    """Convert a parsed natural-language request into MCP-friendly payload."""
    payload: dict[str, Any] = {
        "dry_run": parsed_command.get("dry_run", False),
    }
    if parsed_command.get("target_path"):
        payload["mount_path"] = parsed_command["target_path"]
    if parsed_command.get("filters"):
        payload["filters"] = parsed_command["filters"]
    if parsed_command.get("destination"):
        payload["destination_path"] = parsed_command["destination"]
    return payload
