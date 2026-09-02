#!/usr/bin/env python3
"""生成节奏型 X 谱 SVG（简谱式：下划线表示音值，弧线表示跨拍连音）。

输出:
  docs/assets/images/rhythm-patterns/maj7-4-88-4-1616-8.svg     大七和弦四小节节奏
  docs/assets/images/rhythm-patterns/add9-m7-8x8-tie.svg        小七和弦四小节节奏
规则: X = 一次弹奏；一道下划线 = 八分音符；两道 = 十六分音符；无下划线 = 四分音符。
"""
import os

OUT_DIR = 'docs/assets/images/rhythm-patterns'

# ---- 布局常量（间距标准化：以十六分音符为基本网格） ----
UNIT = 22            # 一个十六分音符的宽度
BEAT = UNIT * 4      # 一拍
BAR = BEAT * 4       # 一小节
LEFT = 60            # 左边距
RIGHT_PAD = 30       # 结尾双线后留白
Y_TITLE = 30
Y_CHORD = 72
Y_NOTE = 124         # X 基线
Y_LINE1 = 134        # 第一道下划线
Y_LINE2 = 142        # 第二道下划线
Y_BAR_TOP = 52
Y_BAR_BOT = 146
Y_TIE = 100          # 连音弧线最高点（X 上方）
GLYPH_HALF = 9       # X 字形半宽（下划线端点余量）

# ---- 节奏模式（每个 = 一套小节的网格布局） ----
# bar 网格: 每小节的 (X 位置列表, [(下划线层, 起始, 结束)])，全局 unit 坐标
# ties: 跨小节/跨拍的连音对 (起始 unit, 结束 unit)
PATTERNS = {
    'maj7': {
        'title': '节奏型示例',
        'out': 'maj7-4-88-4-1616-8.svg',
        # 第1拍(4分)、第2拍(两个8分)、第3拍(4分) 固定；第4拍三种变体
        'fixed_units': [0, 4, 6, 8],
        'fixed_lines': [(1, 4, 6)],
        'variants': {
            'basic':    ([12, 13, 14], [(1, 12, 14), (2, 12, 13)]),   # 16-16-8
            'four16':   ([12, 13, 14, 15], [(1, 12, 15), (2, 12, 15)]),  # 四个16分
            'u8_16_16': ([12, 14, 15], [(1, 12, 15), (2, 14, 15)]),   # 前8后16
        },
        'bars': [  # (和弦名, 末拍变体)
            ('1maj7', 'basic'),
            ('4maj7', 'four16'),
            ('1maj7', 'u8_16_16'),
            ('4maj7', 'four16'),
        ],
        'ties': [],
    },
    'add9': {
        'title': '节奏型示例',
        'out': 'add9-m7-8x8-tie.svg',
        # 8 个八分音符一拍一个，两两共用下划线；第 3、4 音之间加跨拍连音线
        'fixed_units': [0, 2, 4, 6, 8, 10, 12, 14],
        'fixed_lines': [(1, 0, 2), (1, 4, 6), (1, 8, 10), (1, 12, 14)],
        'variants': {'': ([], [])},
        'bars': [
            ('1add9', ''),
            ('3m7', ''),
            ('4sus2', ''),
            ('5sus4', ''),
        ],
        # 第 3、4 个八分音符（全局 unit 6、8）跨第 2/3 拍连接
        'ties': [(6, 8)],
    },
}


def x_center(bar_x, unit):
    return bar_x + unit * UNIT + UNIT / 2


def render(pattern):
    fixed_units = pattern['fixed_units']
    fixed_lines = pattern['fixed_lines']
    variants = pattern['variants']
    bars = pattern['bars']
    ties = pattern['ties']

    width = LEFT + BAR * len(bars) + RIGHT_PAD
    height = 170
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="{Y_TITLE}" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#2c3e50">{pattern["title"]}</text>',
        '',
        '<!-- 和弦行 -->',
        '<g font-family="Arial,sans-serif" font-size="17" fill="#2c3e50">',
    ]

    notes, lines, bar_lines, tie_paths = [], [], [], []
    for i, (chord, variant) in enumerate(bars):
        bx = LEFT + i * BAR
        # 和弦名 + 后三拍保持线
        parts.append(f'  <text x="{bx + 10}" y="{Y_CHORD}" font-weight="bold">{chord}</text>')
        for b in (1, 2, 3):
            parts.append(f'  <text x="{bx + b * BEAT + BEAT / 2}" y="{Y_CHORD}" text-anchor="middle">—</text>')

        units = fixed_units + variants[variant][0]
        u_lines = fixed_lines + variants[variant][1]
        for u in units:
            notes.append(f'    <text x="{x_center(bx, u)}" y="{Y_NOTE}">X</text>')
        for layer, u1, u2 in u_lines:
            y = Y_LINE1 if layer == 1 else Y_LINE2
            lines.append(f'    <line x1="{x_center(bx, u1) - GLYPH_HALF}" y1="{y}" x2="{x_center(bx, u2) + GLYPH_HALF}" y2="{y}"/>')
        bar_lines.append(f'    <line x1="{bx}" y1="{Y_BAR_TOP}" x2="{bx}" y2="{Y_BAR_BOT}" stroke-width="1.5"/>')

    end_x = LEFT + BAR * len(bars)
    bar_lines.append(f'    <line x1="{end_x}" y1="{Y_BAR_TOP}" x2="{end_x}" y2="{Y_BAR_BOT}" stroke-width="1.5"/>')
    bar_lines.append(f'    <line x1="{end_x + 7}" y1="{Y_BAR_TOP}" x2="{end_x + 7}" y2="{Y_BAR_BOT}" stroke-width="4"/>')

    # 连音弧线（跨拍 tie，画在 X 上方）
    for u1, u2 in ties:
        cx1, cx2 = x_center(LEFT, u1), x_center(LEFT, u2)
        mid = (cx1 + cx2) / 2
        tie_paths.append(
            f'    <path d="M {cx1} {Y_NOTE - 14} Q {mid} {Y_TIE} {cx2} {Y_NOTE - 14}" '
            f'fill="none" stroke="#c0392b" stroke-width="2.5" stroke-linecap="round"/>')

    parts += ['</g>', '',
              '<!-- 节奏行：X -->',
              '<g font-family="\'Courier New\',monospace" font-size="22" font-weight="bold" fill="#111" text-anchor="middle">',
              *notes, '</g>', '',
              '<!-- 下划线：一道=八分，两道=十六分 -->',
              '<g stroke="#111" stroke-width="2.5" stroke-linecap="round">',
              *lines, '</g>', '',
              '<!-- 跨拍连音线 -->',
              '<g>',
              *tie_paths, '</g>', '',
              '<!-- 小节线 -->',
              '<g stroke="#111">',
              *bar_lines, '</g>', '</svg>']

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, pattern['out'])
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts) + '\n')
    print(f'Generated: {path}')


if __name__ == '__main__':
    for p in PATTERNS.values():
        render(p)
