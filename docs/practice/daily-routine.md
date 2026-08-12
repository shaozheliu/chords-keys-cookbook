# 每日练习模板

本练习模板以**五度圈（Circle of Fifths）**为核心框架，将和弦按类别拆分为每日可执行的练习单元，帮助你系统化地掌握键盘和声。

---

## 为什么要按五度圈练习？

五度圈是音乐理论的基石，选择以五度圈为练习框架，有四个核心原因：

**1. 覆盖全部 12 个调**

五度圈自然遍历 12 个调性（C → G → D → A → E → B/Cb → F#/Gb → Db → Ab → Eb → Bb → F → C），确保没有调性盲区。很多学习者只习惯于 C 调或少数常用调，五度圈练习能强制补齐短板。

**2. 符合和声进行的内在逻辑**

大多数和弦进行中，根音运动以四度/五度上行为主（如 ii-V-I），五度圈练习让你在调与调之间感受到这种自然的和声张力-解决关系。

**3. 渐进式积累升降号**

顺时针方向每个新调增加一个升号，逆时针方向增加一个降号，五指位记忆与调号理解同步成长，不会一次性被过多升降号压垮。

**4. 可拆解、可量化**

五度圈将练习内容封装为"每天一个调 × N 类和弦"的结构，目标清晰，进度可控，适合每日固定时间的刻意练习。

### 五度圈全景

<div align="center">

<svg viewBox="0 0 620 620" width="100%" style="max-width:560px" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1a1a2e"/>
      <stop offset="100%" stop-color="#16213e"/>
    </radialGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="620" height="620" rx="16" fill="url(#bg)"/>

  <!-- Outer ring -->
  <circle cx="310" cy="310" r="230" fill="none" stroke="#2a2a4a" stroke-width="1"/>
  <circle cx="310" cy="310" r="155" fill="none" stroke="#2a2a4a" stroke-width="1"/>
  <circle cx="310" cy="310" r="3" fill="#7c8db5"/>

  <!-- Rays from center to each position -->
  <g stroke="#2a2a4a" stroke-width="0.5" opacity="0.5">
    <line x1="310" y1="310" x2="310" y2="80"/>
    <line x1="310" y1="310" x2="425" y2="111"/>
    <line x1="310" y1="310" x2="505" y2="195"/>
    <line x1="310" y1="310" x2="540" y2="310"/>
    <line x1="310" y1="310" x2="505" y2="425"/>
    <line x1="310" y1="310" x2="425" y2="509"/>
    <line x1="310" y1="310" x2="310" y2="540"/>
    <line x1="310" y1="310" x2="195" y2="509"/>
    <line x1="310" y1="310" x2="115" y2="425"/>
    <line x1="310" y1="310" x2="80" y2="310"/>
    <line x1="310" y1="310" x2="115" y2="195"/>
    <line x1="310" y1="310" x2="195" y2="111"/>
  </g>

  <!-- Connecting lines between outer and inner -->
  <g stroke="#3a3a5a" stroke-width="0.5" opacity="0.4">
    <line x1="310" y1="80"  x2="310" y2="155"/>
    <line x1="425" y1="111" x2="383" y2="176"/>
    <line x1="505" y1="195" x2="434" y2="233"/>
    <line x1="540" y1="310" x2="465" y2="310"/>
    <line x1="505" y1="425" x2="434" y2="387"/>
    <line x1="425" y1="509" x2="383" y2="444"/>
    <line x1="310" y1="540" x2="310" y2="465"/>
    <line x1="195" y1="509" x2="237" y2="444"/>
    <line x1="115" y1="425" x2="186" y2="387"/>
    <line x1="80"  y1="310" x2="155" y2="310"/>
    <line x1="115" y1="195" x2="186" y2="233"/>
    <line x1="195" y1="111" x2="237" y2="176"/>
  </g>

  <!-- Major keys (outer ring) -->
  <g font-family="Arial, sans-serif" font-size="15" font-weight="bold" fill="#f0a060" text-anchor="middle" dominant-baseline="central" filter="url(#glow)">
    <text x="310" y="68">C</text>
    <text x="442" y="99">G</text>
    <text x="525" y="192">D</text>
    <text x="558" y="310">A</text>
    <text x="525" y="428">E</text>
    <text x="442" y="523">B</text>
    <text x="310" y="558">F♯</text>
    <text x="178" y="523">D♭</text>
    <text x="95"  y="428">A♭</text>
    <text x="62"  y="310">E♭</text>
    <text x="95"  y="192">B♭</text>
    <text x="178" y="99">F</text>
  </g>

  <!-- Minor keys (inner ring) -->
  <g font-family="Arial, sans-serif" font-size="13" fill="#7eb8c9" text-anchor="middle" dominant-baseline="central">
    <text x="310" y="145">Am</text>
    <text x="388" y="170">Em</text>
    <text x="442" y="228">Bm</text>
    <text x="465" y="310">F♯m</text>
    <text x="442" y="392">C♯m</text>
    <text x="388" y="450">G♯m</text>
    <text x="310" y="475">D♯m</text>
    <text x="232" y="450">B♭m</text>
    <text x="178" y="392">Fm</text>
    <text x="155" y="310">Cm</text>
    <text x="178" y="228">Gm</text>
    <text x="232" y="170">Dm</text>
  </g>

  <!-- Center label -->
  <text x="310" y="300" font-family="Arial, sans-serif" font-size="13" fill="#7c8db5" text-anchor="middle" dominant-baseline="central">五度圈</text>
  <text x="310" y="318" font-family="Arial, sans-serif" font-size="10" fill="#5a6a8a" text-anchor="middle" dominant-baseline="central">Circle of Fifths</text>

  <!-- Arrows: clockwise = +P5, counter-clockwise = +P4 -->
  <!-- Clockwise arrow between C and G -->
  <g fill="none" stroke="#f0a060" stroke-width="1.5" opacity="0.6">
    <!-- Top-right between C and G -->
    <path d="M 350,78 Q 370,68 390,75" marker-end="url(#arrow-cw)"/>
  </g>

  <!-- Counter-clockwise arrow between C and F -->
  <g fill="none" stroke="#6a9fb5" stroke-width="1.5" opacity="0.6">
    <path d="M 270,78 Q 250,68 230,75" marker-end="url(#arrow-ccw)"/>
  </g>

  <!-- Arrow markers -->
  <defs>
    <marker id="arrow-cw" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0,0 L 6,3 L 0,6 Z" fill="#f0a060"/>
    </marker>
    <marker id="arrow-ccw" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0,0 L 6,3 L 0,6 Z" fill="#6a9fb5"/>
    </marker>
  </defs>

  <!-- Legend -->
  <g transform="translate(20, 580)">
    <rect x="0" y="0" width="8" height="8" rx="1" fill="#f0a060"/>
    <text x="14" y="8" font-family="Arial, sans-serif" font-size="11" fill="#8899aa">大调（顺时针 = 纯五度）</text>
    <rect x="0" y="16" width="8" height="8" rx="1" fill="#7eb8c9"/>
    <text x="14" y="24" font-family="Arial, sans-serif" font-size="11" fill="#8899aa">关系小调（内圈）</text>
  </g>
</svg>

</div>

> **读图指引**：外圈为大调，内圈为对应关系小调。顺时针每走一步上行纯五度，逆时针每走一步上行纯四度。

---

## 每日练习模块

| 模块 | 章节 | 建议时长 |
|------|------|---------|
| 大三和弦 | [大三和弦练习](major-triads.md) | 10 min |
| 小三和弦 | [小三和弦练习](minor-triads.md) | 10 min |
| 色彩和弦 | [挂留和弦](sus-chords.md) | 10 min |
| 色彩和弦 | [加九音和弦](add9-chords.md) | 10 min |
| 色彩和弦 | [六和弦与六九和弦](sixth-chords.md) | 10 min |

---

## 每日练习建议

- **初学者**：每天选 2~3 个调，依次练习大三 → 小三 → 一组色彩和弦，3~4 天完成一轮五度圈。
- **进阶者**：每天完成全部 12 个调的 1~2 个模块（如今天只练大三 + 挂留），保持手感。
- 以**慢速、均匀、放松**为第一原则，速度在准确性之后。
- 每完成一轮五度圈，可以尝试将当天的色彩和弦应用到 [经典曲目拆解](song-breakdown.md) 的曲目中。
