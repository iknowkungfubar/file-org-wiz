# Tests for file-org-wiz MCP Server
"""Pytest configuration and fixtures."""

import os
import shutil
import tempfile
from pathlib import Path
import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp = tempfile.mkdtemp()
    yield temp
    shutil.rmtree(temp, ignore_errors=True)


@pytest.fixture
def mount_dir(temp_dir):
    """Create a mount directory for testing."""
    mount = os.path.join(temp_dir, "mount")
    os.makedirs(mount)
    return mount


@pytest.fixture
def backup_dir(temp_dir):
    """Create a backup directory for testing."""
    backup = os.path.join(temp_dir, "backup")
    os.makedirs(backup)
    return backup


@pytest.fixture
def sample_files(mount_dir):
    """Create sample files for testing."""
    files = [
        "document.txt",
        "image.png",
        "notes.md",
    ]
    for file in files:
        path = os.path.join(mount_dir, file)
        with open(path, "w") as f:
            f.write(f"Sample content for {file}")
    return files


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    # Import here to avoid circular imports
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

    from mcp_server import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app():
    """Create a test Flask app."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

    from mcp_server import app
    app.config["TESTING"] = True
    return app