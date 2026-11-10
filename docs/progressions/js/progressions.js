/* ==========================================================================
   和弦进行模块
   列表页（L5）+ 详情页（L6），对齐 Figma：
   - 列表：代号 + 标签 + 级数（roman）+ 情绪
   - 详情：介绍 / 代表曲目 / 情绪 / 好听组合（Practice Kit + 紧凑卡）
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

  const progressions = progressionCatalog(progData);

  if (!progData || !progressions.length) {
    root.innerHTML = renderState('和弦进行数据加载失败，请稍后重试');
    return;
  }

  let detailPracticeKey = 'C';

  function moodLine(prog) {
    return (prog.moodTags || []).join(' · ');
  }

  function renderComboCard(combo, compact) {
    const tagClass = combo.tagTone === 'accent' ? 'chip accent' : 'chip';
    const symbols = (combo.symbols || []).map(s =>
      `<span class="combo-sym">${escapeHtml(s)}</span>`
    ).join('<span class="combo-arrow">→</span>');
    const degrees = (combo.degrees || []).map(escapeHtml).join(' · ');
    const featured = combo.featured && !compact;
    const kit = featured
      ? `<div class="combo-expand">${renderPracticeKit(
        detailProgRef,
        combo,
        chordsData,
        {
          showHead: false,
          tonicLabel: `${detailPracticeKey} 大调`,
          practiceKey: detailPracticeKey,
          showProgressionStrip: false,
        }
      )}</div>`
      : '';

    return `
      <article class="combo-card ${featured ? 'is-featured' : 'is-compact'}" data-combo="${escapeHtml(combo.id)}">
        <div class="combo-head">
          <strong>${escapeHtml(combo.title)}</strong>
          <span class="${tagClass}">${escapeHtml(combo.tag || '')}</span>
        </div>
        <div class="combo-flow">${symbols}</div>
        <div class="combo-degrees">${degrees}</div>
        <p class="note">${escapeHtml(combo.note || '')}</p>
        <div class="combo-mood">情绪：${escapeHtml(combo.mood || '—')}</div>
        ${kit}
        ${featured ? '<p class="combo-foot">整条组合可反复练习。</p>' : ''}
      </article>
    `;
  }

  let detailProgRef = null;

  function renderList() {
    const cards = progressions.map(prog => {
      const title = prog.code || prog.name;
      return `
        <a class="prog-card" href="detail.html#id=${encodeURIComponent(prog.id)}">
          <div class="prog-card-top">
            <strong>${escapeHtml(title)}</strong>
            <span class="chip">${escapeHtml(prog.tag || prog.key)}</span>
          </div>
          <div class="prog-roman">${escapeHtml(prog.roman || '')}</div>
          <div class="prog-mood">${escapeHtml(moodLine(prog) || '—')}</div>
        </a>
      `;
    }).join('');

    root.innerHTML = `
      <p class="crumb"><a href="../">首页</a> / 进行</p>
      <h1>和弦进行大全</h1>
      <p class="lead">每张卡片展示：进行代号 · 标签 · 级数骨架 · 情绪。点进二级页可看介绍、代表曲目与好听组合（节奏型 + 固定指法）。</p>

      <div class="section-head">
        <h2>热门进行</h2>
        <span class="crumb" style="margin:0">共 ${progressions.length} 条</span>
      </div>
      <div class="prog-grid">${cards}</div>
    `;
  }

  function renderDetail(prog) {
    detailProgRef = prog;

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

    const combos = (prog.combos || []).map(c => renderComboCard(c)).join('');

    const basicLine = (prog.basicChords || []).join(' → ');

    root.innerHTML = `
      <p class="crumb"><a href="../">首页</a> / <a href="./">进行</a> / ${escapeHtml(prog.name.replace(/\s*进行$/, '') || prog.id)}</p>
      <div class="detail-hero">
        <div class="detail-hero-title">
          <h1>${escapeHtml(prog.name)}</h1>
          <span class="chip">${escapeHtml(prog.tag || '')}</span>
        </div>
        <p class="detail-sub">${escapeHtml(prog.roman || '')} · 基本和弦 ${basicLine}</p>
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
          <div class="info-row"><dt>说明</dt><dd>${escapeHtml(prog.description)}</dd></div>
        </div>
      </section>

      <section class="section">
        <h2 class="block-title">代表曲目</h2>
        <div class="song-list">${songs}</div>
      </section>

      <section class="section">
        <h2 class="block-title">情绪色彩分析</h2>
        <div class="chips" style="margin-bottom:14px">${moodTags || '<span class="chip ghost">待补充</span>'}</div>
        <p class="note" style="margin:0">${escapeHtml(prog.moodAnalysis || '待补充')}</p>
      </section>

      <section class="section" data-combo-section>
        <div class="section-head">
          <h2>好听组合</h2>
          <span class="crumb" style="margin:0">每张卡 = 一整条组合</span>
        </div>
        <p class="note" style="margin-bottom:12px">主推组合与每日练习「进行练习」一致：节奏型 + 按拍指法小图（不含四拍手位总览）。</p>
        ${renderKeySwitcherCompact(detailPracticeKey, chordsData.tonics || ['F', 'C', 'G'])}
        <div class="combo-list">${combos}</div>
      </section>

      <div class="chips" style="margin-top:8px">
        <a class="chip ghost" href="./">← 返回进行列表</a>
        <a class="chip" href="../practice/">打开每日练习 · 进行态</a>
      </div>
    `;

    bindPracticeKeySwitcher(root, key => {
      detailPracticeKey = key;
      renderDetail(prog);
    });
  }

  if (isDetail) {
    function show() {
      const id = getQueryParam('id') || window.location.hash.replace(/^#\/?/, '').replace(/^id=/, '');
      const prog = progressions.find(p => p.id === id) || progressions[0];
      if (!prog) {
        root.innerHTML = renderState('未找到该进行');
        return;
      }
      renderDetail(prog);
      document.title = `${prog.name} — 钢琴即兴`;
    }

    window.addEventListener('hashchange', show);
    show();
  } else {
    renderList();
  }
})();
