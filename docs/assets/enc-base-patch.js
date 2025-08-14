(function () {
  // Determine /<repo>/encyclopedia/ … even if deployed under a subpath
  const canon = document.querySelector('link[rel="canonical"]');
  const encBase = (canon ? new URL(canon.href).pathname : location.pathname)
    .replace(/index\.html?$/i,'').replace(/\/?$/,'/'); // e.g. /echo-station11.4/encyclopedia/
  const toAbs = (rel) => new URL(rel, location.origin + encBase).toString();

  const targets = new Set(['search.json','index.json','tags.json','clusters.json']);
  const origFetch = window.fetch;
  window.fetch = function (input, init) {
    try {
      if (typeof input === 'string') {
        const last = input.split('/').pop();
        if (targets.has(last)) {
          // Force these to resolve under the encyclopedia base
          input = toAbs(last);
        }
      }
    } catch (e) { /* no-op */ }
    return origFetch.call(this, input, init);
  };
})();
