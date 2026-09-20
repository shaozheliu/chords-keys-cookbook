/* ==========================================================================
   和弦进行模块
   数据：progressions.json（进行定义 + 小节手位），measures.tonic 形如 "F" / "Am"，
        尾部的 m 仅用于标注小三大度，展示符号时需去掉后再拼和弦后缀。
   ========================================================================== */

(async function init() {
  renderNav('progressions');
  renderFooter();

  const root = document.getElementById('app');
  const [progData, chordsData] = await Promise.all([
    fetchJSON('progressions.json'),
    fetchJSON('chords.json'),
  ]);

  if (!progData || !progData.progressions.length) {
    root.innerHTML = renderState('和弦进行数据加载失败，请稍后重试');
    return;
  }

  const progressions = progData.progressions;

  // 支持 #<id> 直达（练习页的「关联进行」入口）
  const wanted = getQueryParam('id') || window.location.hash.replace(/^#\/?/, '');
  const hit = progressions.find(p => p.id === wanted);
  let activeId = hit ? hit.id : progressions[0].id;

  /** 去掉 tonic 尾部的 m（如 "Am" → "A"），得到可拼接后缀的根音 */
  const rootOf = tonic => String(tonic).replace(/m$/, '');

  /** 小节展示符号：根音 + 和弦后缀 */
  function measureSymbol(measure) {
    const chord = (chordsData && findChord(chordsData.chords, measure.chordId)) || null;
    const rootName = rootOf(measure.tonic);
    if (!chord) return rootName;
    const suffix = SUFFIX_SYMBOL[chord.suffix];
    return `${rootName}${suffix === undefined ? chord.suffix : suffix}`;
  }

  /** 小节符号指向的和弦详情链接 */
  function measureHref(measure) {
    if (!chordsData) return null;
    const rootName = rootOf(measure.tonic);
    const tonicSlug = chordsData.tonicSlugMap[rootName];
    const chord = findChord(chordsData.chords, measure.chordId);
    if (!tonicSlug || !chord) return null;
    return `../chords/detail.html#slug=${chordSlug(chord, rootName, chordsData.tonicSlugMap)}`;
  }

  function handLabel(measure) {
    if (!chordsData) return '';
    const chord = findChord(chordsData.chords, measure.chordId);
    const hand = chord && chord.handShapes.find(h => h.id === measure.handShapeId);
    return hand ? hand.label.split('·')[0].trim() : '';
  }

  function refresh() {
    const active = progressions.find(p => p.id === activeId) || progressions[0];

    const cards = progressions.map(prog => `
      <button type="button" class="text-card ${prog.id === active.id ? 'active' : ''}" data-prog="${prog.id}">
        <div class="text-card-head">
          <strong>${escapeHtml(prog.name)}</strong>
          <span class="chip">${escapeHtml(prog.key)}</span>
        </div>
        <p>${escapeHtml(prog.description)}</p>
        <div class="symbol-line">
          ${prog.measures.map(m => escapeHtml(measureSymbol(m))).join(' <em>→</em> ')}
        </div>
      </button>
    `).join('');

    const measures = active.measures.map(m => {
      const href = measureHref(m);
      const symbol = escapeHtml(measureSymbol(m));
      const hand = handLabel(m);
      return `
        <div class="measure">
          <div class="measure-head">
            <span class="measure-degree">${escapeHtml(m.degree)}</span>
            <span class="measure-symbol">${href ? `<a href="${href}">${symbol}</a>` : symbol}</span>
          </div>
          <dl>
            <div><dt>左手</dt><dd>${escapeHtml(m.leftHand)}</dd></div>
            <div><dt>右手</dt><dd>${escapeHtml(m.rightHand)}</dd></div>
            ${hand ? `<div><dt>手型</dt><dd>${escapeHtml(hand)}</dd></div>` : ''}
          </dl>
        </div>
      `;
    }).join('');

    const handFigure = active.folder ? `
      <section class="panel">
        <h2 class="block-title">进行手位图</h2>
        <figure class="figure">
          <img src="${svgProgressionPath(active.folder, rootOf(active.measures[0].tonic))}"
               alt="${escapeHtml(`${active.name} 手位图`)}" loading="lazy"
               onerror="imgFallback(this, '手位图待生成')">
          <figcaption>以 ${escapeHtml(active.key)} 为例，五个八度内的完整手位走向。</figcaption>
        </figure>
      </section>
    ` : `
      <section class="panel">
        <h2 class="block-title">进行手位图</h2>
        <div class="placeholder">手位图待生成</div>
      </section>
    `;

    const rhythmFigure = active.rhythmSvg ? `
      <section class="panel">
        <h2 class="block-title">节奏型</h2>
        <figure class="figure">
          <img src="${svgAssetPath(active.rhythmSvg)}" alt="${escapeHtml(`${active.name} 节奏型`)}" loading="lazy"
               onerror="imgFallback(this, '节奏型待生成')">
          <figcaption>把这条进行套进节奏型里，先慢速对齐，再逐步提速。</figcaption>
        </figure>
      </section>
    ` : `
      <section class="panel">
        <h2 class="block-title">节奏型</h2>
        <div class="placeholder">节奏型待生成</div>
      </section>
    `;

    const otherChips = progressions
      .filter(p => p.id !== active.id)
      .map(p => `<a class="chip" href="#${p.id}">${escapeHtml(p.name)}</a>`)
      .join('');

    root.innerHTML = `
      <p class="crumb">进行</p>
      <h1>和弦进行</h1>
      <p class="lead">四条最常用的弹唱进行，从下属到属、从挂留到解决。每条进行都拆到小节手位，可以直接照着练。</p>

      <div class="card-grid wide" style="margin-bottom:40px">${cards}</div>

      <div class="section-head">
        <h2>${escapeHtml(active.name)}</h2>
        <span class="crumb" style="margin:0">${escapeHtml(active.key)} · 共 ${active.measures.length} 小节</span>
      </div>

      <article class="detail-layout">
        <div class="detail-main">
          <section>
            <h2 class="block-title">进行概览</h2>
            <div class="info">
              <div class="info-row"><dt>调性</dt><dd>${escapeHtml(active.key)}</dd></div>
              <div class="info-row"><dt>级数序列</dt><dd>${active.measures.map(m => escapeHtml(m.degree)).join(' → ')}</dd></div>
              <div class="info-row"><dt>和弦序列</dt><dd>${active.measures.map(m => escapeHtml(measureSymbol(m))).join(' → ')}</dd></div>
              <div class="info-row"><dt>进行说明</dt><dd>${escapeHtml(active.description)}</dd></div>
            </div>
          </section>

          <section>
            <h2 class="block-title">小节拆解</h2>
            <div class="measure-grid">${measures}</div>
          </section>

          ${handFigure}
          ${rhythmFigure}
        </div>

        <aside class="related">
          <h2>练习提示</h2>
          <p class="note" style="margin-bottom:0">
            先分手再合手：左手固定根音—五音框架，右手只走上方三音，对齐后再加节奏。
          </p>
          <h2 style="margin-top:24px">其它进行</h2>
          <div class="chips tight">${otherChips}</div>
        </aside>
      </article>
    `;

    root.querySelectorAll('[data-prog]').forEach(btn => {
      btn.addEventListener('click', () => {
        activeId = btn.dataset.prog;
        history.replaceState(null, '', `#${activeId}`);
        refresh();
        root.querySelector('.section-head')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  // 通过 hash 切换进行（浏览器前进/后退）
  window.addEventListener('hashchange', () => {
    const next = window.location.hash.replace(/^#\/?/, '');
    if (next && next !== activeId && progressions.some(p => p.id === next)) {
      activeId = next;
      refresh();
    }
  });

  refresh();
})();
