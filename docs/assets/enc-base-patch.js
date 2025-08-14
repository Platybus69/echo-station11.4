(function () {
  function basePath() {
    // Prefer canonical if present, else derive from current path
    try {
      const c = document.querySelector('link[rel="canonical"]');
      if (c && c.href) return new URL(c.href).pathname.replace(/index\.html?$/,'').replace(/\/?$/,'/') ;
    } catch(e){}
    const p = location.pathname;
    const i = p.indexOf('/encyclopedia/');
    return (i>=0 ? p.slice(0, i+14) : p).replace(/\/?$/,'/') + 'encyclopedia/';
  }
  const ENC = basePath();                  // e.g. /echo-station11.4/encyclopedia/
  const WANT = new Set(['search.json','index.json','tags.json','clusters.json']);
  const orig = window.fetch;
  window.fetch = function(input, init){
    try{
      if (typeof input === 'string') {
        const last = input.split('/').pop();
        if (WANT.has(last)) input = ENC + last;
      }
    }catch(e){}
    return orig.call(this, input, init);
  };
})();
