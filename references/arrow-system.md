# Connector and Vector Arrow System

Read this reference when arrow appearance, routing, or vector-library arrows
matter. The goal is a coherent scientific connection grammar without losing
native editability or confusing a relation with an operation.

## Separate relation, marker, and operator

Treat these as three different objects:

1. **Relation connector** — the semantic edge between named ports. It carries
   route, direction, relation type, and optional label. Keep it as a native
   PowerPoint/Draw.io connector whenever possible.
2. **Arrow marker or short transition motif** — an optional small SVG from one
   consistent vector family. The default is a continuous native connector with
   a restrained arrowhead. Use an SVG marker only when it materially improves
   a supplied visual reference; never repeat circular/boxed arrow pictures in
   every gap or visually break one continuous flow into disconnected badges.
3. **Operation symbol** — a compact named SVG such as funnel/filter, merge,
   split, aggregation, routing, or zoom/detail. It is a node with input and
   output connectors, not an arrow.

An oversized chevron between blocks is rejected when a reader could interpret
it as either the data-flow arrow or the computation itself.

## Why a PowerPoint arrow often does not match the reference

Do not treat `endArrowType` as a complete arrow style. A reference exported
from Illustrator, Visio, TikZ, SVG, or a paper authoring tool may use a custom
marker whose silhouette and proportions do not exist among PowerPoint's
defaults. PowerPoint and independent renderers can also scale the built-in
arrowhead differently from the shaft.

The visible mismatch usually comes from one or more of these variables:

- arrowhead silhouette: narrow triangle, broad triangle, stealth, open V, or
  custom shape;
- head length and width relative to the shaft;
- shaft width, cap, join, and whether the shaft visually enters the head;
- gap between the visible head tip and the target border;
- route geometry and bend radius, especially for a long curved callout;
- dash length/space and phase;
- stroke color and opacity;
- scaling introduced by the PPTX renderer or export resolution.

When a supplied reference is being replicated, record these fields for every
arrow family in `visual-spec.md`. Inspect representative arrows at 200–400%
zoom and measure in source pixels before converting to points. A visually
similar route with the wrong head-to-shaft ratio is not a style match.

## Reference-matched implementation ladder

Choose the lowest tier that survives an independent PowerPoint render:

1. **Native connector with built-in marker.** Use only when its silhouette,
   head proportion, endpoint gap, and rendered result match the reference.
2. **Hybrid editable arrow.** Draw the shaft as a native connector and add a
   separate native/freeform or named SVG arrowhead. Align and group them while
   retaining the semantic edge in the connector ledger. This is preferred when
   the default PowerPoint head is too large, too blunt, or shifts during export.
3. **Custom vector path.** Use an editable freeform or embedded SVG for a
   distinctive curved, looped, bidirectional, or illustrated arrow. Record its
   semantic source and target explicitly because the path may not remain
   auto-attached when a module moves.

Do not select an arrow from a vector library merely because it is attractive.
Search by the required morphology and relation, compare silhouettes side by
side, and lock one arrow family for the panel. The visible marker may come from
Flaticon/Iconfont or a custom SVG, but the data/control topology must remain
recoverable from named ports and the connector ledger.

## Preferred and fallback visual families

For visible arrow markers and operation symbols, first test whether native
geometry communicates the science more accurately. Search Flaticon or Alibaba
Iconfont only when the requested reference uses a richer coherent marker
family. Prefer a single pack, download and register the actual SVG files, and
keep the relation topology as native connectors. Do not replace a scientific
operation such as Top-m token retention with a generic metaphor when editable
scores, tokens, or selection geometry are clearer.

The skill bundles a small Lucide-derived **fallback** set in
`assets/vector-arrows/`:

- `arrow-right.svg` — short main-path transition;
- `arrow-down-right.svg` — controlled diagonal/detail transition when an
  orthogonal route is not available;
- `funnel.svg` — pruning/filtering operator;
- `zoom-in.svg` — detail-view/expansion marker.

Lucide is an open-source SVG library under the ISC license; preserve the notice
in `assets/vector-arrows/LICENSE.txt`. Recolor a copy for a project rather than
changing the canonical bundled asset. Use this family only when the preferred
Flaticon/Iconfont search has no suitable coherent result, the provider download
is blocked and disclosed, or the user explicitly selects the minimalist style.
Record every selected or rejected provider asset and license state in
`asset-ledger.md`.

## Relation styles

| Relation | Connector | SVG marker/operator | Color |
|---|---|---|---|
| Primary data flow | straight, solid, 1.6–2.0 px | rounded `arrow-right` marker | `#1F1F1F` |
| Secondary data | solid, 1.2–1.6 px | same family, smaller | `#4B5563` |
| Conditioning/control | dashed, orthogonal, 1.2–1.5 px | small open marker only if directional | lavender/gray |
| Skip/feedback | dashed outer lane, at most two bends | small marker at re-entry | gray |
| Detail expansion | thin dashed connector without data-flow arrowhead | `zoom-in` at source or label | gray |
| Pruning/filtering | connector into and out of a node | compact `funnel` operator | warm orange |

Use colored arrows only when color encodes a documented relation family. Main
data flow stays dark. Avoid gradients, shadows, cartoon arrows, multiple icon
families, and filled arrow bodies that are thicker than module strokes.

The table above is a fallback style, not permission to overwrite a supplied
reference. For exact replication, the measured reference profile wins. Store a
token for each family, for example `main-flow`, `text-conditioning`,
`degradation-control`, and `long-callout`, with its complete morphology rather
than only color and width.

## Placement gate

- Main-path module centers share one horizontal baseline.
- Straight transitions occupy the gap between boxes and remain visually
  centered on the ports.
- The SVG marker must not overlap a module outline or connector label.
- Operation symbols are normally 28–46 px on a 1600 × 900 canvas and smaller
  than standard modules.
- Detail markers are visually subordinate to the main path.
- If a connector route changes after review, move or regenerate its SVG marker;
  do not leave detached arrowheads behind.

## Review questions

1. Can every arrow be named as data, conditioning, skip, feedback, update, or
   annotation?
2. Is every visible arrow direction consistent with the edge ledger?
3. Can a reader distinguish the Top-m/filter operation from the connectors on
   both sides?
4. Are all main-path arrows on one baseline and equally weighted?
5. Would hiding the SVG markers still leave a valid connector topology?
6. Does the independently rendered head silhouette and head-to-shaft ratio
   match the source crop, rather than only the authoring preview?
7. Do arrow tips stop at a consistent optical gap from target borders?

If the answer to the fifth question is no, the figure has become a collection
of decorative arrow images instead of an editable scientific diagram.
