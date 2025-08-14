# 2025-08-14 — Encyclopedia link fixes & JSON Feed urls

**Why:** Entry links were refreshing (click handler intercepted), and `feed.json` needed absolute URLs. Also keep Pages static via `.nojekyll`.

**Changes:**
- `docs/assets/search.js`: only intercepts filter chips (`data-filter`); normal links navigate.
- `docs/encyclopedia/data.json`: each item url → `./<slug>/index.html` (UI also works with slug).
- `docs/feed.json`: absolute item URLs:
  `https://platybus69.github.io/echo-station11.4/encyclopedia/<slug>/index.html`.
- Preserve `.nojekyll`.

**Checks:**
- `/encyclopedia/index.html` shows entries; clicking an entry navigates.
- `/encyclopedia/data.json` has `url` ending `/index.html`.
- `/feed.json` is valid JSON Feed (browser shows JSON—expected).
- `.nojekyll` exists in `docs/`.
