# ============================================================
# 属七 turnaround 手位图（12 调）
# 2m7 → 5⁷ → 1maj7 → 6⁷ → 2m7 → 5⁷sus4 → 1maj7
# ============================================================

from pathlib import Path

# 复用 m7 进行脚本的绘制逻辑
from gen_m7_progression import (
    BASE,
    BLACK_X_OFFSET,
    BLACK_H,
    BLACK_W,
    FLAT_NAMES,
    LEFT_STROKE,
    LEGEND_H,
    MARGIN,
    PRESS_FILL,
    RIGHT_STROKE,
    ROW_DEGREE_Y,
    ROW_H,
    ROW_KEY_Y,
    ROW_NOTE_Y,
    ROW_TITLE_Y,
    SHARP_NAMES,
    SUBTITLE_Y,
    TITLE_Y,
    TONIC_INFO,
    TONICS,
    WHITE_H,
    WHITE_INDEX,
    WHITE_NAMES,
    WHITE_W,
    count_whites,
    degree_note_names,
    draw_chromatic_keyboard,
    draw_legend,
    finger_dot,
    is_white,
)

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'dom7-progressions'

# 相对「该和弦根音」的 voicing（收缩型为主）
VOICINGS = {
    'm7': [
        (-12, 3, 'L', '根音'),
        (-5, 1, 'L', '五音'),
        (-2, 1, 'R', '七音'),
        (3, 2, 'R', '三音'),
        (7, 4, 'R', '五音'),
    ],
    'dom7': [
        (-12, 3, 'L', '根音'),
        (-5, 1, 'R', '五音'),
        (-2, 2, 'R', '七音'),
        (4, 4, 'R', '三音'),
    ],
    'maj7': [
        (-12, 3, 'L', '根音'),
        (-5, 1, 'R', '五音'),
        (-1, 2, 'R', '七音'),
        (4, 4, 'R', '三音'),
    ],
    'dom7sus4': [
        (-12, 3, 'L', '根音'),
        (-5, 1, 'R', '五音'),
        (-2, 2, 'R', '七音'),
        (5, 4, 'R', '四音'),
    ],
}

# (级数标签, 类型, 大调级数半音偏移)
STEPS = [
    ('2m7', 'm7', 2),
    ('5⁷', 'dom7', 7),
    ('1maj7', 'maj7', 0),
    ('6⁷', 'dom7', 9),
    ('2m7', 'm7', 2),
    ('5⁷sus4', 'dom7sus4', 7),
    ('1maj7', 'maj7', 0),
]

SUFFIX = {'m7': 'm7', 'dom7': '7', 'maj7': 'maj7', 'dom7sus4': '7sus4'}


def root_name(key_off, semi, mode):
    from gen_m7_progression import note_name
    return note_name((key_off + semi) % 12, mode)


def chord_name_for(key_off, kind, semi, mode):
    r = root_name(key_off, semi, mode)
    return f'{r}{SUFFIX[kind]}'


def build_step_chord(key_offset, step):
    _label, kind, semi = step
    notes = VOICINGS[kind]
    rels = [rel for rel, _, _, _ in notes]
    return {
        'degree': _label,
        'kind': kind,
        'root_semi': semi,
        'notes': notes,
        'range': (min(rels) - 1, max(rels) + 1),
    }


def draw_row(svg, W, key_tonic, chord, row_idx, mode):
    key_off = TONIC_INFO[key_tonic][0]
    root_off = chord['root_semi']
    row_top = SUBTITLE_Y + 14 + row_idx * ROW_H

    cname = chord_name_for(key_off, chord['kind'], root_off, mode)
    svg.append(
        f'<text x="{MARGIN}" y="{row_top + ROW_TITLE_Y}" font-family="Arial,sans-serif" '
        f'font-size="16" font-weight="bold" fill="#2c3e50">{chord["degree"]} = {cname}</text>'
    )

    start = BASE + key_off + root_off + chord['range'][0]
    end = BASE + key_off + root_off + chord['range'][1]
    abs_notes = [
        (BASE + key_off + root_off + rel, finger, side)
        for rel, finger, side, _ in chord['notes']
    ]
    highlights = {p for p, _, _ in abs_notes}

    n_white = count_whites(start, end)
    x0 = (W - n_white * WHITE_W) / 2
    centers = draw_chromatic_keyboard(svg, x0, row_top + ROW_KEY_Y, start, end, highlights, mode)

    for rel, finger, side, deg in chord['notes']:
        p = BASE + key_off + root_off + rel
        cx, cy = centers[p]
        if not is_white(p):
            cy = row_top + ROW_KEY_Y + BLACK_H - 16
        color = LEFT_STROKE if side == 'L' else RIGHT_STROKE
        finger_dot(svg, cx, cy, color, str(finger))
        svg.append(
            f'<text x="{cx:.1f}" y="{row_top + ROW_DEGREE_Y}" text-anchor="middle" '
            f'font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="{color}">{deg}</text>'
        )
    return x0


def build_single_svg(key_tonic):
    offset, mode = TONIC_INFO[key_tonic]

    chords = [build_step_chord(offset, s) for s in STEPS]

    max_white = 0
    for ch in chords:
        s = BASE + offset + ch['root_semi'] + ch['range'][0]
        e = BASE + offset + ch['root_semi'] + ch['range'][1]
        max_white = max(max_white, count_whites(s, e))
    W = int(2 * MARGIN + max_white * WHITE_W)
    H = SUBTITLE_Y + 14 + ROW_H * len(chords) + LEGEND_H + 6

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{W/2}" y="{TITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" '
        f'font-size="18" font-weight="bold" fill="#2c3e50">{key_tonic} 大调 · ii–V 属七 turnaround</text>',
        f'<text x="{W/2}" y="{SUBTITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" '
        f'font-size="12" fill="#888">收缩型手型 · 每行一个换和弦点</text>',
    ]

    first_x0 = None
    for i, ch in enumerate(chords):
        x0 = draw_row(svg, W, key_tonic, ch, i, mode)
        if first_x0 is None:
            first_x0 = x0

    legend_y = SUBTITLE_Y + 14 + ROW_H * len(chords) + LEGEND_H - 8
    draw_legend(svg, first_x0 if first_x0 else MARGIN, legend_y)
    svg.append('</svg>')

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f'{key_tonic}-progression.svg'
    path.write_text('\n'.join(svg), encoding='utf-8')
    print(f'{path.name} done')


if __name__ == '__main__':
    for t in TONICS:
        build_single_svg(t)
    print('All 12 dom7 turnaround progression SVGs generated!')
