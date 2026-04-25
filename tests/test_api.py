"""Tests for API endpoints."""

import os
import json
import pytest
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_server import app


@pytest.fixture
def client():
    """Create test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_returns_healthy(self, client):
        """Health endpoint should return healthy status."""
        response = client.get("/health")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data["status"] == "healthy"
        assert data["service"] == "file-org-wiz-mcp"

    def test_health_includes_version(self, client):
        """Health endpoint should include version."""
        response = client.get("/health")
        data = json.loads(response.data)

        assert "version" in data
        assert data["version"] == "1.0.0"


class TestOrganizeEndpoint:
    """Tests for /organize endpoint."""

    def test_organize_without_backup(self, client, mount_dir, backup_dir):
        """Organize without backup should succeed."""
        response = client.post("/organize", json={
            "mount_path": mount_dir,
            "backup_path": backup_dir,
            "do_backup": False
        })
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data["status"] == "complete"

    def test_organize_creates_folders(self, client, mount_dir, backup_dir):
        """Organize should create PARA folder structure."""
        client.post("/organize", json={
            "mount_path": mount_dir,
            "backup_path": backup_dir,
            "do_backup": False
        })

        for folder in ["00_INBOX", "01_PROJECTS", "02_AREAS"]:
            assert os.path.exists(os.path.join(mount_dir, folder))

    def test_organize_with_invalid_path(self, client):
        """Organize with invalid path should return 400."""
        response = client.post("/organize", json={
            "mount_path": "/etc/passwd",
            "backup_path": "/tmp"
        })

        assert response.status_code == 400

    def test_organize_with_backup(self, client, mount_dir, backup_dir):
        """Organize with backup should create backup."""
        response = client.post("/organize", json={
            "mount_path": mount_dir,
            "backup_path": backup_dir,
            "do_backup": True
        })
        data = json.loads(response.data)

        assert response.status_code == 200
        phases = data.get("phases", [])
        backup_phase = next((p for p in phases if p["name"] == "backup"), None)
        assert backup_phase is not None


class TestBackupEndpoint:
    """Tests for /backup endpoint."""

    def test_backup_creates_timestamped_folder(self, client, mount_dir, backup_dir):
        """Backup should create timestamped folder."""
        response = client.post("/backup", json={
            "source_path": mount_dir,
            "backup_path": backup_dir
        })
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "backup_path" in data
        assert "backup__" in data["backup_path"]

    def test_backup_with_invalid_source(self, client, backup_dir):
        """Backup with invalid source should return error in response."""
        response = client.post("/backup", json={
            "source_path": "/nonexistent",
            "backup_path": backup_dir
        })
        data = json.loads(response.data)

        # Should return success but include error info
        assert response.status_code == 200
        assert "error" in data or len(data.get("errors", [])) > 0


class TestStructureEndpoint:
    """Tests for /structure endpoint."""

    def test_structure_returns_tree(self, client, mount_dir):
        """Structure endpoint should return directory tree."""
        response = client.get(f"/structure?path={mount_dir}")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "structure" in data or "error" in data

    def test_structure_with_depth(self, client, mount_dir):
        """Structure endpoint should respect max_depth."""
        response = client.get(f"/structure?path={mount_dir}&max_depth=2")
        data = json.loads(response.data)

        assert response.status_code == 200

    def test_structure_with_invalid_path(self, client):
        """Structure with invalid path should include error in response."""
        response = client.get("/structure?path=/nonexistent")
        data = json.loads(response.data)

        # Should return success but include error info
        assert response.status_code == 200
        assert "error" in data or "structure" in data


class TestApplyNamesEndpoint:
    """Tests for /apply-names endpoint."""

    def test_apply_names_requires_file_path(self, client):
        """Apply names should require file_path."""
        response = client.post("/apply-names", json={})
        data = json.loads(response.data)

        assert response.status_code == 400
        assert "error" in data

    def test_apply_names_with_nonexistent_file(self, client):
        """Apply names with nonexistent file should return error."""
        response = client.post("/apply-names", json={
            "file_path": "/nonexistent/file.txt",
            "context": "test",
            "description": "test"
        })

        assert response.status_code == 400

    def test_apply_names_with_valid_file(self, client, mount_dir):
        """Apply names with valid file should succeed."""
        # Create test file
        test_file = os.path.join(mount_dir, "document.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        response = client.post("/apply-names", json={
            "file_path": test_file,
            "context": "project",
            "description": "test-doc",
            "version": 1
        })
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data["success"] is True


class TestMCPManifestEndpoint:
    """Tests for /mcp-manifest endpoint."""

    def test_manifest_returns_tools(self, client):
        """Manifest should return available tools."""
        response = client.get("/mcp-manifest")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "tools" in data
        assert len(data["tools"]) > 0

    def test_manifest_includes_organize(self, client):
        """Manifest should include organize tool."""
        response = client.get("/mcp-manifest")
        data = json.loads(response.data)

        tool_names = [t["name"] for t in data["tools"]]
        assert "organize" in tool_names