#!/usr/bin/env python3
import os,re,sys,html
root = sys.argv[1] if len(sys.argv)>1 else 'site'
missing=[]
for dirpath,_,files in os.walk(root):
  for fn in files:
    if not fn.endswith('.html'): continue
    p = os.path.join(dirpath,fn)
    txt=open(p,encoding='utf-8').read()
    for href in re.findall(r'href="([^"]+)"', txt):
      if href.startswith(('http://','https://','mailto:','#')): continue
      tgt = os.path.normpath(os.path.join(dirpath, href))
      if not os.path.exists(tgt):
        missing.append((p, href))
if missing:
  print("Missing internal links:")
  for p,h in missing: print("-", p, "→", h)
  sys.exit(1)
print("OK: no missing internal links.")
