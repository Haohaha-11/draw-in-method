# Semantic-First Figure Workflow

Read this reference before reproducing a reference image or turning a paper,
method description, or codebase into a figure. The purpose is to prevent the
drawing backend or available icon set from deciding the scientific meaning.

## Two separate passes

### Pass A: understand the figure

Describe the figure without coordinates or drawing commands:

- the main claim or reader takeaway;
- named entities and their scientific roles;
- groups, panels, stages, repeated modules, and containment;
- typed relations: data, control, update, feedback, comparison, annotation;
- reading order and branch/merge points;
- training-only, inference-only, frozen, learned, proposed, and standard paths;
- labels, tensor symbols, equations, and uncertain or unreadable evidence;
- physical/context entities that need a named visual asset.

For a reference screenshot, do not treat visual proximity as proof of a
scientific relation. Use arrowheads, captions, repeated structure, paper text,
and user context. Record uncertainty instead of inventing a relation or label.

### Pass B: plan the visual encoding

Only after Pass A is stable, map semantic roles to panels, boxes, connectors,
colors, typography, icons, and coordinates. Preserve a reference image's
layout and style when requested, but keep the semantic graph authoritative.

## Format-neutral figure model

Create `figure-model.json` before authoring PPTX or Draw.io. A compact model is
enough; avoid storing backend-specific XML or slide APIs in it.

```json
{
  "schema_version": "1.0",
  "title": "Method overview",
  "primary_output": "pptx",
  "reading_order": "left-to-right",
  "nodes": [
    {
      "id": "input_image",
      "label": "Input image",
      "role": "input",
      "kind": "physical",
      "group": "overview",
      "aliases": ["image", "输入图像"],
      "asset_strategy": "search"
    }
  ],
  "edges": [
    {
      "id": "input_to_encoder",
      "source": "input_image",
      "target": "encoder",
      "relation": "data",
      "label": ""
    }
  ],
  "groups": [
    {"id": "overview", "label": "Overall Architecture", "members": []}
  ],
  "asset_queries": [
    {
      "node_id": "input_image",
      "canonical_name": "input image",
      "queries": ["input image", "image sample", "输入图像"],
      "providers": ["local-registry", "iconfont", "flaticon", "iconify"],
      "selected_asset": "",
      "fallback_reason": ""
    }
  ],
  "uncertainties": []
}
```

Use stable node and edge ids across backends. When both PPTX and Draw.io are
requested, both artifacts must realize the same node/edge set unless a
backend-specific omission is explicitly documented.

## Understanding gate

Do not start geometry until all of the following are true:

- every required node has a role and a group;
- every semantic edge has a source, target, direction, and relation type;
- the proposed contribution and output are identifiable;
- unreadable reference text is listed as uncertainty;
- every physical/context entity has an asset strategy;
- `brief.md` traceability points to model nodes or edges.

## Named asset planning and Stage 3 resolution gates

For each node with `asset_strategy: search`:

1. generate canonical English and Chinese names plus useful synonyms;
2. record candidate providers and reserve an appropriately sized geometry slot
   during semantic preflight and Stage 1;
3. after Stage 2 text is approved, search the local registry and native shape
   index, then user-authorized providers through their normal visible interface;
4. compare available plausible candidates for semantic fit, visual family, SVG
   quality, editability, and provenance;
5. during Stage 3, select and register an asset, or write a concrete fallback
   reason.

The normal `validate_figure_model.py` preflight accepts a planned query whose
`selected_asset` and `fallback_reason` are still empty. At the end of Stage 3,
run `validate_figure_model.py --require-assets-resolved <figure-model.json>`;
that strict gate rejects every unresolved search.

Do not use a primitive-built device, person, animal, laboratory object, or
application icon merely because it is faster. Primitive composition remains
appropriate for tensors, attention, operators, abstract model blocks, and
paper-specific mechanisms whose meaning comes from diagram geometry.

## Verification questions

Before visual QA, ask:

- Can the figure's scientific story be restated using only node and edge ids?
- Does every visible arrow correspond to one modeled relation?
- Does every icon depict a named entity rather than decorate empty space?
- If all icons were removed, would the computation still be understandable?
- Do PPTX and Draw.io outputs preserve the same semantic graph?
