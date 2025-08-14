#!/usr/bin/env bash
set -euo pipefail
rm -rf ./site ./docs
python3 tools/autofill_and_build_v8.py
mkdir -p docs
rsync -a --delete site/ docs/
echo "Deployed to /docs (remember to set Pages source to /docs)."

BASE_URL="https://platybus69.github.io/echo-station11.4" OUT_DIR="docs" python3 scripts/gen_sitemap_xml.py
