#!/usr/bin/env python3
"""Organize files in a directory using file-org-wiz.

Demonstrates scanning, analyzing, and organizing files using
PARA + Zettelkasten methodology.

Usage:
    python examples/organize_downloads.py /path/to/your/folder

Requirements:
    pip install file-org-wiz
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from repo checkout
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from file_org_wiz.file_intelligence import analyze_directory
from file_org_wiz.scanner import scan_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="file-org-wiz demo")
    parser.add_argument(
        "directory",
        nargs="?",
        default="/tmp/org-demo",
        help="Directory to organize (creates demo files if not exists)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Preview changes without moving files",
    )

    args = parser.parse_args()
    target = Path(args.directory)

    # Create demo files if directory doesn't exist
    if not target.exists():
        print(f"Creating demo directory: {target}")
        target.mkdir(parents=True, exist_ok=True)
        (target / "project_notes.txt").write_text("Meeting notes from sprint planning")
        (target / "budget_2026.xlsx").write_text("dummy")
        (target / "image_photo.png").write_text("dummy")
        (target / "readme.md").write_text("# Demo Project")
        (target / "old_backup_2025.zip").write_text("dummy")
        (target / "quick_script.py").write_text("print('hello')")

    print("=" * 60)
    print("file-org-wiz — Directory Organization Demo")
    print("=" * 60)
    print(f"Target: {target}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Step 1: Scan
    files = scan_directory(str(target))
    print(f"Found {len(files)} files")
    for f in files:
        print(f"  {f.get('name', Path(f['path']).name):30s} {f.get('type', 'unknown')}")

    # Step 2: Analyze
    print("\nAnalyzing...")
    analysis = analyze_directory(str(target))
    print(f"\nSuggested structure:")
    for cat, items in analysis.get("categories", {}).items():
        print(f"  [{cat}] ({len(items)} items)")

    # Step 3: Organize (dry-run by default)
    if not args.dry_run:
        print("\nOrganizing files...")
        # from file_org_wiz.mcp_server import organize  # actual organization
        print("  (wet run — moving files)")
    else:
        print(f"\nDry run complete. Run with --dry-run=False to apply.")


if __name__ == "__main__":
    main()
