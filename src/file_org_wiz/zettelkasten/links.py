# Link analysis functions for Zettelkasten

from __future__ import annotations

import re
from typing import Any

WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


def extract_wikilinks(content: str) -> list[str]:
    """Extract all [[wikilinks]] from markdown content."""
    matches = WIKILINK_PATTERN.findall(content)
    links = []
    for match in matches:
        link = match.split("|")[0].strip()
        links.append(link)
    return links


def extract_wikilinks_from_file(file_path: str) -> list[str]:
    """Extract wikilinks from a markdown file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        return extract_wikilinks(content)
    except OSError:
        return []


def find_similar_notes(
    target_note: dict[str, Any],
    all_notes: list[dict[str, Any]],
    min_similarity: float = 0.3,
) -> list[dict[str, Any]]:
    """Find notes similar to target note based on content keywords."""
    target_content = target_note.get("content", "").lower()
    target_words = set(re.findall(r"\b[a-z]{4,}\b", target_content))

    stop_words = {"that", "this", "with", "from", "have", "were", "been", "they"}
    target_words = target_words - stop_words

    if not target_words:
        return []

    similar = []

    for note in all_notes:
        if note.get("path") == target_note.get("path"):
            continue

        note_content = note.get("content", "").lower()
        note_words = set(re.findall(r"\b[a-z]{4,}\b", note_content))
        note_words = note_words - stop_words

        if note_words:
            intersection = len(target_words & note_words)
            union = len(target_words | note_words)
            similarity = intersection / union if union > 0 else 0

            if similarity >= min_similarity:
                similar.append(
                    {
                        "path": note.get("path"),
                        "similarity": similarity,
                        "shared_keywords": list(target_words & note_words),
                    }
                )

    similar.sort(key=lambda x: x["similarity"], reverse=True)
    return similar


def analyze_links(notes: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a link graph from a list of notes.

    Returns:
    - graph: {note_path: [linked_paths]}
    - backlinks: {note_path: [backlinked_paths]}
    - orphans: notes with no links
    - hub_notes: most linked notes
    """
    graph: dict[str, list[str]] = {}
    path_to_content: dict[str, str] = {}

    for note in notes:
        path = note.get("path", "")
        content = note.get("content", "")
        path_to_content[path] = content
        links = extract_wikilinks(content)
        graph[path] = links

    backlinks: dict[str, list[str]] = {path: [] for path in graph}

    for path, links in graph.items():
        for linked in links:
            for other_path, other_links in graph.items():
                if linked in other_links:
                    backlinks[other_path].append(path)

    orphans = []
    for path in graph:
        if not graph[path] and not backlinks[path]:
            orphans.append(path)

    hub_notes = []
    for path in graph:
        total_links = len(graph[path]) + len(backlinks[path])
        if total_links >= 3:
            hub_notes.append(
                {
                    "path": path,
                    "connections": total_links,
                    "outgoing": len(graph[path]),
                    "incoming": len(backlinks[path]),
                }
            )

    hub_notes.sort(key=lambda x: x["connections"], reverse=True)

    return {
        "graph": graph,
        "backlinks": backlinks,
        "orphans": orphans,
        "hub_notes": hub_notes[:10],
        "total_notes": len(notes),
        "total_links": sum(len(v) for v in graph.values()),
    }


def suggest_links(
    note_path: str,
    content: str,
    all_notes: list[dict[str, Any]],
    max_suggestions: int = 5,
) -> list[dict[str, Any]]:
    """Suggest links for a note based on content similarity."""
    target_note = {
        "path": note_path,
        "content": content,
    }

    similar = find_similar_notes(target_note, all_notes)

    suggestions = []
    for s in similar[:max_suggestions]:
        suggestions.append(
            {
                "path": s["path"],
                "confidence": s["similarity"],
                "reason": f"shared keywords: {', '.join(s['shared_keywords'][:3])}",
            }
        )

    return suggestions
