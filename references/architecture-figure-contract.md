# Architecture Figure Visual Contract

Use this contract for neural-network architectures, system pipelines, module
diagrams, encoder-decoder figures, multi-branch fusion figures, and similar
paper figures. It overrides presentation-slide conventions. The canvas is the
figure itself, not a slide containing a figure.

## 1. Canvas and information hierarchy

- Fill 85–95% of the canvas with the architecture. Use 24–48 px outer margins
  on a 1600 × 900 reference canvas and scale proportionally.
- Do not add a large deck-style headline, subtitle, eyebrow, slide number,
  footer, badge, or bottom explanatory paragraph unless the user explicitly
  requests presentation framing.
- A figure title is optional. If needed, keep it compact and inside the figure
  hierarchy. Prefer panel labels such as `(a) Overall Architecture` and
  `(b) Proposed Module` over a large banner title.
- The dominant visual hierarchy is: proposed module or main path → stage/group
  headings → module labels → tensor and operator annotations.
- Use whitespace to separate stages. Use a container only when it denotes a
  real semantic group, not as a decorative card.
- Do not place workflow/debug labels such as `STAGE 1`, `DRAFT`, or review
  instructions inside the production canvas. Put them in filenames and review
  notes.
- Shadows, gradients, glossy effects, oversized rounded cards, and decorative
  pills are off by default. Corner radii are modest: 4–10 px.

## 2. Typography

Use one typographic family throughout the figure.

- English default: Times New Roman. Cambria is the fallback when equation
  coverage or platform compatibility requires it.
- Chinese default: SimSun for a serif paper style; use Noto Serif CJK SC when
  SimSun is unavailable. Do not mix serif and sans-serif merely for decoration.
- Mathematical variables, tensor symbols, and subscripts are italic. Module
  names may be bold or bold italic only when the reference uses that convention.
- Sentence case is preferred. Avoid all-caps labels except short established
  abbreviations such as CNN, MLP, Q/K/V, or FFT.

Starting sizes on a 1600 × 900 canvas:

| Role | Size | Weight |
|---|---:|---|
| Optional figure/panel heading | 20–24 px | bold |
| Stage or group heading | 18–21 px | bold |
| Main/proposed module | 17–20 px | bold or bold italic |
| Standard module/operator | 15–18 px | regular or bold |
| Tensor/equation/branch label | 12–14 px | regular/italic |
| Legend or secondary annotation | 11–13 px | regular |

Do not solve crowding by shrinking required text below 9 px. Shorten redundant
copy, enlarge the relevant module, or split overview and detail views instead.
Text should normally occupy no more than 65–75% of a module's width, leaving
visible internal padding. Use the lower end only when a dense source figure or
long notation genuinely requires it. During screenshot review, also inspect the
whole figure at approximately 50% scale: panel headings, routine module names,
and the main contribution must remain readable without zooming into a crop.

## 3. Architecture palette

The reference palette is deliberately light and low-saturation. Select only
3–5 semantic fills for one figure, plus neutral background and connector
colors. Do not use all swatches just because they are available.

| Semantic role | Fill | Typical use |
|---|---|---|
| Standard feature block | `#B4C6E7` | encoder/transformer/base block |
| Secondary branch | `#D3D3FF` | text branch, auxiliary pathway |
| Reconstruction / upsample | `#ADD7AC` | decoder, fusion, upsample path |
| Degradation / downsample | `#E8B593` | degradation branch, downsample path |
| Context / output family | `#FAE4D5` | output head, context region |
| Warm secondary block | `#FCDAB1` | prompts, small auxiliary operators |
| Neutral panel | `#FAF6E7` | group background, module interior |
| Attention / query accent | `#A2B6FA` | query, attention, selected feature |
| Proposed / learnable accent | `#EA717A` | paper contribution, learnable item |
| Soft proposed container | `#F7E7EA` | contribution group background |

Use white or `#FAF6E7` as the main canvas. Normal strokes and main arrows are
`#1F1F1F` or `#30343B`; use 65–85% darker versions of a fill for its boundary.
The coral accent is scarce: normally one proposed module family or one
learnable mechanism, not every important-looking object. Every arrow color must
have a semantic meaning and, if more than two non-black edge types are used, a
compact legend.

## 4. Module scale and spacing

Starting dimensions on a 1600 × 900 canvas:

| Object | Typical size |
|---|---|
| Standard module | 120–190 × 56–96 px |
| Small operator cell | 48–92 × 28–50 px |
| Proposed/key module | 160–240 × 80–120 px |
| Stage/group container | 280–680 × 150–430 px |
| Tensor/token cell | 16–26 px square |

- Internal padding: 8–14 px. Gap between adjacent modules: 20–42 px. Gap
  between stages: 42–80 px. Repeated modules must use identical dimensions.
- Use an 8 px alignment grid. Align the main path to a common horizontal
  baseline; align parallel branches to consistent rows.
- Key modules may be 1.15–1.35× a standard module. They must not become giant
  presentation cards. Helper cells must not visually outweigh the contribution.
- Tensor stacks, cubes, and token strips are compact data encodings, not
  decoration. Show only enough repetition to communicate dimensionality.

### Depth and frame gate

When a supplied reference distinguishes flat controls, framed operators,
layered tensors, and 2.5D computation blocks, preserve that distinction. Do not
flatten the source's repeated neural blocks or apply pseudo-3D to every box.
Extract one extrusion vector and face-color rule per family, and extract frame
styles by semantic role rather than using one global black outline. Read
`shape-depth-and-frame-system.md` and record the tokens in `visual-spec.md`.
Inventory every depth family and its expected instance/plate/face counts before
drawing. In PowerPoint, Cube/Bevel and 3-D Format are quick-mode choices; use
independent editable faces and transparent semantic connector envelopes when
camera-ready fidelity, mirrored tensors, per-face colors, or stable ports matter.

### Density gate

Outer-frame occupancy is not enough. A panel can fill the canvas and still feel
empty when its modules occupy only a narrow band. Use these as diagnostic
starting points, not quotas:

- after excluding the panel heading and intentional connector lanes, the
  content envelope should normally use at least about 55% of the available
  panel height and 65% of its width;
- a detail panel with three modules should not retain an unused band larger
  than the modules themselves unless that band is reserved for real branches,
  tensors, or annotations;
- when a draft feels sparse, first reduce container depth and panel gaps, then
  enlarge module families and scientific glyphs together; do not stretch only
  one box or add decorative filler;
- preserve at least 12–18 px connector and label clearance while increasing
  density. Dense means information-rich, not congested.

Reject a checkpoint when the panel frames are visually dominant, when module
labels become readable only in a crop, or when more than roughly one third of a
detail panel is unassigned whitespace without a semantic reason.

## 5. Connector grammar

Create a connector ledger before placement. Every edge records: source node,
source port, target node, target port, relation type, route/lane, label, and
whether an arrowhead is required.

### Ports

- Left: primary input.
- Right: primary output.
- Top: control, prompt, text, or global conditioning.
- Bottom: auxiliary branch, loss, parameter update, or feedback.
- Do not attach a connector to a title badge or arbitrary point when a semantic
  module port exists.

### Line styles

- Main data flow: solid `#1F1F1F`, 1.5–2.0 px, small filled triangle at the
  destination only.
- Secondary data branch: solid dark gray, 1.2–1.8 px.
- Skip/residual: dashed gray, 1.2–1.6 px, routed on a dedicated outer lane.
- Downsample/degradation: warm orange only when the operation is semantically
  encoded and included in the legend.
- Upsample/reconstruction: green only when semantically encoded and included
  in the legend.
- Control/conditioning: lavender or gray dashed line; use an arrowhead only if
  the relation is directional.

### Routing rules

- Main flow is left-to-right on one baseline. Branches should leave vertically,
  travel in a dedicated lane, then re-enter through the correct port.
- A normal edge has zero or one bend. Skip, feedback, or long control edges may
  use at most two bends. Curves are reserved for unavoidable feedback arcs.
- Maintain at least 12–18 px clearance from text and module boundaries; keep
  parallel lanes 8–12 px apart.
- No line may cross text, pass through a module, terminate ambiguously, or touch
  a non-target box. Avoid line-line crossings; when unavoidable, use a bridge or
  an explicit junction dot whose meaning is stated.
- When four or more edges fan into or out of one region, use an explicit bus,
  spine, or junction rather than overlapping arrowheads.
- Repeated long edges share named lanes. Do not improvise a new route for each
  connector after the boxes have already been placed.
- Create connectors before nodes in PowerPoint so lines sit behind shapes, but
  approve the connector-only skeleton before adding dense internal content.
- Library SVG arrows may define the visible arrowhead or short transition
  motif, but they do not replace the semantic connector ledger. Use a separate
  compact SVG operator (for example a funnel for Top-m pruning) when an action
  occurs between modules. Read `arrow-system.md` for the required split.
- For reference replication, a connector is approved only after its rendered
  arrowhead silhouette, head-to-shaft ratio, cap/join, optical endpoint gap,
  and route curvature match the extracted source family. A built-in
  PowerPoint arrowhead is not automatically acceptable merely because the edge
  points in the correct direction.

## 6. Four-stage incremental production

Complete the semantic brief, `figure-model.json`, and edge ledger as a
**preflight**. This understanding work is mandatory, but it is not counted as
one of the four visible drawing stages. Then follow
`staged-drawing-workflow.md`:

1. **Architecture, base color, modules, and arrows** — establish canvas regions,
   low-saturation semantic fills, module-size families, flat/2.5D/layered form
   classes, frame-style tokens, alignment baselines, ports, and every connector.
   Review incrementally after the canvas/regions,
   module composition, main connector skeleton, and branch/merge/skip/feedback
   routes. Base color belongs here because it changes grouping and visual
   weight; final text and decorative assets do not.
2. **Scientific text and annotations** — add module names, tensor labels,
   equations, stage captions, panel labels, and only explanations that help the
   reader decode the method. Reflow modules before shrinking important text.
3. **Named vector assets or transparent cutouts** — for physical/context
   imagery, reuse a provenance-complete Flaticon/Iconfont asset or search and
   download a matching SVG from Flaticon or Alibaba Iconfont first. Other
   providers and native/basic symbols are documented fallbacks. Image
   generation may provide a transparent-background raster cutout when a bespoke
   context illustration is appropriate, but that PNG is not an editable vector.
4. **Full visual review and coordinated refinement** — render the entire canvas
   and dense crops, then tune spacing, alignment, font sizes, color weight,
   connector clearance, and asset scale without changing approved semantics.

In interactive work, stop at each requested approval gate and record the
preview, findings, fixes, and decision in `production-review.md`. Do not advance
while the current preview has ambiguous arrows, inconsistent module sizes,
incorrect semantics, or an unapproved composition. If Stage 4 exposes a
structural defect, return to Stage 1 instead of disguising it with decoration.
For an autonomous request, the same stages and checks remain separate even if
they are completed in one run.

## 7. Architecture-mode rejection checks

Reject or revise a draft when any of the following is true:

- a large title or explanation consumes space needed by the architecture;
- the figure resembles a business presentation infographic rather than a paper
  figure;
- module sizes vary without semantic reason;
- more than five saturated semantic fills compete for attention;
- arrow colors are decorative, arrowheads overlap, or routes cross labels;
- the reference's arrow morphology, 2.5D family, or frame hierarchy has been
  replaced by backend defaults without a documented reason;
- a helper card is larger than the proposed mechanism;
- the main reading path is not immediately visible at paper scale;
- the output is a flattened screenshot instead of native editable objects.
