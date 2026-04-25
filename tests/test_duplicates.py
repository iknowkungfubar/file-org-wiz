# Tests for duplicates module

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from duplicates import (
    find_duplicates_by_size,
    quick_hash_file,
    full_hash_file,
    get_newest_file,
    get_oldest_file,
    merge_duplicates,
    format_bytes,
)


class TestFindDuplicatesBySize:
    """Tests for find_duplicates_by_size function."""

    def test_no_duplicates_by_size(self):
        """Different sizes should not be duplicates."""
        files = [
            {"path": "/a.txt", "size": 100},
            {"path": "/b.txt", "size": 200},
        ]
        result = find_duplicates_by_size(files)
        assert result == {}

    def test_finds_same_size(self):
        """Same size should be grouped."""
        files = [
            {"path": "/a.txt", "size": 100},
            {"path": "/b.txt", "size": 100},
        ]
        result = find_duplicates_by_size(files)
        assert 100 in result
        assert len(result[100]) == 2


class TestQuickHashFile:
    """Tests for quick_hash_file function."""

    def test_same_content_same_hash(self, mount_dir):
        """Same content should produce same hash."""
        f1 = os.path.join(mount_dir, "f1.txt")
        f2 = os.path.join(mount_dir, "f2.txt")
        
        with open(f1, "w") as f:
            f.write("test content here")
        with open(f2, "w") as f:
            f.write("test content here")
        
        h1 = quick_hash_file(f1)
        h2 = quick_hash_file(f2)
        
        assert h1 == h2
        assert len(h1) > 0


class TestFullHashFile:
    """Tests for full_hash_file function."""

    def test_different_content_different_hash(self, mount_dir):
        """Different content should produce different hash."""
        f1 = os.path.join(mount_dir, "f1.txt")
        f2 = os.path.join(mount_dir, "f2.txt")
        
        with open(f1, "w") as f:
            f.write("content A")
        with open(f2, "w") as f:
            f.write("content B")
        
        h1 = full_hash_file(f1)
        h2 = full_hash_file(f2)
        
        assert h1 != h2


class TestGetNewestFile:
    """Tests for get_newest_file function."""

    def test_returns_newest(self):
        """Should return file with newest mtime."""
        files = [
            {"path": "/old.txt", "size": 100, "modified": "2024-01-01T00:00:00"},
            {"path": "/new.txt", "size": 100, "modified": "2024-12-31T00:00:00"},
        ]
        result = get_newest_file(files)
        assert result["path"] == "/new.txt"


class TestGetOldestFile:
    """Tests for get_oldest_file function."""

    def test_returns_oldest(self):
        """Should return file with oldest mtime."""
        files = [
            {"path": "/old.txt", "size": 100, "modified": "2024-01-01T00:00:00"},
            {"path": "/new.txt", "size": 100, "modified": "2024-12-31T00:00:00"},
        ]
        result = get_oldest_file(files)
        assert result["path"] == "/old.txt"


class TestMergeDuplicates:
    """Tests for merge_duplicates function."""

    def test_dry_run_no_changes(self):
        """Dry run should not make changes."""
        files = [
            {"path": "/keep.txt", "size": 100},
            {"path": "/dup1.txt", "size": 100},
        ]
        result = merge_duplicates(files, keep_strategy="newest", dry_run=True)
        
        assert result["kept"] == "/keep.txt" or result["kept"] == "/dup1.txt"
        assert result["deleted"] == ["/dup1.txt"]  # Preview deletion
        assert result["saved_bytes"] == 0  # No actual savings in dry run

    def test_no_duplicates(self):
        """Single file should not trigger merge."""
        files = [{"path": "/only.txt", "size": 100}]
        result = merge_duplicates(files)
        
        # Single file - should not attempt merge
        assert len(result["archived"]) == 0
        assert len(result["deleted"]) == 0


class TestFormatBytes:
    """Tests for format_bytes function."""

    def test_bytes(self):
        """Should format bytes."""
        assert format_bytes(100) == "100.0 B"

    def test_kilobytes(self):
        """Should format KB."""
        assert "KB" in format_bytes(1024)

    def test_megabytes(self):
        """Should format MB."""
        assert "MB" in format_bytes(1024 * 1024)