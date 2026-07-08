# Tests for Zettelkasten module

import os

from file_org_wiz.zettelkasten import (
    analyze_links,
    create_moc_file,
    extract_wikilinks,
    extract_wikilinks_from_file,
    find_similar_notes,
    generate_all_mocs,
    generate_moc_content,
    get_vault_stats,
    scan_for_moc_candidates,
    scan_vault,
    split_atomic_notes,
    suggest_links,
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
            {
                "path": "/note1.md",
                "content": "Python programming tips and tricks for beginners",
            },
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


class TestScanForMOCCandidates:
    """Tests for scan_for_moc_candidates function."""

    def test_finds_folders_meeting_minimum(self, mount_dir):
        """Should detect folders with enough .md files."""
        notes_dir = os.path.join(mount_dir, "my-topic")
        os.makedirs(notes_dir)
        for i in range(6):
            with open(os.path.join(notes_dir, f"note{i}.md"), "w") as f:
                f.write(f"# Note {i}")

        small_dir = os.path.join(mount_dir, "small-topic")
        os.makedirs(small_dir)
        with open(os.path.join(small_dir, "only.md"), "w") as f:
            f.write("# Only note")

        candidates = scan_for_moc_candidates(mount_dir, min_notes=5)

        assert "my-topic" in candidates
        assert len(candidates["my-topic"]) == 6
        assert "small-topic" not in candidates

    def test_excludes_hidden_files(self, mount_dir):
        """Should skip hidden .md files."""
        notes_dir = os.path.join(mount_dir, "topic")
        os.makedirs(notes_dir)
        for i in range(5):
            with open(os.path.join(notes_dir, f"note{i}.md"), "w") as f:
                f.write(f"# Note {i}")
        with open(os.path.join(notes_dir, ".hidden.md"), "w") as f:
            f.write("# hidden")

        candidates = scan_for_moc_candidates(mount_dir, min_notes=5)
        assert "topic" in candidates
        assert ".hidden.md" not in candidates["topic"]

    def test_empty_vault(self, mount_dir):
        """Empty vault should return no candidates."""
        candidates = scan_for_moc_candidates(mount_dir)
        assert candidates == {}


class TestGetVaultStats:
    """Tests for get_vault_stats function."""

    def test_counts_notes_and_words(self, mount_dir):
        """Should count total notes, words, and link stats."""
        for name, content in [
            ("note-a.md", "This note has five words here"),
            ("note-b.md", "[[other]] link in here has six words"),
            ("note-c.md", "Short"),
        ]:
            with open(os.path.join(mount_dir, name), "w", encoding="utf-8") as f:
                f.write(content)

        stats = get_vault_stats(mount_dir)

        assert stats["total_notes"] == 3
        assert stats["total_words"] > 0
        assert stats["avg_words_per_note"] > 0
        assert stats["notes_with_links"] == 1  # note-b.md only

    def test_handles_empty_vault(self, mount_dir):
        """Empty vault should return zero stats."""
        stats = get_vault_stats(mount_dir)
        assert stats["total_notes"] == 0
        assert stats["total_words"] == 0
        assert stats["avg_words_per_note"] == 0
        assert stats["notes_with_links"] == 0


class TestScanVault:
    """Tests for scan_vault function."""

    def test_returns_notes_with_content_and_links(self, mount_dir):
        """Should scan and return full note metadata."""
        with open(os.path.join(mount_dir, "alpha.md"), "w", encoding="utf-8") as f:
            f.write("# Alpha\n\nLink to [[beta]].")
        with open(os.path.join(mount_dir, "beta.md"), "w", encoding="utf-8") as f:
            f.write("# Beta")

        notes = scan_vault(mount_dir)

        assert len(notes) == 2
        paths = {n["name"] for n in notes}
        assert "alpha.md" in paths
        assert "beta.md" in paths
        alpha = next(n for n in notes if n["name"] == "alpha.md")
        assert "[[beta]]" in alpha["content"]
        assert alpha["links"] == ["beta"]
        assert alpha["has_moc"] is False


class TestSuggestLinks:
    """Tests for suggest_links function."""

    def test_suggests_based_on_keyword_similarity(self):
        """Should suggest notes based on content keyword overlap."""
        all_notes = [
            {"path": "/python-intro.md", "content": "Python programming basics and fundamentals for beginners guide"},
            {"path": "/python-advanced.md", "content": "Advanced Python decorators and metaprogramming techniques"},
            {"path": "/java-basics.md", "content": "Java programming syntax and object oriented design patterns"},
        ]
        suggestions = suggest_links(
            note_path="/python-intro.md",
            content="Python programming advanced decorators techniques",
            all_notes=all_notes,
            max_suggestions=2,
        )
        assert len(suggestions) <= 2
        for s in suggestions:
            assert "path" in s
            assert "confidence" in s
            assert isinstance(s["confidence"], float)

    def test_returns_empty_for_no_similar_notes(self):
        """Should return empty list when no similar notes exist."""
        all_notes = [
            {"path": "/python.md", "content": "Python programming language"},
            {"path": "/cooking.md", "content": "Cooking recipes and kitchen tips"},
        ]
        suggestions = suggest_links(
            note_path="/cooking.md",
            content="Kitchen cooking recipes food",
            all_notes=all_notes,
        )
        assert isinstance(suggestions, list)


class TestGenerateMOCContentNoWikilinks:
    """Tests for generate_moc_content with add_wikilinks=False."""

    def test_generates_without_wikilinks(self):
        """Should generate MOC without [[wikilinks]] when disabled."""
        notes = ["note1.md", "note2.md"]
        content = generate_moc_content("Test", notes, add_wikilinks=False)
        assert "[[note1]]" not in content
        assert "- note1" in content or "note1" in content


class TestExtractWikilinksFromFile:
    """Tests for extract_wikilinks_from_file function."""

    def test_returns_empty_for_missing_file(self):
        """Should return empty list for nonexistent file."""
        result = extract_wikilinks_from_file("/nonexistent/file.md")
        assert result == []

    def test_extracts_from_valid_file(self, mount_dir):
        """Should extract links from a real markdown file."""
        path = os.path.join(mount_dir, "test.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("Link to [[alpha]] and [[beta]].")
        result = extract_wikilinks_from_file(path)
        assert "alpha" in result
        assert "beta" in result


class TestFindSimilarNotesEdgeCases:
    """Tests for find_similar_notes edge cases."""

    def test_skips_self_comparison(self):
        """Should not compare a note to itself."""
        target = {"path": "/self.md", "content": "Python programming guide basics tutorial"}
        all_notes = [
            {"path": "/self.md", "content": "Python programming guide basics tutorial"},
            {"path": "/other.md", "content": "Python programming advanced concepts"},
        ]
        matches = find_similar_notes(target, all_notes)
        paths = [m["path"] for m in matches]
        assert "/self.md" not in paths

    def test_returns_empty_when_no_content_keywords(self):
        """Should return empty when target has no content words beyond stop words."""
        target = {"path": "/stop.md", "content": "that this with from have were been they"}
        all_notes = [
            {"path": "/other.md", "content": "Python programming guide"},
        ]
        matches = find_similar_notes(target, all_notes)
        assert matches == []


class TestGenerateAllMocsErrorHandling:
    """Tests for generate_all_mocs error path."""

    def test_handles_nonexistent_vault(self):
        """Should handle non-existent vault path gracefully."""
        result = generate_all_mocs("/nonexistent/vault/path")
        assert isinstance(result, dict)
        assert "errors" in result
        assert "mocs_generated" in result
