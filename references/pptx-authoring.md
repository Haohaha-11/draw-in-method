# Native Editable PowerPoint Backend

Read this reference when the requested primary output is `.pptx`. Follow the
available Presentations skill for the supported runtime, Artifact Tool API,
export, slide rendering, overflow checks, and delivery rules. This reference
adds academic-figure-specific requirements.

## Source of truth

Use `figure-model.json` as the semantic source of truth and the native PPTX as
the editable visual source. Do not convert a finished Draw.io canvas into one
full-slide PNG or SVG and call that an editable PowerPoint.

When both formats are requested, author both from the same model. A converted
Draw.io SVG may be useful as a visual comparison layer during development, but
it must not replace native PowerPoint text, modules, or connectors.

## Object mapping

| Figure concept | PowerPoint representation |
|---|---|
| panel/container | native rectangle or rounded rectangle |
| module/operator | native shape with editable text |
| label/equation | native text box; use supported equation strategy when needed |
| data/control relation | native connector with explicit arrowhead and route |
| repeated stage | grouped native objects with consistent size and spacing |
| physical/context icon | embedded local SVG object with provenance |
| photograph/heatmap | raster image only when it is genuinely data or context |
| legend | native text and swatches |

Create connectors before entity nodes so edges remain behind boxes. Keep text
separate from imported icons unless the asset itself semantically includes the
text. Group logical modules, but avoid one giant group that makes ordinary
editing cumbersome.

## What “editable” means

The following must be separately selectable and editable in PowerPoint:

- all scientific labels and captions;
- main boxes, panels, operators, and token/tensor primitives;
- all semantic connectors and their arrowheads;
- repeated module groups;
- each imported icon as an independent vector object.

An embedded SVG remains resolution-independent and can be moved, resized, and
usually recolored, but its internal paths may not be individually editable in
every PowerPoint version. Disclose this distinction. If internal path editing
is required, prefer native shapes or a user-approved converted shape group.

## Slide and scale

Use a custom landscape slide size matching the figure aspect ratio unless the
user requests standard 16:9. Treat the slide as a figure canvas rather than a
normal presentation slide: paper-scale readability and faithful scientific
structure override ordinary deck title/body conventions.

For architecture figures, follow `architecture-figure-contract.md`. The
architecture occupies 85–95% of the canvas. Do not add a large slide title,
subtitle, eyebrow, slide number, footer, takeaway, or bottom explanatory text
unless the user explicitly requests presentation framing. Optional figure and
panel headings belong inside the compact figure hierarchy.

Preserve the typography hierarchy from `visual-spec.md`. Avoid shrinking
critical labels to fit; enlarge the important module, abbreviate redundant
copy, or split into multiple panels/slides.

After semantic preflight, build architecture slides through the four production
stages in `staged-drawing-workflow.md`. Stage 1 creates the native architecture
with restrained base fills, module-size families, alignment baselines, ports,
and all connector routes; use only the placeholder labels required to review
geometry. Render and review its canvas/regions, module composition, main flow,
and branch/merge/skip/feedback routes incrementally. Stage 2 adds scientific
text and annotations. Stage 3 inserts approved SVG assets or explicitly raster
transparent cutouts. Stage 4 renders the full slide and dense crops for
coordinated layout, font-size, color-weight, and connector-clearance refinement.
Record review gates in `production-review.md` and resolve structural problems in
Stage 1 rather than masking them during decoration.

## Asset handling

Resolve icons through `references/vector-assets.md`. Embed sanitized local SVG
files; do not leave CDN URLs or browser-session dependencies. Record provider,
asset name, author/license state when available, local file, node id, and color
mode in `asset-ledger.md` and presentation source notes.

## QA gate

Before delivery:

1. render every figure slide to PNG at high resolution;
2. inspect the full slide and representative dense regions;
3. run the supported slide overflow test;
4. fix unintended overlap, clipping, wrapping, font substitution, and broken
   connector routes;
5. verify representative text, box, connector, group, and icon objects are
   independently selectable;
6. confirm the slide does not contain a whole-canvas cover image that hides or
   replaces native objects;
7. compare the rendered slide with the reference or approved visual spec for
   at least three screenshot-driven refinement cycles when fidelity matters.

Deliver the `.pptx` plus the latest rendered PNG preview. Add SVG/PDF only when
requested or useful for publication.
