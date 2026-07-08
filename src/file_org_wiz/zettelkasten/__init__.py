# Zettelkasten module - MOC generator and link analysis

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

# Re-export from sub-modules
from file_org_wiz.zettelkasten.links import (  # noqa: F401
    WIKILINK_PATTERN,
    analyze_links,
    extract_wikilinks,
    extract_wikilinks_from_file,
    find_similar_notes,
    suggest_links,
)
from file_org_wiz.zettelkasten.notes import (  # noqa: F401
    create_atomic_notes,
    split_atomic_notes,
)

# =============================================================================
# Maps of Content (MOC) Generator
# =============================================================================


def generate_moc_content(
    topic_name: str, notes: list[str], add_wikilinks: bool = True
) -> str:
    """
    Generate MOC (Map of Content) content for a topic.

    Args:
        topic_name: Name of the topic
        notes: List of note filenames/paths
        add_wikilinks: Whether to add [[wikilinks]]

    Returns:
        MOC content as string
    """
    lines = [
        f"# {topic_name}",
        "",
        f"> MOC - Map of Content for {topic_name}",
        "",
        "## Notes",
        "",
    ]

    sorted_notes = sorted(notes)

    for note in sorted_notes:
        note_name = Path(note).stem
        if add_wikilinks:
            lines.append(f"- [[{note_name}]]")
        else:
            lines.append(f"- {note_name}")

    lines.extend(
        [
            "",
            "---",
            f"generated: {datetime.now().isoformat()}",
            f"note_count: {len(notes)}",
        ]
    )

    return "\n".join(lines)


def create_moc_file(
    output_dir: str, topic_name: str, notes: list[str], add_wikilinks: bool = True
) -> str:
    """Create a MOC file for a topic."""
    safe_name = re.sub(r"[^a-zA-Z0-9\s-]", "", topic_name)
    safe_name = safe_name.strip().replace(" ", "-")

    filename = f"{safe_name}-MOC.md"
    output_path = os.path.join(output_dir, filename)

    content = generate_moc_content(topic_name, notes, add_wikilinks)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


def scan_for_moc_candidates(
    vault_path: str, min_notes: int = 5
) -> dict[str, list[str]]:
    """Find folders that need MOC files.

    Returns dict of {folder_name: [note_files]}
    """
    candidates = {}

    try:
        for root, dirs, files in os.walk(vault_path):
            md_files = [f for f in files if f.endswith(".md")]
            md_files = [f for f in md_files if not f.startswith(".")]

            if len(md_files) >= min_notes:
                folder_name = os.path.basename(root) or "root"
                candidates[folder_name] = md_files
    except OSError:
        pass

    return candidates


def generate_all_mocs(
    vault_path: str, output_path: str | None = None
) -> dict[str, Any]:
    """Generate MOC files for all folders with sufficient notes.

    Args:
        vault_path: Path to Obsidian vault
        output_path: Where to save MOCs (defaults to vault_path)

    Returns:
        Summary of generated MOCs
    """
    if output_path is None:
        output_path = vault_path

    candidates = scan_for_moc_candidates(vault_path)

    generated = []
    errors = []

    for folder, notes in candidates.items():
        try:
            path = create_moc_file(output_path, folder, notes)
            generated.append(
                {
                    "folder": folder,
                    "note_count": len(notes),
                    "moc_path": path,
                }
            )
        except OSError as e:
            errors.append(
                {
                    "folder": folder,
                    "error": str(e),
                }
            )

    return {
        "vault_path": vault_path,
        "folders_scanned": len(candidates),
        "mocs_generated": len(generated),
        "errors": errors,
        "mocs": generated,
    }


# =============================================================================
# Vault Analysis
# =============================================================================


def get_vault_stats(vault_path: str) -> dict[str, Any]:
    """Get statistics about an Obsidian vault."""
    notes = []
    total_words = 0

    try:
        for root, dirs, files in os.walk(vault_path):
            for f in files:
                if f.endswith(".md"):
                    path = os.path.join(root, f)
                    try:
                        with open(path, encoding="utf-8") as file:
                            content = file.read()

                        words = len(content.split())
                        total_words += words

                        links = extract_wikilinks(content)

                        notes.append(
                            {
                                "path": path,
                                "name": f,
                                "word_count": words,
                                "link_count": len(links),
                            }
                        )
                    except OSError:
                        continue
    except OSError:
        pass

    return {
        "vault_path": vault_path,
        "total_notes": len(notes),
        "total_words": total_words,
        "avg_words_per_note": total_words // len(notes) if notes else 0,
        "notes_with_links": sum(1 for n in notes if n["link_count"] > 0),
    }


# =============================================================================
# Convenience Functions
# =============================================================================


def scan_vault(vault_path: str) -> list[dict[str, Any]]:
    """Scan an Obsidian vault and return note metadata."""
    notes = []

    try:
        for root, dirs, files in os.walk(vault_path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for f in files:
                if f.startswith("."):
                    continue
                if not f.endswith(".md"):
                    continue

                path = os.path.join(root, f)

                try:
                    with open(path, encoding="utf-8") as file:
                        content = file.read()

                    links = extract_wikilinks(content)

                    notes.append(
                        {
                            "path": path,
                            "name": f,
                            "title": f[:-3],
                            "content": content,
                            "links": links,
                            "has_moc": f.endswith("-MOC.md"),
                        }
                    )
                except OSError:
                    continue
    except OSError:
        pass

    return notes
