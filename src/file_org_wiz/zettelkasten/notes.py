# Note splitting functions for Zettelkasten

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def split_atomic_notes(
    content: str, original_name: str, id_prefix: str = ""
) -> list[dict[str, Any]]:
    """Split a note into atomic (one idea each) notes.

    Splits on ## or ### headings.
    Returns list of note dicts with 'content', 'title', 'id'.
    """
    frontmatter = ""
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]

    heading_pattern = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
    matches = list(heading_pattern.finditer(body))

    if not matches:
        return [
            {
                "content": content,
                "title": original_name,
                "id": id_prefix or datetime.now().strftime("%Y%m%d%H%M%S"),
            }
        ]

    notes = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)

        section_title = match.group(1).strip()
        section_content = body[start:end].strip()

        section_id = id_prefix
        if not section_id:
            section_id = datetime.now().strftime("%Y%m%d%H%M%S") + f"{i:02d}"

        if frontmatter:
            section_content = f"---\n{frontmatter}---\n\n{section_content}"

        notes.append(
            {
                "content": section_content,
                "title": section_title,
                "id": section_id,
            }
        )

    return notes


def create_atomic_notes(output_dir: str, source_note: dict[str, Any]) -> list[str]:
    """Create atomic notes from a source note.

    Args:
        output_dir: Where to save notes
        source_note: Dict with 'path' and 'content'

    Returns:
        List of created file paths
    """
    content = source_note.get("content", "")
    original_path = source_note.get("path", "note.md")
    original_name = Path(original_path).stem

    id_prefix = datetime.now().strftime("%Y%m%d%H%M%S")

    atoms = split_atomic_notes(content, original_name, id_prefix)

    created = []

    for atom in atoms:
        safe_title = re.sub(r"[^a-zA-Z0-9\s-]", "", atom["title"])
        safe_title = safe_title.strip().replace(" ", "-")

        filename = f"{atom['id']}-{safe_title}.md"
        output_path = os.path.join(output_dir, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(atom["content"])

        created.append(output_path)

    return created
