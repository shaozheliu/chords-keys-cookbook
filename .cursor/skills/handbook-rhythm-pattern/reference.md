# 节奏型 skill 速查

权威格式：`reference/notation-format.md`

## 生成管线（唯一）

1. 拍型：`docs/rhythm-patterns/cells/canon.yaml` → `scripts/rhythm_cells.py` 的 `expand_beat`
2. 小节谱：`docs/rhythm-patterns/examples/*.yaml`（`rhythm-score/1`）或 Python `bars` dict（与 `gen_2516251_rhythm.py` 相同）
3. 渲染：`gen_rhythm_patterns.render_rhythm_score_v2`（layout v2）
4. 构建：`build_rhythm_patterns.py <target>`

## 十六八 / 八十六（符杠）

| id | 含义 | X | 下划线 |
|----|------|---|--------|
| `two-sixteenth-eighth` | 16+16+8 | 3 | 前两个 X **两道**线；第三个 X **一道**线 |
| `eighth-two-sixteenth` | 8+16+16 | 3 | 第一个 X **一道**线（八分跨 0–1）；后两个 X **两道**线 |

legacy v1 `PATTERNS` / `render(pattern)` 已移除；存量示范 SVG（如 `maj7-*.svg`）仅作教材引用，不再由脚本再生。
