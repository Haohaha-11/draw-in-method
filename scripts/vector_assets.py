#!/usr/bin/env python3
"""Import, normalize, search, and embed local SVG assets for draw.io figures.

The importer is intentionally provider-agnostic. It accepts SVG files already
downloaded by the user from Iconfont, Flaticon, Iconify, or another source; SVG
directories and ZIP exports; and Iconfont-style JavaScript symbol bundles. It
does not scrape provider websites or depend on provider-private APIs.

Examples:
  python vector_assets.py import sensor.svg --provider iconfont --aliases "sensor,传感器"
  python vector_assets.py import flaticon-pack.zip --provider flaticon --color-mode academic
  python vector_assets.py search "传感器"
  python vector_assets.py drawio iconfont:wearable-sensor --size 96 --json
  python vector_assets.py validate
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import html
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Iterator
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parent
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

ALLOWED_TAGS = {
    "svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline",
    "polygon", "defs", "linearGradient", "radialGradient", "stop",
    "clipPath", "mask", "pattern", "use", "symbol", "style", "title", "desc",
}
DANGEROUS_TAGS = {"script", "foreignObject", "iframe", "object", "embed", "image"}
ACADEMIC_FILLS = ["#E8F2F5", "#EAF0F6", "#EDE9F4", "#F4EEDC", "#F1D7D4", "#E5F1E3"]
ACADEMIC_STROKES = ["#58727D", "#63758A", "#7B6A9A", "#9A7B3F", "#B44948", "#5A8A55"]
COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsla?\([^)]*\)")
SYMBOL_RE = re.compile(r"<symbol\b.*?</symbol>", re.IGNORECASE | re.DOTALL)
TOKEN_RE = re.compile(r"[a-z0-9]+|[\u3400-\u9fff]+", re.IGNORECASE)


class AssetError(ValueError):
    """Raised for an unsafe or unsupported vector asset."""


@dataclass
class SourceSvg:
    name: str
    data: bytes
    origin: str


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def slugify(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9\u3400-\u9fff-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "asset"


def split_aliases(values: Iterable[str]) -> list[str]:
    aliases: list[str] = []
    for value in values:
        for item in re.split(r"[,;]", value):
            item = item.strip()
            if item and item not in aliases:
                aliases.append(item)
    return aliases


def reject_document_level_hazards(data: bytes) -> None:
    head = data[:8192].lower()
    if b"<!doctype" in head or b"<!entity" in head:
        raise AssetError("DOCTYPE and ENTITY declarations are not accepted")
    if b"javascript:" in data.lower():
        raise AssetError("javascript: references are not accepted")


def parse_svg(data: bytes) -> ET.Element:
    reject_document_level_hazards(data)
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise AssetError(f"invalid SVG XML: {exc}") from exc
    if local_name(root.tag) != "svg":
        raise AssetError("root element is not <svg>")
    return root


def style_is_safe(value: str) -> bool:
    lowered = value.lower().replace(" ", "")
    if any(token in lowered for token in ("javascript:", "expression(", "@import", "-moz-binding")):
        return False
    for match in re.finditer(r"url\(([^)]*)\)", value, re.IGNORECASE):
        target = match.group(1).strip(" \"'")
        if target and not target.startswith("#"):
            return False
    return True


def sanitize_tree(root: ET.Element) -> dict[str, int]:
    removed_elements = 0
    removed_attributes = 0
    for parent in list(root.iter()):
        for child in list(parent):
            tag = local_name(child.tag)
            unsafe_style = tag == "style" and not style_is_safe(child.text or "")
            if tag in DANGEROUS_TAGS or tag not in ALLOWED_TAGS or unsafe_style:
                parent.remove(child)
                removed_elements += 1

    for elem in root.iter():
        for attr, value in list(elem.attrib.items()):
            name = local_name(attr).lower()
            if name.startswith("on"):
                del elem.attrib[attr]
                removed_attributes += 1
                continue
            if name in {"href", "src"}:
                target = value.strip()
                if target and not target.startswith("#"):
                    del elem.attrib[attr]
                    removed_attributes += 1
                    continue
            if name == "style" and not style_is_safe(value):
                del elem.attrib[attr]
                removed_attributes += 1
                continue
            if "url(" in value.lower() and not style_is_safe(value):
                del elem.attrib[attr]
                removed_attributes += 1

    return {"removed_elements": removed_elements, "removed_attributes": removed_attributes}


def numeric_dimension(value: str | None) -> float | None:
    if not value:
        return None
    match = re.match(r"\s*([0-9]+(?:\.[0-9]+)?)", value)
    return float(match.group(1)) if match else None


def normalize_root(root: ET.Element) -> None:
    view_box = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if not view_box:
        width = numeric_dimension(root.attrib.get("width"))
        height = numeric_dimension(root.attrib.get("height"))
        if width and height:
            root.set("viewBox", f"0 0 {width:g} {height:g}")
        else:
            raise AssetError("SVG needs a viewBox or numeric width and height")
    elif "viewbox" in root.attrib:
        root.set("viewBox", root.attrib.pop("viewbox"))
    root.attrib.pop("width", None)
    root.attrib.pop("height", None)
    root.set("preserveAspectRatio", "xMidYMid meet")


def recolor_value(value: str, replacement: str) -> str:
    if value.strip().lower() in {"none", "transparent"} or value.strip().lower().startswith("url("):
        return value
    return COLOR_RE.sub(replacement, value) if COLOR_RE.search(value) else replacement


def apply_color_mode(root: ET.Element, mode: str, mono_color: str) -> None:
    if mode == "preserve":
        return
    fill_index = 0
    stroke_index = 0
    fill_map: dict[str, str] = {}
    stroke_map: dict[str, str] = {}

    for elem in root.iter():
        if local_name(elem.tag) == "style" and elem.text:
            if mode == "mono":
                elem.text = COLOR_RE.sub(mono_color, elem.text)
            else:
                css_map: dict[str, str] = {}

                def academic_css_color(match: re.Match[str]) -> str:
                    key = match.group(0).lower()
                    if key not in css_map:
                        css_map[key] = ACADEMIC_FILLS[len(css_map) % len(ACADEMIC_FILLS)]
                    return css_map[key]

                elem.text = COLOR_RE.sub(academic_css_color, elem.text)
        for attr in ("fill", "stroke", "stop-color", "color"):
            if attr not in elem.attrib:
                continue
            value = elem.attrib[attr]
            if value.strip().lower() in {"none", "transparent"} or value.strip().lower().startswith("url("):
                continue
            if mode == "mono":
                elem.set(attr, recolor_value(value, mono_color))
            elif attr in {"stroke", "color"}:
                key = value.lower()
                if key not in stroke_map:
                    stroke_map[key] = ACADEMIC_STROKES[stroke_index % len(ACADEMIC_STROKES)]
                    stroke_index += 1
                elem.set(attr, recolor_value(value, stroke_map[key]))
            else:
                key = value.lower()
                if key not in fill_map:
                    fill_map[key] = ACADEMIC_FILLS[fill_index % len(ACADEMIC_FILLS)]
                    fill_index += 1
                elem.set(attr, recolor_value(value, fill_map[key]))

        style = elem.attrib.get("style")
        if style:
            declarations = []
            for declaration in style.split(";"):
                if ":" not in declaration:
                    if declaration.strip():
                        declarations.append(declaration)
                    continue
                key, value = declaration.split(":", 1)
                key_l = key.strip().lower()
                if key_l in {"fill", "stroke", "stop-color", "color"}:
                    if mode == "mono":
                        value = recolor_value(value, mono_color)
                    elif key_l in {"stroke", "color"}:
                        value = ACADEMIC_STROKES[0]
                    else:
                        value = ACADEMIC_FILLS[0]
                declarations.append(f"{key}:{value}")
            elem.set("style", ";".join(declarations))


def serialize_svg(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def svg_from_symbol(symbol_xml: str, origin: str) -> SourceSvg:
    try:
        symbol = ET.fromstring(symbol_xml)
    except ET.ParseError as exc:
        raise AssetError(f"invalid SVG symbol in {origin}: {exc}") from exc
    symbol_id = symbol.attrib.get("id", "symbol")
    root = ET.Element(f"{{{SVG_NS}}}svg")
    if symbol.attrib.get("viewBox"):
        root.set("viewBox", symbol.attrib["viewBox"])
    for child in list(symbol):
        root.append(copy.deepcopy(child))
    return SourceSvg(slugify(re.sub(r"^icon-", "", symbol_id)), serialize_svg(root), origin)


def symbols_from_js(data: bytes, origin: str) -> list[SourceSvg]:
    text = html.unescape(data.decode("utf-8", errors="replace"))
    text = text.replace("\\\"", '"').replace("\\'", "'").replace("\\n", "")
    return [svg_from_symbol(match.group(0), origin) for match in SYMBOL_RE.finditer(text)]


def sources_from_zip(path: Path) -> Iterator[SourceSvg]:
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            member = PurePosixPath(info.filename)
            if info.is_dir() or member.name.startswith("."):
                continue
            suffix = member.suffix.lower()
            if suffix == ".svg":
                yield SourceSvg(member.stem, archive.read(info), f"{path}!{info.filename}")
            elif suffix == ".js" and "iconfont" in member.name.lower():
                yield from symbols_from_js(archive.read(info), f"{path}!{info.filename}")


def sources_from_path(path: Path) -> Iterator[SourceSvg]:
    if not path.exists():
        raise AssetError(f"input does not exist: {path}")
    if path.is_dir():
        for child in sorted(path.rglob("*")):
            if child.is_file() and child.suffix.lower() in {".svg", ".zip", ".js"}:
                yield from sources_from_path(child)
        return
    suffix = path.suffix.lower()
    if suffix == ".svg":
        yield SourceSvg(path.stem, path.read_bytes(), str(path))
    elif suffix == ".zip":
        yield from sources_from_zip(path)
    elif suffix == ".js":
        symbols = symbols_from_js(path.read_bytes(), str(path))
        if not symbols:
            raise AssetError(f"no <symbol> entries found in {path}")
        yield from symbols
    else:
        raise AssetError(f"unsupported input type: {path}")


def load_registry(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "assets": []}
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssetError(f"cannot read registry {path}: {exc}") from exc
    if registry.get("schema_version") != 1 or not isinstance(registry.get("assets"), list):
        raise AssetError(f"unsupported registry schema in {path}")
    return registry


def save_registry(path: Path, registry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def path_for_registry(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def import_assets(args: argparse.Namespace) -> int:
    root_dir = args.root.resolve()
    registry_path = args.registry if args.registry.is_absolute() else root_dir / args.registry
    assets_dir = args.assets_dir if args.assets_dir.is_absolute() else root_dir / args.assets_dir
    registry = load_registry(registry_path)
    aliases = split_aliases(args.aliases)
    source_items: list[SourceSvg] = []
    for raw_path in args.paths:
        source_items.extend(sources_from_path(raw_path.resolve()))
    if not source_items:
        raise AssetError("no SVG assets found")
    if args.name and len(source_items) != 1:
        raise AssetError("--name can only be used when exactly one SVG is imported")

    existing_ids = {item["id"] for item in registry["assets"]}
    existing_hashes = {item.get("sha256"): item for item in registry["assets"]}
    imported = 0
    skipped = 0
    for source in source_items:
        root = parse_svg(source.data)
        sanitization = sanitize_tree(root)
        normalize_root(root)
        apply_color_mode(root, args.color_mode, args.color)
        payload = serialize_svg(root)
        digest = hashlib.sha256(payload).hexdigest()
        if digest in existing_hashes and not args.overwrite:
            skipped += 1
            continue

        display_name = args.name or source.name
        slug = slugify(display_name)
        asset_id = f"{args.provider}:{slug}"
        if asset_id in existing_ids:
            if args.overwrite:
                registry["assets"] = [item for item in registry["assets"] if item["id"] != asset_id]
                existing_ids.remove(asset_id)
            else:
                asset_id = f"{asset_id}-{digest[:8]}"
        collection = slugify(args.collection) if args.collection else "default"
        output_dir = assets_dir / slugify(args.provider) / collection
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{slug}.svg"
        if output_path.exists() and hashlib.sha256(output_path.read_bytes()).hexdigest() != digest:
            output_path = output_dir / f"{slug}-{digest[:8]}.svg"
        output_path.write_bytes(payload)

        entry = {
            "id": asset_id,
            "name": display_name,
            "aliases": aliases if len(source_items) == 1 else [],
            "provider": args.provider,
            "collection": args.collection or "default",
            "source_url": args.source_url or None,
            "source_origin": source.origin,
            "author": args.author or None,
            "license": args.license or None,
            "attribution": args.attribution or None,
            "color_mode": args.color_mode,
            "file": path_for_registry(output_path, root_dir),
            "sha256": digest,
            "sanitization": sanitization,
        }
        registry["assets"].append(entry)
        existing_ids.add(asset_id)
        existing_hashes[digest] = entry
        imported += 1
        print(f"imported {asset_id} -> {entry['file']}")

    registry["assets"].sort(key=lambda item: item["id"])
    save_registry(registry_path, registry)
    print(f"summary: imported={imported} skipped_duplicate={skipped} registry={registry_path}")
    return 0


def searchable_text(asset: dict) -> str:
    fields = [asset.get("id", ""), asset.get("name", ""), asset.get("provider", ""), asset.get("collection", "")]
    fields.extend(asset.get("aliases") or [])
    return " ".join(str(field) for field in fields).lower()


def score_asset(asset: dict, query: str) -> float:
    haystack = searchable_text(asset)
    query_l = query.strip().lower()
    if not query_l:
        return 1.0
    score = 0.0
    if query_l == asset.get("id", "").lower():
        score += 100.0
    if query_l == str(asset.get("name", "")).lower():
        score += 80.0
    if query_l in haystack:
        score += 30.0
    for token in TOKEN_RE.findall(query_l):
        if token in haystack:
            score += 10.0
        if any(token == str(alias).lower() for alias in asset.get("aliases") or []):
            score += 8.0
    return score


def registry_for_args(args: argparse.Namespace) -> tuple[Path, dict]:
    registry_path = args.registry if args.registry.is_absolute() else args.root.resolve() / args.registry
    return registry_path, load_registry(registry_path)


def search_assets(args: argparse.Namespace) -> int:
    _, registry = registry_for_args(args)
    ranked = [(score_asset(asset, args.query), asset) for asset in registry["assets"]]
    ranked = [(score, asset) for score, asset in ranked if score > 0]
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    results = [dict(asset, score=score) for score, asset in ranked[: args.limit]]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for asset in results:
            print(f"{asset['id']}  score={asset['score']:.1f}  file={asset['file']}")
    return 0 if results else 1


def find_asset(registry: dict, asset_id: str) -> dict:
    exact = [asset for asset in registry["assets"] if asset["id"] == asset_id]
    if exact:
        return exact[0]
    ranked = [(score_asset(asset, asset_id), asset) for asset in registry["assets"]]
    ranked.sort(key=lambda pair: -pair[0])
    if not ranked or ranked[0][0] <= 0:
        raise AssetError(f"asset not found: {asset_id}")
    return ranked[0][1]


def asset_file(root: Path, asset: dict) -> Path:
    path = Path(asset["file"])
    return path if path.is_absolute() else root / path


def drawio_style(args: argparse.Namespace) -> int:
    _, registry = registry_for_args(args)
    asset = find_asset(registry, args.asset_id)
    path = asset_file(args.root.resolve(), asset)
    payload = path.read_bytes()
    encoded = base64.b64encode(payload).decode("ascii")
    # Marker-less base64 avoids draw.io splitting style values at ';base64,'.
    image = "data:image/svg+xml," + encoded
    style = (
        "shape=image;html=1;imageAspect=0;aspect=fixed;"
        "verticalLabelPosition=bottom;verticalAlign=top;image=" + image
    )
    result = {"id": asset["id"], "w": args.size, "h": args.size, "style": style,
              "attribution": asset.get("attribution")}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(style)
    return 0


def validate_assets(args: argparse.Namespace) -> int:
    registry_path, registry = registry_for_args(args)
    findings: list[str] = []
    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    for asset in registry["assets"]:
        asset_id = asset.get("id", "<missing-id>")
        if asset_id in seen_ids:
            findings.append(f"FAIL duplicate id: {asset_id}")
        seen_ids.add(asset_id)
        path = asset_file(args.root.resolve(), asset)
        if not path.exists():
            findings.append(f"FAIL missing file: {asset_id} -> {path}")
            continue
        try:
            parsed = parse_svg(path.read_bytes())
            sanitize_result = sanitize_tree(parsed)
            if sanitize_result["removed_elements"] or sanitize_result["removed_attributes"]:
                findings.append(f"FAIL unsafe content remains: {asset_id} {sanitize_result}")
        except AssetError as exc:
            findings.append(f"FAIL invalid SVG: {asset_id}: {exc}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != asset.get("sha256"):
            findings.append(f"FAIL hash mismatch: {asset_id}")
        if digest in seen_hashes:
            findings.append(f"WARN duplicate payload: {asset_id}")
        seen_hashes.add(digest)
        if asset.get("provider") == "flaticon" and not asset.get("attribution") and not asset.get("license"):
            findings.append(f"WARN Flaticon metadata missing attribution/license: {asset_id}")
    for finding in findings:
        print(finding)
    failures = sum(item.startswith("FAIL") for item in findings)
    warnings = sum(item.startswith("WARN") for item in findings)
    print(f"validated {len(registry['assets'])} assets: failures={failures} warnings={warnings} registry={registry_path}")
    return 1 if failures else 0


def list_assets(args: argparse.Namespace) -> int:
    _, registry = registry_for_args(args)
    if args.json:
        print(json.dumps(registry["assets"], indent=2, ensure_ascii=False))
    else:
        for asset in registry["assets"]:
            print(f"{asset['id']}  provider={asset['provider']}  file={asset['file']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local SVG assets for academic draw.io figures.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Skill root (default: parent of scripts/).")
    parser.add_argument("--registry", type=Path, default=Path("data/icon-registry.json"))
    sub = parser.add_subparsers(dest="command", required=True)

    imp = sub.add_parser("import", help="Import SVG files, directories, ZIPs, or Iconfont symbol JS bundles.")
    imp.add_argument("paths", nargs="+", type=Path)
    imp.add_argument("--provider", choices=["iconfont", "flaticon", "iconify", "local", "generated"], default="local")
    imp.add_argument("--collection", default="default")
    imp.add_argument("--name")
    imp.add_argument("--aliases", action="append", default=[], help="Comma-separated aliases; repeatable.")
    imp.add_argument("--source-url")
    imp.add_argument("--author")
    imp.add_argument("--license")
    imp.add_argument("--attribution")
    imp.add_argument("--color-mode", choices=["preserve", "academic", "mono"], default="preserve")
    imp.add_argument("--color", default="#58727D", help="Color used by --color-mode mono.")
    imp.add_argument("--assets-dir", type=Path, default=Path("assets/icons"))
    imp.add_argument("--overwrite", action="store_true")
    imp.set_defaults(func=import_assets)

    search = sub.add_parser("search", help="Search the local vector asset registry.")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--json", action="store_true")
    search.set_defaults(func=search_assets)

    drawio = sub.add_parser("drawio", help="Emit a self-contained draw.io image style for a registered asset.")
    drawio.add_argument("asset_id")
    drawio.add_argument("--size", type=int, default=96)
    drawio.add_argument("--json", action="store_true")
    drawio.set_defaults(func=drawio_style)

    validate = sub.add_parser("validate", help="Validate registry entries, SVG safety, and file hashes.")
    validate.set_defaults(func=validate_assets)

    listing = sub.add_parser("list", help="List registered assets.")
    listing.add_argument("--json", action="store_true")
    listing.set_defaults(func=list_assets)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (AssetError, OSError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
