import sys, re, os, glob
bad = []
for root in ('docs','site'):
  for p in glob.glob(root+'/**/*.html', recursive=True):
    s = open(p, 'r', encoding='utf-8', errors='ignore').read()
    for i, line in enumerate(s.splitlines(), 1):
      # catch href="/..." or src="/..." or fetch("/...")
      if re.search(r'\b(href|src)\s*=\s*"/', line) or re.search(r'\bfetch\s*\(\s*"/', line):
        bad.append((p, i, line.strip()))
if bad:
  print('Absolute-root links detected (should be relative):')
  for p,i,l in bad[:200]:
    print(f'{p}:{i}: {l}')
  sys.exit(1)
print('OK: no absolute-root links found.')
