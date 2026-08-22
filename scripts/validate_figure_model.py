#!/usr/bin/env python3
"""Validate the semantic figure model before drawing or before final asset use."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "title",
    "primary_output",
    "reading_order",
    "nodes",
    "edges",
    "groups",
    "asset_queries",
    "uncertainties",
}


def validate_model(data: object, *, require_assets_resolved: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top level must be a JSON object"]

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append("missing top-level keys: " + ", ".join(missing))

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    groups = data.get("groups", [])
    queries = data.get("asset_queries", [])

    if data.get("primary_output") not in {"pptx", "drawio", "both"}:
        errors.append("primary_output must be pptx, drawio, or both")
    if not isinstance(nodes, list) or not nodes:
        errors.append("nodes must be a non-empty list")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be a list")
        edges = []
    if not isinstance(groups, list):
        errors.append("groups must be a list")
        groups = []
    if not isinstance(queries, list):
        errors.append("asset_queries must be a list")
        queries = []

    node_ids: set[str] = set()
    search_nodes: set[str] = set()
    for index, node in enumerate(nodes):
        where = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{where} must be an object")
            continue
        node_id = str(node.get("id", "")).strip()
        if not node_id:
            errors.append(f"{where}.id is required")
        elif node_id in node_ids:
            errors.append(f"duplicate node id: {node_id}")
        else:
            node_ids.add(node_id)
        for key in ("label", "role", "kind", "group"):
            if not str(node.get(key, "")).strip():
                errors.append(f"{where}.{key} is required")
        strategy = str(node.get("asset_strategy", "none")).strip()
        if strategy not in {"search", "native-shape", "none", "raster-context"}:
            errors.append(f"{where}.asset_strategy has unsupported value: {strategy}")
        if strategy == "search" and node_id:
            search_nodes.add(node_id)

    edge_ids: set[str] = set()
    for index, edge in enumerate(edges):
        where = f"edges[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{where} must be an object")
            continue
        edge_id = str(edge.get("id", "")).strip()
        if not edge_id:
            errors.append(f"{where}.id is required")
        elif edge_id in edge_ids:
            errors.append(f"duplicate edge id: {edge_id}")
        else:
            edge_ids.add(edge_id)
        source = str(edge.get("source", "")).strip()
        target = str(edge.get("target", "")).strip()
        if source not in node_ids:
            errors.append(f"{where}.source does not name a node: {source}")
        if target not in node_ids:
            errors.append(f"{where}.target does not name a node: {target}")
        if not str(edge.get("relation", "")).strip():
            errors.append(f"{where}.relation is required")

    query_nodes: set[str] = set()
    for index, query in enumerate(queries):
        where = f"asset_queries[{index}]"
        if not isinstance(query, dict):
            errors.append(f"{where} must be an object")
            continue
        node_id = str(query.get("node_id", "")).strip()
        query_nodes.add(node_id)
        terms = query.get("queries", [])
        if node_id not in node_ids:
            errors.append(f"{where}.node_id does not name a node: {node_id}")
        if not str(query.get("canonical_name", "")).strip():
            errors.append(f"{where}.canonical_name is required")
        if not isinstance(terms, list) or not any(str(term).strip() for term in terms):
            errors.append(f"{where}.queries must contain at least one term")
        if (
            require_assets_resolved
            and not str(query.get("selected_asset", "")).strip()
            and not str(query.get("fallback_reason", "")).strip()
        ):
            errors.append(
                f"{where} needs selected_asset or fallback_reason before completing Stage 3"
            )

    for node_id in sorted(search_nodes - query_nodes):
        errors.append(f"node '{node_id}' requires a planned asset query")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="path to figure-model.json")
    parser.add_argument(
        "--require-assets-resolved",
        action="store_true",
        help="require every asset query to select an asset or document a fallback (Stage 3 gate)",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.model.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: model not found: {args.model}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_model(data, require_assets_resolved=args.require_assets_resolved)
    if errors:
        print(f"MODEL VALIDATION FAILED for {args.model}:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Figure model is valid: {args.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
