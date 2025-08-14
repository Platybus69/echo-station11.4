# Sitemap XML: remove empty <loc>, list all entries

**Issue**  
Live `sitemap.xml` had a blank `<loc>` and omitted encyclopedia entries due to an earlier generator that included `""` in extras.

**Change**  
Rewrote sitemap generation: absolute URLs, no empty entries, includes all `encyclopedia/**/index.html` pages + root endpoints.

**Verify**  
`curl -s https://platybus69.github.io/echo-station11.4/sitemap.xml | sed -n '1,12p'`
