# Sitemap: switch to XML with absolute URLs

**Why**
- Prior sitemap was space-separated relative paths; not crawler-friendly.

**Changes**
- Generate docs/sitemap.xml as valid XML urlset with absolute URLs.
- Add docs/robots.txt referencing the sitemap.

**Verify**
- Open /sitemap.xml; it should be XML and pretty-printed.
- Validate with `curl -s https://platybus69.github.io/echo-station11.4/sitemap.xml | head`
