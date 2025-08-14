# Search: base-path fix for project pages

**Why**
- Some assets used absolute `/encyclopedia/...` fetches, which 404 on project pages like `/echo-station11.4/`.

**Changes**
- Replaced `assets/search.js` with a base-path aware implementation and copied to `docs/assets/search.js`.
- (If present) Updated `docs/opensearch.xml` template to project base.

**Verification**
- `https://platybus69.github.io/echo-station11.4/encyclopedia/?q=glome` shows results with working links and in-page highlights.
- No 404s for `encyclopedia/search.json` in DevTools.
