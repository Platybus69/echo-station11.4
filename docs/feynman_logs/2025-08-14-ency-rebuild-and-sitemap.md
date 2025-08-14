# 2025-08-14 — Encyclopedia rebuild, search index, sitemap

- Rebuilt encyclopedia and search index; ensured dark inline fallback on index.
- Deployed assets (`assets/style.css`, `assets/search.js`) and restored `.nojekyll`.
- Regenerated `sitemap.xml` with absolute URLs via `BASE_URL`.
- Added root redirect `docs/index.html` → `/encyclopedia/`.
- No content changes to entries; navigation integrity only.

Checks:
- 200 for /encyclopedia/index.html, /encyclopedia/search.json, /opensearch.xml, /feed.json, /sitemap.xml.
