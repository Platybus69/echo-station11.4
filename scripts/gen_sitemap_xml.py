import os, glob, html, sys
BASE=os.environ.get("BASE_URL","").rstrip("/")
OUT=os.environ.get("OUT_DIR","docs")
if not BASE: sys.exit("Missing BASE_URL")
urls=[]
for p in glob.glob(os.path.join(OUT,"encyclopedia","**","index.html"), recursive=True):
    rel=os.path.relpath(p, OUT).replace(os.sep,"/")
    rel=rel[:-10] if rel.endswith("/index.html") else rel
    urls.append(f"{BASE}/{rel}".rstrip("/"))
root=[f"{BASE}/", f"{BASE}/opensearch.xml", f"{BASE}/feed.json"]
urls=sorted(set(urls))
with open(os.path.join(OUT,"sitemap.xml"),"w",encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in root + urls:
        f.write(f'  <url><loc>{html.escape(u)}</loc></url>\n')
    f.write('</urlset>\n')
print("sitemap: wrote", 3+len(urls), "URLs")
