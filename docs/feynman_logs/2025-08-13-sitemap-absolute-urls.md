# Sitemap: switch to absolute URLs (XML)

**Why**
- Prior sitemap contained relative paths and wasn’t crawler-friendly.

**Changes**
- Regenerated `docs/sitemap.xml` as XML with absolute `<loc>` values.

**Verify**
- `curl -s https://platybus69.github.io/echo-station11.4/sitemap.xml | head`
- Entries start with `https://platybus69.github.io/echo-station11.4/…`
