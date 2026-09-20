/* ==========================================================================
   和弦模块 — 三级路由：
     chords/index.html                     和弦大全
     chords/family.html#type=triads        分类列表
     chords/detail.html#slug=c-major       和弦详情
   ========================================================================== */

const CHORDS_INDEX_PREVIEW = 6; // 大全页每个分类预览的和弦数量

(async function init() {
  renderNav('chords');
  renderFooter();

  const root = document.getElementById('app');
  const data = await fetchJSON('chords.json');
  if (!data) {
    root.innerHTML = renderState('和弦数据加载失败，请稍后重试');
    return;
  }

  const slug = getQueryParam('slug');
  const type = getQueryParam('type');

  if (slug) renderDetail(root, data, slug);
  else if (type) renderFamily(root, data, type);
  else renderOverview(root, data);
})();

/* ---------- 分类下的和弦总数 ---------- */
function familyChordCount(data, family) {
  return family.kinds.length * data.tonics.length;
}

/* ---------- 一体化：大全页 ---------- */
function renderOverview(root, data) {
  const chips = data.families.map((family, i) => `
    <a class="chip ${i === 0 ? 'active' : ''}" href="#${family.id}">${family.title} (${familyChordCount(data, family)})</a>
  `).join('');

  const sections = data.families.map(family => {
    // 每个子类型取前若干个调，凑满 6 张预览卡
    const perKind = Math.ceil(CHORDS_INDEX_PREVIEW / family.kinds.length);
    const cards = [];
    family.kinds.forEach(kindId => {
      const chord = findChord(data.chords, kindId);
      if (!chord) return;
      data.tonics.slice(0, perKind).forEach(tonic => cards.push(chordCardHtml(data, chord, tonic)));
    });

    return `
      <section class="section" id="${family.id}">
        <div class="section-head">
          <h2>${escapeHtml(family.title)}</h2>
          <a href="family.html#type=${family.id}">查看全部 →</a>
        </div>
        <div class="card-grid">${cards.slice(0, CHORDS_INDEX_PREVIEW).join('')}</div>
      </section>
    `;
  }).join('');

  root.innerHTML = `
    <p class="crumb">和弦</p>
    <h1>钢琴和弦大全</h1>
    <p class="lead">和弦是钢琴即兴的基础。每个和弦都配有键盘图、构成说明和练习建议。</p>
    <div class="chips">${chips}</div>
    ${sections}
  `;
}

/* ---------- 分类列表页 ---------- */
function renderFamily(root, data, type) {
  const family = data.families.find(f => f.id === type);
  if (!family) {
    root.innerHTML = renderState('未找到该和弦分类');
    return;
  }

  const kinds = family.kinds.map(id => findChord(data.chords, id)).filter(Boolean);

  const ownChips = kinds.map((chord, i) => `
    <a class="chip ${i === 0 ? 'active' : ''}" href="#${chord.id}">${escapeHtml(chord.typeName)} (${data.tonics.length})</a>
  `).join('');

  const otherChips = data.families
    .filter(f => f.id !== family.id)
    .map(f => `<a class="chip ghost" href="family.html#type=${f.id}">${escapeHtml(f.title)} (${familyChordCount(data, f)})</a>`)
    .join('');

  const sections = kinds.map(chord => `
    <section class="section" id="${chord.id}">
      <div class="section-head">
        <h2>${escapeHtml(chord.typeName)}</h2>
        <span></span>
      </div>
      <div class="card-grid">
        ${data.tonics.map(tonic => chordCardHtml(data, chord, tonic)).join('')}
      </div>
    </section>
  `).join('');

  root.innerHTML = `
    <p class="crumb"><a href="./">和弦</a> / ${escapeHtml(family.title)}</p>
    <h1>${escapeHtml(family.title)}</h1>
    <p class="lead">${escapeHtml(family.lead)}</p>
    <div class="chips">${ownChips}${otherChips}</div>
    ${sections}
  `;
}

/* ---------- 详情页 ---------- */
function renderDetail(root, data, slug) {
  const hit = buildSlugIndex(data)[slug];
  if (!hit) {
    root.innerHTML = renderState('未找到该和弦');
    return;
  }

  const { chord, tonic } = hit;
  const symbol = chordSymbol(chord, tonic);
  const slugKey = chordSlug(chord, tonic, data.tonicSlugMap);
  const family = data.families.find(f => f.id === chord.familyId);

  const handBlocks = chord.handShapes.map(hand => {
    const noteRows = (hand.notes || []).map(note => `
      <tr>
        <td>${note.hand === 'L' ? '左手' : '右手'}</td>
        <td>${note.finger} 指</td>
        <td>${escapeHtml(note.degree)}</td>
        <td>${note.offset > 0 ? `+${note.offset}` : note.offset}</td>
      </tr>
    `).join('');

    const notesTable = noteRows ? `
      <table class="table" style="margin-top:16px">
        <thead>
          <tr><th>手</th><th>指法</th><th>声部</th><th>八度位移</th></tr>
        </thead>
        <tbody>${noteRows}</tbody>
      </table>
    ` : '';

    return `
      <div class="hand-block">
        <h3>${escapeHtml(hand.label)}</h3>
        <p>${escapeHtml(hand.description)}</p>
        <img src="${svgHandShapePath(chord.folder, tonic, hand.id)}"
             alt="${escapeHtml(`${symbol} ${hand.label}`)}" width="640" height="360" loading="lazy"
             onerror="imgFallback(this, '手位图待生成')">
        ${notesTable}
      </div>
    `;
  }).join('');

  const tonicChips = data.tonics.map(t => {
    const tSlug = chordSlug(chord, t, data.tonicSlugMap);
    return `<a class="chip ${t === tonic ? 'active' : ''}" href="detail.html#slug=${tSlug}">${escapeHtml(t)}</a>`;
  }).join('');

  const siblingChips = data.chords
    .filter(c => c.familyId === chord.familyId)
    .map(c => `<a class="chip ${c.id === chord.id ? 'active' : ''}" href="detail.html#slug=${chordSlug(c, tonic, data.tonicSlugMap)}">${escapeHtml(c.typeName)}</a>`)
    .join('');

  root.innerHTML = `
    <p class="crumb">
      <a href="./">和弦</a> /
      ${family ? `<a href="family.html#type=${family.id}">${escapeHtml(family.title)}</a> /` : ''}
      ${escapeHtml(tonic)}
    </p>
    <article class="detail-layout">
      <div class="detail-main">
        <div class="hero-card">
          <div>
            <h1 class="hero-symbol">${escapeHtml(symbol)}</h1>
            <p class="hero-name">${escapeHtml(chordCName(chord, tonic, data.tonicCn))}</p>
          </div>
          <img src="${svgCardKeyPath(slugKey, 'hero')}" alt="${escapeHtml(`${symbol} 键盘图`)}"
               width="360" height="202" onerror="imgFallback(this, '键盘图待生成')">
        </div>

        <section>
          <h2 class="block-title">和弦信息</h2>
          <div class="info">
            <div class="info-row"><dt>根音</dt><dd>${escapeHtml(tonic)}</dd></div>
            <div class="info-row"><dt>和弦类型</dt><dd>${escapeHtml(chord.typeName)}</dd></div>
            <div class="info-row"><dt>组成音</dt><dd>${escapeHtml(chordNotes(chord, tonic, data.tonicPc))}</dd></div>
            <div class="info-row"><dt>音程关系</dt><dd>${escapeHtml(chord.formula)}</dd></div>
            <div class="info-row"><dt>音色特征</dt><dd>${escapeHtml(chord.tone)}</dd></div>
            <div class="info-row"><dt>适用风格</dt><dd>${escapeHtml(chord.style)}</dd></div>
          </div>
        </section>

        <section class="practice">
          <h2 class="block-title">练习建议</h2>
          ${handBlocks}
        </section>

        <section class="panel">
          <h2 class="block-title">切换到其它调</h2>
          <div class="chips tight">${tonicChips}</div>
        </section>
      </div>

      <aside class="related">
        <h2>和弦家族</h2>
        <div class="chips tight">${siblingChips}</div>
        <h2 style="margin-top:24px">相关歌曲</h2>
        <div class="placeholder">敬请期待</div>
      </aside>
    </article>
  `;
}

/* ---------- 辅助 ---------- */

/** 建立 slug → {chord, tonic} 索引（9 类型 × 12 调） */
function buildSlugIndex(data) {
  const index = {};
  data.chords.forEach(chord => {
    data.tonics.forEach(tonic => {
      index[chordSlug(chord, tonic, data.tonicSlugMap)] = { chord, tonic };
    });
  });
  return index;
}

function chordCardHtml(data, chord, tonic) {
  const slug = chordSlug(chord, tonic, data.tonicSlugMap);
  return renderChordCard({
    href: `detail.html#slug=${slug}`,
    symbol: chordSymbol(chord, tonic),
    label: chordCName(chord, tonic, data.tonicCn),
    slug,
    alt: `${chordSymbol(chord, tonic)} 键盘图`,
  });
}
