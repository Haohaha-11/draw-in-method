# Shape Depth and Frame System

Read this reference when a supplied figure uses flat boxes, pseudo-3D network
blocks, layered tensors, image frames, dashed group containers, or role-specific
border colors. The goal is to reproduce the source's shape language instead of
reducing every object to the same rounded PowerPoint rectangle.

## 1. Classify before drawing

Assign every visible object one form class in `visual-spec.md`:

| class | typical meaning | construction |
|---|---|---|
| flat label/control | decoder, prompt, small operator, annotation | 2D rectangle or text; no artificial depth |
| framed module | fusion, projection, output head | one native shape with measured fill, stroke, and corner treatment |
| 2.5D computation block | deep/repeated encoder or transformer block | grouped front, top, and side faces |
| layered tensor/feature stack | multiscale features, maps, channels | several offset plates with a shared depth vector |
| data/image frame | input or output image | image plus independent border/caption objects |
| semantic container | modality group, stage, training-only region | light or dashed boundary only when the grouping is real |

Do not decide the form from the module name alone. Match how the reference
encodes that semantic family. In many paper figures a heavy neural block is
2.5D, while control, prompt, projection, and output modules remain flat.

### Family-coverage audit

Do not stop after finding one obvious cuboid. Before authoring geometry, create
a depth-family inventory in `visual-spec.md`:

| required field | meaning |
|---|---|
| family id | stable semantic name, such as `saformer`, `multiscale-feature-stack`, or `tim-side-tensor` |
| form class | flat, framed, 2.5D block, layered tensor, data frame, or container |
| reference count | number of visible instances in the supplied source |
| planned count | number required in the editable figure |
| plate/face grammar | front/top/side faces, number of plates, and drawing order |
| depth token | extrusion vector, slant, and face-color rule |
| mirror rule | none, left/right mirror, or stage-specific perspective |
| connector target | named front-face port or semantic envelope |
| status | matched, uncertain, intentionally simplified, or missing |

The counts are a coverage check, not a mandate to copy meaningless repetition.
When the source clearly uses six major cuboids, three multiscale feature stacks,
and twelve compact branch tensors, a correct six-cuboid implementation does not
make the depth pass complete if the other families were flattened. Document any
intentional simplification and preserve its scientific meaning.

## 2. Extract the depth grammar

For each 2.5D family, measure and record:

- visible faces: front only, front+top, front+side, or front+top+side;
- extrusion vector `(dx, dy)` in source pixels and as a fraction of the front
  face width/height;
- perspective direction and slant angle;
- front, top, and side fill colors;
- per-face stroke color and weight;
- whether repeated back plates are present and their spacing;
- text plane and connector ports.

Construct pseudo-3D blocks from separate editable faces rather than applying
PowerPoint's generic 3D rotation, bevel, shadow, or gradient. A normal grouped
block contains a front quadrilateral/rectangle, a lighter top polygon, and a
darker side polygon. Use one extrusion vector and one face-color rule for the
entire family. Put text on the front face and connect semantic edges to named
front-face ports, not to a decorative side face.

Layered tensor stacks use the same depth vector but remain separate plates.
Show only enough plates to communicate channels/scales. The rear plates must
not create false modules or ambiguous connection targets.

Keep a depth hierarchy when several families coexist. A major computation block
normally has the largest extrusion, a multiscale feature plate uses a smaller
one, and compact branch tensors use the smallest visible depth. Measure the
reference first. When the source is unclear, use these only as relative starting
relationships:

- major block extrusion: about 8–12% of front-face width and 12–20% of height;
- feature-plate extrusion: about one-half to two-thirds of the major-block
  vector;
- compact branch-tensor extrusion: enough to reveal a top/side face at the
  independent render scale, but visually subordinate to the feature stack;
- repeated plate rhythm: one shared offset vector per family;
- left/right counterparts: mirror slant and visible side direction, not merely
  the plate positions.

## 3. Extract the frame grammar

Do not choose one universal border. Build a frame-style table by semantic role:

| required field | examples |
|---|---|
| role | data image, standard module, key module, control, output, semantic container |
| fill | exact sampled hex and opacity |
| stroke | exact sampled hex; often a darker relative of the fill rather than black |
| weight | points in PPTX and equivalent source pixels |
| pattern | solid, dashed, dotted; include dash and gap length |
| corner | sharp, subtle radius, rounded, pill |
| inset/padding | text/image gap to the frame |
| hierarchy | subordinate, normal, emphasized |

At 96 dpi, 1 pt is approximately 1.33 px. Measure the source at its native
resolution and convert deliberately; do not paste a 1.5–2.0 pt presentation
default into a dense paper figure. As starting relationships when the source is
unclear:

- image and routine module borders: restrained and similar in weight;
- semantic group containers: lighter and often thinner/dashed so they do not
  dominate their contents;
- key or proposed modules: modestly stronger or semantically colored, not a
  heavy black outline;
- small internal cells: equal to or thinner than their parent module;
- border color: a darkened fill hue or neutral gray chosen from the reference.

Corner treatment is also semantic. A sharp 2.5D network block, a lightly
rounded fusion cell, a dashed rounded modality container, and a square image
frame should not all be converted to the same rounded rectangle.

## 4. Backend implementation

### PowerPoint

Use this authoring ladder. Choose the lowest-complexity option that matches the
reference and survives independent rendering:

1. **Cube/Bevel AutoShape quick mode.** PowerPoint includes native Cube and
   Bevel shapes. Use them for rough drafts or simple standard blocks only when
   one fill, one outline, preset depth control, and generic connection sites are
   sufficient. Do not claim per-face editability.
2. **PowerPoint 3-D Format / 3-D Rotation.** Use only when the reference itself
   has a rendered material/lighted look or the user explicitly wants a true
   PowerPoint 3-D effect. Bevel, depth, lighting, and rotation are one rendered
   object; they do not create independently selectable semantic faces, and
   cross-renderer results may vary.
3. **Inserted 3D model.** Reserve real 3D models for physical/context objects
   that genuinely need 360-degree views. They are not the default representation
   for encoders, transformers, tensors, or fusion modules.
4. **Editable face-built prism.** This is the camera-ready default when exact
   face colors, measured extrusion, mirrored perspective, stable ports, or
   reference fidelity matter. Build independent native front, top, and side
   faces and group the logical object at handoff.

For editable face-built prisms:

- draw rear instances before front instances;
- within one plate, create decorative top/side faces before the front face;
- keep text on a separate front-plane text object when grouping or z-order
  would otherwise make it hard to edit;
- give every face a stable name such as
  `family-instance-plate-02-front-face`, `...-top-face`, and `...-side-face`;
- use explicit RGB colors and point weights instead of theme-dependent `auto`
  values;
- use a lighter top and darker side only when the reference supports that
  shading rule; do not add gradients or lighting merely to make a block look
  more dimensional;
- create connectors behind blocks and bind them to a named front-face port or
  a transparent semantic connector envelope that covers the whole logical
  stack;
- use the envelope for layered tensors when different routes enter from the
  top, bottom, left, and right. The envelope is a topology target, not visible
  decoration;
- keep the connector ledger linked to the logical family even when the visible
  faces are individually selectable;
- render through PowerPoint after generation. Face order, thin strokes, and
  connector endpoints can differ from a library preview.

### Reusable PowerPoint recipes

#### Major computation block

- front rectangle or quadrilateral carries the label;
- lighter top polygon and darker side polygon share one extrusion vector;
- semantic input/output ports lie on the full visible outline or on explicit
  invisible port shapes, never on a decorative side face;
- repeated blocks share dimensions, face colors, stroke weights, and object
  naming.

#### Layered multiscale feature stack

- every visible plate is its own thin prism, not one flat polygon copied with
  offsets;
- each plate has front/top/side faces when those faces survive at paper scale;
- use a smaller depth vector than the major computation block;
- vary front fills only when color encodes scale/channel order in the source;
- use one transparent group-sized connector envelope for the stack.

#### Mirrored branch tensor

- use a slanted front parallelogram plus explicit top and visible side faces;
- the counterpart on the opposite side mirrors the slant, extrusion direction,
  and visible side face;
- keep both families identical in geometry unless color carries a different
  semantic role, such as text-image versus image-image interaction;
- reject a result that looks like corrugated flat paper rather than plates with
  measurable thickness.

### Draw.io

- Prefer grouped polygons/rectangles with explicit geometry and colors.
- Keep the front-face node or explicit port as the semantic connector target.
- Do not rely on a style preset whose extrusion or stroke changes with theme.

## 5. Review gate

Reject the stage when:

- a source 2.5D family has been flattened without a documented reason;
- the implemented family or plate counts do not match the depth-family
  inventory and the mismatch is not explicitly justified;
- different repeated blocks use different extrusion vectors or face shading;
- left/right tensor counterparts reverse only position but not their slant and
  visible depth direction;
- a connector terminates on a decorative top/side face;
- a layered stack uses one decorative plate as the topology target when routes
  need to address the whole semantic stack;
- all borders are black or the same weight despite clear source hierarchy;
- group frames visually dominate modules;
- corners are globally rounded even though the source distinguishes sharp,
  subtle, and rounded families;
- an independently rendered thin border disappears or becomes heavier than the
  source;
- a frame or depth effect has no semantic/style evidence and was added merely
  to make the diagram look more elaborate.

For final review, compare representative crops side by side: one 2.5D block,
one layered tensor, one mirrored branch-tensor pair, one flat control block,
one data frame, and one semantic container. Record the measured source token
and the rendered PPTX/Draw.io token in `visual-spec.md`. Inspect the final object
inventory as well as the screenshot: for a family with `instances × plates ×
faces`, verify the expected editable face count and the expected number of
connector envelopes. A visually correct raster or one correctly modeled family
does not satisfy this gate.
