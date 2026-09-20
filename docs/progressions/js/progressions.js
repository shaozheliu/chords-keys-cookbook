/* ==========================================================================
   和弦进行模块
   列表页（L5）+ 详情页（L6），对齐 Figma：
   - 列表：罗马数字 + 标签 + 情绪
   - 详情：介绍 / 代表曲目 / 情绪 / 好听组合
   ========================================================================== */

(async function init() {
  renderNav('progressions');
  renderFooter();

  const root = document.getElementById('app');
  const isDetail = document.body.dataset.page === 'detail';

  const [progData, chordsData] = await Promise.all([
    fetchJSON('progressions.json'),
    fetchJSON('chords.json'),
  ]);

  if (!progData || !progData.progressions.length) {
    root.innerHTML = renderState('和弦进行数据加载失败，请稍后重试');
    return;
  }

  const progressions = progData.progressions;

  /** 去掉 tonic 尾部的 m（如 "Am" → "A"） */
  const rootOf = tonic => String(tonic).replace(/m$/, '');

  function measureSymbol(measure) {
    const chord = (chordsData && findChord(chordsData.chords, measure.chordId)) || null;
    const tonic = String(measure.tonic);
    const rootName = rootOf(tonic);
    if (!chord) return tonic;
    const suffix = SUFFIX_SYMBOL[chord.suffix];
    const s = suffix === undefined ? chord.suffix : suffix;
    // tonic 形如 "Am"：小三保留 Am；加九写成 Amadd9；小七写成 Am7
    if (/m$/.test(tonic)) {
      if (chord.suffix === 'minor') return tonic;
      if (chord.suffix === 'm7') return `${rootName}m7`;
      if (chord.suffix === 'add9') return `${tonic}add9`;
    }
    return `${rootName}${s}`;
  }

  function measureHref(measure) {
    if (!chordsData) return null;
    const rootName = rootOf(measure.tonic);
    const chord = findChord(chordsData.chords, measure.chordId);
    if (!chordsData.tonicSlugMap[rootName] || !chord) return null;
    return `../chords/detail.html#slug=${chordSlug(chord, rootName, chordsData.tonicSlugMap)}`;
  }

  function handLabel(measure) {
    if (!chordsData) return '';
    const chord = findChord(chordsData.chords, measure.chordId);
    const hand = chord && chord.handShapes.find(h => h.id === measure.handShapeId);
    return hand ? hand.label.split('·')[0].trim() : '';
  }

  function moodLine(prog) {
    return (prog.moodTags || []).join(' · ');
  }

  function renderList() {
    const cards = progressions.map(prog => {
      const seq = (prog.listChords || []).map(escapeHtml).join(' → ');
      return `
        <a class="prog-card" href="detail.html#id=${encodeURIComponent(prog.id)}">
          <div class="prog-card-top">
            <strong>${escapeHtml(prog.name)}</strong>
            <span class="chip">${escapeHtml(prog.tag || prog.key)}</span>
          </div>
          <div class="prog-roman">${escapeHtml(prog.roman || '')}</div>
          <div class="prog-seq">${seq}</div>
          <p class="prog-desc">${escapeHtml(prog.description)}</p>
          <div class="prog-mood">情绪：${escapeHtml(moodLine(prog) || '—')}</div>
        </a>
      `;
    }).join('');

    root.innerHTML = `
      <p class="crumb"><a href="../">首页</a> / 进行</p>
      <h1>和弦进行大全</h1>
      <p class="lead">每张卡片是一条可复用的和弦组合。点进二级页可查看介绍、代表曲目、情绪分析，以及支持 sus2 / sus4 / add9 等变体的小节拆解。</p>

      <div class="section-head">
        <h2>热门进行</h2>
        <span class="crumb" style="margin:0">共 ${progressions.length} 条</span>
      </div>
      <div class="prog-grid">${cards}</div>
    `;
  }

  function renderDetail(prog) {
    const basicCards = (prog.basicChords || []).map((sym, i) => `
      <div class="basic-chord">
        <span class="basic-degree">${escapeHtml((prog.basicDegrees || [])[i] || '')}</span>
        <strong>${escapeHtml(sym)}</strong>
      </div>
    `).join('');

    const songs = (prog.songs || []).map((s, i) => `
      <div class="song-row">
        <span class="song-index">${i + 1}</span>
        <div>
          <strong>${escapeHtml(s.title)} · ${escapeHtml(s.artist)}</strong>
          <p>${escapeHtml(s.note || '')}</p>
        </div>
      </div>
    `).join('') || `<div class="placeholder">曲目示例待补充</div>`;

    const moodTags = (prog.moodTags || []).map(t =>
      `<span class="chip active">${escapeHtml(t)}</span>`
    ).join('');

    const combos = (prog.combos || []).map(combo => {
      const tagClass = combo.tagTone === 'accent' ? 'chip accent' : 'chip';
      const symbols = (combo.symbols || []).map(s =>
        `<span class="combo-sym">${escapeHtml(s)}</span>`
      ).join('<span class="combo-arrow">→</span>');
      const degrees = (combo.degrees || []).map(escapeHtml).join(' · ');

      const measures = (combo.measures || []).map(m => {
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

      return `
        <article class="combo-card" data-combo="${escapeHtml(combo.id)}">
          <div class="combo-head">
            <strong>${escapeHtml(combo.title)}</strong>
            <span class="${tagClass}">${escapeHtml(combo.tag || '')}</span>
          </div>
          <div class="combo-flow">${symbols}</div>
          <div class="combo-degrees">${degrees}</div>
          <p class="note">${escapeHtml(combo.note || '')}</p>
          <div class="combo-mood">情绪：${escapeHtml(combo.mood || '')}</div>
          <div class="measure-grid" style="margin-top:16px">${measures}</div>
        </article>
      `;
    }).join('');

    const firstTonic = prog.basicChords && prog.basicChords[0]
      ? rootOf(prog.basicChords[0])
      : 'C';

    const handFigure = prog.folder ? `
      <section class="panel">
        <h2 class="block-title">进行手位图</h2>
        <figure class="figure">
          <img src="${svgProgressionPath(prog.folder, firstTonic)}"
               alt="${escapeHtml(`${prog.name} 手位图`)}" loading="lazy"
               onerror="imgFallback(this, '手位图待生成')">
          <figcaption>以 ${escapeHtml(prog.key)} 为例。</figcaption>
        </figure>
      </section>
    ` : '';

    const rhythmFigure = prog.rhythmSvg ? `
      <section class="panel">
        <h2 class="block-title">节奏型</h2>
        <figure class="figure">
          <img src="${svgAssetPath(prog.rhythmSvg)}" alt="${escapeHtml(`${prog.name} 节奏型`)}" loading="lazy"
               onerror="imgFallback(this, '节奏型待生成')">
        </figure>
      </section>
    ` : '';

    root.innerHTML = `
      <p class="crumb"><a href="../">首页</a> / <a href="./">进行</a> / ${escapeHtml(prog.name.replace(/\s*进行$/, '') || prog.id)}</p>
      <div class="detail-hero">
        <div class="detail-hero-title">
          <h1>${escapeHtml(prog.name)}</h1>
          <span class="chip">${escapeHtml(prog.tag || '')}</span>
        </div>
        <p class="detail-sub">${escapeHtml(prog.roman || '')} · 基本和弦 ${(prog.basicChords || []).join(' → ')}</p>
        <p class="lead" style="margin-bottom:0">介绍层只写基本和弦；色彩变体（sus / add9 等）收在下方「好听组合」。</p>
      </div>

      <section class="section">
        <h2 class="block-title">和弦介绍</h2>
        <p class="note" style="margin-bottom:20px">${escapeHtml(prog.intro || prog.description)}</p>
        <div class="basic-grid">${basicCards}</div>
        <div class="info" style="margin-top:20px">
          <div class="info-row"><dt>调性</dt><dd>${escapeHtml(prog.key)}</dd></div>
          <div class="info-row"><dt>罗马数字</dt><dd>${escapeHtml(prog.roman || '')}</dd></div>
          <div class="info-row"><dt>基本和弦</dt><dd>${(prog.basicChords || []).map(escapeHtml).join(' → ')}</dd></div>
          <div class="info-row"><dt>说明</dt><dd>${escapeHtml(prog.description)}（基本三和弦骨架）</dd></div>
        </div>
      </section>

      <section class="section">
        <h2 class="block-title">代表曲目</h2>
        <div class="song-list">${songs}</div>
      </section>

      <section class="section">
        <h2 class="block-title">情绪色彩分析</h2>
        <div class="chips" style="margin-bottom:14px">${moodTags}</div>
        <p class="note" style="margin:0">${escapeHtml(prog.moodAnalysis || '')}</p>
      </section>

      <section class="section">
        <div class="section-head">
          <h2>好听组合</h2>
          <span class="crumb" style="margin:0">每张卡 = 一整条组合</span>
        </div>
        <p class="note" style="margin-bottom:20px">点开任一组合，可对照小节手位反复练习。</p>
        <div class="combo-list">${combos}</div>
      </section>

      ${handFigure}
      ${rhythmFigure}

      <div class="chips" style="margin-top:8px">
        <a class="chip ghost" href="./">← 返回进行列表</a>
      </div>
    `;
  }

  if (isDetail) {
    const wanted = getQueryParam('id') || window.location.hash.replace(/^#\/?/, '').replace(/^id=/, '');
    const hit = progressions.find(p => p.id === wanted) || progressions[0];

    function show() {
      const id = getQueryParam('id') || window.location.hash.replace(/^#\/?/, '').replace(/^id=/, '');
      const prog = progressions.find(p => p.id === id) || progressions[0];
      renderDetail(prog);
      document.title = `${prog.name} — 钢琴即兴`;
    }

    window.addEventListener('hashchange', show);
    show();
  } else {
    renderList();
  }
})();
