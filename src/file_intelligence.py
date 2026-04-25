"""Content heuristics for auto-tagging and smart filenames."""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path


TEXT_EXTENSIONS = {"txt", "md", "csv", "log", "json", "yaml", "yml"}

TAG_KEYWORDS = {
    "finance": {"invoice", "tax", "budget", "receipt", "expense", "payment", "payroll"},
    "project": {"project", "milestone", "launch", "roadmap", "proposal", "client"},
    "meeting": {"meeting", "agenda", "notes", "minutes", "follow-up"},
    "research": {"research", "study", "analysis", "reference", "paper", "report"},
    "personal": {"personal", "journal", "family", "home", "health"},
    "legal": {"contract", "agreement", "nda", "policy", "terms"},
}


def _slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "document"


def _read_text_excerpt(file_path: str, max_chars: int = 4000) -> str:
    path = Path(file_path)
    if path.suffix.lstrip(".").lower() not in TEXT_EXTENSIONS:
        return ""

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.read(max_chars)
    except OSError:
        return ""


def _extract_terms(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]{3,}", text.lower())


def generate_content_tags(file_path: str) -> list[str]:
    """Generate semantic tags from filename and readable text content."""
    path = Path(file_path)
    source_text = f"{path.stem} {_read_text_excerpt(file_path)}".lower()
    terms = set(_extract_terms(source_text))

    tags: set[str] = set()
    for tag, keywords in TAG_KEYWORDS.items():
        if terms.intersection(keywords):
            tags.add(tag)
            tags.update(sorted(terms.intersection(keywords))[:2])

    if not tags:
        suffix = path.suffix.lstrip(".").lower()
        if suffix:
            tags.add(suffix)

    return sorted(tags)


def infer_context_description(file_path: str) -> tuple[str, str]:
    """Infer naming context and description from file content."""
    path = Path(file_path)
    tags = generate_content_tags(file_path)
    source_text = f"{path.stem} {_read_text_excerpt(file_path)}"
    terms = [term for term in _extract_terms(source_text) if term not in {"this", "that", "with", "from", "file"}]

    context = next((tag for tag in tags if tag in TAG_KEYWORDS), tags[0] if tags else "file")

    preferred_terms: list[str] = []
    for term in terms:
        if term not in preferred_terms and len(preferred_terms) < 4:
            preferred_terms.append(term)

    description = "-".join(preferred_terms[:4]) if preferred_terms else path.stem
    return _slugify(context), _slugify(description)


def suggest_smart_filename(file_path: str, version: int = 1) -> str:
    """Suggest a descriptive filename using the project naming convention."""
    path = Path(file_path)
    context, description = infer_context_description(file_path)
    timestamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
    safe_version = max(int(version), 1)
    return f"{timestamp}__{context}__{description}__v{safe_version:02d}{path.suffix}"
