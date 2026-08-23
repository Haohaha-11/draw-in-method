# Contextual Asset Strategy

Use this reference whenever a figure needs icons, reference-derived artwork,
generated transparent cutouts, brand marks, or other non-primitive visual
assets. Its purpose is to prevent attractive individual assets from becoming
an incoherent clip-art collage or weakening the scientific explanation.

## 1. Icon necessity gate

Before searching or generating an asset, answer all five questions:

1. What named entity does the asset depict?
2. Is the entity physical/contextual, a brand, or an established domain symbol?
3. Does the asset improve recognition beyond native text and scientific
   geometry at manuscript scale?
4. Is the asset's meaning literal rather than a vague metaphor?
5. Can it belong to the panel's declared visual family?

Reject the asset if any answer is unclear. Encoder, decoder, attention, fusion,
adaptation, pruning, ranking, and routing are abstract computation and are
icon-free by default. A brain does not explain adaptation, a computer does not
explain progressive decoding, and a funnel does not explain Top-m retention as
accurately as tokens, scores, and an explicit selection operation.

Use assets mainly for photographs, modalities, people, devices, sensors,
experimental apparatus, application scenes, outputs, and required brand marks.
If removing an icon preserves the meaning and improves clarity, remove it.

### Reference-symbol preservation gate

For exact or close reference replication, first classify each vector-like
symbol visible in the source:

1. **Official identity mark** — brand, organization, software, or model logo.
   Retrieve the official or provenance-complete SVG; do not approximate it with
   circles, text, or generic PowerPoint shapes.
2. **Conventional domain/status glyph** — person, flame/learnable marker,
   sensor, chart, database, modality, or other widely recognized literal
   symbol. Search for the exact or same-family SVG before composing it from
   primitives.
3. **Paper-specific operator glyph** — a distinctive fusion, exchange,
   rotation, attention, or interaction symbol. Prefer the paper/source asset,
   a carefully traced custom vector, or a coordinated generated symbol. Do not
   substitute a generic library icon unless its semantics and silhouette both
   match.
4. **Decorative mark** — omit it when no named meaning can be established.

The rule that computation is normally icon-free does not authorize replacing a
visible established symbol with a crude approximation. It prevents decorative
metaphors; it does not erase the reference's actual visual vocabulary.

## 2. One-family contract

Before choosing candidates, record one visual-family contract per panel:

| field | required decision |
|---|---|
| family id | stable short name |
| source | provider/pack/author, reference image, or generated asset sheet |
| drawing language | outline, flat fill, duotone, lineal color, or realistic cutout |
| stroke | weight, cap/join, dark/light treatment |
| depth | flat, subtle isometric, or photographic; do not mix casually |
| palette | 3–5 shared colors plus neutral |
| perspective | front, side, isometric, or mixed only with justification |
| detail level | recognizable at intended paper scale |
| background | transparent unless the data itself is a rectangular image |
| typical size | one consistent paper-scale range |

Select assets as a set. A candidate that fits one entity but breaks the family
is rejected. Brand marks may remain exact, but they are visually subordinate
and do not redefine the panel's family.

## 3. Asset routes

Choose the route that preserves both meaning and coherence:

### A. Native scientific geometry

Default for model computation, tensors, operators, attention maps, token
selection, feature fusion, and paper-specific mechanisms. Native PowerPoint or
Draw.io objects preserve editability and explain the operation directly.

### B. Coherent external SVG pack

Use for justified physical/context entities when one Flaticon or Alibaba
Iconfont pack covers the needed subjects. Compare a set of candidates, not one
slot at a time. Record pack, author, license, URLs, and local SVG files.

For reference replication, provider priority is: identifiable original/official
asset → exact silhouette from a provenance-complete source → same-family
Flaticon/Iconfont candidate → custom vector reconstruction. Do not prefer a
provider over a visibly better source match. Compare semantic match, silhouette
match, stroke/fill language, perspective, and paper-scale legibility.

### C. Coordinated generated asset sheet

When no external pack fits, generate multiple isolated subjects together in a
single prompt so they share palette, stroke, perspective, and detail. Request
transparent backgrounds and no text. Crop each subject into an independent
asset. These outputs are raster unless a separately validated vectorization
workflow converts them; never call the PNGs editable vectors.

### D. Reference/generated draft decomposition

An AutoFigure-Edit-style route may use a supplied or generated raster draft as
an appearance source: identify assets, assign stable ids, extract transparent
RGBA cutouts, reserve matching placeholders, and inject them into an editable
SVG/PPT scaffold. The semantic graph and connector ledger remain authoritative.
Do not infer scientific topology from segmentation boxes or visual proximity.
Embedded cutouts remain raster even when placed inside an SVG.

For exact reference replication, reuse or crop supplied photographs and
context artwork when permitted, but redraw computation, text, boxes, and
connectors as native objects. Do not introduce unrelated external icons that
were absent from the reference.

## 4. Appearance-versus-structure boundary

Maintain two layers:

- **structure layer:** groups, modules, ports, connectors, labels, tensors,
  operators, and semantic colors;
- **appearance layer:** photos, real-object cutouts, brand marks, and approved
  contextual illustrations.

The structure layer must remain understandable when the appearance layer is
hidden. Appearance assets may reinforce domain recognition but cannot carry an
otherwise missing relation or operation.

## 5. Review gate

Reject Stage 3 when:

- icons come from visibly unrelated families;
- an abstract module uses a decorative metaphor instead of showing its
  operation;
- arrows are floating images rather than continuous semantic connectors;
- raster assets are described as vector paths;
- one standard/context asset visually outweighs the proposed method;
- an asset lacks a named role, family id, source, or license/fallback record;
- the figure becomes clearer after hiding the assets.

Record the family contract, necessity decision, selected route, and remaining
editability limits in `asset-ledger.md`.
