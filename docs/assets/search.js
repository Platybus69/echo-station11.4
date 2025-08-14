(function(){
  // Detect project base: "/" for user sites, "/repo/" for project pages
  const BASE = (function(){
    const segs = location.pathname.split('/').filter(Boolean);
    return (segs.length && segs[0] !== 'encyclopedia') ? `/${segs[0]}/` : '/';
  })();

  async function getJSON(rel){
    const url = rel.startsWith('http') ? rel : `${BASE}${rel.replace(/^\//,'')}`;
    const res = await fetch(url, {cache: 'no-store'});
    if(!res.ok) throw new Error(`Fetch ${url} -> ${res.status}`);
    return res.json();
  }

  // Wire up search box
  const input = document.querySelector('#search input, input[type=search], input[name=q]');
  const results = document.querySelector('#search-results');
  const params = new URLSearchParams(location.search);
  const q = params.get('q') || '';

  if (input) {
    input.value = q;
    document.addEventListener('keydown', (e)=>{ if(e.key === '/') { e.preventDefault(); input.focus(); }});
    input.addEventListener('keydown', (e)=>{ if(e.key === 'Escape'){ input.value=''; location.search=''; }});
  }

  // Highlight utility
  function highlight(el, term){
    if(!el || !term) return;
    const rx = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`,'gi');
    el.innerHTML = el.innerHTML.replace(rx, '<mark>$1</mark>');
  }

  // 1) In-page highlight on entry pages
  if (q && document.body.classList.contains('entry')) {
    document.querySelectorAll('main, article').forEach(el=>highlight(el,q));
  }

  // 2) Index search: load and render hits
  if (results) {
    getJSON('encyclopedia/search.json').then(data=>{
      const term = q.trim().toLowerCase();
      const f = (s)=> (s||'').toLowerCase();
      const hits = (data.items||[]).filter(it=>{
        const hay = f(it.title)+' '+f(it.summary)+' '+(it.tags||[]).map(f).join(' ');
        return term ? hay.includes(term) : true;
      });
      results.innerHTML = hits.map(it=>{
        const href = `${BASE}${(it.url||'').replace(/^\.\//,'')}`;
        return `<li><a href="${href}">${it.title||href}</a><p>${it.summary||''}</p></li>`;
      }).join('') || '<li>No results</li>';
    }).catch(err=>{
      console.error(err);
      results.innerHTML = '<li>Search unavailable</li>';
    });
  }
})();
