from __future__ import annotations

import copy
import unittest

from scripts.validate_figure_model import validate_model


def model_with_planned_asset() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "title": "Stage gate test",
        "primary_output": "pptx",
        "reading_order": "left-to-right",
        "nodes": [
            {
                "id": "input_image",
                "label": "Input image",
                "role": "input",
                "kind": "context",
                "group": "overview",
                "asset_strategy": "search",
            }
        ],
        "edges": [],
        "groups": [{"id": "overview", "label": "Overview", "members": ["input_image"]}],
        "asset_queries": [
            {
                "node_id": "input_image",
                "canonical_name": "input image",
                "queries": ["input image", "输入图像"],
                "providers": ["local-registry", "iconfont", "flaticon"],
                "selected_asset": "",
                "fallback_reason": "",
            }
        ],
        "uncertainties": [],
    }


class FigureModelStageGateTests(unittest.TestCase):
    def test_preflight_accepts_planned_unselected_asset(self) -> None:
        self.assertEqual([], validate_model(model_with_planned_asset()))

    def test_stage_three_gate_rejects_unresolved_asset(self) -> None:
        errors = validate_model(model_with_planned_asset(), require_assets_resolved=True)
        self.assertTrue(any("before completing Stage 3" in error for error in errors))

    def test_stage_three_gate_accepts_selected_asset(self) -> None:
        model = copy.deepcopy(model_with_planned_asset())
        model["asset_queries"][0]["selected_asset"] = "assets/input-image.svg"
        self.assertEqual([], validate_model(model, require_assets_resolved=True))


if __name__ == "__main__":
    unittest.main()
