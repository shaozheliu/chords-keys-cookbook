# sus2 挂留二和弦 文档与图片生成计划

## 一、目标

新增「挂留二和弦（sus2）」练习文档与 24 张键盘手型示意图，复用大三/小三已建立的「四节结构 + 五度圈分组」框架，但按 sus2 的两种手型特征与「单一排列」口径编写。

## 二、现状分析

- `docs/practice/` 已有 `daily-routine.md` / `major-triads.md` / `minor-triads.md`；尚无任何 sus 文档（`sus-chords.md` 未创建）。
- `scripts/` 已有 `gen_circle.py` / `gen_major_hand_groups.py` / `gen_minor_hand_groups.py`。其中 `gen_minor_hand_groups.py` 已含 `import os` + `os.makedirs(exist_ok=True)`，是最佳复制模板（自包含、无跨脚本 import，符合用户「不耦合」要求）。
- `docs/assets/images/` 已有 `common/` / `major-triads/` / `minor-triads/`；尚无 `sus2-chords/`。
- `docs/_sidebar.md` 第 22 行、`docs/practice/daily-routine.md` 第 68 行各有一处「挂留和弦 → sus-chords.md」合并口径引用，需改为 sus2。

## 三、拟改动

### 1. 新建 `scripts/gen_sus2_hand_groups.py`（自包含脚本）

复制 `gen_minor_hand_groups.py` 的整体结构（函数、配色、键盘渲染、布局常量全部保留），仅改以下关键部分：

**头部注释**：改为「十二调挂留二和弦手型图生成器」，说明 `sus2 = 根音 + 大二度(+2) + 纯五度(+7)`。

**TONIC_INFO**：与大三脚本一致（`C/G/D/A/E/B/F = 'sharp'`；`F#/Db/Ab/Eb/Bb = 'flat'`）。因 sus2 无三音、不引入降三音，无需像小三那样把 C/G/F 改为 flat。

**HANDS 手型定义**：

手型一（紧凑型）——左手根音不变，右手 so-do-re（1-2-3 指）：

```python
{
    'label': '紧凑型',
    'sub': '手型一',
    'desc': '左手 3指(根音) ｜ 右手 1-2-3指 五音-根音-二音',
    'notes': [
        (-12, 3, 'L'),   # 左手根音（低八度）
        (-5, 1, 'R'),    # 右手五音（so）
        (0, 2, 'R'),     # 右手根音（do）
        (2, 3, 'R'),     # 右手二音（re）
    ],
    'range': (-12, 12),
}
```

手型二（扩张型）——左手 do-so-do（5-2-1 指），右手 re-so-re（1-2-5 指）：

```python
{
    'label': '扩张型',
    'sub': '手型二',
    'desc': '左手 5-2-1指 根音-五音-高八度根音 ｜ 右手 1-2-5指 二音-五音-高八度二音',
    'notes': [
        (-12, 5, 'L'),   # 左手根音（do，低八度）
        (-5, 2, 'L'),    # 左手五音（so）
        (0, 1, 'L'),     # 左手高八度根音（do）
        (2, 1, 'R'),     # 右手二音（re）
        (7, 2, 'R'),     # 右手五音（so）
        (14, 5, 'R'),    # 右手高八度二音（re）
    ],
    'range': (-12, 14),
}
```

**音级标注映射**：`{0: '根音', 2: '二音', 7: '五音'}`（替换小三的 `{0, 3, 7}`）。

**标题**：`f'{tonic_name}sus2 · {hand["label"]}（{hand["sub"]}）'`（如 `Csus2 · 紧凑型（手型一）`）。

**输出目录**：`docs\assets\images\sus2-chords\`。

**收尾打印**：`All 24 sus2 SVGs generated!`。

保留 `import os` 与 `os.makedirs(os.path.dirname(path), exist_ok=True)`。

### 2. 新建 `docs/practice/sus2-chords.md`

结构对齐 major/minor 四节，但手型一为「单一排列」（不展开三种转位）：

- **一、和弦结构**：根音 + 大二度 + 纯五度；示例 `Csus2 = C - D - G`；注明「sus2 用二音替代三音，无大小之分」。
- **二、手型与弹奏位置**：
  - 手型一：左手根音（3 指）不变，右手 so-do-re（五音-根音-二音），1-2-3 指；示意 `../assets/images/sus2-chords/C-hand-shape-1.svg`。
  - 手型二：左手 do-so-do（5-2-1 指），右手 re-so-re（1-2-5 指）；示意 `../assets/images/sus2-chords/C-hand-shape-2.svg`。
  - 两种手型对比表。
- **三、练习分组**：五度圈五组周轮动（周一 F/C/G、周二 D/A/E、周三~周四 B/F#/Db、周五~周六 Ab/Eb/Bb、周日全量），图片引用 `sus2-chords/{调名}-hand-shape-{1|2}.svg`（F# 用 `F%23`）。
- **四、练习步骤**：纵向（手型一 so-do-re → 手型二扩张型，先柱式后琶音）→ 横向（五度圈移调）→ 视唱练耳（引用 [daily-routine.md](daily-routine.md) 贯穿原则，唱级数 1-2-5）。

### 3. 修改 `docs/_sidebar.md`

第 22 行：

```
- [挂留和弦](practice/sus-chords.md)
```
改为：
```
- [挂留二和弦（sus2）](practice/sus2-chords.md)
```

### 4. 修改 `docs/practice/daily-routine.md`

第 68 行模块表：

```
| 色彩和弦 | [挂留和弦](sus-chords.md) | 10 min |
```
改为：
```
| 色彩和弦 | [挂留二和弦（sus2）](sus2-chords.md) | 10 min |
```

## 四、假设与决策

1. 文件命名：`sus2-chords.md` 独立（用户已确认），图片目录 `sus2-chords/`；为将来 `sus4-chords.md` 留位。
2. 手型一：单一排列 so-do-re（用户已确认），不展开三种转位。
3. 和弦符号：标题与文档统一用「Csus2」风格（如 `Csus2` / `F#sus2` / `Dbsus2`）。
4. 黑键标注风格：sus2 无降三音，TONIC_INFO 与大三一致（sharp/flat 按调号）。
5. 图片仍放 `docs/assets/images/` 内部，兼容 GitHub Pages 部署。

## 五、验证

1. 运行 `python scripts\gen_sus2_hand_groups.py`，输出 24 条 done、无报错；`docs/assets/images/sus2-chords/` 出现 24 张 svg。
2. 抽查 `Csus2` 两张图：标题「Csus2 · 紧凑型/扩张型」；手型一指法 1-2-3（G-C-D）；手型二 6 音（C-G-C + D-G-D）；音级标注 根音/二音/五音。
3. 抽查 `F#sus2`（`F%23` 编码）与 `Dbsus2` 黑键标注正确。
4. `_sidebar.md` / `daily-routine.md` 链接均指向 `sus2-chords.md`，无残留 `sus-chords.md` 引用。
