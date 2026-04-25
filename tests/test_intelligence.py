"""Tests for natural language and content intelligence features."""

from __future__ import annotations

import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from file_intelligence import generate_content_tags, suggest_smart_filename
from nlp_processor import generate_mcp_payload, parse_organization_command


class TestNaturalLanguageParsing:
    """Tests for natural language command parsing."""

    def test_parses_find_pdf_command(self):
        parsed = parse_organization_command("find all PDF files from last month")

        assert parsed["action"] == "find"
        assert "pdf" in parsed["filters"]["file_types"]
        assert "date_range" in parsed["filters"]

    def test_parses_dry_run_organize_command(self):
        parsed = parse_organization_command("preview organize my downloads folder")
        payload = generate_mcp_payload(parsed)

        assert parsed["action"] == "organize"
        assert parsed["dry_run"] is True
        assert payload["dry_run"] is True
        assert payload["mount_path"].endswith("Downloads")


class TestContentTagging:
    """Tests for file content tagging and smart naming."""

    def test_generates_finance_tags_from_content(self, mount_dir):
        file_path = os.path.join(mount_dir, "scan001.txt")
        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write("Invoice total due. Tax summary for quarterly budget review.")

        tags = generate_content_tags(file_path)

        assert "finance" in tags
        assert "invoice" in tags

    def test_suggests_descriptive_filename(self, mount_dir):
        file_path = os.path.join(mount_dir, "scan001.txt")
        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write("Team meeting notes about project launch timeline and client milestones.")

        suggested = suggest_smart_filename(file_path)

        assert suggested.endswith(".txt")
        assert "meeting" in suggested or "project" in suggested
