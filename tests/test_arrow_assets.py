from pathlib import Path
import xml.etree.ElementTree as ET


SKILL_ROOT = Path(__file__).resolve().parents[1]
ARROW_DIR = SKILL_ROOT / "assets" / "vector-arrows"


def test_bundled_arrow_family_is_complete_and_safe():
    expected = {"arrow-right.svg", "arrow-down-right.svg", "funnel.svg", "zoom-in.svg"}
    assert expected.issubset({path.name for path in ARROW_DIR.glob("*.svg")})
    assert (ARROW_DIR / "LICENSE.txt").is_file()

    for name in expected:
        text = (ARROW_DIR / name).read_text(encoding="utf-8")
        root = ET.fromstring(text)
        assert root.tag.endswith("svg")
        assert "<script" not in text.lower()
        assert "foreignObject" not in text
        assert "http://" not in text.replace("http://www.w3.org/2000/svg", "")
        assert "https://" not in text
        assert "currentColor" in text
