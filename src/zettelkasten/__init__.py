# Zettelkasten module - MOC generator and link analysis

from __future__ import annotations

import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, List, Dict


# =============================================================================
# Wikilink Extraction
# =============================================================================


WIKILINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')


def extract_wikilinks(content: str) -> List[str]:
    """Extract all [[wikilinks]] from markdown content."""
    matches = WIKILINK_PATTERN.findall(content)
    # Clean up links (remove pipe alias if present)
    links = []
    for match in matches:
        # Handle [[link|alias]] format
        link = match.split('|')[0].strip()
        links.append(link)
    return links


def extract_wikilinks_from_file(file_path: str) -> List[str]:
    """Extract wikilinks from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return extract_wikilinks(content)
    except (OSError, IOError):
        return []


# =============================================================================
# Maps of Content (MOC) Generator
# =============================================================================


def generate_moc_content(topic_name: str, notes: List[str], add_wikilinks: bool = True) -> str:
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
    
    # Sort notes
    sorted_notes = sorted(notes)
    
    for note in sorted_notes:
        note_name = Path(note).stem
        if add_wikilinks:
            lines.append(f"- [[{note_name}]]")
        else:
            lines.append(f"- {note_name}")
    
    # Add metadata
    lines.extend([
        "",
        "---",
        f"generated: {datetime.now().isoformat()}",
        f"note_count: {len(notes)}",
    ])
    
    return "\n".join(lines)


def create_moc_file(
    output_dir: str,
    topic_name: str,
    notes: List[str],
    add_wikilinks: bool = True
) -> str:
    """Create a MOC file for a topic."""
    # Sanitize topic name for filename
    safe_name = re.sub(r'[^a-zA-Z0-9\s-]', '', topic_name)
    safe_name = safe_name.strip().replace(' ', '-')
    
    filename = f"{safe_name}-MOC.md"
    output_path = os.path.join(output_dir, filename)
    
    content = generate_moc_content(topic_name, notes, add_wikilinks)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path


def scan_for_moc_candidates(
    vault_path: str,
    min_notes: int = 5
) -> Dict[str, List[str]]:
    """
    Find folders that need MOC files.
    
    Returns dict of {folder_name: [note_files]}
    """
    candidates = {}
    
    try:
        for root, dirs, files in os.walk(vault_path):
            # Get markdown files
            md_files = [f for f in files if f.endswith('.md')]
            
            # Skip system files
            md_files = [f for f in md_files if not f.startswith('.')]
            
            if len(md_files) >= min_notes:
                folder_name = os.path.basename(root) or "root"
                candidates[folder_name] = md_files
    except OSError:
        pass
    
    return candidates


def generate_all_mocs(vault_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate MOC files for all folders with sufficient notes.
    
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
            generated.append({
                "folder": folder,
                "note_count": len(notes),
                "moc_path": path,
            })
        except (OSError, IOError) as e:
            errors.append({
                "folder": folder,
                "error": str(e),
            })
    
    return {
        "vault_path": vault_path,
        "folders_scanned": len(candidates),
        "mocs_generated": len(generated),
        "errors": errors,
        "mocs": generated,
    }


# =============================================================================
# Link Analysis & Suggestions
# =============================================================================


def find_similar_notes(
    target_note: Dict[str, Any],
    all_notes: List[Dict[str, Any]],
    min_similarity: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Find notes similar to target note based on content keywords.
    
    Simple keyword-based similarity (not full NLP).
    """
    target_content = target_note.get("content", "").lower()
    target_words = set(re.findall(r'\b[a-z]{4,}\b', target_content))
    
    # Remove common words
    stop_words = {'that', 'this', 'with', 'from', 'have', 'were', 'been', 'they'}
    target_words = target_words - stop_words
    
    if not target_words:
        return []
    
    similar = []
    
    for note in all_notes:
        if note.get("path") == target_note.get("path"):
            continue
        
        note_content = note.get("content", "").lower()
        note_words = set(re.findall(r'\b[a-z]{4,}\b', note_content))
        note_words = note_words - stop_words
        
        # Calculate Jaccard similarity
        if note_words:
            intersection = len(target_words & note_words)
            union = len(target_words | note_words)
            similarity = intersection / union if union > 0 else 0
            
            if similarity >= min_similarity:
                similar.append({
                    "path": note.get("path"),
                    "similarity": similarity,
                    "shared_keywords": list(target_words & note_words),
                })
    
    # Sort by similarity
    similar.sort(key=lambda x: x["similarity"], reverse=True)
    
    return similar


def analyze_links(notes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a link graph from a list of notes.
    
    Returns:
    - graph: {note_path: [linked_paths]}
    - backlinks: {note_path: [backlinked_paths]}  
    - orphans: notes with no links
    - hub_notes: most linked notes
    """
    # Build forward links
    graph: Dict[str, List[str]] = {}
    path_to_content: Dict[str, str] = {}
    
    for note in notes:
        path = note.get("path", "")
        content = note.get("content", "")
        
        path_to_content[path] = content
        
        links = extract_wikilinks(content)
        graph[path] = links
    
    # Build backlinks
    backlinks: Dict[str, List[str]] = {path: [] for path in graph}
    
    for path, links in graph.items():
        for linked in links:
            for other_path, other_links in graph.items():
                if linked in other_links:
                    backlinks[other_path].append(path)
    
    # Find orphans (no links in or out)
    orphans = []
    for path in graph:
        if not graph[path] and not backlinks[path]:
            orphans.append(path)
    
    # Find hub notes (most connections)
    hub_notes = []
    for path in graph:
        total_links = len(graph[path]) + len(backlinks[path])
        if total_links >= 3:  # At least 3 connections
            hub_notes.append({
                "path": path,
                "connections": total_links,
                "outgoing": len(graph[path]),
                "incoming": len(backlinks[path]),
            })
    
    # Sort by connections
    hub_notes.sort(key=lambda x: x["connections"], reverse=True)
    
    return {
        "graph": graph,
        "backlinks": backlinks,
        "orphans": orphans,
        "hub_notes": hub_notes[:10],  # Top 10
        "total_notes": len(notes),
        "total_links": sum(len(l) for l in graph.values()),
    }


def suggest_links(
    note_path: str,
    content: str,
    all_notes: List[Dict[str, Any]],
    max_suggestions: int = 5
) -> List[Dict[str, Any]]:
    """
    Suggest links for a note based on content similarity.
    """
    target_note = {
        "path": note_path,
        "content": content,
    }
    
    similar = find_similar_notes(target_note, all_notes)
    
    suggestions = []
    for s in similar[:max_suggestions]:
        suggestions.append({
            "path": s["path"],
            "confidence": s["similarity"],
            "reason": f"shared keywords: {', '.join(s['shared_keywords'][:3])}",
        })
    
    return suggestions


# =============================================================================
# Atomic Note Splitter
# =============================================================================


def split_atomic_notes(
    content: str,
    original_name: str,
    id_prefix: str = ""
) -> List[Dict[str, Any]]:
    """
    Split a note into atomic (one idea each) notes.
    
    Splits on ## or ### headings.
    Returns list of note dicts with 'content', 'title', 'id'.
    """
    # Extract frontmatter if present
    frontmatter = ""
    body = content
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
    
    # Find all heading sections
    heading_pattern = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
    matches = list(heading_pattern.finditer(body))
    
    if not matches:
        # No headings - return as single note
        return [{
            "content": content,
            "title": original_name,
            "id": id_prefix or datetime.now().strftime("%Y%m%d%H%M%S"),
        }]
    
    # Split at each heading
    notes = []
    
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        
        section_title = match.group(1).strip()
        section_content = body[start:end].strip()
        
        # Extract ID from section or generate
        section_id = id_prefix
        if not section_id:
            # Use timestamp + index
            section_id = datetime.now().strftime("%Y%m%d%H%M%S") + f"{i:02d}"
        
        # Re-add frontmatter
        if frontmatter:
            section_content = f"---\n{frontmatter}---\n\n{section_content}"
        
        notes.append({
            "content": section_content,
            "title": section_title,
            "id": section_id,
        })
    
    return notes


def create_atomic_notes(
    output_dir: str,
    source_note: Dict[str, Any]
) -> List[str]:
    """
    Create atomic notes from a source note.
    
    Args:
        output_dir: Where to save notes
        source_note: Dict with 'path' and 'content'
    
    Returns:
        List of created file paths
    """
    content = source_note.get("content", "")
    original_path = source_note.get("path", "note.md")
    original_name = Path(original_path).stem
    
    # Generate unique ID prefix
    id_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Split into atomic notes
    atoms = split_atomic_notes(content, original_name, id_prefix)
    
    created = []
    
    for atom in atoms:
        # Create filename
        safe_title = re.sub(r'[^a-zA-Z0-9\s-]', '', atom["title"])
        safe_title = safe_title.strip().replace(' ', '-')
        
        filename = f"{atom['id']}-{safe_title}.md"
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(atom["content"])
        
        created.append(output_path)
    
    return created


# =============================================================================
# Vault Analysis
# =============================================================================


def get_vault_stats(vault_path: str) -> Dict[str, Any]:
    """Get statistics about an Obsidian vault."""
    notes = []
    total_words = 0
    
    try:
        for root, dirs, files in os.walk(vault_path):
            for f in files:
                if f.endswith('.md'):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            
                        # Count words
                        words = len(content.split())
                        total_words += words
                        
                        # Extract links
                        links = extract_wikilinks(content)
                        
                        notes.append({
                            "path": path,
                            "name": f,
                            "word_count": words,
                            "link_count": len(links),
                        })
                    except (OSError, IOError):
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


def scan_vault(vault_path: str) -> List[Dict[str, Any]]:
    """Scan an Obsidian vault and return note metadata."""
    notes = []
    
    try:
        for root, dirs, files in os.walk(vault_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for f in files:
                # Skip hidden and non-markdown files
                if f.startswith('.'):
                    continue
                if not f.endswith('.md'):
                    continue
                
                path = os.path.join(root, f)
                
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    links = extract_wikilinks(content)
                    
                    notes.append({
                        "path": path,
                        "name": f,
                        "title": f[:-3],  # Remove .md
                        "content": content,
                        "links": links,
                        "has_moc": f.endswith("-MOC.md"),
                    })
                except (OSError, IOError):
                    continue
    except OSError:
        pass
    
    return notes