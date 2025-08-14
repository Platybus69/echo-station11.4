/* Echo Station: minimal runtime hardening for encyclopedia pages */
(function () {
  // 1) Ignore cache-buster (?v=...) unless a real search param (?q=...) exists.
  try {
    const params = new URLSearchParams(location.search);
    if (params.has('v') && !params.has('q')) {
      history.replaceState(null, "", location.pathname); // drop ?v to show all entries
    }
  } catch (_) {}

  // 2) Normalize the FEED link to the site root under this project.
  try {
    const a = document.querySelector('a[href^="feed"], a[href="/feed"], a[href^="./feed"], a[href$="feed.json"]');
    if (a) {
      // compute "/<user>/<repo>/" prefix from current path, then append feed.json
      const parts = location.pathname.split('/').filter(Boolean);
      const idx = parts.indexOf('encyclopedia');
      const base = '/' + parts.slice(0, idx >= 0 ? idx : parts.length).join('/') + '/';
      a.setAttribute('href', base + 'feed.json');
    }
  } catch (_) {}

  // 3) If the UI rendered anchors with a data-url, make sure href isn’t empty/#.
  try {
    document.querySelectorAll('a[data-url]').forEach(a => {
      const u = a.getAttribute('data-url');
      const h = a.getAttribute('href') || '';
      if (u && (h === '' || h === '#')) a.setAttribute('href', u);
    });
  } catch (_) {}
})();
