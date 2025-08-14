#!/usr/bin/env python3
import os, re, json, hashlib, datetime, pathlib, html
from collections import defaultdict

ROOT = os.getcwd()
SRC  = ROOT
OUT  = os.path.join(ROOT, 'site')
ENC  = os.path.join(OUT, 'encyclopedia')
ASSETS_SRC = os.path.join(ROOT, 'assets')
ASSETS_OUT = os.path.join(OUT, 'assets')
INLINE_DARK = """<style id="inline-dark-fallback">body{background:#0b0d12;color:#e6e6e6;margin:0}a{color:#8fd3ff;text-decoration:none}</style>"""
CLUSTERS_ALLOWED = {"glome-s3","hopf","stereographic","tesseract","lattice","spiral-engine","echo-station","glyphs","core"}

def read(path): 
    with open(path,'r',encoding='utf-8') as f: return f.read()

def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,'w',encoding='utf-8') as f: f.write(data)

def parse_frontmatter(md):
    meta, body = {}, md
    if md.startswith('---'):
        parts = md.split('\n',1)[1].split('\n---\n',1)
        if len(parts)==2:
            fm, body = parts
            for line in fm.splitlines():
                if ':' in line:
                    k,v=line.split(':',1)
                    meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    # tags: support comma lists
    if 'tags' in meta and isinstance(meta['tags'], str):
        meta['tags'] = [t.strip().lower() for t in re.split('[, ]+', meta['tags']) if t.strip()]
    if 'tags' not in meta: meta['tags']=[]
    if 'cluster' in meta: meta['cluster']=meta['cluster'].strip().lower()
    if 'title' not in meta:
        m = re.search(r'^#\s+(.+)$', body, re.M)
        if m: meta['title']=m.group(1).strip()
    if 'summary' not in meta:
        m = re.search(r'\*\*Summary\*\*[:\s]*(.+)', body)
        meta['summary'] = (m.group(1).strip() if m else re.sub(r'\s+',' ', body)[:180])
    if 'type' not in meta:
        meta['type']='concept'
    if meta.get('cluster') not in CLUSTERS_ALLOWED:
        meta['cluster'] = (meta.get('cluster') or 'core')
    # dedupe, cap to 6 tags
    meta['tags'] = list(dict.fromkeys([t for t in meta['tags'] if t]))[:6]
    return meta, body

def slugify(name): 
    s = re.sub(r'[^a-zA-Z0-9\-]+','-', name.strip()).strip('-').lower()
    return s or hashlib.sha1(name.encode()).hexdigest()[:8]

def render_template(meta, body_html, all_entries):
    title = html.escape(meta.get('title','Untitled'))
    cluster = meta.get('cluster','')
    tags = meta.get('tags',[])
    slug = meta['slug']
    # prev/next
    idx_map = {e['slug']:i for i,e in enumerate(all_entries)}
    i = idx_map[slug]
    prev_slug = all_entries[i-1]['slug'] if i>0 else all_entries[-1]['slug']
    next_slug = all_entries[(i+1)%len(all_entries)]['slug']
    # related (overlap tags + cluster)
    def score(other):
        if other['slug']==slug: return -1
        s = 0
        s += 3 if other.get('cluster')==cluster else 0
        s += len(set(tags)&set(other.get('tags',[])))
        return s
    related = sorted(all_entries, key=score, reverse=True)[:5]
    # html
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Echo Station Encyclopedia</title>
<link rel="canonical" href="./index.html">
{INLINE_DARK}
<link rel="stylesheet" href="../../assets/style.css">
</head><body class="dark">
<header><main>
  <div style="display:flex;gap:16px;align-items:center;justify-content:space-between;padding:12px 0">
    <div><a href="../index.html">← Encyclopedia</a></div>
    <div class="small">{cluster and f'<span class="badge">{cluster}</span>'} {" ".join(f'<span class="badge">#{t}</span>' for t in tags)}</div>
  </div>
</main></header>
<main>
  <h1>{title}</h1>
  <article class="card">{body_html}</article>
  <div class="grid">
    <div class="card">
      <strong>Navigate</strong><br>
      <a href="../{prev_slug}/index.html">Prev</a> · 
      <a href="../random.html">Random</a> · 
      <a href="../{next_slug}/index.html">Next</a>
    </div>
    <div class="card">
      <strong>Related</strong>
      <ul>
        {''.join(f'<li><a href="../{e["slug"]}/index.html">{html.escape(e["title"])}</a></li>' for e in related)}
      </ul>
    </div>
  </div>
</main>
<footer><main class="small">© Echo Station · built {datetime.date.today()}</main></footer>
<script src="../../assets/search.js"></script>
</body></html>"""

def md_to_html(md):
    # ultra-minimal md -> html (headers, paragraphs, code)
    lines = md.splitlines()
    out=[]
    in_code=False
    for ln in lines:
        if ln.startswith('```'):
            in_code = not in_code
            out.append('<pre><code>' if in_code else '</code></pre>')
            continue
        if in_code:
            out.append(html.escape(ln))
        elif ln.startswith('#'):
            lvl = len(ln)-len(ln.lstrip('#'))
            out.append(f"<h{lvl}>{html.escape(ln[lvl:].strip())}</h{lvl}>")
        elif ln.strip():
            out.append(f"<p>{ln}</p>")
    return '\n'.join(out)

def copy_assets():
    os.makedirs(ASSETS_OUT, exist_ok=True)
    for fn in os.listdir(ASSETS_SRC):
        write(os.path.join(ASSETS_OUT, fn), read(os.path.join(ASSETS_SRC, fn)))

def build():
    os.makedirs(ENC, exist_ok=True)
    copy_assets()

    # collect entries
    md_files=[]
    for base in (os.path.join(SRC,'codex','encyclopedia'),):
        if os.path.isdir(base):
            for fn in sorted(os.listdir(base)):
                if fn.lower().endswith('.md'):
                    md_files.append(os.path.join(base,fn))

    entries=[]
    for path in md_files:
        md = read(path)
        meta, body = parse_frontmatter(md)
        base = os.path.basename(path)
        slug = slugify(meta.get('slug') or os.path.splitext(base)[0])
        meta['slug']=slug
        meta['title']=meta.get('title') or base
        meta['summary']=meta.get('summary','')
        entries.append(meta)

    # sort entries by slug for stable prev/next
    entries = sorted(entries, key=lambda e: e['slug'])
    # write pages
    for path in md_files:
        md = read(path); meta,_ = parse_frontmatter(md)
        slug = slugify(meta.get('slug') or os.path.splitext(os.path.basename(path))[0])
        meta['slug']=slug
        # enrich meta from global list so prev/next/related have context
        enriched = [e for e in entries if True]
        html_body = md_to_html(md.split('\n---\n',1)[-1] if md.startswith('---') else md)
        page = render_template(meta, html_body, enriched)
        write(os.path.join(ENC, slug, 'index.html'), page)

    # random redirect helper
    write(os.path.join(ENC,'random.html'),
          f"""<!doctype html><meta charset="utf-8">{INLINE_DARK}
<script>
fetch('./search.json').then(r=>r.json()).then(list=>{{
  const pick = list[Math.floor(Math.random()*list.length)];
  location.href = './'+pick.slug+'/index.html';
}});
</script>""")

    # index page with search
    write(os.path.join(ENC,'index.html'), f"""<!doctype html><html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Echo Station Encyclopedia</title>
{INLINE_DARK}<link rel="stylesheet" href="../assets/style.css">
<link rel="search" type="application/opensearchdescription+xml" href="../opensearch.xml" title="Echo Station Search">
</head><body class="dark"><header><main>
  <div style="padding:12px 0;display:flex;gap:12px;align-items:center;justify-content:space-between">
    <strong>Echo Station · Encyclopedia</strong>
    <a class="small" href="../feed.json">feed</a>
  </div>
  <input class="search" placeholder="Search…  (filters: tag:NAME  cluster:NAME)" />
</main></header><main>
  <div id="search-results" class="grid"></div>
</main>
<footer><main class="small">Type <code>/</code> to focus search · <code>Esc</code> to clear</main></footer>
<script src="../assets/search.js"></script>
</body></html>""")

    # indices
    search = [{k: e[k] for k in ('slug','title','summary','tags','cluster')} for e in entries]
    write(os.path.join(OUT,'encyclopedia','search.json'), json.dumps(search,indent=2))
    write(os.path.join(OUT,'encyclopedia','index.json'), json.dumps(entries,indent=2))

    # tags / clusters counts
    tag_counts=defaultdict(int); cluster_counts=defaultdict(int)
    for e in entries:
        for t in e.get('tags',[]): tag_counts[t]+=1
        if e.get('cluster'): cluster_counts[e['cluster']]+=1
    write(os.path.join(OUT,'encyclopedia','tags.json'), json.dumps(tag_counts,indent=2))
    write(os.path.join(OUT,'encyclopedia','clusters.json'), json.dumps(cluster_counts,indent=2))

    # tag & cluster pages (lists)
    for t,cnt in tag_counts.items():
        items=[e for e in entries if t in e.get('tags',[])]
        write(os.path.join(OUT,'tags',t+'.html'),
              f"<!doctype html><meta charset=utf-8>{INLINE_DARK}<link rel=stylesheet href=../assets/style.css><body class=dark><main><h1>Tag: #{html.escape(t)}</h1><ul>"+''.join(f'<li><a href=../encyclopedia/{e["slug"]}/index.html>{html.escape(e["title"])}</a></li>' for e in items)+"</ul></main>")

    for c,cnt in cluster_counts.items():
        items=[e for e in entries if e.get('cluster')==c]
        write(os.path.join(OUT,'clusters',c+'.html'),
              f"<!doctype html><meta charset=utf-8>{INLINE_DARK}<link rel=stylesheet href=../assets/style.css><body class=dark><main><h1>Cluster: {html.escape(c)}</h1><ul>"+''.join(f'<li><a href=../encyclopedia/{e["slug"]}/index.html>{html.escape(e["title"])}</a></li>' for e in items)+"</ul></main>")

    # opensearch, feed, sitemap, 404
    write(os.path.join(OUT,'opensearch.xml'), f"""<?xml version="1.0"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
<ShortName>Echo Station</ShortName><Description>Search Echo Station Encyclopedia</Description>
<Url type="text/html" template="./encyclopedia/index.html?q={{searchTerms}}"/>
</OpenSearchDescription>""")
    items=[{"id":e["slug"],"title":e["title"],"summary":e["summary"],"url":f"./encyclopedia/{e['slug']}/index.html"} for e in entries]
    write(os.path.join(OUT,'feed.json'), json.dumps({"version":"https://jsonfeed.org/version/1.1","title":"Echo Station","items":items}, indent=2))
    sm="\n".join(f"<url><loc>./encyclopedia/{e['slug']}/index.html</loc></url>" for e in entries)
    write(os.path.join(OUT,'sitemap.xml'), f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    write(os.path.join(OUT,'404.html'), f'<!doctype html><meta charset=utf-8>{INLINE_DARK}<meta http-equiv="refresh" content="0; url=./encyclopedia/index.html">')

    print(f"Built {len(entries)} entries → {OUT}")
if __name__=='__main__': build()
