#!/usr/bin/env bash
set -euo pipefail
rm -rf ./site ./docs
python3 tools/autofill_and_build_v8.py
mkdir -p docs
rsync -a --delete site/ docs/
echo "Deployed to /docs (remember to set Pages source to /docs)."
