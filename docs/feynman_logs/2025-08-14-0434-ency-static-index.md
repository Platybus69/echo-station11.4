# Feynman Log — Encyclopedia static index + same-dir data.json
**Why:** Index rendered empty and push was blocked by the Feynman-log pre-push hook.
**Fix:** Wrote `docs/encyclopedia/data.json` (derived from existing JSON) and a self-contained `docs/encyclopedia/index.html` that fetches `./data.json`, shows all by default, with inline filter and dark CSS. Added `.nojekyll`.
**Verify:** Visit `/encyclopedia/index.html?v=NOW` — entries render immediately; `/` focuses; `Esc` clears; `?q=tag:glome` and `?q=cluster:glome-s3` filter.
