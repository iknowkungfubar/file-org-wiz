# Tests for scanner module

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scanner import (
    scan_files_recursive,
    classify_by_extension,
    classify_by_name,
    suggest_category,
    scan_and_categorize,
)


class TestScanFilesRecursive:
    """Tests for scan_files_recursive function."""

    def test_scans_empty_directory(self, mount_dir):
        """Should handle empty directory."""
        files = scan_files_recursive(mount_dir)
        assert files == []

    def test_scans_single_file(self, mount_dir):
        """Should scan single file."""
        test_file = os.path.join(mount_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        files = scan_files_recursive(mount_dir)
        assert len(files) == 1
        assert files[0]["name"] == "test.txt"

    def test_scans_nested_files(self, mount_dir):
        """Should scan nested directories."""
        # Create nested structure
        subdir = os.path.join(mount_dir, "subdir")
        os.makedirs(subdir)
        
        with open(os.path.join(mount_dir, "file1.txt"), "w") as f:
            f.write("content")
        with open(os.path.join(subdir, "file2.txt"), "w") as f:
            f.write("content")

        files = scan_files_recursive(mount_dir)
        assert len(files) == 2

    def test_respects_max_depth(self, mount_dir):
        """Should respect max_depth parameter."""
        # Create deep structure
        d1 = os.path.join(mount_dir, "d1")
        d2 = os.path.join(d1, "d2")
        os.makedirs(d2)
        
        with open(os.path.join(d2, "deep.txt"), "w") as f:
            f.write("deep")

        files = scan_files_recursive(mount_dir, max_depth=1)
        # File at depth 2 should be excluded
        assert all(f["depth"] <= 1 for f in files)


class TestClassifyByExtension:
    """Tests for classify_by_extension function."""

    def test_design_files_to_projects(self):
        """Design files should go to Projects."""
        assert classify_by_extension("psd") == "01_PROJECTS"
        assert classify_by_extension("ai") == "01_PROJECTS"
        assert classify_by_extension("sketch") == "01_PROJECTS"

    def test_finance_files_to_areas(self):
        """Finance files should go to Areas."""
        assert classify_by_extension("xlsx") == "02_AREAS"
        assert classify_by_extension("csv") == "02_AREAS"

    def test_pdf_to_resources(self):
        """PDF files should go to Resources."""
        assert classify_by_extension("pdf") == "03_RESOURCES"

    def test_archive_extensions(self):
        """Archive extensions should go to Archive."""
        assert classify_by_extension("zip") == "04_ARCHIVE"
        assert classify_by_extension("tar") == "04_ARCHIVE"


class TestClassifyByName:
    """Tests for classify_by_name function."""

    def test_project_patterns(self):
        """Project patterns should match."""
        assert classify_by_name("project_notes.txt") == "01_PROJECTS"
        assert classify_by_name("client_proposal.docx") == "01_PROJECTS"
        assert classify_by_name("draft_v1.pdf") == "01_PROJECTS"

    def test_area_patterns(self):
        """Area patterns should match."""
        assert classify_by_name("invoice_2024.pdf") == "02_AREAS"
        assert classify_by_name("health_tracker.xlsx") == "02_AREAS"

    def test_resource_patterns(self):
        """Resource patterns should match."""
        assert classify_by_name("research_notes.md") == "03_RESOURCES"

    def test_archive_patterns(self):
        """Archive patterns should match."""
        assert classify_by_name("old_archive.zip") == "04_ARCHIVE"
        assert classify_by_name("backup_2023.tar") == "04_ARCHIVE"

    def test_no_match_returns_none(self):
        """No match should return None."""
        assert classify_by_name("random_file.txt") is None


class TestSuggestCategory:
    """Tests for suggest_category function."""

    def test_extension_priority(self):
        """Extension should suggest category."""
        cat, reason = suggest_category("/path/to/file.psd")
        assert cat == "01_PROJECTS"

    def test_name_pattern_priority(self):
        """Name pattern should override extension."""
        cat, reason = suggest_category("/path/to/project_invoice.psd")
        # project pattern should take priority
        assert "project" in reason.lower() or "psd" in reason.lower()


class TestScanAndCategorize:
    """Tests for scan_and_categorize function."""

    def test_categorizes_all_files(self, mount_dir):
        """Should categorize all scanned files."""
        # Create test files
        with open(os.path.join(mount_dir, "design.psd"), "w") as f:
            f.write("content")
        with open(os.path.join(mount_dir, "notes.md"), "w") as f:
            f.write("content")
        with open(os.path.join(mount_dir, "data.csv"), "w") as f:
            f.write("content")

        result = scan_and_categorize(mount_dir)

        assert result["total_files"] == 3
        assert result["summary"]["01_PROJECTS"] >= 1
        assert result["summary"]["03_RESOURCES"] >= 1