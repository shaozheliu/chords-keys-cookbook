# ============================================================
# 功能谱（和弦谱）SVG 生成器 —— 《出现又离开》主歌（一）
#
# 设计：每行 4 小节网格；和弦（18px 粗）/ 级数（11px 灰）/ 歌词（13px）
# 三层左对齐到小节起点；转位低音（slash 后的音）标红；主歌标志性的
# 低音 1-7-6 下行级进用红点连线画出。
#
# 纯 Python 手写 SVG，零第三方依赖，与项目现有脚本同构。
# 输出：docs/assets/images/songs/chuxian-you-likai-chart.svg
# 自包含，不 import 其他脚本。
# ============================================================

from pathlib import Path
from xml.sax.saxutils import escape

# 配色（红/蓝沿用项目约定）
INK = '#1f2937'          # 和弦/标题（深）
LYRIC = '#374151'        # 歌词
MUTE = '#9ca3af'         # 级数/注解（灰）
GRID = '#e5e7eb'         # 小节线
ROW_BG = '#f9fafb'       # 隔行底色
ACCENT = '#dc2626'       # 强调红：转位低音、低音级进
SECTION_BLUE = '#2563eb' # 段落色条

FONT = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif"

# 布局常量
LEFT = 24                # 左边距（网格与段落色条共用）
CELL_W = 150             # 小节宽
CELL_PAD = 12            # 小节内文字左缩进
CHORD_SIZE = 18
DEGREE_SIZE = 11
LYRIC_SIZE = 13
ROW_H = 58               # 无低音线行高
BASS_H = 22              # 低音级进带附加高度

# ------------------------------------------------------------
# 数据：主歌（一）16 小节（前 8 小节和弦由用户提供；后 8 小节同型反复，
# 第 4 个和弦统一按用户给的 Asus2/E，与文档表格的教学简化写法 E 不同）
# ------------------------------------------------------------
TITLE = '出现又离开 · 功能谱（主歌一）'
SUBTITLE = 'A 大调 · 4/4 · ♩≈80 ｜ 和弦 / 级数 / 歌词 三层对位'

SECTIONS = [
    {
        'name': '主歌（一）',
        'note': '平静的叙述 · 分解',
        'rows': [
            {'bass': True, 'cells': [
                ('A', '1', '我和你'),
                ('E/G#', '5/7', '本应该'),
                ('F#m', '6m', '各自好'),
                ('Asus2/E', '5', '各自坏'),
            ]},
            {'cells': [
                ('D', '4', '各自生活的'),
                ('A', '1', '自在'),
                ('D', '4', '毫无关联的'),
                ('E', '5', '存在'),
            ]},
            {'bass': True, 'tag': '第二遍', 'cells': [
                ('A', '1', '直到你'),
                ('E/G#', '5/7', '出现在'),
                ('F#m', '6m', '我眼中'),
                ('Asus2/E', '5', '躲不开'),
            ]},
            {'cells': [
                ('D', '4', '我也占领你的'),
                ('A', '1', '心海'),
                ('D', '4', '充实着你的'),
                ('E', '5', '空白'),
            ]},
        ],
    },
]

LEGEND = [('●', ACCENT), (' 低音级进（1–7–6 下行）　　', MUTE),
          ('G♯', ACCENT), (' 红音 = 转位低音（slash 后的音）', MUTE)]


def text_width_cn(s, size):
    """粗估文本宽度：全角字符 = size，半角 ≈ 0.5 size。"""
    return sum(size if ord(c) > 0x2E7F else size * 0.52 for c in s)


def chord_tspans(chord):
    """和弦名拆 tspan：slash 后的转位低音标红。"""
    if '/' not in chord:
        return f'<tspan>{escape(chord)}</tspan>'
    head, bass = chord.split('/', 1)
    return (f'<tspan>{escape(head)}/</tspan>'
            f'<tspan fill="{ACCENT}">{escape(bass)}</tspan>')


def render_row(row, y):
    """渲染一行 4 小节，返回 (elements, 占用高度)。"""
    els = []
    chord_y = y + 26
    degree_y = chord_y + 20
    lyric_y = chord_y + 40
    bass = row.get('bass', False)
    h = ROW_H + (BASS_H if bass else 0)

    # 小节竖线
    for i in range(5):
        x = LEFT + i * CELL_W
        els.append(f'<line x1="{x}" y1="{y + 6}" x2="{x}" y2="{lyric_y + 8}" '
                   f'stroke="{GRID}" stroke-width="1"/>')

    # 行标签（如「第二遍」），右对齐于网格右缘
    if row.get('tag'):
        els.append(f'<text x="{LEFT + 4 * CELL_W - 10}" y="{chord_y}" '
                   f'font-size="10" fill="{MUTE}" text-anchor="end">'
                   f'{escape(row["tag"])}</text>')

    for ci, (chord, degree, lyric) in enumerate(row['cells']):
        x = LEFT + ci * CELL_W + CELL_PAD
        els.append(f'<text x="{x}" y="{chord_y}" font-size="{CHORD_SIZE}" '
                   f'font-weight="bold" fill="{INK}">{chord_tspans(chord)}</text>')
        els.append(f'<text x="{x}" y="{degree_y}" font-size="{DEGREE_SIZE}" '
                   f'fill="{MUTE}">{escape(degree)}</text>')
        els.append(f'<text x="{x}" y="{lyric_y}" font-size="{LYRIC_SIZE}" '
                   f'fill="{LYRIC}">{escape(lyric)}</text>')

    # 低音 1-7-6 级进：红点连线（本行 4 个小节的低音 A→G#→F#→E）
    if bass:
        by = lyric_y + 22
        pts = [(LEFT + ci * CELL_W + CELL_PAD + 4, by) for ci in range(4)]
        path = ' '.join(f'{px},{py}' for px, py in pts)
        els.append(f'<polyline points="{path}" fill="none" '
                   f'stroke="{ACCENT}" stroke-width="1.2" opacity="0.65"/>')
        for px, py in pts:
            els.append(f'<circle cx="{px}" cy="{py}" r="3.2" fill="{ACCENT}"/>')
        els.append(f'<text x="{pts[-1][0] + 12}" y="{by + 3.5}" font-size="10" '
                   f'fill="{ACCENT}">低音 1–7–6</text>')

    return els, h


def render_section(sec, y):
    els = []
    # 段落头：蓝色条 + 段落名 + 注解
    els.append(f'<rect x="{LEFT}" y="{y}" width="4" height="18" rx="2" '
               f'fill="{SECTION_BLUE}"/>')
    name_x = LEFT + 12
    els.append(f'<text x="{name_x}" y="{y + 14}" font-size="15" '
               f'font-weight="bold" fill="{INK}">{escape(sec["name"])}</text>')
    note_x = name_x + text_width_cn(sec['name'], 15) + 10
    els.append(f'<text x="{note_x:.0f}" y="{y + 14}" font-size="11" '
               f'fill="{MUTE}">{escape(sec["note"])}</text>')
    y += 34

    for i, row in enumerate(sec['rows']):
        # 隔行淡底色（先画背景再画内容）
        row_h = ROW_H + (BASS_H if row.get('bass') else 0)
        if i % 2 == 1:
            els.append(f'<rect x="{LEFT}" y="{y + 4}" width="{4 * CELL_W}" '
                       f'height="{row_h}" rx="6" fill="{ROW_BG}"/>')
        row_els, h = render_row(row, y)
        els.extend(row_els)
        y += h
    return els, y + 14


def main():
    y = 30
    els = [
        f'<text x="{LEFT}" y="{y}" font-size="16" font-weight="bold" '
        f'fill="{INK}">{escape(TITLE)}</text>',
        f'<text x="{LEFT}" y="{y + 20}" font-size="11" '
        f'fill="{MUTE}">{escape(SUBTITLE)}</text>',
    ]
    y += 44

    for sec in SECTIONS:
        sec_els, y = render_section(sec, y)
        els.extend(sec_els)

    # 图例
    lx = LEFT
    ly = y + 12
    for txt, color in LEGEND:
        els.append(f'<text x="{lx:.0f}" y="{ly}" font-size="10" '
                   f'fill="{color}">{escape(txt)}</text>')
        lx += text_width_cn(txt, 10)

    width = LEFT + 4 * CELL_W + LEFT
    height = ly + 16

    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height:.0f}" viewBox="0 0 {width} {height:.0f}" '
        f'font-family="{FONT}">\n'
        f'<rect width="{width}" height="{height:.0f}" fill="#ffffff"/>\n'
        + '\n'.join(els)
        + '\n</svg>\n'
    )

    out = (Path(__file__).resolve().parent.parent
           / 'docs' / 'assets' / 'images' / 'songs'
           / 'chuxian-you-likai-chart.svg')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding='utf-8')
    print(f'done: {out}')


if __name__ == '__main__':
    main()
