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

Use source priority, not merely implementation convenience. For physical and
context assets, the preferred visual source is Flaticon or Alibaba Iconfont.
A cached local SVG counts as preferred only when its registry entry records one
of those providers and the exact asset-page provenance. Choose sources in this
order:

1. Use native editable backend primitives for model computation, tensors, operators,
   attention, feature interaction, and paper-specific mechanisms.
2. Search the local registry with `scripts/vector_assets.py search` for an
   exact previously downloaded **Flaticon or Iconfont** asset using the
   canonical name and aliases. Reuse it only if its style fits the current
   figure.
3. If no exact preferred-provider asset is cached, search Flaticon and Alibaba
   Iconfont through their normal visible UI. Compare a small set of candidates
   before downloading the selected SVG; do not treat a search-result thumbnail
   or page link as the delivered asset.
4. If both preferred providers lack an adequate candidate, consider Iconify or
   another user-authorized external provider, then `scripts/shapesearch.py` for
   native Draw.io engineering/cloud shapes. Use `scripts/aiicons.py` only for a
   required AI/LLM brand mark.
5. Use bundled Lucide assets, generic native symbols, or a constrained custom
   primitive icon only as documented fallbacks. Record the provider queries,
   rejected candidates, and concrete failure reason.

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
endpoints. If sign-in, CAPTCHA, plan selection, or a license confirmation blocks
the actual download, pause at that point and ask the user to take over or supply
the SVG/project pack. Never replace a blocked external download with a
self-drawn icon without disclosing the fallback.

## Preferred-provider candidate gate

Before selecting a physical/context SVG, capture 2–6 plausible candidates when
available. The figure workspace should record:

- canonical entity and Chinese/English search terms;
- provider, asset name/id, asset-page URL, author or pack, and visible license state;
- a preview or screenshot sufficient to compare silhouette and detail level;
- intended slot, orientation, color mode, and expected paper-scale size;
- selection/rejection reason and the final downloaded local SVG path.

Prefer one coherent pack or illustrator across a panel. Do not mix detailed
multicolor Flaticon illustrations with sparse mono Iconfont glyphs merely to
fill every slot. Search again or leave a computation block icon-free when the
family mismatch would weaken the figure.

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
