(function(){
  // Root so we can fetch /encyclopedia/search.json from any depth
  const p = location.pathname;
  const i = p.indexOf('/encyclopedia/');
  const ENC_ROOT = i >= 0 ? p.slice(0, i) : '';
  const SEARCH_JSON = ENC_ROOT + '/encyclopedia/search.json';

  const params = new URLSearchParams(location.search);
  const qParam = params.get('q') || '';

  const input = document.querySelector('#search, input[type="search"], [data-search-input]');
  const box = document.getElementById('search-results');

  if (input) {
    input.value = qParam;
    window.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== input) { e.preventDefault(); input.focus(); input.select(); }
    });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { input.value=''; render([]); history.replaceState({},'',location.pathname); }
    });
  }

  fetch(SEARCH_JSON).then(r=>r.json()).then(index=>{
    function tokenize(q){
      const toks = (q||'').trim().split(/\s+/).filter(Boolean);
      const filters = { tag:[], cluster:[] }, terms=[];
      toks.forEach(t=>{
        const m=t.match(/^(tag|cluster):(.+)$/i);
        if(m) filters[m[1].toLowerCase()].push(m[2].toLowerCase());
        else terms.push(t.toLowerCase());
      });
      return {terms,filters};
    }
    function match(it, terms, filters){
      const tags=(it.tags||[]).map(x=>(''+x).toLowerCase());
      const cluster=(it.cluster||'').toLowerCase();
      const hay=(it.title+' '+(it.summary||'')+' '+cluster+' '+tags.join(' ')).toLowerCase();
      if (filters.tag.length && !filters.tag.every(t=>tags.includes(t))) return false;
      if (filters.cluster.length && !filters.cluster.includes(cluster)) return false;
      return terms.every(t=>hay.includes(t));
    }
    function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
    function highlight(text,q){ if(!q) return text||''; try { return (text||'').replace(new RegExp(escRe(q),'ig'), m=>`<mark>${m}</mark>`);} catch { return text||''; } }
    function render(list){
      if(!box) return;
      box.innerHTML='';
      list.forEach(it=>{
        const card=document.createElement('div'); card.className='card';
        const tagsHtml=(it.tags||[]).map(t=>`<span class="badge">#${t}</span>`).join(' ');
        card.innerHTML = `
          <div><a href="./${it.slug}/index.html"><strong>${highlight(it.title, input?input.value:'')}</strong></a></div>
          <div class="small">${highlight(it.summary||'', input?input.value:'')}</div>
          <div class="small">${it.cluster?`<span class="badge">${it.cluster}</span>`:''} ${tagsHtml}</div>
        `;
        box.appendChild(card);
      });
    }
    function run(q){ const {terms,filters}=tokenize(q); render(index.filter(it=>match(it,terms,filters)).slice(0,200)); }
    run(qParam);
    if (input) input.addEventListener('input', e=>run(e.target.value));
  }).catch(()=>{ /* ok if search not on page */ });
})();
