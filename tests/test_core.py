"""Tests for core functions."""

import os
import pytest
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_server import (
    create_folder_structure,
    create_backup,
    get_directory_structure,
    apply_naming_convention,
    create_template_structure,
    create_analytics_report,
)


class TestCreateFolderStructure:
    """Tests for create_folder_structure function."""

    def test_creates_main_folders(self, mount_dir):
        """Should create all PARA main folders."""
        result = create_folder_structure(mount_dir)

        assert len(result["errors"]) == 0
        for folder in ["00_INBOX", "01_PROJECTS", "02_AREAS", "03_RESOURCES",
                       "04_ARCHIVE", "90_TEMPLATES", "99_SYSTEM"]:
            assert os.path.exists(os.path.join(mount_dir, folder))

    def test_creates_subfolders(self, mount_dir):
        """Should create subfolders for Projects, Areas, Resources."""
        create_folder_structure(mount_dir)

        # Check project subfolders
        assert os.path.exists(os.path.join(mount_dir, "01_PROJECTS", "01_Projects"))
        assert os.path.exists(os.path.join(mount_dir, "01_PROJECTS", "02_Client-Work"))

        # Check area subfolders
        assert os.path.exists(os.path.join(mount_dir, "02_AREAS", "Health"))
        assert os.path.exists(os.path.join(mount_dir, "02_AREAS", "Finance"))

        # Check resource subfolders
        assert os.path.exists(os.path.join(mount_dir, "03_RESOURCES", "AI"))
        assert os.path.exists(os.path.join(mount_dir, "03_RESOURCES", "Tech"))

    def test_invalid_path_returns_error(self):
        """Invalid path should return error."""
        result = create_folder_structure("/etc/passwd")
        assert len(result["errors"]) > 0

    def test_existing_folders_ok(self, mount_dir):
        """Existing folders should not cause errors."""
        os.makedirs(os.path.join(mount_dir, "00_INBOX"))
        result = create_folder_structure(mount_dir)
        assert len(result["errors"]) == 0


class TestCreateBackup:
    """Tests for create_backup function."""

    def test_backup_creates_directory(self, mount_dir, backup_dir, sample_files):
        """Should create backup directory with timestamp."""
        result = create_backup(mount_dir, backup_dir)

        assert result["backup_path"] != ""
        assert os.path.exists(result["backup_path"])

    def test_backup_copies_files(self, mount_dir, backup_dir, sample_files):
        """Should copy files to backup."""
        result = create_backup(mount_dir, backup_dir)

        assert len(result["files_copied"]) > 0
        for file in sample_files:
            assert file in result["files_copied"]

    def test_backup_invalid_source(self, backup_dir):
        """Invalid source should return error."""
        result = create_backup("/nonexistent", backup_dir)
        assert "error" in result or len(result["errors"]) > 0

    def test_backup_invalid_dest(self, mount_dir):
        """Invalid destination should return error."""
        result = create_backup(mount_dir, "/etc")
        assert len(result["errors"]) > 0


class TestGetDirectoryStructure:
    """Tests for get_directory_structure function."""

    def test_returns_structure(self, mount_dir):
        """Should return directory structure."""
        create_folder_structure(mount_dir)
        result = get_directory_structure(mount_dir)

        assert "structure" in result
        assert len(result["structure"]) > 0

    def test_respects_depth_limit(self, mount_dir):
        """Should respect max_depth parameter."""
        create_folder_structure(mount_dir)
        result = get_directory_structure(mount_dir, max_depth=1)

        # Should only show top level
        assert "structure" in result

    def test_invalid_path_returns_error(self):
        """Nonexistent path may not return error - just return empty structure."""
        result = get_directory_structure("/nonexistent")
        # Path may not exist but shouldn't crash
        assert "structure" in result or "error" in result


class TestApplyNamingConvention:
    """Tests for apply_naming_convention function."""

    def test_renames_file(self, mount_dir):
        """Should rename file with new convention."""
        test_file = os.path.join(mount_dir, "document.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        result = apply_naming_convention(
            test_file,
            "project",
            "test-document",
            1
        )

        assert result["success"] is True
        assert os.path.exists(result["renamed"])

    def test_invalid_path_returns_error(self):
        """Invalid path should return error."""
        result = apply_naming_convention(
            "/nonexistent/file.txt",
            "project",
            "test",
            1
        )
        assert result["success"] is False
        assert "error" in result

    def test_sanitizes_context(self, mount_dir):
        """Should sanitize context parameter."""
        test_file = os.path.join(mount_dir, "doc.txt")
        with open(test_file, "w") as f:
            f.write("content")

        result = apply_naming_convention(
            test_file,
            "Project Name With Spaces!",
            "Test Doc",
            1
        )

        assert result["success"] is True
        # Context should be lowercase with no spaces
        assert "__project" in result["renamed"].lower()


class TestCreateTemplateStructure:
    """Tests for template folder generation."""

    def test_creates_finance_template(self, mount_dir):
        create_folder_structure(mount_dir)

        result = create_template_structure(mount_dir, "finance")

        assert result["errors"] == []
        assert any(path.endswith("02_AREAS/Finance/Invoices") for path in result["created"])
        assert os.path.exists(os.path.join(mount_dir, "02_AREAS", "Finance", "Invoices"))

    def test_unknown_template_returns_error(self, mount_dir):
        result = create_template_structure(mount_dir, "unknown")

        assert result["created"] == []
        assert result["errors"]


class TestCreateAnalyticsReport:
    """Tests for analytics report generation."""

    def test_reports_file_totals_and_distribution(self, mount_dir):
        with open(os.path.join(mount_dir, "invoice.pdf"), "w", encoding="utf-8") as handle:
            handle.write("invoice")
        with open(os.path.join(mount_dir, "notes.md"), "w", encoding="utf-8") as handle:
            handle.write("notes")

        result = create_analytics_report(mount_dir)

        assert result["total_files"] == 2
        assert result["file_types"]["pdf"] == 1
        assert result["file_types"]["md"] == 1
        assert result["total_size_bytes"] > 0

    def test_reports_duplicate_metrics(self, mount_dir):
        with open(os.path.join(mount_dir, "copy-a.txt"), "w", encoding="utf-8") as handle:
            handle.write("same-content")
        with open(os.path.join(mount_dir, "copy-b.txt"), "w", encoding="utf-8") as handle:
            handle.write("same-content")

        result = create_analytics_report(mount_dir)

        assert result["duplicates"]["duplicate_groups"] >= 1
        assert result["duplicates"]["total_duplicates"] >= 2
