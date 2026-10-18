#!/usr/bin/env python3
"""属七 turnaround 四小节节奏型（每小节两和弦，对齐练习谱例）。"""

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'rhythm-patterns'
UNIT = 22
BEAT = UNIT * 4
BAR = BEAT * 4
LEFT = 60
RIGHT_PAD = 30
Y_TITLE = 30
Y_CHORD = 72
Y_NOTE = 124
Y_LINE1 = 134
Y_LINE2 = 142
Y_BAR_TOP = 52
Y_BAR_BOT = 146
GLYPH_HALF = 9

# 四小节：每小节 (和弦A, 和弦B)；B 可为 None 表示延音
BARS = [
    ('2m7', '5⁷'),
    ('1maj7', '6⁷'),
    ('2m7', '5⁷sus4'),
    ('1maj7', None),
]

# 每小节：X 的 unit 列表 + 下划线 (layer, u1, u2)，layer 1=八分 2=十六分
BAR_RHYTHMS = [
    {'units': [0, 1, 2, 3, 4, 8, 10, 12], 'lines': [(2, 0, 1), (2, 2, 4), (1, 8, 10)]},
    {'units': [0, 2, 4, 8, 10, 12, 14], 'lines': [(1, 0, 2), (1, 8, 10), (1, 12, 14)]},
    {'units': [0, 2, 4, 5, 6, 7, 8, 10, 12, 13, 14], 'lines': [(1, 0, 2), (2, 4, 7), (1, 8, 10), (2, 12, 14)]},
    {'units': [0], 'lines': []},
]


def x_center(bar_x, unit):
    return bar_x + unit * UNIT + UNIT / 2


def render():
    width = LEFT + BAR * len(BARS) + RIGHT_PAD
    height = 170
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="{Y_TITLE}" text-anchor="middle" font-family="Arial,sans-serif" '
        f'font-size="18" font-weight="bold" fill="#2c3e50">节奏型 · ii–V 属七 turnaround</text>',
        '',
        '<g font-family="Arial,sans-serif" font-size="16" fill="#2c3e50">',
    ]

    notes, lines, bar_lines = [], [], []

    for i, (ch_a, ch_b) in enumerate(BARS):
        bx = LEFT + i * BAR
        parts.append(f'  <text x="{bx + 8}" y="{Y_CHORD}" font-weight="bold">{ch_a}</text>')
        if ch_b:
            parts.append(f'  <text x="{bx + BEAT * 2 + 8}" y="{Y_CHORD}" font-weight="bold">{ch_b}</text>')
        else:
            for b in (1, 2, 3):
                parts.append(
                    f'  <text x="{bx + b * BEAT + BEAT / 2}" y="{Y_CHORD}" text-anchor="middle">—</text>'
                )

        rhythm = BAR_RHYTHMS[i]
        for u in rhythm['units']:
            notes.append(f'    <text x="{x_center(bx, u)}" y="{Y_NOTE}">X</text>')
        for layer, u1, u2 in rhythm['lines']:
            y = Y_LINE1 if layer == 1 else Y_LINE2
            lines.append(
                f'    <line x1="{x_center(bx, u1) - GLYPH_HALF}" y1="{y}" '
                f'x2="{x_center(bx, u2) + GLYPH_HALF}" y2="{y}"/>'
            )
        bar_lines.append(f'    <line x1="{bx}" y1="{Y_BAR_TOP}" x2="{bx}" y2="{Y_BAR_BOT}" stroke-width="1.5"/>')

    end_x = LEFT + BAR * len(BARS)
    bar_lines.append(f'    <line x1="{end_x}" y1="{Y_BAR_TOP}" x2="{end_x}" y2="{Y_BAR_BOT}" stroke-width="1.5"/>')
    bar_lines.append(f'    <line x1="{end_x + 7}" y1="{Y_BAR_TOP}" x2="{end_x + 7}" y2="{Y_BAR_BOT}" stroke-width="4"/>')

    parts += ['</g>', '',
              '<g font-family="\'Courier New\',monospace" font-size="22" font-weight="bold" fill="#111" text-anchor="middle">',
              *notes, '</g>', '',
              '<g stroke="#111" stroke-width="2.5" stroke-linecap="round">',
              *lines, '</g>', '',
              '<g stroke="#111">',
              *bar_lines, '</g>', '</svg>']

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / 'dom7-turnaround.svg'
    path.write_text('\n'.join(parts) + '\n', encoding='utf-8')
    print(f'Generated: {path}')


if __name__ == '__main__':
    render()
