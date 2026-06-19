"""Flask route handlers for file-org-wiz MCP server."""

from __future__ import annotations

import os
from typing import Any

from flask import Response, jsonify, request

from file_org_wiz.core.organizer import (
    apply_naming_convention,
    create_analytics_report,
    create_backup,
    create_folder_structure,
    create_template_structure,
    get_directory_structure,
    validate_path,
)

try:
    from file_org_wiz.nlp_processor import (
        generate_mcp_payload,
        parse_organization_command,
    )
except ImportError:
    parse_organization_command = None
    generate_mcp_payload = None

try:
    from file_org_wiz.file_intelligence import (
        generate_content_tags,
        infer_context_description,
    )
except ImportError:
    infer_context_description = None
    generate_content_tags = None


def register_routes(app: Any) -> None:
    """Register all MCP routes on the Flask app."""

    @app.route("/health", methods=["GET"])
    def health_check() -> Response:
        return jsonify(
            {"status": "healthy", "service": "file-org-wiz-mcp", "version": "1.3.0"}
        )

    @app.route("/organize", methods=["POST"])
    def organize() -> tuple[Response, int]:
        data = request.get_json(silent=True) or {}
        mount_path = data.get(
            "mount_path",
            data.get("path", os.environ.get("FILE_ORG_WIZ_MOUNT", "/data")),
        )
        backup_path = data.get(
            "backup_path", os.environ.get("FILE_ORG_WIZ_BACKUP", "/data/backup")
        )
        dry_run = data.get("dry_run", False)
        template = data.get("template", "")
        data.get("create_vault", False)

        valid, error = validate_path(mount_path)
        if not valid:
            return jsonify({"error": error}), 400

        if dry_run:
            return jsonify(
                {
                    "message": "Dry run mode",
                    "suggested_actions": [
                        "Create PARA folder structure",
                        f"Template: {template}"
                        if template
                        else "Scan and categorize files",
                        f"Backup to {backup_path}"
                        if data.get("do_backup")
                        else "No backup requested",
                    ],
                }
            ), 200

        results: dict[str, Any] = {"phases": [], "errors": []}

        # Create folder structure
        structure_result = create_folder_structure(mount_path)
        results["phases"].append({"name": "structure", **structure_result})
        if structure_result.get("errors"):
            results["errors"].extend(structure_result["errors"])

        # Apply template if specified
        if template:
            template_result = create_template_structure(mount_path, template)
            results["phases"].append({"name": "apply_template", **template_result})
            if template_result.get("errors"):
                results["errors"].extend(template_result["errors"])

        # Backup if requested
        if data.get("do_backup"):
            backup_result = create_backup(mount_path, backup_path)
            results["phases"].append({"name": "backup", **backup_result})
            if backup_result.get("errors"):
                results["errors"].extend(backup_result["errors"])

        results["status"] = "complete"
        return jsonify(results), 200

    @app.route("/backup", methods=["POST"])
    def backup() -> tuple[Response, int]:
        data = request.get_json(silent=True) or {}
        source = data.get("source_path", os.environ.get("FILE_ORG_WIZ_MOUNT", "/data"))
        dest = data.get(
            "backup_path", os.environ.get("FILE_ORG_WIZ_BACKUP", "/data/backup")
        )
        result = create_backup(source, dest)
        return jsonify(result), 200

    @app.route("/structure", methods=["GET"])
    def structure() -> tuple[Response, int]:
        path = request.args.get("path", os.environ.get("FILE_ORG_WIZ_MOUNT", "/data"))
        max_depth = int(request.args.get("max_depth", "3"))
        valid, error = validate_path(path)
        if not valid:
            return jsonify({"error": error}), 400
        result = get_directory_structure(path, max_depth)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200

    @app.route("/analytics", methods=["GET"])
    def analytics() -> tuple[Response, int]:
        path = request.args.get("path", os.environ.get("FILE_ORG_WIZ_MOUNT", "/data"))
        valid, error = validate_path(path)
        if not valid:
            return jsonify({"error": error}), 400
        result = create_analytics_report(path)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200

    @app.route("/apply-names", methods=["POST"])
    def apply_names() -> tuple[Response, int]:
        data = request.get_json(silent=True) or {}
        file_path = data.get("file_path", "")
        context = data.get("context", "general")
        description = data.get("description", "unnamed")
        version = int(data.get("version", 1))
        auto_describe = data.get("auto_describe", False)
        if auto_describe and infer_context_description:
            inferred = infer_context_description(file_path)
            if isinstance(inferred, str):
                description = inferred
        result = apply_naming_convention(file_path, context, description, version)
        status = 200 if result.get("success") else 400
        return jsonify(result), status

    @app.route("/analyze-file", methods=["POST"])
    def analyze_file() -> tuple[Response, int]:
        data = request.get_json(silent=True) or {}
        file_path = data.get("file_path", "")
        valid, error = validate_path(file_path)
        if not valid:
            return jsonify({"error": error}), 400
        tags = generate_content_tags(file_path) if generate_content_tags else []
        description = (
            infer_context_description(file_path) if infer_context_description else ""
        )
        return jsonify(
            {
                "file_path": file_path,
                "tags": tags,
                "suggested_description": description or os.path.basename(file_path),
            }
        ), 200

    @app.route("/nlp-command", methods=["POST"])
    def nlp_command() -> tuple[Response, int]:
        data = request.get_json(silent=True) or {}
        command = data.get("command", "")
        data.get("preview_only", False)
        if not command:
            return jsonify({"error": "No command provided"}), 400
        if parse_organization_command:
            parsed = parse_organization_command(command)
            if generate_mcp_payload:
                payload = generate_mcp_payload(parsed)
                payload["status"] = "parsed"
                payload["parsed_command"] = parsed
                return jsonify(payload), 200
        return jsonify(
            {"parsed": command, "message": "NLP processing not available"}
        ), 200

    @app.route("/mcp-manifest", methods=["GET"])
    def mcp_manifest() -> Response:
        return jsonify(
            {
                "protocol": "MCP",
                "version": "1.0",
                "tools": [
                    {"name": "health", "description": "Health check"},
                    {"name": "organize", "description": "Execute reorganization"},
                    {"name": "backup", "description": "Create backup"},
                    {"name": "structure", "description": "Get directory structure"},
                    {"name": "analytics", "description": "Get analytics"},
                    {"name": "apply-names", "description": "Apply naming convention"},
                    {"name": "analyze-file", "description": "Analyze single file"},
                    {"name": "nlp-command", "description": "Natural language commands"},
                    {"name": "mcp-manifest", "description": "This manifest"},
                ],
                "endpoints": [
                    {
                        "path": "/health",
                        "methods": ["GET"],
                        "description": "Health check",
                    },
                    {
                        "path": "/organize",
                        "methods": ["POST"],
                        "description": "Execute reorganization",
                    },
                    {
                        "path": "/backup",
                        "methods": ["POST"],
                        "description": "Create backup",
                    },
                    {
                        "path": "/structure",
                        "methods": ["GET"],
                        "description": "Get directory structure",
                    },
                    {
                        "path": "/analytics",
                        "methods": ["GET"],
                        "description": "Get analytics",
                    },
                    {
                        "path": "/apply-names",
                        "methods": ["POST"],
                        "description": "Apply naming convention",
                    },
                    {
                        "path": "/analyze-file",
                        "methods": ["POST"],
                        "description": "Analyze single file",
                    },
                    {
                        "path": "/nlp-command",
                        "methods": ["POST"],
                        "description": "Natural language commands",
                    },
                    {
                        "path": "/mcp-manifest",
                        "methods": ["GET"],
                        "description": "This manifest",
                    },
                ],
            }
        )
