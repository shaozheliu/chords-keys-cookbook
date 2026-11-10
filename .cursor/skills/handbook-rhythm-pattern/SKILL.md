---
name: handbook-rhythm-pattern
description: >-
  Generates handbook rhythm-pattern SVGs (Nashville chord row + X grid, underlines,
  ties)—not staff notation. Use for 练习节奏型示意图, progression rhythmSvg assets, or
  new pattern definitions under docs/rhythm-patterns/. Do NOT use handbook-staff-score
  or mcp-score for this product.
---

# Handbook rhythm pattern (X 谱)

## 与五线谱 / MCP 分工（必遵守）

| 用户要什么 | 用本 Skill | 不要用 |
|------------|-----------|--------|
| 级数和弦 + **X** + 下划线/连音弧线示意 | `build_rhythm_patterns.py` / `render()` | `handbook-staff-score`, **mcp-score** |
| 钢琴五线谱、MusicXML、织体 PNG | `handbook-staff-score` | 本 Skill |
| 虫虫整曲弹唱 PDF | 外部 XML + `annotate_musicxml_from_accompaniment.py` | 两者混用 |
| MuseScore 里试写、改活谱 | **mcp-score**（可选） | 本 Skill |

**禁止**：用 MusicXML 或 MCP 生成 X 节奏型；用 `sheet.yaml` 的 `jianpu` 冒充节奏型图（那是五线谱音高源稿）。

---

## 产物

- **输出目录**：`docs/assets/images/rhythm-patterns/*.svg`
- **站点引用**：`docs/data/progressions.json` 的 `rhythmSvg`、每日练习 Markdown 的 `![节奏型](...)`

---

## Skill 包位置

| 内容 | 路径 |
|------|------|
| 说明 | `.cursor/skills/handbook-rhythm-pattern/SKILL.md` |
| **标准表达格式（必读）** | `.cursor/skills/handbook-rhythm-pattern/reference/notation-format.md` |
| 速查 / legacy API | `reference.md` |
| 管线脚本 | `scripts/`（`layout.py` = v2 拍间距） |
| 单拍型注册表 | `docs/rhythm-patterns/cells/canon.yaml` |
| 小节谱源稿 | `docs/rhythm-patterns/examples/*.yaml` |
| 构建索引 | `docs/rhythm-patterns/index.json` |

12 调具体和弦名依赖仓库根目录 `scripts/gen_*_progression.py`（键盘进行图生成器里的 `TONIC_INFO` / `note_name`），**不**搬进本 skill。

---

## 记谱规则（摘要）

完整定义见 **[notation-format.md](reference/notation-format.md)**：

1. **`rhythm-cell/1`**：一拍内的标准型（四、二八、八十六…三连音），DSL 如 `8+16+16`、`16x4`、`8t3`。
2. **`rhythm-score/1`**：多小节 + `chords` + 每拍 cell + `ties` / `rests`；**`layout: v2`**（拍内 `SLOT_W`、拍间 `BEAT_GAP`）。
3. **Legacy v1**：`PATTERNS` + 均匀 `fixed_units`（仅维护旧图）。

Agent 写新练习图时：**先 YAML（rhythm-score/1），再编译 SVG**；不要直接堆 flat unit 除非过渡。

---

## 构建命令

```bash
python .cursor/skills/handbook-rhythm-pattern/scripts/build_rhythm_patterns.py exercise-1
python .cursor/skills/handbook-rhythm-pattern/scripts/build_rhythm_patterns.py 1564-12
python .cursor/skills/handbook-rhythm-pattern/scripts/build_rhythm_patterns.py 2516251
python .cursor/skills/handbook-rhythm-pattern/scripts/build_rhythm_patterns.py all
```

新进行图：在 `docs/rhythm-patterns/examples/*.yaml` 写 `rhythm-score/1`，在 `scripts/` 增加薄入口调用 `render_rhythm_score_v2`；拍型用 `rhythm_cells.expand_beat`（对齐 `cells/canon.yaml`）。

---

## Agent 工作流

1. 确认用户要 **节奏型示意**（非五线谱）→ 读本 Skill。
2. 查 `docs/rhythm-patterns/index.json` 是否已有 target。
3. 新图：YAML + `rhythm_cells.py` + `render_rhythm_score_v2`；**禁止** legacy `fixed_units` v1。
4. 若站点要挂链：更新 `progressions.json` / 对应 Markdown 的 `rhythmSvg` 路径（相对 `assets/images/…`）。
5. **不要** 调 mcp-score  unless 用户同时要五线谱。

---

## 参考

- [reference.md](reference.md) — `pattern` dict 字段
- [handbook-staff-score](../handbook-staff-score/SKILL.md) — 五线谱管线
