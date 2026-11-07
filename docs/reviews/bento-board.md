# Bento Board UI — source-derived brand presentation

Source: https://www.figma.com/community/skill/72022/bento-board-ui

The installed skill calls for a brand poster, not a dashboard. Deliverable: [live brand board](http://127.0.0.1:8000/assets/brand-board.html), implemented in `frontend/brand-board.html` and `frontend/brand-board.css`. A link is available from the research report.

## Source inventory

The app contained no raster photography. The board uses the prescribed flat-copy hero and source-logo fallback. Logo bars and wordmark markup were copied from the app. The measured Best tuned WER card was copied from the rendered overview (E1, 20.9%, validation); it is a dated presentation snapshot, not a live metric feed. No stock or invented image assets were added.

Fonts: Manrope display, DM Sans supporting text. Palette: #18242B, #1D3334, #D1F281, #364BE8, #F1F3EF. Mission and hero copy are from the app. The metric 4,110 is the prepared Spanish dataset clip count.

## Geometry and composition

Browser measurement: frame 1920×1080, padding 32, gaps 16, radius 28. Three equal 386px left columns plus one full-height 650px hero; rows 320 / 344 / 320. Eight tiles: mission spans two columns, metric, logo, typography, colors, logo-mark fallback, how-it-works spans two columns, and the right hero. The hero occupies about 34% of the frame width. Tile bounds showed no content overflow.

Tiles use flat varied fills, including blue and lime accents and dark type/hero surfaces; adjacent tiles do not share identical fills. Tiles are borderless and shadowless. The copied UI fragment retains its source card treatment. On narrow screens the poster uses a named keyboard-focusable horizontal scroll region; the separate working app remains responsive. Print styles remove surrounding toolbar and notes.

Evidence: `../brand-board-preview.png`. Heading order begins with the hero h1, followed by tile h2 headings. This is a local website artifact; no new Figma file, upload, or canvas annotation is claimed.


After the accuracy follow-up, the live poster source card was updated to E8’s current validation WER (5.7%), and its copy to “One lab. Measured progress.” The original poster preview records the earlier design review; current measured-result proof is `../accuracy-results-preview.png`.
