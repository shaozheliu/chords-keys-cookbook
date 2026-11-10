# ============================================================
# 1564 色彩进行手位图（12 调）
# 骨架：1add9 → 5（大三扩张）→ 6m7（手型二）→ 4（薄手型），节奏级数仍标 5/7 / 6m7
# 输出：docs/assets/images/1564-progressions/{主音}-progression.svg
# ============================================================

from pathlib import Path

from gen_m7_progression import (  # noqa: E402
    BASE,
    LEGEND_H,
    MARGIN,
    PROGRESSION as _M7_PROG,
    ROW_DEGREE_Y,
    ROW_H,
    ROW_KEY_Y,
    ROW_TITLE_Y,
    SUBTITLE_Y,
    TITLE_Y,
    TONICS,
    TONIC_INFO,
    WHITE_H,
    count_whites,
    degree_note_names,
    draw_chromatic_keyboard,
    draw_legend,
    finger_dot,
    is_white,
)

# 复用 1add9 voicing；其余按 1564 级数偏移
PROGRESSION = [
    {**_M7_PROG[0], "degree": "1add9", "deg_offset": 0},
    {
        "degree": "5/7",
        "deg_offset": 7,
        "notes": [
            (-12, 5, "L", "根音"),
            (-5, 2, "L", "五音"),
            (0, 1, "R", "根音"),
            (4, 2, "R", "三音"),
            (7, 3, "R", "五音"),
            (12, 5, "R", "根音"),
        ],
        "range": (-12, 12),
    },
    {
        "degree": "6m7",
        "deg_offset": 9,
        "notes": [
            (-12, 5, "L", "根音"),
            (-5, 2, "L", "五音"),
            (0, 1, "L", "根音"),
            (3, 1, "R", "三音"),
            (7, 2, "R", "五音"),
            (10, 3, "R", "七音"),
            (15, 5, "R", "三音"),
        ],
        "range": (-12, 16),
    },
    {
        "degree": "4",
        "deg_offset": 5,
        "notes": [
            (-7, 3, "L", "根音"),
            (0, 1, "L", "五音"),
            (7, 1, "R", "三音"),
            (12, 2, "R", "五音"),
            (16, 5, "R", "根音"),
        ],
        "range": (-7, 16),
    },
]

def chord_display(tonic_name: str, chord: dict, names: dict[str, str]) -> tuple[str, str]:
    degree = chord["degree"]
    off = chord["deg_offset"]
    mode = TONIC_INFO[tonic_name][1]
    if degree == "1add9":
        return degree, f"{names[1]}add9"
    if degree == "5/7":
        return degree, names[5]
    if degree == "6m7":
        root = (TONIC_INFO[tonic_name][0] + off) % 12
        from gen_m7_progression import note_name

        return degree, f"{note_name(root, mode)}m7"
    if degree == "4":
        return degree, names[4]
    return degree, degree


def draw_row(svg, W, tonic_name, chord, row_idx, names):
    offset, mode = TONIC_INFO[tonic_name]
    row_top = SUBTITLE_Y + 14 + row_idx * ROW_H
    degree, chord_name = chord_display(tonic_name, chord, names)
    row_mode = mode

    svg.append(
        f'<text x="{MARGIN}" y="{row_top + ROW_TITLE_Y}" font-family="Arial,sans-serif" '
        f'font-size="16" font-weight="bold" fill="#2c3e50">{degree} = {chord_name}</text>'
    )

    deg_off = chord["deg_offset"]
    start = BASE + offset + deg_off + chord["range"][0]
    end = BASE + offset + deg_off + chord["range"][1]
    notes = [(BASE + offset + deg_off + rel, finger, side) for rel, finger, side, _ in chord["notes"]]
    highlights = {p for p, _, _ in notes}

    n_white = count_whites(start, end)
    x0 = (W - n_white * 40) / 2
    centers = draw_chromatic_keyboard(svg, x0, row_top + ROW_KEY_Y, start, end, highlights, row_mode)

    for rel, finger, side, deg in chord["notes"]:
        p = BASE + offset + deg_off + rel
        cx, cy = centers[p]
        if not is_white(p):
            cy = row_top + ROW_KEY_Y + 90 - 16
        color = "#dc2626" if side == "L" else "#2563eb"
        finger_dot(svg, cx, cy, color, str(finger))
        svg.append(
            f'<text x="{cx:.1f}" y="{row_top + ROW_DEGREE_Y}" text-anchor="middle" '
            f'font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="{color}">{deg}</text>'
        )
    return x0


def build_single_svg(tonic_name: str) -> None:
    offset, mode = TONIC_INFO[tonic_name]
    names = degree_note_names(offset, mode)

    max_white = 0
    for chord in PROGRESSION:
        deg_off = chord["deg_offset"]
        s = BASE + offset + deg_off + chord["range"][0]
        e = BASE + offset + deg_off + chord["range"][1]
        max_white = max(max_white, count_whites(s, e))
    W = int(2 * MARGIN + max_white * 40)
    H = SUBTITLE_Y + 14 + ROW_H * len(PROGRESSION) + LEGEND_H + 6

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{W/2}" y="{TITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" '
        f'font-size="18" font-weight="bold" fill="#2c3e50">{tonic_name} 大调 · 1564 色彩进行</text>',
        f'<text x="{W/2}" y="{SUBTITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" '
        f'font-size="12" fill="#888">1add9 → 5/7 → 6m7 → 4（5 扩张 · 6m7 手型二）</text>',
    ]

    first_x0 = None
    for i, chord in enumerate(PROGRESSION):
        x0 = draw_row(svg, W, tonic_name, chord, i, names)
        if first_x0 is None:
            first_x0 = x0

    legend_y = SUBTITLE_Y + 14 + ROW_H * len(PROGRESSION) + LEGEND_H - 8
    draw_legend(svg, first_x0 if first_x0 else MARGIN, legend_y)
    svg.append("</svg>")

    out = Path(__file__).resolve().parent.parent / "docs" / "assets" / "images" / "1564-progressions"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{tonic_name}-progression.svg"
    path.write_text("\n".join(svg), encoding="utf-8")
    print(path.name, "done")


if __name__ == "__main__":
    for t in TONICS:
        build_single_svg(t)
    print("All 12 × 1564 progression SVGs generated.")
