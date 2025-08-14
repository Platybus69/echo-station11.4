# Feynman Log — Encyclopedia index loader harden
**Why:** `/encyclopedia/index.html` showed “No results” despite `search.json` 200 OK.
**Fix:** Self-contained index that auto-detects repo base, fetches `search.json` with fallback to `index.json`, accepts multiple JSON shapes, and renders all entries by default. Keeps `/` focus and `Esc` clear.
**Verify:** Visit `/encyclopedia/index.html?cachebust=$(date +%s)` → list renders. `?q=tag:lattice` and `?q=cluster:glome-s3` filter correctly.
