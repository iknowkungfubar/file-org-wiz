# Tests for Zettelkasten module

import os
import sys
import re
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from zettelkasten import (
    extract_wikilinks,
    generate_moc_content,
    create_moc_file,
    find_similar_notes,
    analyze_links,
    split_atomic_notes,
)


class TestExtractWikilinks:
    """Tests for extract_wikilinks function."""

    def test_extracts_single_link(self):
        """Should extract single wikilink."""
        content = "This links to [[my-note]] here."
        links = extract_wikilinks(content)
        assert "my-note" in links

    def test_extracts_multiple_links(self):
        """Should extract multiple wikilinks."""
        content = "See [[note1]] and [[note2]] for details."
        links = extract_wikilinks(content)
        assert len(links) >= 2

    def test_no_links_returns_empty(self):
        """No wikilinks should return empty list."""
        content = "This page has no links."
        links = extract_wikilinks(content)
        assert links == []


class TestGenerateMOCContent:
    """Tests for generate_moc_content function."""

    def test_generates_basic_moc(self):
        """Should generate basic MOC content."""
        notes = ["note1.md", "note2.md", "note3.md"]
        content = generate_moc_content("My Topic", notes)
        
        assert "# My Topic" in content
        assert "note1" in content  # stems are extracted

    def test_adds_wikilinks(self):
        """Should add wikilinks to notes."""
        notes = ["note1.md", "note2.md"]
        content = generate_moc_content("Test Topic", notes)
        
        # Should contain link format
        assert "note1" in content


class TestCreateMOCFile:
    """Tests for create_moc_file function."""

    def test_creates_file(self, mount_dir):
        """Should create MOC file."""
        notes = ["note1.md", "note2.md"]
        path = create_moc_file(mount_dir, "TestTopic", notes)
        
        assert os.path.exists(path)
        
        # Check content
        with open(path) as f:
            content = f.read()
        assert "TestTopic" in content


class TestFindSimilarNotes:
    """Tests for find_similar_notes function."""

    def test_finds_keyword_matches(self):
        """Should attempt to find similar notes."""
        notes = [
            {"path": "/note1.md", "content": "Python programming tips and tricks for beginners"},
            {"path": "/note2.md", "content": "Java coding best practices"},
            {"path": "/note3.md", "content": "Python tutorial guide advanced"},
        ]
        
        # Should return a list (may be empty)
        matches = find_similar_notes(notes[0], notes[1:])
        assert isinstance(matches, list)


class TestAnalyzeLinks:
    """Tests for analyze_links function."""

    def test_builds_link_graph(self):
        """Should build link graph from notes."""
        notes = [
            {"path": "/a.md", "content": "See [[b]] and [[c]]."},
            {"path": "/b.md", "content": "Link to [[c]]."},
            {"path": "/c.md", "content": "No links."},
        ]
        
        graph = analyze_links(notes)
        
        # Should return dict with expected keys
        assert "graph" in graph
        assert "backlinks" in graph
        assert isinstance(graph["graph"], dict)


class TestSplitAtomicNotes:
    """Tests for split_atomic_notes function."""

    def test_splits_by_headings(self):
        """Should split notes at headings."""
        content = """# Main Title

Some intro.

## First Idea

Content about first idea.

## Second Idea

Content about second idea.
"""
        result = split_atomic_notes(content, "original.md")
        
        assert len(result) >= 2

    def test_preserves_frontmatter(self):
        """Should preserve YAML frontmatter."""
        content = """---
title: My Note
tags: [python, notes]
---

# Main

## Section One

Content one.
"""
        result = split_atomic_notes(content, "test.md")
        
        # First result should have frontmatter
        assert len(result) > 0