#!/usr/bin/env bash
set -euo pipefail
rm -rf ./site
python3 tools/autofill_and_build_v8.py
rsync -a --delete site/ ./
echo "Deployed to repo root."
