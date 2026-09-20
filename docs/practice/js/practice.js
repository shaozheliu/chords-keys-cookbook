/* ==========================================================================
   每日练习模块
   数据：practice.json（周维度轮动 + 练习步骤）
   UI：对齐 Figma L4 — 五度圈扇形双圈 + 当日调组高亮 + 练习步骤
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

  // 五度圈：C 居中朝上，顺时针五度
  const CIRCLE_MAJOR = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F'];
  const CIRCLE_MINOR = ['Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'Ebm', 'Bbm', 'Fm', 'Cm', 'Gm', 'Dm'];
  const RELATIVE_MINOR = {
    C: 'Am', G: 'Em', D: 'Bm', A: 'F#m', E: 'C#m', B: 'G#m',
    'F#': 'Ebm', Db: 'Bbm', Ab: 'Fm', Eb: 'Cm', Bb: 'Gm', F: 'Dm',
  };

  const GREEN = {
    outIdle: '#F4F4F5',
    inIdle: '#FAFAFA',
    outActive: '#047857',
    inActive: '#059669',
    center: '#10B981',
    on: '#FFFFFF',
    strokeIdle: '#E5E5E5',
    strokeActive: '#065F46',
    labelMuted: '#737373',
  };

  let dayIndex = 0;
  let practiceIndex = 0;

  const tonicsOf = group => (group.tonics === 'all' ? chordsData.tonics : group.tonics);

  function activeMajors(group) {
    return tonicsOf(group);
  }

  function activeMinors(group) {
    return activeMajors(group).map(t => RELATIVE_MINOR[t]).filter(Boolean);
  }

  /** 极坐标：0° 在正上方，顺时针 */
  function polar(cx, cy, r, deg) {
    const rad = (deg - 90) * Math.PI / 180;
    return [cx + r * Math.cos(rad), cy + r * Math.sin(rad)];
  }

  /** 环形扇区路径（外径 → 内径） */
  function ringWedge(cx, cy, rOuter, rInner, i) {
    const start = i * 30 - 15;
    const end = start + 30;
    const [x1, y1] = polar(cx, cy, rOuter, start);
    const [x2, y2] = polar(cx, cy, rOuter, end);
    const [x3, y3] = polar(cx, cy, rInner, end);
    const [x4, y4] = polar(cx, cy, rInner, start);
    return `M${x1.toFixed(2)} ${y1.toFixed(2)} A${rOuter} ${rOuter} 0 0 1 ${x2.toFixed(2)} ${y2.toFixed(2)} L${x3.toFixed(2)} ${y3.toFixed(2)} A${rInner} ${rInner} 0 0 0 ${x4.toFixed(2)} ${y4.toFixed(2)} Z`;
  }

  function labelAt(cx, cy, r, i, text, fill, size) {
    const mid = i * 30;
    const [x, y] = polar(cx, cy, r, mid);
    return `<text x="${x.toFixed(2)}" y="${y.toFixed(2)}" text-anchor="middle" dominant-baseline="central"
      font-size="${size}" font-weight="600" fill="${fill}" font-family="inherit">${escapeHtml(text)}</text>`;
  }

  function renderCircle(group) {
    const majors = new Set(activeMajors(group));
    const minors = new Set(activeMinors(group));
    const cx = 200;
    const cy = 200;
    const rOut = 188;
    const rMid = 128;
    const rIn = 72;

    const outer = CIRCLE_MAJOR.map((name, i) => {
      const on = majors.has(name);
      return `<path d="${ringWedge(cx, cy, rOut, rMid, i)}"
        fill="${on ? GREEN.outActive : GREEN.outIdle}"
        stroke="${on ? GREEN.strokeActive : '#FFFFFF'}" stroke-width="2"/>`;
    }).join('');

    const inner = CIRCLE_MINOR.map((name, i) => {
      const on = minors.has(name);
      return `<path d="${ringWedge(cx, cy, rMid, rIn, i)}"
        fill="${on ? GREEN.inActive : GREEN.inIdle}"
        stroke="${on ? GREEN.strokeActive : '#FFFFFF'}" stroke-width="2"/>`;
    }).join('');

    const majorLabels = CIRCLE_MAJOR.map((name, i) =>
      labelAt(cx, cy, (rOut + rMid) / 2, i, name, majors.has(name) ? GREEN.on : GREEN.labelMuted, 15)
    ).join('');

    const minorLabels = CIRCLE_MINOR.map((name, i) =>
      labelAt(cx, cy, (rMid + rIn) / 2, i, name, minors.has(name) ? GREEN.on : '#A1A1AA', 12)
    ).join('');

    const dayLabel = escapeHtml(group.day);
    return `
      <svg class="fifths-svg" viewBox="0 0 400 400" role="img" aria-label="五度圈：${dayLabel} 当日调组">
        ${outer}
        ${inner}
        <circle cx="${cx}" cy="${cy}" r="${rIn - 2}" fill="${GREEN.center}"/>
        <text x="${cx}" y="${cy - 8}" text-anchor="middle" fill="${GREEN.on}" font-size="13" font-weight="700">${dayLabel}</text>
        <text x="${cx}" y="${cy + 12}" text-anchor="middle" fill="${GREEN.on}" font-size="12" font-weight="500">当日调组</text>
        ${majorLabels}
        ${minorLabels}
      </svg>
    `;
  }

  function refresh() {
    const group = practice.weeklyGroups[dayIndex];
    const tonics = tonicsOf(group);
    const current = practice.practices[practiceIndex];
    const chord = findChord(chordsData.chords, current.chordId);
    const progression = (progData && progData.progressions || [])
      .find(p => p.id === current.progressionId);

    const dayChips = practice.weeklyGroups.map((g, i) => `
      <button type="button" class="chip ${i === dayIndex ? 'active-green' : ''}" data-day="${i}">${escapeHtml(g.day)}</button>
    `).join('');

    const practiceChips = practice.practices.map((p, i) => {
      const c = findChord(chordsData.chords, p.chordId);
      return `<button type="button" class="chip ${i === practiceIndex ? 'active' : ''}" data-practice="${i}">
        ${escapeHtml(c ? c.typeName : p.chordId)}
      </button>`;
    }).join('');

    const tonicPills = tonics.map(tonic =>
      `<span class="tonic-pill">${escapeHtml(tonic)}</span>`
    ).join('');

    const stepRows = current.steps.map((step, i) => `
      <div class="step-card">
        <div class="step-index">${i + 1}</div>
        <div class="step-body">
          <div class="step-top">
            <strong>${escapeHtml(step.name)}</strong>
            <span class="step-phase">${escapeHtml(step.phase)}</span>
          </div>
          <p>${escapeHtml(step.detail)}</p>
          <span class="chip ghost sm">${escapeHtml(step.type)}</span>
        </div>
      </div>
    `).join('');

    const chordSide = chord ? `
      <div class="panel chord-side">
        <h3>${escapeHtml(chord.typeName)}</h3>
        <p class="note">${escapeHtml(chord.tone)}</p>
        <div class="info">
          <div class="info-row"><dt>音程关系</dt><dd>${escapeHtml(chord.formula)}</dd></div>
          <div class="info-row"><dt>音色特征</dt><dd>${escapeHtml(chord.tone)}</dd></div>
          <div class="info-row"><dt>适用风格</dt><dd>${escapeHtml(chord.style)}</dd></div>
        </div>
        <div class="chips tight" style="margin-top:16px">
          <a class="chip" href="../chords/family.html#type=${chord.familyId}">查看该分类</a>
          <a class="chip" href="../chords/detail.html#slug=${chordSlug(chord, 'C', chordsData.tonicSlugMap)}">C 调详情</a>
        </div>
        ${current.progressionId && progression ? `
          <a class="text-card" style="margin-top:16px" href="../progressions/detail.html#id=${progression.id}">
            <div class="text-card-head">
              <strong>${escapeHtml(progression.name)}</strong>
              <span class="chip">${escapeHtml(progression.key)}</span>
            </div>
            <p>${escapeHtml(progression.description)}</p>
          </a>
        ` : ''}
      </div>
    ` : renderState('未找到引用的和弦');

    root.innerHTML = `
      <p class="crumb"><a href="../">首页</a> / 练习</p>
      <h1>每日练习</h1>
      <p class="lead">按五度圈把 12 个调摊到一周里。点选日期，圈上会亮起当日调组；每天只练一组，纵向站稳、横向移调、开口视唱。</p>

      <div class="chips">${dayChips}</div>

      <section class="section">
        <div class="fifths-panel">
          <div class="fifths-visual">
            ${renderCircle(group)}
          </div>
          <div class="fifths-meta">
            <h2>${escapeHtml(group.day)} · 今日练习调</h2>
            <p class="note">${escapeHtml(group.note)}</p>
            <div class="tonic-row">${tonicPills}</div>
            <p class="fifths-hint">扁平实心、无反光。绿色由深到浅递进（外→内→圆心），对齐 OpenMAIC 按钮质感。</p>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="section-head">
          <h2>练习步骤</h2>
          <span class="crumb" style="margin:0">共 ${current.steps.length} 步</span>
        </div>
        <div class="chips">${practiceChips}</div>

        <div class="detail-layout practice-layout">
          <div class="detail-main step-list">${stepRows}</div>
          <aside class="related">${chordSide}</aside>
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
  }

  refresh();
})();
