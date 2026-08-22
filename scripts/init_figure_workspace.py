#!/usr/bin/env python3
"""Create the evidence workspace used by draw-in-method.

The command is intentionally conservative: it creates missing files and never
overwrites an existing brief, style contract, asset ledger, or defect log.
"""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATES = {
    "brief.md": """# Diagram brief\n\n## User goal\n- Audience: \n- Primary editable output: `.pptx` / `.drawio` / both\n- Review exports: PNG / SVG / PDF\n- Must communicate: \n- Must not do: \n\n## Source inventory\n| Source | Role (content/structure/style/layout/asset) | Notes |\n|---|---|---|\n| | | |\n\n## Requirement traceability\n| Requirement | Figure-model node/edge evidence | Status |\n|---|---|---|\n\n## Semantic model summary\n- Input: \n- Stages: \n- Proposed contribution: \n- Output: \n- Training-only path: \n- Reading order: \n\n## Open assumptions and unreadable evidence\n- \n""",
    "figure-model.json": """{\n  \"schema_version\": \"1.0\",\n  \"title\": \"Untitled research figure\",\n  \"primary_output\": \"pptx\",\n  \"reading_order\": \"left-to-right\",\n  \"nodes\": [],\n  \"edges\": [],\n  \"groups\": [],\n  \"asset_queries\": [],\n  \"uncertainties\": []\n}\n""",
    "visual-spec.md": """# Visual specification\n\n## Mode and global style\n- Figure mode: architecture / framework / module-detail / other\n- Presentation framing requested: no\n- Canvas/aspect: landscape, 1600–2200 × 850–1200 px\n- Architecture occupancy: 85–95%\n- Font: Times New Roman/Cambria (SimSun or Noto Serif CJK SC for Chinese)\n- Grid/margins: 8 px grid; 24–48 px outer margin at 1600 × 900\n- Corner radius / stroke: 4–10 px / 1.5–2 px\n- Shadows/gradients: off\n- Arrow grammar: black main flow; gray dashed skip/control; semantic color only with legend\n\n## Architecture palette (select only 3–5 semantic fills)\n| Meaning | Fill | Used in |\n|---|---|---|\n| Standard feature block | #B4C6E7 | |\n| Secondary branch | #D3D3FF | |\n| Reconstruction / upsample | #ADD7AC | |\n| Degradation / downsample | #E8B593 | |\n| Context / output family | #FAE4D5 | |\n| Warm secondary block | #FCDAB1 | |\n| Neutral panel | #FAF6E7 | |\n| Attention / query accent | #A2B6FA | |\n| Proposed / learnable accent | #EA717A | |\n| Soft proposed container | #F7E7EA | |\n\n## Typography\n- Optional figure/panel heading: 17–21 px, bold\n- Stage/group heading: 15–18 px, bold\n- Main/proposed module: 14–17 px, bold or bold italic\n- Standard module/operator: 12–15 px\n- Tensor/equation/legend: 9–13 px\n\n## Module scale at 1600 × 900\n- Standard module: 105–180 × 48–82 px\n- Small operator: 48–92 × 28–50 px\n- Proposed module: 140–230 × 64–110 px\n- Stage/group: 280–680 × 150–430 px\n- Repeated block size: \n\n## Composition notes\n- Main baseline: \n- Parallel branches: \n- Overview/detail split: \n- Legend: \n- Explicit exclusions (no large title/footer/explanation): \n""",
    "layout-grid.md": """# Layout and connector grid\n\n- Canvas: \n- Coordinate origin: \n- Major panels and bounding boxes: \n- Main horizontal baseline: \n- Parallel branch rows: \n- Repeated block size: \n- Dedicated connector lanes: \n- Forbidden crossing zones: text, labels, equations, modules, dense icon rows\n- Drawing order: background → containers → connectors → nodes → labels → legend\n\n## Connector ledger\n| Edge id | Source + port | Target + port | Relation | Route/lane | Label | Arrowhead |\n|---|---|---|---|---|---|---|\n| | | | data/control/skip/feedback/update | | | |\n\n## Routing audit\n- Main flow uses one baseline: \n- Normal edges have ≤1 bend: \n- Skip/feedback edges have ≤2 bends: \n- Text/module clearance ≥12 px: \n- Parallel lanes separated ≥8 px: \n- Fan-in/out ≥4 uses bus or junction: \n- No ambiguous endpoints or crossings: \n""",
    "asset-ledger.md": """# Asset ledger\n\n## Named search plan\n| Node id | Canonical entity | Chinese/English aliases | Providers searched | Candidate assets | Selection/fallback reason |\n|---|---|---|---|---|---|\n| | | | local registry, native shapes, Iconfont, Flaticon, Iconify | | |\n\n## Used assets\n| Asset | Role | Source/provenance | Editable? | Color mode | Decision |\n|---|---|---|---|---|---|\n| | input/context | | | | |\n\nGenerated concept images are references unless explicitly approved as input/context assets. Do not embed a screenshot of the entire algorithm as the final figure. Primitive-built physical/context icons require a documented search failure or a user request for a custom symbol.\n""",
    "production-review.md": """# Production review\n\nRecord each preview, finding, fix, and decision without overwriting earlier approved gates. Semantic preflight is mandatory but is not counted as one of the four visible production stages.\n\n## Semantic preflight\n- Figure-model validation: \n- Open uncertainties: \n- Decision: \n\n## Stage 1 — Architecture, base color, modules, and arrows\n\n### Checkpoint 1A — Canvas, background, and semantic regions\n- Preview: \n- Findings: \n- Fixes: \n- Decision: \n\n### Checkpoint 1B — Module composition and size families\n- Preview: \n- Findings: \n- Fixes: \n- Decision: \n\n### Checkpoint 1C — Main connector skeleton\n- Preview: \n- Findings: \n- Fixes: \n- Decision: \n\n### Checkpoint 1D — Branches, merges, skips, and feedback\n- Preview: \n- Findings: \n- Fixes: \n- Decision: \n\n## Stage 2 — Scientific text and annotations\n- Preview: \n- Paper-scale readability findings: \n- Fixes: \n- Decision: \n\n## Stage 3 — Named vector assets or transparent cutouts\n- Preview: \n- Asset-ledger update: \n- Strict asset-gate result: \n- Scale/style findings: \n- Fixes: \n- Decision: \n\n## Stage 4 — Full visual review and coordinated refinement\n- Full-canvas preview: \n- Dense-region crops: \n- Layout/font/color/connector findings: \n- Editability and export checks: \n- Fixes: \n- Final decision: \n""",
    "defect-log.md": """# Defect log\n\n## Pass 0 — Plan review\n- Status: \n- Open risks: \n\n## Screenshot review cycles\n\n### Cycle 1\n- Screenshot (canvas-only): \n- P0/P1 inventory: \n- Fixes and verification: \n\n### Cycle 2\n- Screenshot (canvas-only): \n- P0/P1 inventory: \n- Fixes and verification: \n\n### Cycle 3\n- Screenshot (canvas-only): \n- P0/P1 inventory: \n- Fixes and verification: \n\n## Red-team audit\n- Text: \n- Arrows: \n- Boxes/overlap: \n- Spacing/layout: \n- Color/typography: \n- Icons/assets: \n- Semantics/regressions: \n\n## Self-score\n| Dimension | Score /10 | Evidence |\n|---|---:|---|\n| Text readability | | |\n| Arrow accuracy | | |\n| Color coherence | | |\n| Layout consistency | | |\n| Style/spec match | | |\n| **Total /50** | | |\n\n## Remaining gaps\n- \n""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="figure work directory to create")
    parser.add_argument("--title", default="Untitled research figure")
    args = parser.parse_args()

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    created = []
    for name, body in TEMPLATES.items():
        path = out / name
        if path.exists():
            continue
        path.write_text(body.replace("Untitled research figure", args.title), encoding="utf-8")
        created.append(name)

    print(f"Workspace: {out}")
    print("Created: " + (", ".join(created) if created else "nothing (all files already existed)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
