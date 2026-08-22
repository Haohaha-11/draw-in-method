# Reference Image Replication Protocol

Use this protocol whenever the user provides a reference image and asks to reproduce, redraw, copy, or closely match it in editable PowerPoint or Draw.io.

The goal is to make high-fidelity drawing an evidence-driven engineering process. First understand the semantic graph, then convert the image into a mechanical visual specification, then author the selected native backend, and finally verify with rendered screenshots.

## Hard Rules

1. Do not begin Draw.io XML or PowerPoint authoring until the required intermediate artifacts and `figure-model.json` exist.
2. The requested native editable backend is primary: `.pptx` for PowerPoint or `.drawio` for Draw.io. Preview images/HTML are derived and must not be treated as the source of truth.
3. Never silently omit a visible component. If an icon, formula, symbol, or image cannot be reproduced exactly, add it to `asset-ledger.md`. Search named vector assets before primitive-building a physical/context icon.
4. Do not reproduce only the geometry. Identify connector semantics: source, target, direction, fan-in/fan-out, feedback, grouping, and arrowhead placement.
5. Do not use "close enough" language for high-fidelity work. Record remaining mismatches in `defect-log.md`.
6. For Draw.io, run `scripts/validate_visual_quality.py` before the first preview; zero FAILs are required. For PowerPoint, render the slide and run the supported overflow/slide test before the first fidelity claim.
7. Do not finish without at least 3 rendered screenshot review cycles (each with a canvas-only screenshot). First drafts are always flawed.
8. Do not finish without a complete 9-zone defect inventory (graduated minimum: C1≥30, C2≥15, C3≥8), all P0/P1 fixed and verified, a red-team audit (≥15 findings, or ≥10 if self-score ≥45/50), and a self-score card (TOTAL ≥ 40 AND every dimension ≥ 6; a dimension of 5 is borderline — review and improve before handoff).
9. Do not judge fidelity from a full browser screenshot. The diagram must fill ≥ 80% of the screenshot image. A screenshot showing the diagrams.net toolbar, sidebar, or browser chrome is INVALID — you cannot read text or see spacing at that scale. Crop to the canvas rectangle or zoom the viewport.
10. If the screenshot shows large structural errors, repair `visual-spec.md` and `layout-grid.md` first, then patch XML. Do not keep nudging objects without updating the plan.
11. Do not overwrite screenshot review history. A generator may create `defect-log.md` only before review begins; after the first screenshot row exists, append new passes and corrections instead of replacing the file.
12. Do not run artifact validation in parallel with generation, preview creation, screenshot capture, or scripts that write the same workdir. Validate only after those writes complete so the result reflects one coherent artifact state.

## Required Artifacts

Create these files next to the working native artifact:

```text
brief.md
figure-model.json
visual-spec.md
layout-grid.md
asset-ledger.md
production-review.md
defect-log.md
```

Run `scripts/validate_replication_artifacts.py <workdir>` before authoring Draw.io XML. For PPTX, verify the same evidence set manually until the validator supports the backend-specific deliverable.

Use `production-review.md` to preserve the semantic preflight decision and the
four production-stage gates defined in `staged-drawing-workflow.md`, including
the four incremental Stage 1 architecture checkpoints. Use `defect-log.md` for
the deeper screenshot inventories, red-team audit, and final quality evidence;
the two files serve different purposes.

For either backend, also run:

```powershell
python scripts/validate_figure_model.py <workdir>/figure-model.json
```

Do not proceed to Stage 1 while the semantic model has an unknown edge endpoint
or a physical/context entity lacks a named-asset plan. Asset selection itself
belongs to Stage 3. At the end of Stage 3, run:

```powershell
python scripts/validate_figure_model.py <workdir>/figure-model.json --require-assets-resolved
```

Do not proceed to final review while that strict asset gate fails.

After the latest screenshot pass and before handoff, run:

```powershell
python scripts/validate_replication_artifacts.py <workdir> --require-screenshot-review
```

This final check fails if `defect-log.md` still contains placeholder screenshot rows.

## 1. visual-spec.md

This file captures what is visible.

Required sections:

```markdown
# Visual Spec

## Source
- Reference image:
- Target editable output:
- Canvas:
- Font policy:

## Global Style
- Background:
- Primary font:
- Stroke style:
- Arrow style:
- Color palette:

## Regions
| id | bbox x,y,w,h | role | visual notes |

## Text Blocks
| id | bbox x,y,w,h | text | font | alignment | priority |

## Shapes
| id | bbox x,y,w,h | type | fill | stroke | notes |

## Connectors
| id | from | to | route | arrowheads | label | notes |

## Semantic Relations And Flow
| id | source | target | meaning | direction/cardinality | visual evidence |

## Icons And Images
| id | bbox x,y,w,h | meaning | exact/approx/missing | replacement plan |
```

For complex research figures, use region IDs such as:

- `top_problem_statement`
- `bottom_method_overview`
- `memory_hierarchy`
- `routing_controller`
- `latent_workspace`
- `multimodal_streams`

## 2. layout-grid.md

This file turns the visual spec into coordinates. High-fidelity drawing needs explicit geometry, not vague relative placement.

Required sections:

```markdown
# Layout Grid

## Canvas
- width:
- height:
- scale assumption:
- margin:

## Grid Lines
| name | x | y | purpose |

## Region Boxes
| id | x | y | w | h |

## Repeated Components
| family | count | cell size | spacing | start x,y |

## Drawing Order
1. background regions
2. containers
3. internal shapes
4. connectors
5. text
6. icons
7. highlights/overlays
```

If the reference has a dense layout, do not rely on relative placement only. Use explicit x/y/w/h for each major container.

## 3. asset-ledger.md

This file prevents silent icon loss.

Required sections:

```markdown
# Asset Ledger

## Exact Assets
| id | source | path | usage |

## Named Asset Searches
| id | canonical name and aliases | providers/candidates | selection/fallback reason |

## Editable Primitive Icons
| id | built from | why retrieval was unsuitable | fidelity notes |

## Approximations
| id | reference meaning | approximation | why |

## Missing Assets
| id | reference meaning | blocking issue | user action needed |
```

If using an embedded raster image, state why editability is intentionally reduced.

For physical/context entities, read `semantic-first-workflow.md` and `vector-assets.md` before inventing one-off approximations. Use `primitive-icons.md` mainly for abstract computation or a documented retrieval fallback. The asset ledger must name the search queries and the primitive recipe used.

## 4. defect-log.md

This file records screenshot-based refinement.

Required sections:

```markdown
# Defect Log

## Pass 0 - Initial Plan Review
| issue | reference evidence | planned fix |

## Pass 1 - Screenshot Review
| issue | observed screenshot | reference evidence | objects to change | patch summary | status |

## Screenshot Evidence
| pass | screenshot path | capture type | full canvas visible | crop/viewport notes |

## Requirement And Semantic Audit
| check | observed screenshot | expected from reference | actual | status |

## Red-Team Visual Audit
| check | observed screenshot | finding | objects to change | status |

## Remaining Gaps
| gap | severity | reason | next action |
```

Each screenshot pass must add concrete defects. Avoid entries like "looks bad"; write "right-side multimodal panel is 18% too narrow" or "top dense-token bar missing icon cells".

The screenshot evidence table must state whether the evidence is `full-page`, `canvas-only`, `deliberate-crop`, `editor-full-canvas`, or `editor-partial`. Use `editor-partial` only for debugging; it is not enough for final fidelity claims. For final handoff, the latest evidence should show the full canvas/page or a deliberate crop that contains the whole diagram.

`defect-log.md` is append-only after the first rendered screenshot review. If an earlier row becomes outdated, add a later pass row explaining the correction; do not delete or regenerate previous screenshot evidence. This preserves the visual debugging chain and prevents a new generation run from erasing regressions the user already saw.

The red-team audit is a separate pass whose goal is to find mistakes, not to confirm improvement. It must explicitly inspect:

- arrow direction and arrowhead placement
- fan-in/fan-out, grouped routes, merge/split points, and feedback semantics
- bracket orientation and grouped annotation direction
- connector paths that cross text, pass through boxes, or create impossible flow
- box overlaps, clipped shapes, and z-order mistakes
- text overflow, wrapped titles, illegible formulas, and labels crossed by lines
- regressions introduced by the latest patch

## Minimum Quality Gate

Before handoff, verify:

- The requested native `.pptx` or `.drawio` exists and is the primary artifact; the whole figure is not flattened into a cover image.
- For Draw.io, `validate_visual_quality.py` passed with zero FAILs and `validate_drawio.py` passes.
- For PowerPoint, every slide was rendered, the supported slide/overflow test passes, and representative text, shape, connector, group, and SVG objects are independently selectable.
- `validate_replication_artifacts.py <workdir> --require-screenshot-review` passes.
- Preview HTML was regenerated after the latest XML edit.
- At least 3 screenshot→inventory→fix→verify cycles were completed with canvas-only screenshots (graduated minimum: C1≥30, C2≥15, C3≥8).
- `defect-log.md` includes all cycle reports, each meeting the graduated per-cycle minimum.
- `defect-log.md` includes a screenshot evidence row with capture type ("canvas-only" if valid, "full-browser" = INVALID).
- `defect-log.md` includes a requirement and semantic audit of the latest screenshot.
- `defect-log.md` includes a red-team visual audit of the latest screenshot (≥15 findings across 9 zones; ≥10 if self-score ≥45/50).
- `defect-log.md` lists remaining mismatches.
- A self-score card exists with TOTAL ≥ 40 AND every dimension ≥ 6, with concrete evidence for every deduction.
- Validation was run after generation and preview writes completed, not concurrently with them.
- No visible reference component was silently omitted.

For a "100% reproduction" request, the defect log must not claim perfection. It must either show that no visible mismatches remain after screenshot review, or list the exact remaining mismatches and the next patch targets.

## Graduated Minimums Reference

The flat "30 everything" was replaced with a graduated model that prevents fabrication on clean diagrams:

| Phase | Minimum |
|-------|---------|
| Cycle 1 defect inventory | ≥30 |
| Cycle 2 defect inventory | ≥15 |
| Cycle 3+ defect inventory | ≥8 (or ≥5 if P0=0 and self-score ≥40) |
| Red-team audit (default) | ≥15 |
| Red-team audit (self-score ≥45/50) | ≥10 |

See `references/self-supervision-and-intake.md` Section 4.1 for the full graduated model rationale.

## High-Fidelity Replication Discipline

If the first draft is messy, do not continue patching randomly. Return to `visual-spec.md` and `layout-grid.md`, identify which observation or coordinate assumption failed, and repair the plan before editing XML again.

Prefer a simpler but structurally faithful first draft over a visually dense but incoherent drawing:

1. Correct semantic nodes, groups, relations, uncertainties, and asset plans in
   `figure-model.json`.
2. Correct canvas, base color regions, module-size families, and container
   hierarchy.
3. Correct arrows, ports, and connector semantics.
4. Correct scientific text, annotations, and paper-scale readability.
5. Resolve and place named physical/context assets.
6. Complete full-canvas review, coordinated micro-adjustments, and export QA.

Only after the structure is correct should the agent increase visual density.

When a generated result looks bad, inspect these first-principles failure points:

- canvas scale or browser zoom makes the page clipped
- headings are too large and wrap unexpectedly
- multiline labels overlap nearby annotations
- bottom labels escape or touch the page edge
- connector routes use straight lines where the reference uses loops
- connector routes preserve geometry but invert the meaning, such as drawing a fan-in as five independent arrows
- icons were silently replaced with generic symbols
- background fills, shadows, and dashed borders were skipped
- generated scripts reset evidence files instead of appending new screenshot observations
- validator results were taken while another process was still rewriting the workdir

Use the defect log as an engineering ledger: every visible mismatch should map to a semantic misunderstanding, missing observation, incorrect coordinate, unavailable asset, or backend rendering difference.
