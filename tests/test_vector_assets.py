from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "vector_assets.py"


class VectorAssetsCliTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, msg=result.stdout + result.stderr)
        return result

    def test_import_search_embed_and_validate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "wearable.svg"
            source.write_text(
                """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"
                onload="alert(1)">
                <style>.accent { fill: #224466; }</style>
                <script>alert(1)</script>
                <image href="https://example.com/tracker.png" width="64" height="64"/>
                <rect x="8" y="4" width="48" height="56" fill="#ff0000" stroke="#111111"/>
                <circle cx="32" cy="32" r="10" fill="#00ff00"/>
                </svg>""",
                encoding="utf-8",
            )

            self.run_cli(
                root,
                "import", str(source),
                "--provider", "flaticon",
                "--name", "Wearable Sensor",
                "--aliases", "wearable sensor,可穿戴传感器",
                "--author", "Test Author",
                "--license", "Free with attribution",
                "--attribution", "Designed by Test Author from Flaticon",
                "--color-mode", "academic",
            )

            registry = json.loads((root / "data" / "icon-registry.json").read_text(encoding="utf-8"))
            self.assertEqual(1, len(registry["assets"]))
            asset = registry["assets"][0]
            self.assertEqual("flaticon:wearable-sensor", asset["id"])
            self.assertEqual("Test Author", asset["author"])
            self.assertEqual(2, asset["sanitization"]["removed_elements"])
            payload = (root / asset["file"]).read_text(encoding="utf-8")
            self.assertNotIn("script", payload.lower())
            self.assertNotIn("example.com", payload)
            self.assertNotIn("onload", payload.lower())
            self.assertIn("viewBox", payload)
            self.assertIn("#E8F2F5", payload)
            self.assertNotIn("#224466", payload)

            search = self.run_cli(root, "search", "可穿戴传感器", "--json")
            self.assertEqual("flaticon:wearable-sensor", json.loads(search.stdout)[0]["id"])

            drawio = self.run_cli(root, "drawio", "flaticon:wearable-sensor", "--json")
            result = json.loads(drawio.stdout)
            self.assertTrue(result["style"].startswith("shape=image;"))
            self.assertIn("data:image/svg+xml,", result["style"])
            self.assertNotIn("https://", result["style"])

            mxfile = ET.Element("mxfile")
            diagram = ET.SubElement(mxfile, "diagram", {"name": "Page-1"})
            model = ET.SubElement(diagram, "mxGraphModel")
            cells = ET.SubElement(model, "root")
            ET.SubElement(cells, "mxCell", {"id": "0"})
            ET.SubElement(cells, "mxCell", {"id": "1", "parent": "0"})
            icon = ET.SubElement(cells, "mxCell", {
                "id": "icon-1", "value": "Wearable Sensor", "style": result["style"],
                "vertex": "1", "parent": "1",
            })
            ET.SubElement(icon, "mxGeometry", {
                "x": "40", "y": "40", "width": "96", "height": "96", "as": "geometry",
            })
            drawio_path = root / "embedded-icon.drawio"
            ET.ElementTree(mxfile).write(drawio_path, encoding="utf-8", xml_declaration=True)
            validation = subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts" / "validate_drawio.py"), str(drawio_path)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, validation.returncode, msg=validation.stdout + validation.stderr)

            self.run_cli(root, "validate")

    def test_iconfont_symbol_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / "iconfont.js"
            bundle.write_text(
                "var svgSprite='<svg><symbol id=\"icon-microscope\" viewBox=\"0 0 1024 1024\">"
                "<path fill=\"#333333\" d=\"M0 0h100v100H0z\"/></symbol></svg>';",
                encoding="utf-8",
            )
            self.run_cli(root, "import", str(bundle), "--provider", "iconfont", "--color-mode", "mono")
            registry = json.loads((root / "data" / "icon-registry.json").read_text(encoding="utf-8"))
            self.assertEqual("iconfont:microscope", registry["assets"][0]["id"])
            payload = (root / registry["assets"][0]["file"]).read_text(encoding="utf-8")
            self.assertIn("#58727D", payload)

    def test_flaticon_zip_preserves_multicolor_svg(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / "flaticon-pack.zip"
            with zipfile.ZipFile(bundle, "w") as archive:
                archive.writestr(
                    "svg/laboratory.svg",
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
                    '<path fill="#123456" d="M0 0h16v32H0z"/>'
                    '<path fill="#abcdef" d="M16 0h16v32H16z"/></svg>',
                )
            self.run_cli(
                root, "import", str(bundle), "--provider", "flaticon",
                "--collection", "laboratory", "--color-mode", "preserve",
                "--attribution", "Designed by Test Author from Flaticon",
            )
            registry = json.loads((root / "data" / "icon-registry.json").read_text(encoding="utf-8"))
            payload = (root / registry["assets"][0]["file"]).read_text(encoding="utf-8")
            self.assertIn("#123456", payload)
            self.assertIn("#abcdef", payload)


if __name__ == "__main__":
    unittest.main()
