(async () => {
  const bust = 'v=' + Date.now();
  const resp = await fetch('./data.json?' + bust);
  const rows = await resp.json();

  const slugify = s => (s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
  const html = rows.map(it => {
    const title = it.title || '(untitled)';
    const slug  = it.slug || slugify(title);
    const href  = (it.url && /index\.html$/.test(it.url)) ? it.url : `./${slug}/index.html`;
    const tags  = (it.tags||[]).map(t=>`<a data-filter="tag:${t}" href="#">${t}</a>`).join(' ');
    return `
      <article class="entry">
        <h2><a class="entry-link" href="${href}">${title}</a></h2>
        <p class="summary">${it.summary||''}</p>
        <p class="tags">${tags}</p>
      </article>`;
  }).join('');

  document.querySelector('#results').innerHTML = html;

  document.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (!a) return;
    if (a.hasAttribute('data-filter')) {
      e.preventDefault();
      // TODO: your existing filter handling here
    }
    // normal links are NOT prevented
  });
})();
