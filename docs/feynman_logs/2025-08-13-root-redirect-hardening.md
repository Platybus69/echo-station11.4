# Pages hardening: root index + 404 redirect

**Why**
- Root `/` returned 404 despite `docs/index.html` existing.
- Add JS-redirect fallback and a 404 redirect to `/encyclopedia/`.

**Changes**
- Rewrote `docs/index.html` (meta refresh + canonical + JS).
- Added `docs/404.html`.
- Confirmed `.nojekyll` present.

**Verify**
- Root 200/HTML served, browser redirects to `/encyclopedia/`.
- `/opensearch.xml`, `/feed.json`, `/sitemap.xml` stay 200.
