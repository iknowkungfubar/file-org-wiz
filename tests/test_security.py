"""Tests for security functions."""

import os
import pytest
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_server import validate_path, safe_join_path, sanitize_filename


class TestValidatePath:
    """Tests for validate_path function."""

    def test_empty_path_returns_invalid(self):
        """Empty path should be invalid."""
        valid, error = validate_path("")
        assert valid is False
        assert "empty" in error.lower()

    def test_valid_absolute_path(self):
        """Valid absolute path should pass."""
        valid, error = validate_path("/tmp")
        assert valid is True
        assert error == ""

    def test_valid_home_path(self):
        """Path with tilde should expand and pass."""
        valid, error = validate_path("~/test")
        assert valid is True

    def test_path_traversal_rejected(self):
        """Path traversal attempts should be rejected."""
        valid, error = validate_path("../etc/passwd")
        assert valid is False
        assert "traversal" in error.lower()

    def test_etc_passwd_rejected(self):
        """/etc/passwd access should be rejected."""
        valid, error = validate_path("/etc/passwd")
        assert valid is False
        assert "not allowed" in error.lower()

    def test_ssh_path_rejected(self):
        """SSH directory access should be rejected."""
        valid, error = validate_path("/.ssh")
        assert valid is False
        assert "not allowed" in error.lower()

    def test_proc_rejected(self):
        """/proc access should be rejected."""
        valid, error = validate_path("/proc")
        assert valid is False
        assert "not allowed" in error.lower() or "restricted" in error.lower()


class TestSafeJoinPath:
    """Tests for safe_join_path function."""

    def test_simple_join(self):
        """Simple path join should work."""
        result = safe_join_path("/tmp", "subdir")
        assert result == os.path.abspath("/tmp/subdir")

    def test_join_with_file(self):
        """Join with file should work."""
        result = safe_join_path("/tmp", "subdir", "file.txt")
        assert result == os.path.abspath("/tmp/subdir/file.txt")

    def test_traversal_blocked(self):
        """Path traversal should return None."""
        result = safe_join_path("/tmp", "../etc")
        assert result is None

    def test_absolute_path_blocked(self):
        """Absolute path in join should return None."""
        result = safe_join_path("/tmp", "/etc/passwd")
        assert result is None


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""

    def test_simple_filename(self):
        """Simple filename should pass through."""
        result = sanitize_filename("document.txt")
        assert result == "document.txt"

    def test_spaces_removed(self):
        """Spaces should be removed."""
        result = sanitize_filename("my document.pdf")
        assert " " not in result

    def test_special_chars_removed(self):
        """Special characters should be removed."""
        result = sanitize_filename("file<script>.txt")
        assert "<" not in result
        assert ">" not in result

    def test_path_components_stripped(self):
        """Path components should be stripped."""
        result = sanitize_filename("/path/to/file.txt")
        assert "/" not in result

    def test_empty_becomes_unnamed(self):
        """Empty result should become 'unnamed'."""
        result = sanitize_filename("///")
        assert result == "unnamed"