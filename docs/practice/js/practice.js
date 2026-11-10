/* ==========================================================================
   每日练习模块
   L4：五度圈 + 练习工作区（和弦 | 进行）
   - 和弦：F/C/G + 和弦类型 → 构成音 + 薄/厚手型图对照
   - 进行：F/C/G + 1564 / 2516251 Practice Kit
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

  const progressions = progressionCatalog(progData);

  let dayIndex = 0;
  let practiceIndex = 0;
  let practiceMode = 'chord';
  let progressionId = progressions[0] ? progressions[0].id : '1564';
  let drillTonic = 'C';

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

  const tonicsOf = group => (group.tonics === 'all' ? chordsData.tonics : group.tonics);

  function activeMajors(group) {
    return tonicsOf(group);
  }

  function activeMinors(group) {
    return activeMajors(group).map(t => RELATIVE_MINOR[t]).filter(Boolean);
  }

  function drillTonicsForDay(group) {
    return tonicsOf(group);
  }

  function defaultDrillTonic(group) {
    const dayTonics = drillTonicsForDay(group);
    return dayTonics[0] || 'C';
  }

  function polar(cx, cy, r, deg) {
    const rad = (deg - 90) * Math.PI / 180;
    return [cx + r * Math.cos(rad), cy + r * Math.sin(rad)];
  }

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

  function renderTonicSwitch(dayTonics) {
    return dayTonics.map(t => `
      <button type="button" class="${t === drillTonic ? 'active' : ''}" data-drill-tonic="${escapeHtml(t)}">${escapeHtml(t)}</button>
    `).join('');
  }

  function renderModeTabs() {
    const chordActive = practiceMode === 'chord';
    return `
      <div class="practice-mode-tabs">
        <button type="button" class="${chordActive ? 'active' : ''}" data-practice-mode="chord">和弦练习</button>
        <button type="button" class="${chordActive ? '' : 'active'}" data-practice-mode="progression">进行练习</button>
      </div>
    `;
  }

  function renderWorkspaceShell(bodyHtml, dayTonics) {
    return `
      <section class="section">
        <div class="practice-workspace">
          <div class="practice-bar">
            ${renderModeTabs()}
            <div class="tonic-switch" aria-label="当日练习调">
              ${renderTonicSwitch(dayTonics)}
            </div>
          </div>
          ${bodyHtml}
        </div>
      </section>
    `;
  }

  function renderProgressionWorkspace(dayTonics) {
    const prog = progressions.find(p => p.id === progressionId) || progressions[0];
    if (!prog) {
      return renderWorkspaceShell('<p class="note">进行练习数据待补充。</p>', dayTonics);
    }
    const combo = featuredCombo(prog);
    const progChips = progressions.map(p => `
      <button type="button" class="${p.id === progressionId ? 'active' : ''}" data-progression-id="${escapeHtml(p.id)}">
        ${escapeHtml(p.code)}
      </button>
    `).join('');

    const body = `
      <p class="note" style="margin:0 0 16px">练习调与当日调组一致；展示节奏型与按拍指法小图（不含四拍手位总览长图）。</p>
      <div class="practice-filters">${progChips}</div>
      ${renderPracticeKit(prog, combo, chordsData, {
        tonicLabel: `${drillTonic} 大调`,
        practiceKey: drillTonic,
        showProgressionStrip: false,
      })}
      <div class="chips" style="margin-top:16px">
        <a class="chip" href="../progressions/detail.html#id=${encodeURIComponent(prog.id)}">查看 ${escapeHtml(prog.code)} 进行详情</a>
      </div>
    `;
    return renderWorkspaceShell(body, dayTonics);
  }

  function renderChordWorkspace(dayTonics) {
    const current = practice.practices[practiceIndex];
    const chord = findChord(chordsData.chords, current.chordId);
    const linkedProg = (current.progressionId && progressions.find(p => p.id === current.progressionId)) || null;

    const typeChips = practice.practices.map((p, i) => {
      const c = findChord(chordsData.chords, p.chordId);
      const label = c ? c.typeName.replace(/和弦$/, '') : p.chordId;
      return `<button type="button" class="${i === practiceIndex ? 'active' : ''}" data-practice="${i}">${escapeHtml(label)}</button>`;
    }).join('');

    const body = `
      <p class="note" style="margin:0 0 16px">对照构成音与薄 / 厚手型（大七另有「中」）。练习调与当日调组一致，点选 F / C / G 等即切换该调的和弦内容。</p>
      <div class="practice-filters">${typeChips}</div>
      ${renderChordPracticePanel(chord, drillTonic, chordsData, linkedProg)}
    `;
    return renderWorkspaceShell(body, dayTonics);
  }

  function refresh() {
    const group = practice.weeklyGroups[dayIndex];
    const dayTonics = drillTonicsForDay(group);

    if (!dayTonics.includes(drillTonic)) {
      drillTonic = defaultDrillTonic(group);
    }

    const dayChips = practice.weeklyGroups.map((g, i) => `
      <button type="button" class="chip ${i === dayIndex ? 'active-green' : ''}" data-day="${i}">${escapeHtml(g.day)}</button>
    `).join('');

    const body = practiceMode === 'progression'
      ? renderProgressionWorkspace(dayTonics)
      : renderChordWorkspace(dayTonics);

    root.innerHTML = `
      <p class="crumb"><a href="../">首页</a> / 练习</p>
      <h1>每日练习</h1>
      <p class="lead">选定日期与调，直接在页面查看构成音与手型图；和弦与进行两类练习在下方工作区切换。</p>

      <div class="chips">${dayChips}</div>

      <section class="section">
        <div class="fifths-panel">
          <div class="fifths-visual">
            ${renderCircle(group)}
          </div>
          <div class="fifths-meta">
            <h2>${escapeHtml(group.day)} · 今日练习调</h2>
            <p class="note">${escapeHtml(group.note)}</p>
            <p class="fifths-hint">高亮为当日调组。下方工作区按钮与之一致，点选即可切换和弦 / 进行内容。</p>
          </div>
        </div>
      </section>

      ${body}
    `;

    root.querySelectorAll('[data-day]').forEach(btn => {
      btn.addEventListener('click', () => {
        dayIndex = Number(btn.dataset.day);
        const g = practice.weeklyGroups[dayIndex];
        if (!drillTonicsForDay(g).includes(drillTonic)) {
          drillTonic = defaultDrillTonic(g);
        }
        refresh();
      });
    });

    root.querySelectorAll('[data-practice]').forEach(btn => {
      btn.addEventListener('click', () => {
        practiceIndex = Number(btn.dataset.practice);
        refresh();
      });
    });

    root.querySelectorAll('[data-practice-mode]').forEach(btn => {
      btn.addEventListener('click', () => {
        practiceMode = btn.dataset.practiceMode;
        refresh();
      });
    });

    root.querySelectorAll('[data-progression-id]').forEach(btn => {
      btn.addEventListener('click', () => {
        progressionId = btn.dataset.progressionId;
        refresh();
      });
    });

    root.querySelectorAll('[data-drill-tonic]').forEach(btn => {
      btn.addEventListener('click', () => {
        drillTonic = btn.dataset.drillTonic;
        refresh();
      });
    });
  }

  drillTonic = defaultDrillTonic(practice.weeklyGroups[dayIndex]);
  refresh();
})();
