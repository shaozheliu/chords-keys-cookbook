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

/** 卡片键盘图：card-keys/{slug}-{list|hero}.svg */
function svgCardKeyPath(slug, variant = 'list') {
  return `${ASSET_BASE}card-keys/${slug}-${variant}.svg`;
}

/** 手位图：{folder}/{调名}-hand-shape-{id}.svg */
function svgHandShapePath(folder, tonic, shapeId) {
  return `${ASSET_BASE}${folder}/${encodeURIComponent(`${tonic}-hand-shape-${shapeId}.svg`)}`;
}

/** 进行图：{folder}/{调名}-progression.svg */
function svgProgressionPath(folder, tonic) {
  if (!folder) return '';
  return `${ASSET_BASE}${folder}/${encodeURIComponent(`${tonic}-progression.svg`)}`;
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

/** 组成音：C - E - G（按调名决定升/降号写法） */
function chordNotes(chord, tonic, tonicPc) {
  if (!chord || !tonic) return '';
  const useFlat = String(tonic).includes('b');
  const names = useFlat ? PITCH_FLAT : PITCH_SHARP;
  const root = (tonicPc || {})[tonic];
  const base = root === undefined ? 0 : root;
  return chord.intervals
    .map(interval => names[(base + interval) % 12])
    .join(' - ');
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
