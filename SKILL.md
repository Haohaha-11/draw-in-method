---
name: draw-in-method
description: "Understand, design, and replicate camera-ready academic figures from papers, method descriptions, code, or reference images. Produce native editable PowerPoint (`.pptx`) or Draw.io figures, with semantic-first image analysis, named vector-asset retrieval, explicit connector meaning, preview validation, and screenshot-driven refinement."
---

# Draw in Method

Turn a paper, description, or reference image into a figure that is easy to decode at two-column size. Understand the scientific story before drawing. Use a small semantic figure model as the format-neutral source of truth, then author the requested native backend: editable `.pptx` or `.drawio`. PNG/SVG/PDF are review or publication exports, not substitutes for the editable source.

## Operating contract

- Make the story explicit: **input → transformation → contribution → output**.
- Separate understanding from rendering. Do not infer the semantic graph from whatever primitives are easiest to draw.
- For a reference image, identify entities, relations, groups, stage order, visual encodings, and uncertain text before reproducing geometry. Read `references/semantic-first-workflow.md`.
- Use a concise framework view for the global story and a separate module view only when internal mechanics matter.
- Every shape, color, icon, tensor label, and connector must have a named meaning. Delete decorative grids, token cards, or colored blocks that do not encode real data.
- Keep real-object imagery (sensor, device, body part, waveform, application scene) in input/data/context regions only. Represent model computation with editable vector primitives.
- Distinguish prior/standard components from the paper contribution with one restrained accent color and an explicit legend.
- Preserve the paper's terminology, tensor symbols, stage order, and training/inference distinction. Never invent results, dimensions, or module names.
- Use rich vector assets for physical inputs, devices, subjects, experimental apparatus, application context, or outputs; keep model computation as native editable backend primitives and do not add icons decoratively.
- Resolve every physical/context icon by semantic name. Search existing vector assets before composing one from primitives; record queries, candidates, provenance, and any fallback reason in `asset-ledger.md`.
- Apply the reusable quality rules in `references/general-quality-contract.md`; they encode paper-scale readability, compact composition, explicit connector semantics, rendered LaTeX, real-object asset boundaries, and export-driven review.
- For neural-network, system-pipeline, encoder-decoder, fusion, or module architecture figures, enable **architecture figure mode** and read `references/architecture-figure-contract.md`. It overrides presentation-slide habits: no large headline, subtitle, footer explanation, or decorative card framing by default.

## Fast decision tree

1. **Framework overview** — 5–8 major stages, one dominant left-to-right path, only key tensors and one or two branch relations.
2. **Module detail** — zoom into the novelty: operation order, input/output dimensions, Q/K/V or feature-interaction direction, residual/skip paths, and where parameters are learned. Do not expand routine Linear/Norm/Activation layers unless they explain the novelty.
3. **Multi-panel figure** — use `(a) Overall Architecture`, `(b) Proposed Module`, and optionally `(c) Training/Downstream Tasks)` when one canvas would otherwise be unreadable. Panels share the same grid and legend.
4. **Reference replication** — treat the image as a style/layout source, not as the scientific source. Follow `references/reference-replication-protocol.md` and create the required intermediate artifacts before writing XML.

For architecture figures, the deliverable is a paper figure on a slide-sized canvas, not a conventional presentation slide. Use the staged architecture workflow: semantic skeleton → monochrome wireframe and connector routing → typography → palette/assets → native backend and QA. Do not decorate a semantically or geometrically unapproved wireframe.

After choosing a diagram type, choose exactly one primary editable backend:

- **PowerPoint** — default when the user asks for PPT/PPTX, presentation editing, or easy manual rearrangement. Use native PowerPoint text, shapes, groups, and connectors; embed selected SVG icons as vector objects. Read `references/pptx-authoring.md` and follow the available Presentations skill for runtime, export, rendering, and QA.
- **Draw.io** — use when the user asks for Draw.io/XML, diagram-library editing, or source-controlled diagram XML. The `.drawio` is the editable source.
- **Both** — build both from the same `figure-model.json`; do not flatten one backend into an image inside the other.

Ask at most three focused questions only when the input cannot establish the diagram type, output format, or missing scientific semantics. Otherwise infer a safe default: landscape, editable PPTX plus PNG preview, English labels unless the source is Chinese.

## End-to-end workflow

### 1. Intake and semantic brief

Read the paper section, abstract/method, prompt, code, and supplied images. Classify each source as content, structure, style, layout, or asset. Extract:

- raw input and its modality/shape;
- preprocessing or patching that is essential to the story;
- named stages and their data dependencies;
- the novel module(s), their operation sequence, and any tensor reshapes;
- training-only branches, losses, inference path, and final output;
- known/frozen components versus trainable/new components.

Create `brief.md` with goal, audience, output backend, must-communicate items, exclusions, terminology, and open assumptions. Create `figure-model.json` with named nodes, groups, typed edges, reading order, asset needs, and unresolved evidence. Use `references/semantic-first-workflow.md` and `references/self-supervision-and-intake.md` for the model and traceability table. Do not author layout geometry until every required edge has a source, target, and relation meaning.

Before drawing, run `python <skill-dir>/scripts/validate_figure_model.py <workdir>/figure-model.json`. Resolve all reported errors, including unresolved named-asset searches.

### 2. Style contract before drawing

If reference images are provided, read `references/style-extraction.md` and record exact or measured values in `visual-spec.md`: palette, font, type hierarchy, corner radius, stroke widths, dash pattern, margins, spacing rhythm, arrow grammar, icon language, density, and panel composition.

If the chosen diagram is an architecture figure, read `references/architecture-figure-contract.md` and use its compact serif typography, low-saturation architecture palette, module scale, explicit ports, connector ledger, and routing constraints. In this mode, do not add a deck-style title, subtitle, footer, explanatory takeaway, slide number, or status badge unless the user asks for presentation framing. The architecture should occupy 85–95% of the canvas.

If no style reference is available, read `references/topconf-paper-style.md` and apply `references/figure-contract.md`.

For non-architecture diagrams, use this default semantic palette unless the extracted contract overrides it:

| Meaning | Fill | Stroke |
|---|---|---|
| Input/raw signal/context | `#E8F2F5` | `#58727D` |
| Existing or standard component | `#EAF0F6` | `#63758A` |
| Feature/tensor transform | `#EDE9F4` | `#7B6A9A` |
| Training/task/output head | `#F4EEDC` | `#9A7B3F` |
| Paper contribution (accent) | `#F1D7D4` | `#B44948` |
| Output/decision | `#E5F1E3` | `#5A8A55` |
| Main data flow | none | `#263238` |
| Auxiliary/skip/feedback | none | `#6B7280` (dashed) |

Use one font family throughout (Arial/Helvetica; Noto Sans CJK for Chinese text), 1.5–2 px normal strokes, 2–3 px contribution strokes, 10–14 px body labels, 16–24 px panel/stage headings, 8 px alignment grid, and 16–28 px outer margins. Architecture figure mode instead defaults to Times New Roman/Cambria (SimSun or Noto Serif CJK SC for Chinese) and the scale in `references/architecture-figure-contract.md`. Tune these values to the actual canvas and render; never shrink important text below paper-scale legibility.

Relative-scale gate: treat typography and module area as a final design constraint, not an afterthought. Before handoff, inspect a canvas-only screenshot at the intended paper width and verify that panel titles are the largest text, contribution/module titles are visibly larger than annotations, and standard helper cells are not larger than the innovation block. As a practical starting point, use ≥20 px panel titles, ≥15 px key-module labels, ≥12 px tensor annotations on a 1600–2200 px canvas, and reserve at least 80–120 px width or 120–180 px height for a key module. If the figure is dense, enlarge the important module and remove redundant words before shrinking its font. Record any intentional deviations in `visual-spec.md` and the final screenshot review.

### 3. Optional image-2 concept pass

Use the image-generation capability only when it helps explore composition or supplies a real-world input/context asset. Prompt for a clean academic concept with **no scientific text, no equations, and no tiny unlabeled blocks**. Treat the result as a visual reference; keep the paper-derived semantic graph authoritative. Do not embed the generated bitmap as the model pipeline. If a real input asset is used, record its provenance and role in `asset-ledger.md`.

Recommended concept prompt shape: “wide camera-ready scientific figure, left-to-right input–core innovation–output story, muted blue/teal/lavender/ochre palette, one restrained coral highlight for the proposed module, consistent rounded vector cards and arrows, generous whitespace, no words or equations, no decorative grids.” After generation, inspect the bitmap, write the semantic/layout inventory, and redraw the shapes and connectors in XML. If editing a user image, inspect it first and pass its local path as the image-generation reference; never use a guessed or missing path.

### 4. Resolve named assets, then plan the composition

For every physical object, device, subject, experimental apparatus, application context, or output illustration:

1. give the entity a canonical semantic name and Chinese/English aliases;
2. search the local asset registry and native shape libraries;
3. when needed and authorized, search Iconfont, Flaticon, or another provider through its normal visible UI;
4. compare semantic fit, viewBox quality, visual family, editability, and provenance;
5. import, sanitize, recolor, register, and embed the selected SVG;
6. compose a new icon from primitives only when no adequate asset exists, the user requests a custom symbol, or the entity is an abstract paper-specific mechanism.

Read `references/vector-assets.md`. An unexplained primitive-built physical icon is a quality-gate failure when a named asset search was feasible. Model computation, tensors, attention, operators, and paper-specific mechanisms should still use native editable primitives rather than decorative library icons.

For a framework view, choose a wide landscape canvas (roughly 1600–2200 × 850–1200 px), align stages on a single baseline, and leave whitespace around the contribution. For a module view, use a large central container with 3–6 labeled operations and small tensor-shape annotations. Use dashed containers only for meaningful groups (encoder, training-only path, memory bank, optional branch). Put the legend near a corner, never in the main flow.

Define each edge before authoring it: source, source port, target, target port, direction, relation type (data/control/feedback/update/annotation), cardinality, route/lane, label, arrowhead requirement, and forbidden crossing zones. For architecture figures, approve a connector-only skeleton before adding dense text or assets. Prefer orthogonal or short straight routes; use waypoints and `exitX/exitY`/`entryX/entryY` when fan-in/out would stack or cross.

Use one dominant non-brand icon family per panel and record every used or rejected candidate in `asset-ledger.md`. Prefer previously imported local assets, then native library shapes, then provider search. Import user-downloaded Iconfont, Flaticon, Iconify, or local SVGs with `scripts/vector_assets.py`; sanitize and embed them so the final artifact has no render-time CDN dependency.

### 5. Author the native editable backend

#### PowerPoint backend

Read `references/pptx-authoring.md`. Author a one-slide figure (or one slide per requested panel) with native PowerPoint objects. Text must remain text; boxes must remain shapes; semantic edges must remain connectors; repeated modules should be grouped; selected icons should be embedded SVG objects rather than a whole-slide raster. Create connectors before nodes so they stay behind nodes. In architecture figure mode, keep the slide free of presentation chrome and apply the five staged review gates in `references/architecture-figure-contract.md`. Render and inspect the resulting PPTX; do not claim editability if the scientific figure is only a single PNG/SVG covering the slide.

#### Draw.io backend

Read `references/xml-authoring.md` before hand-authoring XML. Use explicit `mxGeometry` positions and stable ids (never reuse reserved ids `0` and `1`). Use rounded rectangles, containers, arrows, and simple editable primitives. Use `scripts/shapesearch.py` for a specific Draw.io library shape, `scripts/vector_assets.py` for a registered local SVG, and `scripts/aiicons.py` only for a required AI brand mark. Use `scripts/autolayout.py` only as a first placement for large graphs; manually restore the paper composition afterward. Run `scripts/edgeports.py` when several edges leave the same side of a node.

Annotate dimensions only where they answer a reader question, using a compact second line such as `X ∈ R^(B×T×D)` or `(B, C, H, W) → (B, T, D)`. For attention, show Q/K/V and arrow direction; for feature interaction, show the actual axes or branches being mixed. Add a legend mapping every used semantic color to a category and mark the contribution explicitly (e.g., `Proposed / trainable`).

### 6. Preflight and visual verification

Use `references/general-quality-contract.md` as the review contract. In particular, verify that the canvas is fitted to the composition, every arrow has an explicit semantic source and target, and formulas are rendered in the exported artifacts rather than shown as source delimiters.

For Draw.io, before any preview, run:

```powershell
python <skill-dir>\scripts\validate_visual_quality.py <figure>.drawio
python <skill-dir>\scripts\validate_drawio.py <figure>.drawio
```

Zero `FAIL` items are required. Review every warning, especially text overflow, arrow-box collision, overlap, spacing variance, palette scatter, orphan labels, and edge-density hotspots. Read `references/xml-preflight.md` when a warning is ambiguous.

For PowerPoint, render every slide, run the available overflow/slide tests, and inspect the canvas at full size. Zero unintended overlap, clipping, broken connector, missing font, or whole-slide-flattening issues are required. Verify that a user can separately select and edit representative text, a module shape, a connector, and an icon.

Run a proportion pass after static preflight: compare title/body/annotation scale, compare contribution versus standard-module area, and confirm that the smallest required label remains readable in the canvas-only screenshot. A figure is not ready if the XML is structurally valid but the key innovation or tensor dimensions disappear at paper scale.

Preferred preview on Windows or when URLs are long:

```powershell
python <skill-dir>\scripts\serve_drawio_preview.py <figure>.drawio --port 8765
```

Open the local preview and capture a canvas-only screenshot (the diagram should fill most of the crop). If browser automation is unavailable, export a preview with draw.io CLI without `-e`; if the CLI is unavailable, deliver XML and a browser-fallback URL from `scripts/encode_drawio_url.py`.

For a camera-ready or user-critical figure, perform at least three screenshot → complete 9-zone defect inventory → fix all P0/P1 → re-render → verify cycles. Log them in `defect-log.md`; use `references/self-supervision-and-intake.md` for the inventory, red-team pass, and self-score. Compare at paper scale, not only at editor zoom.

### 7. Final export and handoff

Export the requested formats. For an editable PNG, use the double extension and repair the known draw.io IEND truncation:

```powershell
drawio -x -f png -e -s 2 -o <figure>.drawio.png <figure>.drawio
python <skill-dir>\scripts\repair_png.py <figure>.drawio.png
```

SVG/PDF exports may also embed the XML. For PPTX, report the native `.pptx`, rendered preview, validation status, self-score, and any objects that are vector but not internally path-editable. For Draw.io, report the `.drawio` source and requested exports. Never claim completion when a required component/edge is missing, text is clipped, semantics are ambiguous, the primary deliverable is flattened, or the latest evidence is partial.

## Input-specific notes

- **Paper/PDF:** use the available PDF/document reader to extract method and notation; cite no fabricated numbers. Separate training, inference, and evaluation paths.
- **Description only:** state assumptions in `brief.md` and keep the first version abstract; ask only for information that changes the semantic graph.
- **Reference screenshot:** first reconstruct its semantic graph and uncertainty ledger, then preserve layout rhythm and typography. Redraw computation as native objects; use raster only for an explicitly requested input/context image.
- **Existing `.drawio`:** patch labels, geometry, styles, or edges in place for local changes; regenerate only for a layout-wide change. Re-run both validators after every edit.

## Bundled resources

- `references/figure-contract.md` — concise ICML/NeurIPS/ICLR visual and semantic contract.
- `references/architecture-figure-contract.md` — compact paper-architecture typography, reference palette, module scale, strict connector grammar, and staged PPTX workflow.
- `references/semantic-first-workflow.md` — required image/paper understanding pass and format-neutral figure model.
- `references/pptx-authoring.md` — native editable PowerPoint backend and PPTX-specific QA.
- `references/topconf-paper-style.md`, `style-extraction.md`, `reference-replication-protocol.md`, `self-supervision-and-intake.md` — paper-figure intake, reference extraction, and evidence loop.
- `references/xml-authoring.md`, `xml-preflight.md`, `primitive-icons.md` — editable XML, layout, and icon recipes.
- `references/vector-assets.md` — import, sanitize, recolor, register, and embed user-downloaded Iconfont, Flaticon, Iconify, local, or generated SVG assets.
- `references/diagram-types.md`, `shapes.md`, `troubleshooting.md` — draw.io shape vocabulary and fallback guidance.
- `references/THIRD_PARTY_NOTICES.md` — license notices for included utility portions.
- `scripts/make_drawio_preview.py`, `serve_drawio_preview.py`, `validate_drawio.py`, `validate_visual_quality.py`, and `validate_replication_artifacts.py` — preview and quality gates.
- `scripts/validate_figure_model.py` — semantic graph, edge, group, and named-asset resolution gate before geometry.
- `scripts/init_figure_workspace.py` — create non-destructive `brief.md`, `visual-spec.md`, `layout-grid.md`, `asset-ledger.md`, and `defect-log.md` scaffolding.
- `scripts/repair_png.py`, `encode_drawio_url.py`, `shapesearch.py`, `aiicons.py`, `autolayout.py`, `edgeports.py`, and `validate.py` — export repair, browser fallback, shape lookup, optional layout, edge-port distribution, and structural lint.
- `scripts/vector_assets.py` and `data/icon-registry.json` — provider-agnostic local SVG import, Iconfont symbol extraction, safety cleaning, palette mapping, search, provenance, validation, and self-contained Draw.io image styles.
- `data/shape-index.json.gz` and `data/lobe-icons.json` — local indexes used by shape and AI-icon lookup scripts.
