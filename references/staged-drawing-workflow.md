# Four-Stage Incremental Drawing Workflow

Use this workflow for architecture figures, method diagrams, reference-image
reconstruction, and any user-critical figure whose layout should be reviewed
incrementally. It defines four **user-visible production stages**. Semantic
understanding remains a required preflight and is not counted as a drawing
stage.

## Preflight — understand before drawing

Create or update `brief.md` and `figure-model.json`. Resolve the main claim,
nodes, groups, reading order, typed edges, contribution, training/inference
distinction, asset needs, and uncertainties. Validate the figure model before
placing geometry.

Preflight may use plain text and JSON. Do not spend time polishing a visual
artifact before the scientific graph is stable enough to draw.

## Stage 1 — architecture, base color, modules, and arrows

The goal is a strong architecture that remains understandable with only
minimal placeholder labels. Establish the canvas, background, semantic regions,
module families, module sizes, alignment, and connector grammar. This stage
includes restrained base fills because color blocks affect grouping and visual
weight, but it excludes final typography, explanatory annotations, icons, and
decorative assets.

Build and review incrementally:

### Checkpoint 1A — canvas, background, and regions

- Choose the canvas/aspect ratio and outer margins.
- Add only meaningful panel or stage containers.
- Apply the neutral background and initial semantic region fills.
- Check that the architecture will occupy roughly 85–95% of the canvas when
  architecture mode is active.
- Review region proportions before inserting internal modules.

### Checkpoint 1B — module composition and size families

- Add the main-path modules using short placeholder names or stable node IDs.
- Establish standard, small-operator, proposed-module, and group-container size
  families.
- Add repeated modules with identical dimensions and spacing.
- Compare the visual weight of proposed versus helper modules.
- Review alignment, gaps, padding, branch capacity, and unused whitespace.

### Checkpoint 1C — main connector skeleton

- Add the primary left-to-right data path.
- Attach connectors to explicit semantic ports.
- Verify arrow direction, arrowhead placement, baseline continuity, and label
  clearance.
- Render a connector-focused preview before adding secondary routes.

### Checkpoint 1D — branches, merges, skip paths, and feedback

- Add control, conditioning, auxiliary, skip, feedback, and update edges one
  relation family at a time.
- Use dedicated lanes, buses, or explicit junctions for dense fan-in/fan-out.
- Check crossings, ambiguous endpoints, bend counts, and forbidden zones after
  each relation family is added.
- Do not proceed while an arrow passes through text, a module, or an unrelated
  region.

### Stage 1 approval gate

Approve the architecture only when:

- module size ratios are coherent;
- the dominant reading path is immediately visible;
- repeated modules match;
- the base color blocks communicate grouping without decoration;
- every connector has an explicit source, target, direction, and meaning;
- all routes have enough room for the text and assets that will be added later.

After approval, treat the architecture as provisionally frozen. Later stages
may make small spacing corrections, but a structural problem must return to
Stage 1 rather than being hidden with typography or decoration.

## Stage 2 — scientific text, annotations, and explanation

Add the minimum text required to make the approved architecture scientifically
precise:

- final module and stage names;
- tensor shapes, Q/K/V, operator labels, or equations where they answer a
  reader question;
- short branch labels and control annotations;
- compact legends for semantic colors or edge types;
- panel labels such as `(a) Overall Architecture` and `(b) Proposed Module`;
- concise explanatory notes only where the relationship is not self-evident.

Do not add a deck-style headline, subtitle, footer takeaway, or long paragraph
unless the user explicitly requests presentation framing. Prefer a short label
close to its target over a separate explanatory card.

Review at this stage:

- terminology and notation against the scientific source;
- text hierarchy and font consistency;
- unexpected wrapping, overflow, and tiny type;
- line-text collisions and labels that obscure arrowheads;
- whether explanations duplicate what the architecture already shows;
- paper-scale readability before any icons are added.

Stage 2 is approved when a reader can explain the method without relying on
decorative assets.

## Stage 3 — named vector assets or generated transparent cutouts

Add visual assets only after structure and text have been approved. Assets
support physical context, experimental apparatus, input/output examples, and
domain recognition; they do not define the model's scientific graph.

### Asset decision order

1. Search the local asset registry and native backend libraries by canonical
   semantic name and aliases.
2. Search or import user-authorized SVG assets from Iconfont, Flaticon,
   Iconify, or another provider.
3. Use image generation for a bespoke transparent-background bitmap cutout,
   scene fragment, or illustrative context asset when no suitable vector
   exists or a custom appearance is required.
4. Construct an asset from primitives only for an abstract paper-specific
   mechanism, an explicit user request, or a documented retrieval failure.

### Image-generation boundary

Image generation produces raster imagery, including transparent-background
PNG cutouts. It does **not** by itself produce a genuine editable SVG/vector
asset. Never label an ImageGen PNG as vector. If true vector editability is
required, retrieve an SVG or use a separately approved vectorization workflow
and validate the traced result.

For generated assets:

- request a transparent background and preserve alpha;
- request one isolated subject with a tight crop and no baked scientific text;
- specify viewpoint, orientation, palette, and empty-side composition so it
  fits the reserved slot;
- move the selected output into the project workspace instead of leaving it in
  a temporary or tool-owned location;
- record the prompt, local file, semantic role, and raster status in
  `asset-ledger.md`.

For retrieved vectors:

- inspect semantic fit, viewBox quality, visual family, license/provenance, and
  editability;
- sanitize scripts, external references, and unsafe content;
- normalize color only when it preserves the asset's meaning;
- embed the local SVG so the final figure has no render-time CDN dependency.

At the end of Stage 3, run:

```powershell
python <skill-dir>/scripts/validate_figure_model.py <workdir>/figure-model.json --require-assets-resolved
```

Do not approve Stage 3 while a named search lacks either a selected local asset
or a concrete fallback reason.

Review asset placement for scale, crop, orientation, family consistency,
contrast, and clearance from text and arrows. Assets should fit the reserved
geometry; do not casually resize the approved architecture around a late asset.

## Stage 4 — full visual review and coordinated refinement

Render the complete native artifact and inspect both the full canvas and dense
regions. This is a coordination pass, not a license to conceal structural
errors with cosmetic nudges.

Review:

- global balance, optical centering, and whitespace distribution;
- module size consistency and contribution/helper hierarchy;
- all arrow endpoints, directions, crossings, bends, lanes, and arrowheads;
- text hierarchy, font substitution, wrapping, clipping, and paper-scale size;
- base colors, accent scarcity, legend consistency, and contrast;
- asset crop, alpha, orientation, visual family, and semantic placement;
- formulas, tensor notation, panel labels, and scientific terminology;
- native editability of representative text, module, connector, group, image,
  and SVG objects;
- output-specific overflow and export rendering.

Make coordinated micro-adjustments to spacing, alignment, module dimensions,
font sizes, label positions, and asset scale. Re-render after each correction
set. If the review finds an incorrect relation, missing stage, or fundamentally
wrong module hierarchy, return to Stage 1; do not keep nudging Stage 4 objects.

For camera-ready, reference-replication, or user-critical figures, complete the
required screenshot-driven defect cycles and red-team audit before handoff.

## Approval artifacts

| Gate | Required evidence |
|---|---|
| Preflight | validated `figure-model.json`, assumptions, unresolved evidence |
| Stage 1 | architecture preview, module-size review, connector ledger and route review |
| Stage 2 | labeled preview, terminology/notation check, text-overflow review |
| Stage 3 | asset ledger, selected SVG/PNG files, strict asset-gate result, placement preview |
| Stage 4 | final full-canvas render, dense-region review, validation results, editability check |

Use `production-review.md` to record the current gate, screenshot, findings,
fixes, and user decision. Do not erase earlier review history after a gate has
been reviewed.

## Interactive versus autonomous execution

When the user asks to review step by step, stop after each requested gate and
wait for approval before advancing. Within Stage 1, also stop at the requested
sub-checkpoints when module size or arrow routing is the main concern.

When the user asks for a complete result in one run, the same four stages still
apply internally. Preserve intermediate artifacts and conduct each review gate,
but do not manufacture unnecessary approval pauses.
