/* ==========================================================================
   每日练习模块
   数据：practice.json（周维度轮动 + 四步练习）
   UI：五度圈扇形双圈 + 当日调组高亮 + Step1~Step4 练习步骤
   Step1 三和弦 / Step2 七和弦 / Step3 色彩和弦 / Step4 和弦进行
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

  const steps = practice.practiceSteps || [];
  const progressions = (progData && progData.progressions) || [];

  let dayIndex = 0;
  let stepIndex = 0;

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

  /** 一组练习细则（纵向 / 横向 / 视唱 / 切换） */
  function subSteps(list) {
    const rows = (list || []).map(s => `
      <li>
        <span class="sub-step-phase">${escapeHtml(s.phase)}</span>
        <div class="sub-step-body">
          <strong>${escapeHtml(s.name)}</strong>
          <p>${escapeHtml(s.detail)}</p>
        </div>
        <span class="chip ghost sm">${escapeHtml(s.type)}</span>
      </li>
    `).join('');
    return `<ul class="sub-steps">${rows}</ul>`;
  }

  /** Step1~3：按类目展示各和弦的练习细则 */
  function renderChordStep(step, group, tonics) {
    const scopeBar = `
      <div class="chips" style="margin-bottom:16px">
        <span class="chip active-green">${escapeHtml(group.day)} · 扇区调组</span>
        ${tonics.map(t => `<span class="tonic-pill">${escapeHtml(t)}</span>`).join('')}
      </div>
    `;

    const cards = (step.chords || []).map((entry, idx) => {
      const chord = findChord(chordsData.chords, entry.chordId);
      if (!chord) return '';
      const detailHref = `../chords/detail.html#slug=${chordSlug(chord, 'C', chordsData.tonicSlugMap)}`;
      const familyHref = `../chords/family.html#type=${chord.familyId}`;
      return `
        <div class="step-card">
          <div class="step-index">${idx + 1}</div>
          <div class="step-body">
            <div class="step-top">
              <strong>${escapeHtml(chord.typeName)}</strong>
              <span class="step-phase">${escapeHtml(chord.formula)} · ${escapeHtml(chord.style)}</span>
            </div>
            <p>${escapeHtml(entry.note || chord.tone)}</p>
            ${subSteps(entry.steps)}
            <div class="chips tight" style="margin-top:12px">
              <a class="chip ghost sm" href="${detailHref}">C 调详情</a>
              <a class="chip ghost sm" href="${familyHref}">和弦分类</a>
            </div>
          </div>
        </div>
      `;
    }).join('');

    return scopeBar + cards;
  }

  /** Step4：四条经典进行 + 通用练习方法 */
  function renderProgressionStep(step, group, tonics) {
    const cards = (step.progressionIds || []).map(id => {
      const prog = progressions.find(p => p.id === id);
      if (!prog) return '';
      const seq = (prog.listChords || []).join(' → ');
      return `
        <a class="text-card" href="../progressions/detail.html#id=${encodeURIComponent(prog.id)}">
          <div class="text-card-head">
            <strong>${escapeHtml(prog.name)}</strong>
            <span class="chip">${escapeHtml(prog.roman || '')}</span>
          </div>
          <p>${escapeHtml(seq)}</p>
          <p class="note">${escapeHtml(prog.description)}</p>
        </a>
      `;
    }).join('');

    const method = `
      <div class="step-card">
        <div class="step-index">${step.no || 4}</div>
        <div class="step-body">
          <div class="step-top">
            <strong>练习方法</strong>
            <span class="step-phase">逐条进行通用</span>
          </div>
          <p>${escapeHtml(step.note || '')}</p>
          ${subSteps(step.steps)}
        </div>
      </div>
    `;

    const scopeBar = `
      <div class="chips" style="margin-bottom:16px">
        <span class="chip active-green">${escapeHtml(group.day)} · 扇区调组</span>
        ${tonics.map(t => `<span class="tonic-pill">${escapeHtml(t)}</span>`).join('')}
      </div>
    `;

    return scopeBar + method + cards;
  }

  function refresh() {
    const group = practice.weeklyGroups[dayIndex];
    const tonics = tonicsOf(group);
    const current = steps[stepIndex] || steps[0];

    const dayChips = practice.weeklyGroups.map((g, i) => `
      <button type="button" class="chip ${i === dayIndex ? 'active-green' : ''}" data-day="${i}">${escapeHtml(g.day)}</button>
    `).join('');

    const stepChips = steps.map((s, i) => `
      <button type="button" class="chip ${i === stepIndex ? 'active' : ''}" data-step="${i}">
        Step ${s.no} · ${escapeHtml(s.title)}
      </button>
    `).join('');

    const tonicPills = tonics.map(tonic =>
      `<span class="tonic-pill">${escapeHtml(tonic)}</span>`
    ).join('');

    const isProg = current.scope === 'progression';
    const main = isProg
      ? renderProgressionStep(current, group, tonics)
      : renderChordStep(current, group, tonics);

    root.innerHTML = `
      <p class="crumb"><a href="../">首页</a> / 练习</p>
      <h1>每日练习</h1>
      <p class="lead">按五度圈把 12 个调摊到一周里。点选日期，圈上会亮起当日调组；练习分四步递进：三和弦 → 七和弦 → 色彩和弦 → 和弦进行。</p>

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
            <p class="fifths-hint">Step1~Step3 都在当前扇区高亮的调组上逐个调完成；Step4 再把整条进行移到这组调上。</p>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="section-head">
          <h2>练习步骤</h2>
          <span class="crumb" style="margin:0">共 ${steps.length} 步</span>
        </div>
        <div class="chips">${stepChips}</div>

        <div class="detail-main step-list">${main}</div>
      </section>
    `;

    root.querySelectorAll('[data-day]').forEach(btn => {
      btn.addEventListener('click', () => {
        dayIndex = Number(btn.dataset.day);
        refresh();
      });
    });

    root.querySelectorAll('[data-step]').forEach(btn => {
      btn.addEventListener('click', () => {
        stepIndex = Number(btn.dataset.step);
        refresh();
      });
    });
  }

  refresh();
})();
