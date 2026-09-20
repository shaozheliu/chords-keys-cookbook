/* ==========================================================================
   曲目拆解模块
   数据：songs.json —— 每首曲目按五个维度结构化：
        曲目信息 / 和弦进行分析 / 段落拆解 / 伴奏手法 / 练习要点。
   ========================================================================== */

(async function init() {
  renderNav('songs');
  renderFooter();

  const root = document.getElementById('app');
  const data = await fetchJSON('songs.json');

  if (!data || !data.songs.length) {
    root.innerHTML = renderState('曲目数据加载失败，请稍后重试');
    return;
  }

  const songs = data.songs;
  const wanted = getQueryParam('song') || window.location.hash.replace(/^#\/?/, '');
  const hit = songs.find(s => s.id === wanted);
  let activeId = hit ? hit.id : songs[0].id;

  function refresh() {
    const song = songs.find(s => s.id === activeId) || songs[0];
    const { info } = song;

    const cards = songs.map(s => `
      <button type="button" class="text-card ${s.id === song.id ? 'active' : ''}" data-song="${s.id}">
        <div class="text-card-head">
          <strong>${escapeHtml(s.title)}</strong>
          <span class="chip">${escapeHtml(s.info.key)}</span>
        </div>
        <div class="mini-chips">
          <span class="chip">${renderStars(s.info.difficulty)}</span>
          <span class="chip">${escapeHtml(s.info.tempo)}</span>
        </div>
        <div class="mini-chips">
          ${s.info.coreTechniques.map(t => `<span class="chip">${escapeHtml(t)}</span>`).join('')}
        </div>
      </button>
    `).join('');

    const harmonicRows = song.harmonicAnalysis.map(item => `
      <tr>
        <td><strong>${escapeHtml(item.section)}</strong></td>
        <td>${escapeHtml(item.progression)}</td>
        <td>${escapeHtml(item.degrees)}</td>
        <td>${escapeHtml(item.function)}</td>
      </tr>
    `).join('');

    const breakdownBlocks = song.sectionBreakdown.map((item, i) => {
      const accomp = song.accompaniment.find(a => a.section === item.section);
      return `
        <div class="sub-section">
          <h3>${i + 1}. ${escapeHtml(item.section)}</h3>
          <div class="info">
            <div class="info-row"><dt>左手</dt><dd style="font-weight:400">${escapeHtml(item.leftHand)}</dd></div>
            <div class="info-row"><dt>右手</dt><dd style="font-weight:400">${escapeHtml(item.rightHand)}</dd></div>
            ${accomp ? `
              <div class="info-row"><dt>织体</dt><dd>${escapeHtml(accomp.texture)}</dd></div>
              <div class="info-row"><dt>手型</dt><dd>${escapeHtml(accomp.handShape)}</dd></div>
              <div class="info-row"><dt>情绪</dt><dd>${escapeHtml(accomp.mood)}</dd></div>
            ` : ''}
          </div>
        </div>
      `;
    }).join('');

    const accompRows = song.accompaniment.map(item => `
      <tr>
        <td><strong>${escapeHtml(item.section)}</strong></td>
        <td>${escapeHtml(item.texture)}</td>
        <td>${escapeHtml(item.handShape)}</td>
        <td>${escapeHtml(item.mood)}</td>
      </tr>
    `).join('');

    const sheetBlock = (song.chartSvg || song.leadSheetSvg) ? `
      <section class="panel">
        <h2 class="block-title">谱面</h2>
        ${song.chartSvg ? `
          <figure class="figure">
            <img src="${svgAssetPath(song.chartSvg)}" alt="${escapeHtml(`${song.title} 弹唱谱`)}"
                 loading="lazy" onerror="imgFallback(this, '弹唱谱待生成')">
            <figcaption>弹唱谱 · 和弦标记与歌词对位</figcaption>
          </figure>
        ` : ''}
        ${song.leadSheetSvg ? `
          <figure class="figure">
            <img src="${svgAssetPath(song.leadSheetSvg)}" alt="${escapeHtml(`${song.title} 五线谱`)}"
                 loading="lazy" onerror="imgFallback(this, '五线谱待生成')">
            <figcaption>五线谱 · 旋律与和声骨架</figcaption>
          </figure>
        ` : ''}
      </section>
    ` : '';

    const pointsBlock = song.practicePoints.length ? `
      <section>
        <h2 class="block-title">练习要点</h2>
        <div class="panel flush">
          <ol class="bullet-list">
            ${song.practicePoints.map(p => `<li>${escapeHtml(p)}</li>`).join('')}
          </ol>
        </div>
      </section>
    ` : '';

    const songChips = songs.map(s => `
      <button type="button" class="chip ${s.id === song.id ? 'active' : ''}" data-song="${s.id}">${escapeHtml(s.title)}</button>
    `).join('');

    root.innerHTML = `
      <p class="crumb">曲目</p>
      <h1>经典曲目拆解</h1>
      <p class="lead">把一首歌拆成和弦进行分析、段落织体、伴奏手法和练习要点四层，照着练就能完整弹下来。</p>

      <div class="card-grid wide" style="margin-bottom:40px">${cards}</div>

      <div class="section-head">
        <h2>${escapeHtml(song.title)}</h2>
        <span class="crumb" style="margin:0">${escapeHtml(info.key)} · ${escapeHtml(info.timeSignature)} · ${escapeHtml(info.tempo)}</span>
      </div>

      <article class="detail-layout">
        <div class="detail-main">
          <section>
            <h2 class="block-title">曲目信息</h2>
            <div class="info">
              <div class="info-row"><dt>调性</dt><dd>${escapeHtml(info.key)}</dd></div>
              <div class="info-row"><dt>拍号</dt><dd>${escapeHtml(info.timeSignature)}</dd></div>
              <div class="info-row"><dt>速度</dt><dd>${escapeHtml(info.tempo)}</dd></div>
              <div class="info-row"><dt>难度</dt><dd>${renderStars(info.difficulty)}</dd></div>
            </div>
          </section>

          <section>
            <h2 class="block-title">和弦进行分析</h2>
            <div class="table-wrap">
              <table class="table">
                <thead>
                  <tr><th>段落</th><th>和弦进行</th><th>级数</th><th>和声功能</th></tr>
                </thead>
                <tbody>${harmonicRows}</tbody>
              </table>
            </div>
          </section>

          <section>
            <h2 class="block-title">段落拆解</h2>
            ${breakdownBlocks}
          </section>

          <section>
            <h2 class="block-title">伴奏手法</h2>
            <div class="table-wrap">
              <table class="table">
                <thead>
                  <tr><th>段落</th><th>织体</th><th>手型</th><th>情绪</th></tr>
                </thead>
                <tbody>${accompRows}</tbody>
              </table>
            </div>
          </section>

          ${sheetBlock}
          ${pointsBlock}
        </div>

        <aside class="related">
          <h2>核心技术</h2>
          <div class="chips tight">
            ${info.coreTechniques.map(t => `<span class="chip">${escapeHtml(t)}</span>`).join('')}
          </div>
          <h2 style="margin-top:24px">曲目列表</h2>
          <div class="chips tight">${songChips}</div>
          <h2 style="margin-top:24px">配套练习</h2>
          <p class="note" style="margin-bottom:12px">先在手型和进行模块把骨架练熟，再回到整曲。</p>
          <div class="chips tight">
            <a class="chip" href="../practice/">每日练习</a>
            <a class="chip" href="../progressions/">和弦进行</a>
          </div>
        </aside>
      </article>
    `;

    root.querySelectorAll('[data-song]').forEach(btn => {
      btn.addEventListener('click', () => {
        activeId = btn.dataset.song;
        history.replaceState(null, '', `#${activeId}`);
        refresh();
        root.querySelector('.section-head')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  window.addEventListener('hashchange', () => {
    const next = window.location.hash.replace(/^#\/?/, '');
    if (next && next !== activeId && songs.some(s => s.id === next)) {
      activeId = next;
      refresh();
    }
  });

  refresh();
})();
