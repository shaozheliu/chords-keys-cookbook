# 五度圈分组手型图（hand-group-1~4.svg）生成计划

## 一、需求概述

按五度圈将 12 个大调分为 4 组（连续三调一组），每组生成一张 SVG 总览图：
- 布局：**3 列（3 个调）× 2 行（手型一 / 手型二）**，每格为该调 × 该手型的键盘示意图
- 文件：`docs/practice/hand-group-1.svg` ~ `hand-group-4.svg`
- 插入 [major-triads.md](file:///d:/Githubprojects/chords-keys-cookbook/docs/practice/major-triads.md) 的「三、练习方法」章节

## 二、现状分析

- [gen_hand_shapes.py](file:///d:/Githubprojects/chords-keys-cookbook/scripts/gen_hand_shapes.py)：现有手型图脚本，**只支持 C 大调**——键位写死（`WHITE_KEYS_7`/`WHITE_KEYS_GE`/`WHITE_KEYS_8`），`draw_keyboard()` 仅支持白键高亮，黑键不能按压、不能画指法点。
- 配色约定（全项目一致，新图必须沿用）：左手红 `#dc2626`、右手蓝 `#2563eb`、按下键绿 `#d1fae5`。
- [major-triads.md](file:///d:/Githubprojects/chords-keys-cookbook/docs/practice/major-triads.md) 练习方法章节（第 63 行起）：开头为五度圈顺序说明段（第 65 行），随后是「基础练习」表格。手型定义：
  - **手型一**：左手 3 指弹根音；右手 1-2-4 指弹 So-Do-Mi（五音-根音-三音）
  - **手型二**：左手 5 指根音 + 2 指五音；右手 1-2-3-5 指弹 Do-Mi-So-Do（根-三-五-高八度根）
- 输出目录 `docs/practice/` 已存在，SVG 与 md 同目录，相对路径引用即可。

## 三、关键决策（用户跳过了澄清提问，按以下方案执行，可在评审时调整）

| 决策点 | 选定方案 | 理由 |
|--------|---------|------|
| 分组与编号 | ① F·C·G ② D·A·E ③ B·F#·Db ④ Ab·Eb·Bb | 用户示例「FCG、DAE」即五度圈上连续三调（F→C→G 环绕顶部），余下依次为 B→F#→Db、Ab→Eb→Bb，恰好覆盖 12 调 |
| 每格样式 | **单条合并键盘**：左右手指法点画在同一键盘上（红=左手低把位，蓝=右手） | 3 列 × 2 行共 6 格，若每格再分双键盘会过宽过高；合并键盘更贴近真实手位，横向紧凑 |
| 脚本组织 | 新建 [gen_hand_groups.py](file:///d:/Githubprojects/chords-keys-cookbook/scripts/gen_hand_groups.py)，不动旧脚本 | 与 gen_circle.py / gen_hand_shapes.py 一脚本一产物的现有惯例一致 |
| 插入位置 | 「三、练习方法」开头五度圈说明段之后、「### 基础练习」之前，新增子节 | 分组图是后续按调练习的视觉总览，紧承五度圈段落逻辑 |

## 四、具体改动

### 1. 新建 `scripts/gen_hand_groups.py`

**（a）通用键盘引擎**（对旧脚本的核心泛化，支持移调与黑键按压）：

- 半音模型：`CHROMA = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']`，白键半音集 `{0,2,4,7,9,11}`。
- `build_keyboard(start_semi, top_semi)`：从起始白键半音开始生成白键序列（每个白键宽 `WHITE_W`），直到覆盖 `top_semi`；黑键按「白键非 E/B 则其后有黑键」规则定位（偏移量 = `WHITE_W×0.675`，与旧脚本 27/40 比例一致）。
- 起始键规则：根音为白键则从根音开始；根音为黑键（F#/Db/Ab/Eb/Bb）则从根音下方相邻白键开始（如 F#→F、Db→C、Bb→A）。
- 每个键记录 `(半音, x坐标, 是否黑键)`，供高亮与指法点定位查表。

**（b）缩放后的单元格尺寸**（6 格需紧凑，相对旧脚本 40px 白键等比缩小）：

```python
WHITE_W, WHITE_H = 24, 100
BLACK_W, BLACK_H = 15, 60
```

**（c）每格音域与指法数据**（固定音程，仅显示名随调变化）：

| 手型 | 左手 | 右手 | 音域（相对根音 R） |
|------|------|------|------|
| 手型一 | 3指→R | 1指→R+7（五）、2指→R+12（根）、4指→R+16（三） | R ~ R+16，约 10~11 白键 |
| 手型二 | 5指→R、2指→R+7 | 1指→R+12、2指→R+16、3指→R+19、5指→R+24 | R ~ R+24，约 15~16 白键 |

- 12 调三和弦构成音显式表（避免升/降记号歧义）：C-E-G、G-B-D、D-F#-A、A-C#-E、E-G#-B、B-D#-F#、F#-A#-C#、Db-F-Ab、Ab-C-Eb、Eb-G-Bb、Bb-D-F、F-A-C。黑键按压时的音名标签按调性用升号（C/G/D/A/E/B/F# 组）或降号（Db/Ab/Eb/Bb 组）。
- 按下键：绿填充高亮（黑键按压则黑键描边变绿/叠加绿框，保证可见）。
- 指法点：白键点 y≈70（黑键下方），黑键点 y≈30（黑键中部），半径 9，白字指法号。
- 键下方两行小字：音名（灰，9px）+ 功能名「根/三/五」（按手配色，9px 粗体）。
- 格顶标题：如「F 大调」（13px 粗体）。

**（d）整图布局**（每张 SVG）：

- 顶部标题：「第 N 组：X · Y · Z」（18px）。
- 左侧行标签：手型一 / 手型二（13px，垂直居中于各行）。
- 列槽宽统一 400px（按手型二最大 16 白键 × 24 = 384 + 余量），手型一键盘在槽内水平居中；总宽 ≈ 70 + 3×400 + 30 ≈ 1300px。
- 行高 ≈ 190px（键盘 100 + 音名/功能名两行 + 格标题 + 间距），总高 ≈ 540px。
- 底部复用旧版图例（绿=按下的键、红=左手、蓝=右手）。
- 白底、Arial 字体，与现有 SVG 风格一致。

**（e）输出**：循环 4 组写入 `docs/practice/hand-group-1.svg` ~ `hand-group-4.svg`，脚本末尾打印完成信息（与旧脚本一致）。

### 2. 修改 `docs/practice/major-triads.md`

在第 65 行五度圈说明段之后、`### 基础练习（每个调）`之前插入：

```markdown
### 分组手型总览（五度圈四组）

12 个调按五度圈连续三调分为 4 组，每组一张图：3 列为同组三个调，2 行为手型一 / 手型二。

**第 1 组：F · C · G**

![第1组 F C G 手型示意](hand-group-1.svg)

**第 2 组：D · A · E**

![第2组 D A E 手型示意](hand-group-2.svg)

**第 3 组：B · F# · Db**

![第3组 B F# Db 手型示意](hand-group-3.svg)

**第 4 组：Ab · Eb · Bb**

![第4组 Ab Eb Bb 手型示意](hand-group-4.svg)
```

## 五、验证步骤

1. 运行 `python scripts/gen_hand_groups.py`，确认 4 个 SVG 生成且无报错。
2. 用 Python `xml.dom.minidom` 解析 4 个产物，确认 XML 合法。
3. 抽查关键坐标：以 D 大调（含黑键 F#）手型二为例，确认 F# 黑键高亮、蓝点落在黑键上；以 Bb 大调为例确认降号音名正确。
4. 检查 [major-triads.md](file:///d:/Githubprojects/chords-keys-cookbook/docs/practice/major-triads.md) 插入位置与相对路径（SVG 与 md 同目录，直接文件名引用）。
5. 确认图片实际视觉效果（浏览器/docsify 打开 major-triads.md）。
