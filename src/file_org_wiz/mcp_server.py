#!/usr/bin/env python3
"""File Organization Wizard MCP Server — entry point.

Creates the Flask app, registers routes from api/routes.py,
and provides the CLI entry point.

Run: python src/file_org_wiz/mcp_server.py [--port PORT] [--host HOST] [--mount PATH]
"""

from __future__ import annotations

import os
import argparse

from flask import Flask
from flask_cors import CORS

from file_org_wiz.api.routes import register_routes

# Re-export core functions for backward compatibility


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # CORS — only enable when explicitly requested
    if os.environ.get("FILE_ORG_WIZ_CORS", "false").lower() == "true":
        CORS(app)

    # Register all route handlers
    register_routes(app)

    return app


# Module-level app instance for compatibility with existing test fixtures
app = create_app()


def main() -> None:
    parser = argparse.ArgumentParser(description="File Organization Wizard MCP Server")
    parser.add_argument(
        "--host", default=os.environ.get("FILE_ORG_WIZ_HOST", "127.0.0.1")
    )
    parser.add_argument(
        "--port", type=int, default=int(os.environ.get("FILE_ORG_WIZ_PORT", "5000"))
    )
    parser.add_argument(
        "--mount", default=os.environ.get("FILE_ORG_WIZ_MOUNT", "/data")
    )
    parser.add_argument(
        "--backup", default=os.environ.get("FILE_ORG_WIZ_BACKUP", "/data/backup")
    )
    parser.add_argument("--cors", action="store_true", default=False)
    args = parser.parse_args()

    if args.cors:
        os.environ["FILE_ORG_WIZ_CORS"] = "true"

    app = create_app()
    print(f"file-org-wiz MCP server starting on http://{args.host}:{args.port}")
    print(f"  Mount path: {args.mount}")
    print(f"  Backup path: {args.backup}")
    print(f"  CORS: {'enabled' if args.cors else 'disabled (localhost only)'}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
