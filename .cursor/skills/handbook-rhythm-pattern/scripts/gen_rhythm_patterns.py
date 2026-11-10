#!/usr/bin/env python3
"""生成节奏型 X 谱 SVG（级数和弦行 + X + 下划线/连音弧线）。

输出目录: docs/assets/images/rhythm-patterns/
规则: X = 一次弹奏；一道下划线 = 八分；两道 = 十六分；无下划线 ≈ 四分。
"""
from __future__ import annotations

from _paths import out_dir
import layout as layout_v2

# ---- 页面布局（layout v2）----
LEFT = 60
RIGHT_PAD = 30
Y_TITLE = 30
Y_CHORD = 72
Y_NOTE = 124
Y_LINE1 = 134
Y_LINE2 = 138
Y_LINE3 = 142
Y_BAR_TOP = 52
Y_BAR_BOT = 146
Y_TIE = 86

BEAM_YS = (Y_LINE1, Y_LINE2, Y_LINE3)


def _beam_line_ys(layers: int) -> list[float]:
    """layers: 1=八分一条线，2=十六分两条线，3=三十二分三条线。"""
    n = max(1, min(3, layers))
    return list(BEAM_YS[:n])


def _x_v2(bx: float, unit: int) -> float:
    return layout_v2.x_center(bx, unit)


def _tie_path_v2(bx: float, u1: int, u2: int, stroke: str = "#111") -> str:
    cx1, cx2 = _x_v2(bx, u1), _x_v2(bx, u2)
    mid = (cx1 + cx2) / 2
    return (
        f'    <path d="M {cx1} {Y_NOTE - 14} Q {mid} {Y_TIE} {cx2} {Y_NOTE - 14}" '
        f'fill="none" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def render_practice1_rhythm(title: str = "练习1", outfile: str = "lianxi-1-demo.svg") -> Path:
    """教材「练习1」— rhythm-score/1，级数 1add9 / 5/7 / 6m7（1564 色彩节奏）。"""
    glyph_half = layout_v2.SLOT_W / 2 + 1
    bars_spec = [
        {
            "chords": [(1, "1add9"), (3, "5/7")],
            "chord_holds": [2, 4],
            "xs": list(range(16)),
            "underlines": [(2, 0, 3), (2, 4, 7), (2, 8, 11), (2, 12, 15)],
            "ties": [(3, 4), (11, 12)],
            "rests": [],
        },
        {
            "chords": [(1, "6m7")],
            "chord_holds": [2, 3, 4],
            "xs": [0, 1, 2, 3],
            "quarters": [2],
            "underlines": [(2, 0, 3)],
            "ties": [],
            "rest_beats": [3, 4],
        },
    ]

    n_bars = len(bars_spec)
    for i in range(n_bars):
        layout_v2.assert_measure_padding(LEFT, i)
    width = layout_v2.bar_width(n_bars, LEFT, RIGHT_PAD)
    height = 170
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="{Y_TITLE}" text-anchor="middle" font-family="PingFang SC, Arial, sans-serif" '
        f'font-size="20" font-weight="bold" fill="#2c3e50">{title}</text>',
        "",
        '<g font-family="Arial,sans-serif" font-size="16" fill="#2c3e50">',
    ]

    notes, lines, bar_lines, tie_paths, rests = [], [], [], [], []

    barlines_x = layout_v2.barline_xs(LEFT, n_bars)

    for i, spec in enumerate(bars_spec):
        gx = layout_v2.rhythm_grid_left(LEFT, i)
        for beat, label in spec["chords"]:
            cx = layout_v2.symbol_x_chord(gx, beat)
            parts.append(
                f'  <text x="{cx}" y="{Y_CHORD}" text-anchor="middle" font-weight="bold">{label}</text>'
            )
        for beat in spec.get("chord_holds", []):
            parts.append(
                f'  <text x="{layout_v2.beat_center(gx, beat)}" y="{Y_CHORD}" text-anchor="middle">—</text>'
            )

        for u in spec["xs"]:
            notes.append(f'    <text x="{layout_v2.symbol_x_rhythm(gx, u)}" y="{Y_NOTE}">X</text>')
        for beat in spec.get("quarters", []):
            notes.append(
                f'    <text x="{layout_v2.rhythm_quarter_x(gx, beat)}" y="{Y_NOTE}">X</text>'
            )
        for layer, u1, u2 in spec["underlines"]:
            for y in _beam_line_ys(layer):
                lines.append(
                    f'    <line x1="{_x_v2(gx, u1) - glyph_half}" y1="{y}" '
                    f'x2="{_x_v2(gx, u2) + glyph_half}" y2="{y}"/>'
                )
        for u1, u2 in spec["ties"]:
            if u2 < 16:
                tie_paths.append(_tie_path_v2(gx, u1, u2))
        for beat in spec.get("rest_beats", []):
            rests.append(
                f'    <text x="{layout_v2.rhythm_rest_x(gx, beat)}" y="{Y_NOTE}" '
                f'font-family="Arial,sans-serif" font-size="18" fill="#333">—</text>'
            )
        for u in spec.get("rests", []):
            rests.append(
                f'    <text x="{layout_v2.symbol_x_rhythm(gx, u)}" y="{Y_NOTE}" '
                f'font-family="Arial,sans-serif" font-size="18" fill="#333">—</text>'
            )

    for bx in barlines_x:
        bar_lines.append(
            f'    <line x1="{bx}" y1="{Y_BAR_TOP}" x2="{bx}" y2="{Y_BAR_BOT}" '
            f'stroke="#64748b" stroke-width="1.5"/>'
        )

    parts += [
        "</g>",
        "",
        '<g font-family="\'Courier New\',monospace" font-size="22" font-weight="bold" fill="#111" text-anchor="middle">',
        *notes,
        "</g>",
        "",
        '<g font-family="Arial,sans-serif" font-size="18" fill="#333" text-anchor="middle">',
        *rests,
        "</g>",
        "",
        '<g stroke="#111" stroke-width="2.5" stroke-linecap="round">',
        *lines,
        "</g>",
        "",
        "<g>",
        *tie_paths,
        "</g>",
        "",
        '<g stroke="#64748b">',
        *bar_lines,
        "</g>",
        "</svg>",
    ]

    dest = out_dir()
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / outfile
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(path)
    return path


def render_exercise_1() -> Path:
    return render_practice1_rhythm("练习1", "lianxi-1-demo.svg")


def render_rhythm_score_v2(
    title: str,
    outfile: str,
    bars_spec: list[dict],
) -> Path:
    """rhythm-score/1 + layout v2（与练习1 同渲染管线）。"""
    from rhythm_cells import expand_beat, merge_beat_specs

    glyph_half = layout_v2.SLOT_W / 2 + 1
    compiled: list[dict] = []

    for bar in bars_spec:
        beat_ids = bar["beats"]
        merged = merge_beat_specs([expand_beat(cid, i + 1) for i, cid in enumerate(beat_ids)])
        compiled.append(
            {
                "chords": bar["chords"],
                "chord_holds": bar.get("chord_holds", []),
                "xs": merged["xs"],
                "underlines": merged["underlines"],
                "quarters": merged["quarters"],
                "ties": bar.get("ties", []),
                "rest_beats": merged["rest_beats"],
                "rests": bar.get("rests", []),
            }
        )

    n_bars = len(compiled)
    for i in range(n_bars):
        layout_v2.assert_measure_padding(LEFT, i)
    width = layout_v2.bar_width(n_bars, LEFT, RIGHT_PAD)
    height = 170
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="{Y_TITLE}" text-anchor="middle" font-family="PingFang SC, Arial, sans-serif" '
        f'font-size="18" font-weight="bold" fill="#2c3e50">{title}</text>',
        "",
        '<g font-family="Arial,sans-serif" font-size="16" fill="#2c3e50">',
    ]

    notes, lines, bar_lines, tie_paths, rests = [], [], [], [], []
    barlines_x = layout_v2.barline_xs(LEFT, n_bars)

    for i, spec in enumerate(compiled):
        gx = layout_v2.rhythm_grid_left(LEFT, i)
        for beat, label in spec["chords"]:
            parts.append(
                f'  <text x="{layout_v2.symbol_x_chord(gx, beat)}" y="{Y_CHORD}" '
                f'text-anchor="middle" font-weight="bold">{label}</text>'
            )
        for beat in spec.get("chord_holds", []):
            parts.append(
                f'  <text x="{layout_v2.beat_center(gx, beat)}" y="{Y_CHORD}" text-anchor="middle">—</text>'
            )

        for u in spec["xs"]:
            notes.append(f'    <text x="{layout_v2.symbol_x_rhythm(gx, u)}" y="{Y_NOTE}">X</text>')
        for beat in spec.get("quarters", []):
            notes.append(
                f'    <text x="{layout_v2.rhythm_quarter_x(gx, beat)}" y="{Y_NOTE}">X</text>'
            )
        for layer, u1, u2 in spec["underlines"]:
            for y in _beam_line_ys(layer):
                lines.append(
                    f'    <line x1="{_x_v2(gx, u1) - glyph_half}" y1="{y}" '
                    f'x2="{_x_v2(gx, u2) + glyph_half}" y2="{y}"/>'
                )
        for u1, u2 in spec.get("ties", []):
            if u2 < 16:
                tie_paths.append(_tie_path_v2(gx, u1, u2))
        for beat in spec.get("rest_beats", []):
            rests.append(
                f'    <text x="{layout_v2.rhythm_rest_x(gx, beat)}" y="{Y_NOTE}" '
                f'font-family="Arial,sans-serif" font-size="18" fill="#333">—</text>'
            )
        for u in spec.get("rests", []):
            rests.append(
                f'    <text x="{layout_v2.symbol_x_rhythm(gx, u)}" y="{Y_NOTE}" '
                f'font-family="Arial,sans-serif" font-size="18" fill="#333">—</text>'
            )

    for bx in barlines_x:
        bar_lines.append(
            f'    <line x1="{bx}" y1="{Y_BAR_TOP}" x2="{bx}" y2="{Y_BAR_BOT}" '
            f'stroke="#64748b" stroke-width="1.5"/>'
        )

    parts += [
        "</g>",
        "",
        '<g font-family="\'Courier New\',monospace" font-size="22" font-weight="bold" fill="#111" text-anchor="middle">',
        *notes,
        "</g>",
        "",
        '<g font-family="Arial,sans-serif" font-size="18" fill="#333" text-anchor="middle">',
        *rests,
        "</g>",
        "",
        '<g stroke="#111" stroke-width="2.5" stroke-linecap="round">',
        *lines,
        "</g>",
        "",
        "<g>",
        *tie_paths,
        "</g>",
        "",
        '<g stroke="#64748b">',
        *bar_lines,
        "</g>",
        "</svg>",
    ]

    dest = out_dir()
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / outfile
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(path)
    return path


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "exercise-1":
        render_exercise_1()
    else:
        print("Usage: gen_rhythm_patterns.py exercise-1", file=sys.stderr)
        sys.exit(1)
