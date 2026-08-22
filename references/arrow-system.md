# Connector and Vector Arrow System

Read this reference when arrow appearance, routing, or vector-library arrows
matter. The goal is a coherent scientific connection grammar without losing
native editability or confusing a relation with an operation.

## Separate relation, marker, and operator

Treat these as three different objects:

1. **Relation connector** — the semantic edge between named ports. It carries
   route, direction, relation type, and optional label. Keep it as a native
   PowerPoint/Draw.io connector whenever possible.
2. **Arrow marker or short transition motif** — a small SVG from one consistent
   vector family. It may replace an unattractive built-in arrowhead or occupy a
   short straight gap, but it must align with the connector and never create a
   second contradictory direction.
3. **Operation symbol** — a compact named SVG such as funnel/filter, merge,
   split, aggregation, routing, or zoom/detail. It is a node with input and
   output connectors, not an arrow.

An oversized chevron between blocks is rejected when a reader could interpret
it as either the data-flow arrow or the computation itself.

## Preferred and fallback visual families

For visible arrow markers and operation symbols, search Flaticon or Alibaba
Iconfont first when the requested style needs a richer family. Prefer a single
pack that includes the required transition, funnel/filter, merge/split, and
detail symbols. Download and register the actual SVG files; keep the relation
topology as native connectors.

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

If the answer to the fifth question is no, the figure has become a collection
of decorative arrow images instead of an editable scientific diagram.
