---
title: Pages bootstrap & search index materialization
date: 2025-08-13
by: build-ops
---

**Why**
- Enable GitHub Pages from `/docs` and avoid Jekyll processing.
- Replace symlinked `search.json` per entry with real files so Pages serves them.

**Changes**
- Added `docs/.nojekyll`.
- Materialized `search.json` for:
  - `encyclopedia/es-000-echo-station-overview/`
  - `encyclopedia/es-010-glome-basics/`
  - `encyclopedia/es-020-tesseract-to-glome/`
  - `encyclopedia/es-030-spiral-reap-glyph/`

**Verification**
- Local build passed (`scripts/check_links.py site` reported 0 missing links).
- Next: enable Pages (main → /docs) and run live checks after publish.
