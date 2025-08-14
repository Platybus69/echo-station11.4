---
title: Echo Station Overview
cluster: echo-station
tags: glyphs lattice core
type: concept
summary: High-level overview of Echo Station as a dark, no-flash, recursive encyclopaedia driven by glyphs and glome-oriented geometry.
---
# Echo Station

**Summary** Echo Station is a human-in-the-loop, symbol-driven encyclopedia and codex. It ships as a static site with dark, no-flash rendering and URL-driven search. Entries are organized with *clusters* (e.g., `glome-s3`, `tesseract`, `spiral-engine`) and short *tags*.

- Prev / Random / Next links are baked at build time.
- Related entries are suggested by tag overlap and cluster match.
- If metadata is missing, the builder **autofills** reasonable defaults.

