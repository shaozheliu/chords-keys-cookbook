# 节奏型标准表达格式（权威）

> 对齐弹唱教材里的 **X 谱**：上和弦、下弹奏点；时值用 **下划线层数** 表示，附点 / 连音 / 三连在元数据里声明。  
> 参考：综合节奏图（四、二八、八十六、十六八、附点、后附、小切分、三连音、四个十六）。

有两层数据，**不要混用**：

| 层 | Schema | 用途 |
|----|--------|------|
| **单拍型 `rhythm-cell/1`** | 一拍内的 X、符杠、附点、三连 | 节奏字典、教材「综合节奏」白框 |
| **小节谱 `rhythm-score/1`** | 多小节 + 和弦行 + 每拍 cell 序列 | 进行练习图（如练习1） |

旧版 Python `PATTERNS`（`fixed_units` 全局 0–15 网格）视为 **legacy/v1**，新稿一律用 **rhythm-score/1** + **layout v2**（拍内均匀、拍与拍之间留白）。

---

## 1. 时间网格

- 拍号默认 **4/4**。
- 每小节 **4 拍**；每拍再细分为 **4 个十六分位置**（slot `0–3`）。
- 小节内逻辑坐标：`(beat, slot)`，其中 `beat ∈ {1,2,3,4}`，`slot ∈ {0,1,2,3}`。
- 扁平 `unit = (beat - 1) * 4 + slot`，范围 `0–15`（仅内部使用）。

**时值与 slot 占用（一拍内）：**

| 时值 | 占用 slot | 说明 |
|------|-----------|------|
| 四分 `q` | 整拍（仅 1 个 X，居中） | 无下划线 |
| 八分 `8` | 2 个 slot（0–1 或 2–3） | 一道下划线 |
| 十六分 `16` | 1 个 slot | 两道下划线 |
| 三十二分 `32` | 半 slot* | 三道下划线（练习1 等快速四连） |

\* 渲染上可将一拍内 4 个 X 均画为十六分位置，用 **三道下划线** 表示「更快」，与教材四连 X 一致。

---

## 2. 单拍型 `rhythm-cell/1`

### 2.1 文件位置

`docs/rhythm-patterns/cells/<id>.yaml` 或集中表 `docs/rhythm-patterns/cells/canon.yaml`。

### 2.2 字段

```yaml
schema: chords-keys-handbook/rhythm-cell/1
id: sync-small          # 机器名
label: 小切分            # 教材中文名
slots:                  # 按时间顺序；每个 X 落在一拍内的 slot 上
  - { at: 0, dur: 16 }   # dur: q | 8 | 16 | 32
  - { at: 1, dur: 8 }
  - { at: 3, dur: 16 }
beams:                  # 符杠分组 [startSlot, endSlot]  inclusive，层数由所含最短 dur 推导
  - { from: 0, to: 3, layers: auto }
dots:                   # 附点：挂在某一个 slot 的 X 右侧
  - { after: 0 }         # 附点八分
tuplet: null            # 或 { ratio: 3, dur: 8, span: [0, 3] } 三连音
display:                # 可选：白框教学图
  box: true
```

### 2.3 标准单拍型注册表（与参考图一致）

| id | label | 推荐 DSL | 含义 |
|----|-------|----------|------|
| `quarter` | 四 | `q` | 一拍一个 X |
| `two-eighth` | 二八 | `8+8` | 两个八分 |
| `eighth-two-sixteenth` | 八十六 | `8+16+16` | 前八后两个十六 |
| `two-sixteenth-eighth` | 十六八 | `16+16+8` | 前两个十六后八 |
| `dotted-eighth-sixteenth` | 附点 | `8.+16` | 附点八分 + 十六 |
| `sixteenth-dotted-eighth` | 后附 | `16+8.` | 十六 + 附点八分 |
| `sync-small` | 小切分 | `16+8+16` | 十六-八-十六 |
| `triplet-eighth` | 三连音 | `8t3` | 一拍内三连八分 + 上方 `3` |
| `four-sixteenth` | 四个十六 | `16x4` | 四个十六分 |

**DSL 约定（Agent 手写时优先用）：**

- `q` `8` `16` `32` — 时值；`+` 连接同拍内多个音
- `.` 紧跟在时值后表示附点，如 `8.`、`8.+16`
- `8t3` 表示三个八分三连（占满一拍）
- `16x4` 表示连续四个十六分
- `r` 或 `—` 表示拍内剩余休止（节奏行画 `—`，不画 X）

---

## 3. 小节谱 `rhythm-score/1`

### 3.1 顶层

```yaml
schema: chords-keys-handbook/rhythm-score/1
title: 练习1
time: 4/4
layout: v2                    # 必须用 v2（见 §4）
output:
  basename: lianxi-1-demo     # → docs/assets/images/rhythm-patterns/<basename>.svg
bars:
  - ...
```

### 3.2 小节 `bars[]`

```yaml
- chords:
    - { beat: 1, text: "1add9" }
    - { beat: 3, text: "5/7" }
  chord_holds:                # 可选：在指定拍心画延音线 —
    - { beat: 2 }
    - { beat: 4 }
  beats:                      # 长度 4；每拍一个 cell id 或内联 DSL
    - 16x4
  ties:                       # 连音弧，flat unit 对 [u1, u2]
    - [3, 4]
    - [11, 12]
  rests:                      # 节奏行用 — 的 unit 位置（非 X）
    - 10
    - 14
```

**和弦行规则：**

- `chords` 里 `beat` 为 **1-based**；文本左对齐该拍起始（v2 布局下拍起点 + 小偏移）。
- 未换和弦的拍，用 `chord_holds` 或自动生成 `—`（实现可选）。
- 一小节仅一个和弦时：`chords: [{ beat: 1, text: "6m7" }]` + `chord_holds: [2,3,4]`。

**节奏行规则：**

- 每拍先由 **cell / DSL** 展开为 slot 上的 X 与 beams，再 **展开到 flat unit** 画下划线。
- `ties` 仅表示 **跨 slot 连奏**（不重新击键），渲染为 X 上方红色弧线。
- `rests` 画节奏位上的 `—`（与和弦行 `—` 字形一致）。

### 3.3 练习1（规范化示例）

```yaml
schema: chords-keys-handbook/rhythm-score/1
title: 练习1
time: 4/4
layout: v2
output:
  basename: lianxi-1-demo
bars:
  - chords:
      - { beat: 1, text: "1add9" }
      - { beat: 3, text: "5/7" }
    chord_holds: [2, 4]
    beats: [16x4, 16x4, 16x4, 16x4]
    ties: [[3, 4], [11, 12]]
  - chords:
      - { beat: 1, text: "6m7" }
    chord_holds: [2, 3, 4]
    beats: [four-sixteenth-tail, r, r, r]   # 或内联：见 canon
    # 第二拍起：一拍内 16x4 + unit4 连音 + 后两拍休止 — 用 beats + rests 表达
```

（第二小节若要保持「XXXX + 连到一拍 + 两拍 —」，在实现层用 `beats: ["16+8", "—", "—", "—"]` 或显式 `slots`；Agent 以 **听感** 为准微调 `cells` 引用。）

---

## 4. 排版 `layout v2`（拍间距）

| 常量 | 推荐值 | 含义 |
|------|--------|------|
| `SLOT_W` | 18 | 一拍内每个十六分位置的步进（px） |
| `BEAT_GAP` | 16 | **拍与拍之间**额外留白 |
| `BAR_GAP` | 0 | 小节**首尾竖线共用**；框宽仅由 `BAR_OUTER` 决定，不因音符种类改变 |
| `BAR_PAD_LEFT` / `BAR_PAD_RIGHT` | 18 | 节奏区与小节线对称内边距（首尾拍距竖线等距） |
| `RHYTHM_W` | `4×BEAT_INNER + 3×BEAT_GAP` | 小节内四拍区宽度 |
| `BAR_OUTER` | `PAD_L + RHYTHM_W + PAD_R` | 小节占位宽（含内边距） |

**坐标：**

```text
unit = (beat-1)*4 + slot
grid_left = measure_left + BAR_PAD_LEFT
x(unit) = grid_left + …（拍内 slot 步进）

measure_left(i) = page_left + i*(BAR_OUTER+BAR_GAP)
measure_right(i) = measure_left(i) + BAR_OUTER
```

**竖线**：`measure_right(i) == measure_left(i+1)`，画在 **[60, 432, 860, …]**，每根线既是左小节右界也是右小节左界。

**全局三原则（必守）**：

1. **首尾间距**：首符常用 `unit 0` 距左线 `content_edge_inset_px()`；小节框宽恒为 `BAR_OUTER`（`assert_measure_padding` 校验 unit 0 / 15 网格）。
2. **十六分 X**：`symbol_x_rhythm(gx, unit)`；**整拍休止** `rhythm_rest_x` = **拍心**；**四分** `rhythm_quarter_x` = **拍心**（与和弦行同 x）。
3. **和弦行**：`symbol_x_chord` = 拍心。
4. **对齐优先**：整拍四分/休止与和弦 `—` 纵向对齐；末拍休止在拍心时，最后墨迹到右线可略大于 27px。

和弦符号、小节线仍以 **拍边界** 对齐；X 不得跨 `BEAT_GAP` 均匀涂抹（v1 的问题）。

---

## 5. 下划线与附点（渲染）

| layers 参数 | 绘制 | 语义 |
|-------------|------|------|
| 0 | 无 | 四分（单 X，无下划线） |
| 1 | **1** 条线 | 八分 |
| 2 | **2** 条线 | 十六分（教材「四个十六」） |
| 3 | **3** 条线 | 三十二分 / 极快四连 |

- **同一 `beams` 组**：组内最短 `dur` 决定 **组底** 符杠层数；组内更短的音可在其位置 **叠加**更高层线（八十六、十六八、小切分）。
- **附点**：紧挨 X 右侧 `.`，不占独立 slot。
- **三连音**：X 上方括号 + 数字 `3`，三下划线（或一线三连样式与教材一致）。

---

## 6. Agent 决策

| 用户要什么 | 格式 |
|------------|------|
| 单拍型教学条（综合节奏图） | `rhythm-cell/1` → 未来 `render_cell_catalog` |
| 和弦进行 + X 节奏 | `rhythm-score/1` + `layout: v2` |
| 快速改旧图 | legacy `PATTERNS`（v1）仅维护存量 |

**禁止** 用 staff-score / MusicXML / mcp-score 画 X 谱。

---

## 7. 实现状态（仓库）

| 能力 | 状态 |
|------|------|
| `notation-format` 规范 | ✅ 本文 |
| `cells/canon.yaml` | ✅ 标准九种单拍型 |
| `layout v2` 坐标 | ✅ `scripts/layout.py` |
| `rhythm-score/1` → SVG | 🔜 `compile_rhythm_score.py`（建议下一步） |
| `render_exercise_1` | 过渡实现，应对齐 `rhythm-score/1` 样例 |
