/* ==========================================================================
   每日练习模块
   数据：practice.json（周维度轮动 + 练习步骤），通过 chordId / progressionId
        引用 chords.json 与 progressions.json 中的定义。
   ========================================================================== */

(async function init() {
  renderNav('practice');
  renderFooter();

  const root = document.getElementById('app');
  const [practice, chordsData, progData] = await Promise.all([
    fetchJSON('practice.json'),
    fetchJSON('chords.json'),
    fetchJSON('progressions.json'),
  ]);

  if (!practice || !chordsData) {
    root.innerHTML = renderState('练习数据加载失败，请稍后重试');
    return;
  }

  let dayIndex = 0;
  let practiceIndex = 0;

  const tonicsOf = group => (group.tonics === 'all' ? chordsData.tonics : group.tonics);

  function refresh() {
    const group = practice.weeklyGroups[dayIndex];
    const tonics = tonicsOf(group);
    const current = practice.practices[practiceIndex];
    const chord = findChord(chordsData.chords, current.chordId);
    const progression = (progData && progData.progressions || [])
      .find(p => p.id === current.progressionId);

    const dayChips = practice.weeklyGroups.map((g, i) => `
      <button type="button" class="chip ${i === dayIndex ? 'active' : ''}" data-day="${i}">${escapeHtml(g.day)}</button>
    `).join('');

    const practiceChips = practice.practices.map((p, i) => {
      const c = findChord(chordsData.chords, p.chordId);
      return `<button type="button" class="chip ${i === practiceIndex ? 'active' : ''}" data-practice="${i}">
        ${escapeHtml(c ? c.typeName : p.chordId)}
      </button>`;
    }).join('');

    const tonicChips = tonics.map(tonic => {
      const slug = chordSlug(chord, tonic, chordsData.tonicSlugMap);
      return `<a class="chip" href="../chords/detail.html#slug=${slug}">${escapeHtml(tonic)}</a>`;
    }).join('');

    const stepRows = current.steps.map((step, i) => `
      <div class="acc-item ${i === 0 ? 'open' : ''}" data-acc-item>
        <button type="button" class="acc-head" data-acc-head aria-expanded="${i === 0 ? 'true' : 'false'}">
          <span class="acc-index">${i + 1}</span>
          <span class="acc-name">${escapeHtml(step.name)}</span>
          <span class="acc-phase">${escapeHtml(step.phase)}</span>
          <span class="acc-arrow">▾</span>
        </button>
        <div class="acc-body">
          ${escapeHtml(step.detail)}
          <div class="mini-chips" style="margin-top:10px">
            <span class="chip">${escapeHtml(step.type)}</span>
          </div>
        </div>
      </div>
    `).join('');

    const chordReference = chord ? `
      <div class="info">
        <div class="info-row"><dt>和弦</dt><dd>${escapeHtml(chordSymbol(chord, 'C'))}</dd></div>
        <div class="info-row"><dt>音程关系</dt><dd>${escapeHtml(chord.formula)}</dd></div>
        <div class="info-row"><dt>音色特征</dt><dd>${escapeHtml(chord.tone)}</dd></div>
        <div class="info-row"><dt>适用风格</dt><dd>${escapeHtml(chord.style)}</dd></div>
      </div>
      <div class="chips tight" style="margin-top:16px">
        <a class="chip" href="../chords/family.html#type=${chord.familyId}">查看该分类</a>
        <a class="chip" href="../chords/detail.html#slug=${chordSlug(chord, 'C', chordsData.tonicSlugMap)}">C 调详情</a>
      </div>
    ` : renderState('未找到引用的和弦');

    // 手位图预览：以当日调组的第一个调为例，白底键盘图作为面板视觉焦点
    const previewTonic = tonics[0];
    const handPreview = chord ? `
      <figure class="figure" style="margin-top:16px">
        <img src="${svgHandShapePath(chord.folder, previewTonic, chord.handShapes[0].id)}"
             alt="${escapeHtml(`${previewTonic} ${chord.typeName} 手位图`)}" loading="lazy"
             onerror="imgFallback(this, '手位图待生成')">
        <figcaption>以 ${escapeHtml(previewTonic)} 调为例 · ${escapeHtml(chord.handShapes[0].label)}</figcaption>
      </figure>
    ` : '';

    const progressionBlock = current.progressionId ? `
      <h2 style="margin-top:24px">关联进行</h2>
      ${progression ? `
        <a class="text-card" href="../progressions/#${progression.id}">
          <div class="text-card-head">
            <strong>${escapeHtml(progression.name)}</strong>
            <span class="chip">${escapeHtml(progression.key)}</span>
          </div>
          <p>${escapeHtml(progression.description)}</p>
        </a>
      ` : `<div class="placeholder">${escapeHtml(current.progressionId)}</div>`}
    ` : '';

    root.innerHTML = `
      <p class="crumb">练习</p>
      <h1>每日练习</h1>
      <p class="lead">按五度圈把 12 个调摊到一周里。每天只练一组，纵向站稳、横向移调、开口视唱，一周走完一个循环。</p>

      <div class="chips">${dayChips}</div>

      <section class="section">
        <div class="section-head">
          <h2>当日调组</h2>
          <span class="crumb" style="margin:0">${escapeHtml(group.day)}</span>
        </div>
        <div class="panel">
          <p class="note" style="margin-bottom:16px">${escapeHtml(group.note)}</p>
          <div class="chips tight">${tonicChips}</div>
        </div>
      </section>

      <section class="section">
        <div class="section-head">
          <h2>练习步骤</h2>
          <span class="crumb" style="margin:0">共 ${current.steps.length} 步</span>
        </div>
        <div class="chips">${practiceChips}</div>

        <div class="detail-layout">
          <div class="detail-main">
            <div class="practice" style="padding:0">${stepRows}</div>
          </div>
          <aside class="related">
            <h2>当前和弦</h2>
            ${chordReference}
            ${handPreview}
            ${progressionBlock}
          </aside>
        </div>
      </section>
    `;

    root.querySelectorAll('[data-day]').forEach(btn => {
      btn.addEventListener('click', () => {
        dayIndex = Number(btn.dataset.day);
        refresh();
      });
    });

    root.querySelectorAll('[data-practice]').forEach(btn => {
      btn.addEventListener('click', () => {
        practiceIndex = Number(btn.dataset.practice);
        refresh();
      });
    });

    initAccordion(root);
  }

  refresh();
})();
