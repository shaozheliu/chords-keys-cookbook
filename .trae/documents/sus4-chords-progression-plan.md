# sus4 和弦练习 + IVsus2 → Vsus4 → I 进行（计划）

## 一、Summary（目标概述）

为钢琴和弦练习手册新增「挂留四和弦（sus4）」练习章节，并配套生成：

1. **12 个调的 sus4 扩张型手型 SVG**（每个调 1 张，共 12 张）。
2. **1 张动画 GIF**：演示 C 大调下 `IVsus2（扩张）→ Vsus4（扩张）→ I（收缩的大三）` 进行，以 **F–G–C** 为例。
3. **sus4 练习文档** `docs/practice/sus4-chords.md`。
4. 在侧边栏与每日练习模板中挂入 sus4 入口。

核心手型事实（用户已给定）：

- sus4 只掌握**扩张型**手型，参考 C 大三扩张位置。
- 左手 `do-so`（5 指、2 指，指法不变）。
- 右手 `do-fa-so-do`（1-2-3-5 指），即把大三扩张型的 `mi(+4)` 换成 `fa(+5)`。

## 二、现状分析（Current State）

- 项目采用 Docsify + GitHub Pages，源目录 `docs/`；图片统一放在 `docs/assets/images/` 下按和弦类型分目录（`major-triads/`、`minor-triads/`、`sus2-chords/`），sus4 需新建 `sus4-chords/`。
- 已有三个同类生成脚本，均为**自包含、不互相 import**（用户明确要求不耦合）：
  - `scripts/gen_major_hand_groups.py`
  - `scripts/gen_minor_hand_groups.py`
  - `scripts/gen_sus2_hand_groups.py`（本次 sus4 脚本的直接模板）
- `scripts/gen_sus2_hand_groups.py` 已确认：键盘渲染基于半音模型（`WHITE_INDEX`、`SHARP_NAMES`、`FLAT_NAMES`），配色为左手红 `#dc2626`、右手蓝 `#2563eb`、按下键绿 `#d1fae5`；手型用 `(相对主音半音, 指法, L/R)` 定义。
- `docs/practice/sus2-chords.md` 已确认四段式结构（一、和弦结构；二、手型与弹奏位置；三、练习分组；四、练习步骤），sus4 文档沿用该风格。
- 环境：已安装 **Pillow 12.2.0**；未安装 cairosvg / imageio / ImageMagick / inkscape / rsvg-convert。因此 **GIF 必须用 Pillow 直接绘制帧**（Pillow 无法光栅化 SVG）。

## 三、变更方案（Proposed Changes）

### 1. 新建 `scripts/gen_sus4_hand_groups.py`（自包含，仅扩张型）

以 `gen_sus2_hand_groups.py` 为模板复制结构，做以下改动：

- 顶部注释改为 sus4 说明：sus4 = 根音 + 纯四度(+5) + 纯五度(+7)。
- `TONIC_INFO` 中 **F 改为降号模式**（`'F': (5, 'flat')`），其余同 sus2。原因：F sus4 的四音是 Bb（黑键），必须用降号标注；Db/Ab/Eb/Bb 本就为 flat，无需再改。
- `HANDS` 列表只保留 **1 个手型**（扩张型）：

```python
{
    'label': '扩张型',
    'sub': '手型二',
    'desc': '左手 5-2指 根音-五音 ｜ 右手 1-2-3-5指 根音-四音-五音-高八度根音',
    'notes': [
        (-12, 5, 'L'),   # 左手根音 do（低八度）
        (-5,  2, 'L'),   # 左手五音 so
        ( 0,  1, 'R'),   # 右手根音 do
        ( 5,  2, 'R'),   # 右手四音 fa
        ( 7,  3, 'R'),   # 右手五音 so
        (12,  5, 'R'),   # 右手高八度根音 do
    ],
    'range': (-12, 12),
},
```

- 标题 `title` 改为 `f'{tonic_name} Sus4 · {hand["label"]}（{hand["sub"]}）'`。
- 音级标注映射改为 `{0: '根音', 5: '四音', 7: '五音'}`。
- 输出路径 `docs/assets/images/sus4-chords/`，文件名 `{tonic_name}-hand-shape-2.svg`（统一沿用「扩张型 = 手型二」命名，sus4 只有手型二，故不生成 hand-shape-1）。
- 主循环只遍历 1 个手型，结束打印 `All 12 sus4 SVGs generated!`。

### 2. 新建 `scripts/gen_sus4_progression_gif.py`（自包含，Pillow 直接绘制）

生成 `docs/assets/images/sus4-chords/F-G-C-progression.gif`，演示 C 大调 `IVsus2（扩张）→ Vsus4（扩张）→ I（收缩的大三）`。

**三个帧配置**（复用现有手型定义，`offset`/`mode` 与各自脚本一致）：

| 帧 | 和弦 | 标题 | offset | mode | 音符 (rel, finger, side) | 音级映射 |
|----|------|------|--------|------|--------------------------|----------|
| 1 | Fsus2 扩张型 | `Fsus2 · 扩张型（IV）` | 5 | sharp | LH：(-12,5),(-5,2),(0,1)；RH：(2,1),(7,2),(14,5) | {0:根音,2:二音,7:五音} |
| 2 | Gsus4 扩张型 | `Gsus4 · 扩张型（V）` | 7 | sharp | LH：(-12,5),(-5,2)；RH：(0,1),(5,2),(7,3),(12,5) | {0:根音,5:四音,7:五音} |
| 3 | C 大三 紧凑型 | `C 大三 · 紧凑型（I）` | 0 | sharp | LH：(-12,3)；RH：(-5,1),(0,2),(4,4) | {0:根音,4:三音,7:五音} |

**绘制实现要点**（自包含，不 import 其他脚本）：

- 复制半音模型常量（`WHITE_INDEX`、`WHITE_NAMES`、`SHARP_NAMES`、`FLAT_NAMES`）与配色常量。
- 用 `PIL.Image` / `ImageDraw` / `ImageFont` 绘制每帧：
  - 固定键盘范围 `C2(MIDI 36)` 到 `C5(MIDI 72)`，三帧共用同一键盘布局（便于眼睛追踪和弦变化）。
  - 白键宽 40 / 高 150，黑键宽 26 / 高 90（与 SVG 同比例）。
  - 高亮按下键为绿色 `#d1fae5`；左手圆点红 `#dc2626`、右手圆点蓝 `#2563eb`，圆点内写指法数字（白字）。
  - 键盘下方写音级标注（根音/二音/四音/三音/五音，随帧而异），颜色与左右手一致。
- 字体：优先 `ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)` 渲染中文标题与音级；若字体不存在则回退 `ImageFont.load_default()`（此时音级可省略，标题仍用 ASCII 和弦符号）。
- 合成 GIF：`frames[0].save(path, save_all=True, append_images=frames[1:], duration=900, loop=0)`，帧间隔 900ms、无限循环。

### 3. 新建 `docs/practice/sus4-chords.md`

沿用 `sus2-chords.md` 的文体与四段式骨架，内容如下（由执行者按既定风格补齐行文）：

- **一、和弦结构**：sus4 = 根音 + 纯四度 + 纯五度；以 Csus4 = C–F–G 为例；说明四音替代三音、不分大小三、音色「紧张、待解决」，四音倾向下行解决到三音。
- **二、手型与弹奏位置（扩张型）**：
  - 说明 sus4 只掌握扩张型，参考 C 大三扩张位置。
  - 表格：左手 `do-so`（5–2 指）、右手 `do-fa-so-do`（1–2–3–5 指）；Csus4 示例 `⑤-C、②-G | ①-C、②-F、③-G、⑤-C（高八度）`。
  - 练习要点（左手纯五度跨度放松、右手 1-2-3-5 跨度 C→C）。
  - 嵌入 `![Csus4 示意图](../assets/images/sus4-chords/C-hand-shape-2.svg)`。
- **三、练习分组（十二调手型平移）**：
  - 按五度圈分四组（F/C/G、D/A/E、B/F#/Db、Ab/Eb/Bb）+ 周日全量，每调一张扩张型 SVG（`{调}-hand-shape-2.svg`，F# 用 `F%23` 编码）。
  - 保留「每组从右往左练」的提示与底层逻辑（沿用 sus2 第 61–63 行表述）。
- **四、练习步骤**：
  - 4.1 手型平移：纵向（柱式→琶音）+ 横向（五度圈移调）+ 视唱（链接 daily-routine 贯穿原则），简述。
  - 4.2 **和弦进行练习（核心）**：`IVsus2（扩张）→ Vsus4（扩张）→ I（收缩的大三）`，以 C 大调 F–G–C 为例：
    - 列出三和弦音与手型：
      - Fsus2（扩张）：左 F–C–F（5–2–1）、右 G–C–G（1–2–5）；
      - Gsus4（扩张）：左 G–D（5–2）、右 G–C–D–G（1–2–3–5）；
      - C 大三（紧凑/收缩）：左 C（3）、右 G–C–E（1–2–4）。
    - 嵌入 `![F-G-C 进行](../assets/images/sus4-chords/F-G-C-progression.gif)`。
    - 说明功能走向（下属→属→主）与解决重力：属回主「落地」；挂留音的共同音平滑进行（Fsus2 的 G 是 V 的根音、Gsus4 的 C 是 I 的根音，形成共同音衔接）。

### 4. 修改 `docs/_sidebar.md`

在第 22 行 `- [挂留二和弦（sus2）](practice/sus2-chords.md)` 之后插入：

```markdown
    - [挂留四和弦（sus4）](practice/sus4-chords.md)
```

### 5. 修改 `docs/practice/daily-routine.md`

在第 68 行 `| 色彩和弦 | [挂留二和弦（sus2）](sus2-chords.md) | 10 min |` 之后插入：

```markdown
| 色彩和弦 | [挂留四和弦（sus4）](sus4-chords.md) | 10 min |
```

## 四、假设与决策（Assumptions & Decisions）

1. **sus4 只有一种手型**：扩张型，文件名用 `{调}-hand-shape-2.svg`（沿用「扩张型 = 手型二」的全局命名约定），不生成 hand-shape-1。
2. **仅 C 大调示例**做进行练习与 GIF（用户已确认），其余调仍提供 12 张扩张型 SVG 用于手型平移。
3. **GIF 用 Pillow 直接绘制**（环境无 cairosvg/ImageMagick），三帧固定同一键盘范围 C2–C5。
4. **F sus4 降号标注**：因四音为 Bb，`TONIC_INFO` 中 F 设为 `flat`；其余调沿用 sus2 的 sharp/flat 配置。
5. 进行顺序按功能 `IV → V → I`（F→G→C），与 sus2「从右往左」的分组练习逻辑是两回事，文档分开表述。

## 五、验证步骤（Verification）

1. 运行 `python scripts/gen_sus4_hand_groups.py`，确认生成 12 张 `docs/assets/images/sus4-chords/*-hand-shape-2.svg`，其中 `F-hand-shape-2.svg` 的四音标注为 Bb（非 A#）。
2. 运行 `python scripts/gen_sus4_progression_gif.py`，确认生成 `docs/assets/images/sus4-chords/F-G-C-progression.gif`，三帧顺序为 Fsus2→Gsus4→C 大三，循环播放。
3. 用浏览器/图片查看器打开几张 SVG 与 GIF，确认键盘、高亮、指法圆点、标题、音级正确，F sus4 无错标。
4. 检查 `docs/practice/sus4-chords.md` 中的相对路径与文件名（尤其 F# 的 `F%23`）均与实际生成文件一致。
5. 启动 Docsify 预览（或 `git status` 核对文件落位），确认侧边栏与每日练习模块出现 sus4 入口且链接可跳转。
