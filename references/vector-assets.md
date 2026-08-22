# Local Vector Asset Workflow

Read this reference when a figure needs a physical object, device, sensor,
medical/industrial scene, brand mark, or another icon richer than editable
Draw.io primitives. The goal is a self-contained `.drawio` source with a
coherent icon family, not unrestricted decoration.

## Name-first source routing

Do not begin by browsing visually unrelated icon grids. First extract a
canonical semantic name from `figure-model.json`, add Chinese/English aliases
and domain synonyms, then search by those names. Record the query terms,
plausible candidates, selection reason, and fallback reason in
`asset-ledger.md`. This makes asset choice reproducible and prevents drawing a
generic substitute before understanding what the entity represents.

Choose the least complex source that preserves the intended meaning:

1. Use native editable backend primitives for model computation, tensors, operators,
   attention, feature interaction, and paper-specific mechanisms.
2. Search the local registry with `scripts/vector_assets.py search` using the
   canonical name and aliases.
3. Search `scripts/shapesearch.py` for native Draw.io engineering, cloud,
   network, UML, and flowchart shapes.
4. Use `scripts/aiicons.py` for an AI/LLM brand mark.
5. If local search fails and the user has authorized provider search, use the
   provider's normal visible UI to search Iconfont, Flaticon, Iconify, or the
   user's preferred library. Prefer semantically exact SVGs from a consistent
   family over the first superficially similar result.
6. If no suitable asset exists, ask the user to download/copy an SVG or author
   a small constrained SVG/primitive icon and record why retrieval failed.

Use rich vector assets mainly for inputs, physical devices, subjects,
experimental apparatus, application contexts, and outputs. Do not put an icon
in every model block. Within one panel, keep one dominant non-brand icon family
unless a semantic exception is necessary.

Arrow and connector assets are a special case. Read `arrow-system.md` before
using them. Search a coherent family by semantic name (`arrow right`,
`conditioning`, `feedback`, `funnel`, `filter`, `zoom detail`) rather than
browsing decorative arrows. Ordinary data-flow relations must still be backed
by editable connectors. Library SVGs are appropriate for consistent rounded
arrowheads, short transition motifs, pruning/routing operators, and detail-view
markers; they are not a license to replace the whole topology with floating
arrow pictures.

## Importing user-downloaded assets

The importer accepts:

- individual `.svg` files;
- directories containing SVGs;
- ZIP exports containing SVGs;
- Iconfont-style JavaScript bundles containing `<symbol>` entries.

It does not search or scrape Iconfont or Flaticon. Acquire assets through the
user's normal browser/account flow, then import the downloaded files. If an
in-app browser with the user's signed-in session is available and the user asks
for provider search, use the provider's normal visible UI to search and
download/copy the selected SVG; do not bulk-acquire results or call private
endpoints. Otherwise ask the user to supply the downloaded SVG or project pack.

Iconfont example:

```powershell
python <skill-dir>\scripts\vector_assets.py import <downloaded.svg> `
  --provider iconfont `
  --collection personal-academic `
  --aliases "wearable sensor,可穿戴传感器" `
  --source-url "<asset-page-url>" `
  --color-mode academic
```

Flaticon example:

```powershell
python <skill-dir>\scripts\vector_assets.py import <downloaded.svg> `
  --provider flaticon `
  --collection personal-academic `
  --author "<author-name>" `
  --source-url "<asset-page-url>" `
  --license "Free with attribution" `
  --attribution "Designed by <author> from Flaticon" `
  --color-mode preserve
```

For a Flaticon Premium asset, record the license state supplied at download
time; do not invent an attribution requirement. Prefer an editable-stroke SVG
over a flattened version when both are available and the richer editability
survives Draw.io export.

## Color modes

- `preserve` keeps multicolor illustrations and gradients. Use it when color
  layers communicate a physical object or application scene.
- `academic` maps explicit fills and strokes to the skill's muted semantic
  palette. Use it when a downloaded illustration is too saturated.
- `mono --color <hex>` produces a single-color symbol when the asset is small
  or secondary.

Always inspect the rendered export. Automatic recoloring cannot infer every
layer's semantic role, especially for gradients, masks, or complex style
blocks.

## Search and Draw.io embedding

```powershell
python <skill-dir>\scripts\vector_assets.py search "传感器" --json
python <skill-dir>\scripts\vector_assets.py drawio iconfont:wearable-sensor --size 96 --json
```

The `drawio` command returns a `shape=image` style containing a marker-less
base64 SVG data URI. This keeps the diagram portable and avoids a render-time
CDN dependency. The SVG remains vector in exports, but Draw.io treats it as one
image cell; use primitives when internal subparts must remain separately
editable.

For PowerPoint, insert the sanitized local SVG as an independent vector image
object. Keep its label as native PowerPoint text. The SVG can be moved, scaled,
and usually recolored, but internal path editability varies by PowerPoint
version; disclose that distinction when it matters.

## Safety and provenance

Import removes scripts, foreign objects, embedded raster images, event
handlers, and non-local URL references. It also records a SHA-256 digest and
sanitization counts in `data/icon-registry.json`.

Record at least the provider and local file. When available, also record the
asset page, author, license state, and attribution text. Copy relevant entries
to the figure's `asset-ledger.md` when the asset is used. Run:

```powershell
python <skill-dir>\scripts\vector_assets.py validate
```

before handoff. A registered asset must be embedded in the `.drawio`; do not
leave `http://` or `https://` image URLs in a camera-ready figure.

## Paper-scale review

At manuscript width verify that the asset:

- is recognizable without competing with the contribution block;
- has no opaque background, clipped edge, halo, or missing layer;
- retains adequate contrast after palette mapping;
- uses no unexplained decorative detail;
- does not make a standard component visually larger than the innovation.
