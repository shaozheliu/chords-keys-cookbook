/* ==========================================================================
   和弦 Keys Cookbook — 公共前端模块
   提供：数据加载、URL 参数、SVG 路径拼接、和弦符号与组成音、
        导航栏 / 页脚 / 卡片 / 折叠面板等共享渲染能力。
   ========================================================================== */

const DATA_BASE = '../data/';
const ASSET_BASE = '../assets/images/';

/** 是否在站点根目录（首页） */
function isRootPage() {
  return document.body.dataset.root === '1';
}

/** 模块页相对路径前缀 */
function navPrefix() {
  return isRootPage() ? '' : '../';
}

/** 首页链接 */
function homeHref() {
  return isRootPage() ? './' : '../';
}

/** 模块导航：首页 / 和弦 / 练习 / 进行（对齐 Figma L0–L6） */
const NAV_DEFS = [
  { id: 'home', label: '首页', path: null },
  { id: 'chords', label: '和弦', path: 'chords/' },
  { id: 'practice', label: '练习', path: 'practice/' },
  { id: 'progressions', label: '进行', path: 'progressions/' },
];

function navItems() {
  const prefix = navPrefix();
  const home = homeHref();
  return NAV_DEFS.map(item => ({
    ...item,
    href: item.path === null ? home : `${prefix}${item.path}`,
  }));
}

/** 和弦后缀 → 和弦符号后缀 */
const SUFFIX_SYMBOL = {
  major: '',
  minor: 'm',
  7: '7',
  '7sus4': '7sus4',
  m7: 'm7',
  maj7: 'maj7',
  sus2: 'sus2',
  sus4: 'sus4',
  add9: 'add9',
  6: '6',
};

const PITCH_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const PITCH_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'];

/* ---------- 数据加载 ---------- */

/**
 * 加载 JSON 数据
 * @param {string} name - 文件名（如 'chords.json'）
 * @returns {Promise<object|null>}
 */
async function fetchJSON(name) {
  try {
    const res = await fetch(`${DATA_BASE}${name}`, { cache: 'no-cache' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error(`[data] 加载 ${name} 失败：`, err);
    return null;
  }
}

/* ---------- URL 参数 ---------- */

/**
 * 读取 URL 参数，同时兼容查询串与 hash 片段两种写法。
 * 静态服务器（如 serve）会把 *.html 301 到无扩展名路径，查询串会在重定向中丢失，
 * 而 hash 片段会被浏览器保留，因此应用内部统一使用 hash 传参。
 * @param {string} key
 * @returns {string|null}
 */
function getQueryParam(key) {
  const fromSearch = new URLSearchParams(window.location.search).get(key);
  if (fromSearch !== null) return fromSearch;
  const hash = window.location.hash.replace(/^#\/?/, '');
  if (!hash) return null;
  return new URLSearchParams(hash).get(key);
}

/* ---------- 通用工具 ---------- */

function escapeHtml(value) {
  return String(value === undefined || value === null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** 在数组中按 id 查找和弦定义 */
function findChord(chords, id) {
  return (chords || []).find(c => c.id === id) || null;
}

/* ---------- SVG 路径拼接 ---------- */

/**
 * 通用资源路径。兼容 JSON 中写 'assets/images/xxx.svg' 或 'xxx.svg' 两种形式。
 * 逐段编码，避免 F# 之类字符被当成 URL 片段。
 */
function svgAssetPath(relativePath) {
  if (!relativePath) return '';
  if (/^(https?:)?\/\//.test(relativePath)) return relativePath;
  const normalized = String(relativePath)
    .replace(/^\/?assets\/images\//, '')
    .replace(/^\.?\//, '');
  return ASSET_BASE + normalized.split('/').map(encodeURIComponent).join('/');
}

/** 卡片键盘图：cards/{slug}-{list|hero}.svg */
function svgCardKeyPath(slug, variant = 'list') {
  return `${ASSET_BASE}cards/${slug}-${variant}.svg`;
}

/** 生成脚本目录名 → hands/by-tonic/{调}/{kind}/（与 scripts/asset_paths.py 一致） */
const HAND_FOLDER_TO_KIND = {
  'major-triads': 'major',
  'minor-triads': 'minor',
  'dom7-chords': 'dom7',
  'dom7sus4-chords': 'dom7sus4',
  'm7-chords': 'm7',
  'maj7-chords': 'maj7',
  'sus2-chords': 'sus2',
  'sus4-chords': 'sus4',
  'add9-chords': 'add9',
  'maj6-chords': 'maj6',
  'maj69-chords': 'maj69',
};

/**
 * 手型 SVG 文件名里的根音（与生成脚本一致：C-hand-shape-1，不含 m / m7 后缀）
 * @param {string} tonic - 如 Am、Dm、Am7（误写时也可纠正）
 */
function handShapeTonicForAsset(tonic) {
  const s = String(tonic);
  if (/m7$/i.test(s)) return s.slice(0, -2);
  if (/m$/i.test(s)) return s.slice(0, -1);
  return s;
}

/** 手位图：hands/by-tonic/{调}/{kind}/shape-{id}.svg */
function svgHandShapePath(folder, tonic, shapeId) {
  const root = handShapeTonicForAsset(tonic);
  const kind = HAND_FOLDER_TO_KIND[folder] || String(folder).replace(/-chords$/, '').replace(/-triads$/, '');
  const seg = `hands/by-tonic/${root}/${kind}/shape-${shapeId}.svg`;
  return `${ASSET_BASE}${seg.split('/').map(encodeURIComponent).join('/')}`;
}

/* ---------- 和弦符号与音名 ---------- */

/**
 * 和弦 slug，与 card-keys 的 SVG 命名保持一致：
 *   major / minor 用连字符（c-major、a-flat-minor），其余后缀直接拼接（c7、cm7、csus4、cadd9、c6）
 */
function chordSlug(chord, tonic, tonicSlugMap) {
  if (!chord || !tonic) return '';
  const tonicSlug = (tonicSlugMap || {})[tonic] || String(tonic).toLowerCase();
  const sep = (chord.suffix === 'major' || chord.suffix === 'minor') ? '-' : '';
  return `${tonicSlug}${sep}${chord.suffix}`;
}

/** 和弦符号：C / Cm / C7 / Cmaj7 / Csus4 … */
function chordSymbol(chord, tonic) {
  if (!chord || !tonic) return '';
  const suffix = SUFFIX_SYMBOL[chord.suffix];
  return `${tonic}${suffix === undefined ? chord.suffix : suffix}`;
}

/** 卡片副标题：C大三和弦 / 降D小七和弦 … */
function chordCName(chord, tonic, tonicCn) {
  if (!chord || !tonic) return '';
  const cn = (tonicCn || {})[tonic] || tonic;
  return `${cn}${chord.typeName}`;
}

/** 组成音：C - E - G（按调名拼写，Cm7 为 C - Eb - G - Bb） */
function chordNotes(chord, tonic, tonicPc) {
  if (!chord || !tonic) return '';
  return spellSet(tonic, chord.intervals, tonicPc);
}

/* ---------- 共享渲染 ---------- */

/** 顶部导航栏：品牌 + 居中文案导航 */
function renderNav(activeId) {
  const host = document.querySelector('[data-nav]');
  if (!host) return;
  const items = navItems();
  host.innerHTML = `
    <a class="brand" href="${homeHref()}">钢琴即兴</a>
    <nav class="site-nav">
      ${items.map(item => `
        <a class="${item.id === activeId ? 'active' : ''}" href="${item.href}">${item.label}</a>
      `).join('')}
    </nav>
  `;
}

/** 底部信息栏 */
function renderFooter() {
  const host = document.querySelector('[data-footer]');
  if (!host) return;
  host.innerHTML = `
    <div>钢琴即兴 · 自学手册</div>
    <div>© 2026 Chords &amp; Keys Handbook</div>
  `;
}

/**
 * 和弦卡片（左符号右键盘图，沿用原站卡片版式）
 * @param {{href:string, symbol:string, label:string, slug:string, alt?:string}} opts
 */
function renderChordCard({ href, symbol, label, slug, alt }) {
  return `
    <a class="chord-card" href="${href}">
      <div class="chord-copy">
        <strong>${escapeHtml(symbol)}</strong>
        <span>${escapeHtml(label)}</span>
      </div>
      <img src="${svgCardKeyPath(slug, 'list')}" alt="${escapeHtml(alt || `${symbol} 键盘图`)}"
           width="228" height="128" loading="lazy"
           onerror="this.style.visibility='hidden'">
    </a>
  `;
}

/** 难度星标 */
function renderStars(value) {
  const n = Math.max(0, Math.min(5, Number(value) || 0));
  const cells = Array.from({ length: 5 }, (_, i) =>
    `<i class="${i < n ? 'on' : ''}">★</i>`).join('');
  return `<span class="stars" title="难度 ${n} / 5">${cells}</span>`;
}

const SPELL_LETTERS = 'CDEFGAB';
const SPELL_LETTER_INDEX = { C: 0, D: 1, E: 2, F: 3, G: 4, A: 5, B: 6 };
const SPELL_PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const SPELL_STEPS = { 0: 0, 2: 1, 3: 2, 4: 2, 5: 3, 7: 4, 9: 5, 10: 6, 11: 6 };

/** 按调名拼写音程，保留正确的升降号（Cm7 的三音是 Eb 不是 D#） */
function spellFromRoot(root, interval, tonicPc) {
  const letter = SPELL_LETTERS[(SPELL_LETTER_INDEX[root[0]] + SPELL_STEPS[interval]) % 7];
  const rootPc = (tonicPc && tonicPc[root] !== undefined) ? tonicPc[root] : SPELL_PC[root[0]];
  let diff = ((rootPc + interval) % 12 - SPELL_PC[letter] + 12) % 12;
  if (diff > 6) diff -= 12;
  const acc = { 0: '', 1: '#', 2: '##', [-1]: 'b', [-2]: 'bb' }[diff];
  return letter + (acc || '');
}

function spellSet(root, intervals, tonicPc) {
  return intervals.map(i => spellFromRoot(root, i, tonicPc)).join(' - ');
}

/** 讲解模板占位符：当前调、组成音，以及七和弦「根音 + 三音上的三和弦」 */
function fillTeach(template, chord, tonic, data) {
  if (!template) return '';
  const pc = data.tonicPc;
  const thirdMaj = spellFromRoot(tonic, 4, pc);
  const thirdMin = spellFromRoot(tonic, 3, pc);
  const vars = {
    '{tonic}': tonic,
    '{symbol}': chordSymbol(chord, tonic),
    '{notes}': spellSet(tonic, chord.intervals, pc),
    '{name}': chordCName(chord, tonic, data.tonicCn),
    '{third}': chord.id === 'minor' || chord.id === 'm7' ? thirdMin : thirdMaj,
    '{upperSymbol}': '',
    '{upperNotes}': '',
  };
  if (chord.id === 'm7') {
    vars['{upperSymbol}'] = thirdMin;
    vars['{upperNotes}'] = spellSet(tonic, [3, 7, 10], pc);
  } else if (chord.id === 'maj7') {
    vars['{upperSymbol}'] = `${thirdMaj}m`;
    vars['{upperNotes}'] = spellSet(tonic, [4, 7, 11], pc);
  }
  return Object.keys(vars)
    .sort((a, b) => b.length - a.length)
    .reduce((text, key) => text.replaceAll(key, vars[key]), String(template));
}

/**
 * 手型图 + 讲解。详情页可带指法表；每日练习页只保留图和文字。
 * @param {{ showTable?: boolean }} [options]
 */
function renderHandBlocks(chord, tonic, data, options) {
  const showTable = !options || options.showTable !== false;
  return (chord.handShapes || []).map(hand => {
    const noteRows = (hand.notes || []).map(note => `
      <tr>
        <td>${note.hand === 'L' ? '左手' : '右手'}</td>
        <td>${note.finger} 指</td>
        <td>${escapeHtml(note.degree)}</td>
        <td>${note.offset > 0 ? `+${note.offset}` : note.offset}</td>
      </tr>
    `).join('');

    const notesTable = showTable && noteRows ? `
      <table class="table" style="margin-top:16px">
        <thead>
          <tr><th>手</th><th>指法</th><th>声部</th><th>八度位移</th></tr>
        </thead>
        <tbody>${noteRows}</tbody>
      </table>
    ` : '';

    const whyTexts = hand.why || hand.description || '';
    const whyHtml = (Array.isArray(whyTexts) ? whyTexts : [whyTexts])
      .filter(Boolean)
      .map(text => `<p class="hand-why">${escapeHtml(fillTeach(text, chord, tonic, data))}</p>`)
      .join('');
    const tip = fillTeach(hand.tip || '', chord, tonic, data);
    const symbol = chordSymbol(chord, tonic);

    return `
      <div class="hand-block">
        <h3>${escapeHtml(hand.label)}</h3>
        ${whyHtml}
        <img src="${svgHandShapePath(chord.folder, tonic, hand.id)}"
             alt="${escapeHtml(`${symbol} ${hand.label}`)}" width="640" height="360" loading="lazy"
             onerror="imgFallback(this, '手位图待生成')">
        ${tip ? `<p class="hand-tip">${escapeHtml(tip)}</p>` : ''}
        ${notesTable}
      </div>
    `;
  }).join('');
}

/** 空态 / 加载态 */
function renderState(message) {
  return `<div class="state">${escapeHtml(message)}</div>`;
}

/** 图片缺失时的占位替换（供 <img onerror> 调用） */
function imgFallback(el, text) {
  const box = document.createElement('div');
  box.className = 'placeholder';
  box.textContent = text || '图待生成';
  if (el && el.parentElement) el.parentElement.replaceChild(box, el);
}

/** 折叠面板：点击 [data-acc-head] 切换所在 [data-acc-item] 的 open 状态 */
function initAccordion(root) {
  (root || document).querySelectorAll('[data-acc-head]').forEach(head => {
    head.addEventListener('click', () => {
      const item = head.closest('[data-acc-item]');
      if (!item) return;
      const open = item.classList.toggle('open');
      head.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
}

/* ---------- 进行 · Practice Kit（L4 / L6） ---------- */

/** 进行列表页与练习页当前仅开放这些 id（占位，可后续在 JSON 扩展） */
const DEFAULT_PROGRESSION_CATALOG_IDS = ['1564', '2516251'];

function progressionCatalog(progData) {
  const ids = (progData && progData.featuredProgressionIds) || DEFAULT_PROGRESSION_CATALOG_IDS;
  const all = (progData && progData.progressions) || [];
  return all.filter(p => ids.includes(p.id));
}

function progressionRootOf(tonic) {
  return handShapeTonicForAsset(tonic);
}

function progressionMeasureSymbol(measure, chordsData) {
  const chord = chordsData && findChord(chordsData.chords, measure.chordId);
  const tonic = String(measure.tonic);
  const rootName = progressionRootOf(tonic);
  if (!chord) return tonic;
  const suffix = SUFFIX_SYMBOL[chord.suffix];
  const s = suffix === undefined ? chord.suffix : suffix;
  if (/m$/.test(tonic)) {
    if (chord.suffix === 'minor') return tonic;
    if (chord.suffix === 'm7') return `${rootName}m7`;
    if (chord.suffix === 'add9') return `${tonic}add9`;
  }
  return `${rootName}${s}`;
}

function featuredCombo(prog) {
  const combos = prog.combos || [];
  return combos.find(c => c.featured) || combos[0] || null;
}

const PROGRESSION_DEGREE_SEMI = { I: 0, ii: 2, iii: 4, IV: 5, V: 7, vi: 9, VI: 9 };

function tonicPcForDegree(keyMajor, degree, chordsData) {
  const semi = PROGRESSION_DEGREE_SEMI[degree];
  if (semi === undefined || !chordsData || !chordsData.tonicPc) return null;
  const keyPc = chordsData.tonicPc[keyMajor];
  if (keyPc === undefined) return null;
  return (keyPc + semi) % 12;
}

function majorTonicNameForPc(pc, chordsData) {
  return (chordsData.tonics || []).find(t => chordsData.tonicPc[t] === pc) || null;
}

function resolveMeasureTonic(keyMajor, measure, chordsData) {
  const pc = tonicPcForDegree(keyMajor, measure.degree, chordsData);
  if (pc === null) return measure.tonic;
  const name = majorTonicNameForPc(pc, chordsData) || keyMajor;
  const id = measure.chordId;
  if (id === 'minor' || id === 'm7') return `${name}m`;
  return name;
}

/** 节奏型图：每条进行一张（级数谱），不随练习调切换 */
function resolveProgressionRhythmSvg(prog, combo) {
  const template = (combo && combo.rhythmSvgTemplate) || (prog && prog.rhythmSvgTemplate);
  if (template) {
    return svgAssetPath(String(template));
  }
  return svgAssetPath((prog && prog.rhythmSvg) || (combo && combo.rhythmSvg) || '');
}

function comboForPracticeKey(combo, keyMajor, chordsData) {
  if (!combo) return combo;
  const measures = (combo.measures || []).map(m => ({
    ...m,
    tonic: resolveMeasureTonic(keyMajor, m, chordsData),
  }));
  const symbols = measures.map(m => progressionMeasureSymbol(m, chordsData));
  return { ...combo, measures, symbols };
}

function progressionRhythmSvg(prog, combo) {
  if (!prog) return '';
  return resolveProgressionRhythmSvg(prog, combo);
}

function renderKeySwitcherCompact(activeTonic, tonics) {
  const list = tonics || ['F', 'C', 'G'];
  return `
    <div class="key-switcher-compact" data-key-switcher>
      <span class="key-switcher-label">练习调</span>
      <div class="key-switcher-pills">
        ${list.map(t => `
          <button type="button" class="key-pill ${t === activeTonic ? 'active' : ''}" data-practice-key="${escapeHtml(t)}">
            ${escapeHtml(t)} 大调
          </button>
        `).join('')}
      </div>
    </div>
  `;
}

function renderHandSlotMeasure(measure, chordsData) {
  const chord = chordsData && findChord(chordsData.chords, measure.chordId);
  const folder = chord && chord.folder;
  const img = folder ? `
    <img src="${svgHandShapePath(folder, measure.tonic, measure.handShapeId)}"
         alt="" loading="lazy" onerror="imgFallback(this, '指法待补充')">
  ` : '<div class="placeholder sm">指法待补充</div>';
  const sym = escapeHtml(progressionMeasureSymbol(measure, chordsData));
  return `
    <div class="hand-slot">
      <div class="hand-slot-symbol">${sym}</div>
      ${img}
      <dl class="hand-slot-meta">
        <div><dt>左</dt><dd>${escapeHtml(measure.leftHand)}</dd></div>
        <div><dt>右</dt><dd>${escapeHtml(measure.rightHand)}</dd></div>
      </dl>
    </div>
  `;
}

/** 手型区统一 2×2 网格，超过 4 拍纵向叠放 */
function renderHandSlotGrids(measures, chordsData) {
  const n = measures.length;
  if (n === 0) return '';
  const cell = m => renderHandSlotMeasure(m, chordsData);
  const block = slice =>
    `<div class="hand-slot-grid hand-slot-grid--2x2">${slice.map(cell).join('')}</div>`;
  const parts = [];
  for (let i = 0; i < n; i += 4) {
    parts.push(block(measures.slice(i, i + 4)));
  }
  return `<div class="hand-slot-stack">${parts.join('')}</div>`;
}

function bindPracticeKeySwitcher(root, onChange) {
  const host = (root || document).querySelector('[data-key-switcher]');
  if (!host || !onChange) return;
  host.querySelectorAll('[data-practice-key]').forEach(btn => {
    btn.addEventListener('click', () => {
      onChange(btn.dataset.practiceKey);
    });
  });
}

/**
 * @param {{ showHead?: boolean, tonicLabel?: string, practiceKey?: string, showHandSlots?: boolean }} [opts]
 */
function renderPracticeKit(prog, combo, chordsData, opts) {
  if (!prog || !combo) {
    return '<div class="practice-kit"><p class="note">进行内容待补充。</p></div>';
  }
  const options = opts || {};
  const practiceKey = options.practiceKey || prog.key?.replace(/大调$/, '') || 'C';
  const kitCombo = comboForPracticeKey(combo, practiceKey, chordsData);
  const rhythmUrl = resolveProgressionRhythmSvg(prog, combo);
  const rhythm = `
    <div class="practice-kit-rhythm">
      <div class="practice-kit-subhead">节奏型 · 固定弹法</div>
      <figure class="figure practice-kit-figure">
        <img src="${rhythmUrl}" alt="${escapeHtml(`${prog.code} 节奏型`)}" width="834" height="170" loading="lazy">
      </figure>
    </div>
  `;

  const showHands = options.showHandSlots !== false;
  const measures = kitCombo.measures || [];
  let hands = '';
  if (showHands) {
    hands = measures.length ? `
      <div class="practice-kit-hands">
        <div class="practice-kit-subhead">固定指法 · 按拍拆解</div>
        ${renderHandSlotGrids(measures, chordsData)}
      </div>
    ` : '<p class="note" style="margin:0">指法拆解待补充。</p>';
  }

  const head = options.showHead === false ? '' : `
    <div class="practice-kit-head">
      <div>
        <strong class="practice-kit-code">${escapeHtml(prog.code)}</strong>
        <span class="chip">${escapeHtml(prog.tag || '')}</span>
      </div>
      <p class="practice-kit-roman">${escapeHtml(prog.roman || '')} · ${escapeHtml((kitCombo.symbols || []).join(' → '))}</p>
    </div>
  `;

  const tonicNote = options.tonicLabel
    ? `<p class="note practice-kit-tonic">练习调：${escapeHtml(options.tonicLabel)}</p>`
    : '';

  return `
    <div class="practice-kit">
      ${head}
      ${tonicNote}
      ${rhythm}
      ${hands}
    </div>
  `;
}

/** 练习页手型厚度标签（薄 / 中 / 厚），替代「手型一、二」 */
function practiceHandDensity(chord, hand) {
  const shapes = chord.handShapes || [];
  const id = hand.id;
  let short = '薄';
  if (shapes.length >= 3) {
    short = id === 1 ? '薄' : id === 2 ? '中' : '厚';
  } else if (shapes.length === 2) {
    short = id === 1 ? '薄' : '厚';
  }

  const leftNotes = (hand.notes || []).filter(n => n.hand === 'L');
  let left = '左：根音';
  if (leftNotes.length >= 3) left = '左：低音区加厚';
  else if (leftNotes.length === 2) left = '左：根音 + 五音';

  const sing = chord.formula ? `唱 ${chord.formula.replace(/-/g, ' – ')}` : '';

  return { short, left, sing };
}

function renderChordPracticePanel(chord, tonic, chordsData, linkedProg) {
  if (!chord) return renderState('未找到和弦类型');

  const symbol = chordSymbol(chord, tonic);
  const cn = (chordsData.tonicCn || {})[tonic] || tonic;
  const notes = chordNotes(chord, tonic, chordsData.tonicPc);
  const noteTokens = notes.split(' - ').filter(Boolean);

  const density = practiceHandDensity(chord, (chord.handShapes || [])[0] || {});
  const singLine = density.sing || (chord.formula ? `唱 ${chord.formula}` : '');

  const notePills = noteTokens.map(n =>
    `<span class="chord-note-pill">${escapeHtml(n)}</span>`
  ).join('');

  const colClass = (chord.handShapes || []).length >= 3 ? ' hand-practice-row--triple' : '';

  const handPanes = (chord.handShapes || []).map(hand => {
    const d = practiceHandDensity(chord, hand);
    return `
      <article class="hand-practice-pane">
        <div class="hand-practice-head">
          <strong>${escapeHtml(d.short)}</strong>
          <span>${escapeHtml(d.left)}</span>
        </div>
        <img src="${svgHandShapePath(chord.folder, tonic, hand.id)}"
             alt="${escapeHtml(`${symbol} · ${d.short}`)}" loading="lazy"
             onerror="imgFallback(this, '手位图待生成')">
      </article>
    `;
  }).join('');

  const progLink = linkedProg ? `
    <div class="chips" style="margin-top:16px">
      <a class="chip" href="../progressions/detail.html#id=${encodeURIComponent(linkedProg.id)}">
        关联进行 · ${escapeHtml(linkedProg.code)}
      </a>
    </div>
  ` : '';

  return `
    <div class="chord-practice-panel">
      <div class="chord-practice-identity">
        <div class="chord-practice-symbol">${escapeHtml(symbol)}</div>
        <p class="chord-practice-meta">${escapeHtml(cn)} 大调 · ${escapeHtml(chord.typeName)}</p>
        <div class="chord-note-row">${notePills}</div>
        <p class="chord-sing-line">${escapeHtml(singLine)}</p>
      </div>
      <div class="hand-practice-row${colClass}">${handPanes}</div>
      <div class="chips tight">
        <a class="chip" href="../chords/family.html#type=${chord.familyId}">该分类说明</a>
        <a class="chip" href="../chords/detail.html#slug=${chordSlug(chord, tonic, chordsData.tonicSlugMap)}">${escapeHtml(symbol)} 详情页</a>
      </div>
      ${progLink}
    </div>
  `;
}
