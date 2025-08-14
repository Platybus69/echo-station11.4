# Pages: root redirect to /encyclopedia/

**Why**
- Ensure site root (`/`) lands on `/encyclopedia/` for a clean entrypoint.

**Changes**
- Added `docs/index.html` with meta refresh and canonical to `./encyclopedia/`.

**Verification**
- After publish, `https://<user>.github.io/echo-station11.4/` should redirect to `/encyclopedia/`.
- `gh api repos/Platybus69/echo-station11.4/pages --jq '.status'` returns `built`.

