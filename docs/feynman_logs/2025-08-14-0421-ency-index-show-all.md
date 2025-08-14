# Feynman Log — Encyclopedia index fix (show-all, robust base)
**Why:** `/encyclopedia/index.html` rendered “No results” even though `/encyclopedia/search.json` returned 200.
**Root Cause (likely):** Base-path/asset mismatch plus old search code requiring a non-empty query.
**What:** Replaced index with a self-contained page that auto-detects `/echo-station11.4` base, loads `search.json` (or `index.json`), and shows all entries by default with tag/cluster filters.
**Verify:** Open `/encyclopedia/index.html` — list renders. `/` focuses; `Esc` clears. `?q=tag:glome` and `?q=cluster:echo-station` filter.
