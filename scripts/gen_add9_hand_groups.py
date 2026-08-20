# ============================================================
# 十二调加九音和弦手型图生成器
# 按五度圈顺序，为 12 个根音逐个生成两张独立 SVG（共 24 张）。
# 每张：和弦标题 + 一张连续键盘（左右手合并）+ 红蓝指法圆点数字。
# 手型一 = 收缩型（左手根音 + 右手 so-do-re-mi）
# 手型二 = 扩张型（左手 do-so-do + 右手 re-mi-so-do）
# 命名：{根音}-hand-shape-{1|2}.svg，如 C-hand-shape-1.svg。
# add9 = 大三和弦（根音+大三度+纯五度）+ 大九度（根音上方大二度的高八度）。
# ============================================================

from pathlib import Path

# 配色（与大三脚本保持一致）
LEFT_STROKE = "#dc2626"    # 左手主色（红）
RIGHT_STROKE = "#2563eb"   # 右手主色（蓝）
PRESS_FILL = "#d1fae5"     # 按下键填充（绿）

# 键盘尺寸
WHITE_W = 40
WHITE_H = 150
BLACK_W = 26
BLACK_H = 90
BLACK_X_OFFSET = WHITE_W - BLACK_W // 2  # 黑键居中于白键右缘

# 半音模型
WHITE_INDEX = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
WHITE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
SHARP_NAMES = {1: 'C#', 3: 'D#', 6: 'F#', 8: 'G#', 10: 'A#'}
FLAT_NAMES = {1: 'Db', 3: 'Eb', 6: 'Gb', 8: 'Ab', 10: 'Bb'}

# 主音：名称 -> (半音偏移, 黑键标注风格)
# add9 保留大三度、不引入降三音，故黑键标注风格与大三一致（按调号）。
TONIC_INFO = {
    'C': (0, 'sharp'), 'G': (7, 'sharp'), 'D': (2, 'sharp'), 'A': (9, 'sharp'),
    'E': (4, 'sharp'), 'B': (11, 'sharp'), 'F': (5, 'sharp'), 'F#': (6, 'sharp'),
    'Db': (1, 'flat'), 'Ab': (8, 'flat'), 'Eb': (3, 'flat'), 'Bb': (10, 'flat'),
}

# 十二调顺序（五度圈顺时针）
TONICS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

# 主音参考音高（C4=60），所有音高叠加该基准，保证为正
BASE = 60

# 手型定义：notes 为 (相对主音半音, 指法编号, 手别 L/R)，range 为键盘展示范围
HANDS = [
    {  # 手型一 = 收缩型：左手根音 + 右手 so-do-re-mi（五音-根音-九音-三音）
        'label': '收缩型',
        'sub': '手型一',
        'desc': '左手 3指(根音) ｜ 右手 1-2-3-4指 五音-根音-九音-三音',
        'notes': [
            (-12, 3, 'L'),   # 左手根音（低八度）
            (-5, 1, 'R'),    # 右手五音（so）
            (0, 2, 'R'),     # 右手根音（do）
            (2, 3, 'R'),     # 右手九音（re）
            (4, 4, 'R'),     # 右手三音（mi）
        ],
        'range': (-12, 12),
    },
    {  # 手型二 = 扩张型：左手 do-so-do + 右手 re-mi-so-do
        'label': '扩张型',
        'sub': '手型二',
        'desc': '左手 5-4-1指 根音-五音-高八度根音 ｜ 右手 1-2-3-5指 九音-三音-五音-高八度根音',
        'notes': [
            (-12, 5, 'L'),   # 左手根音（do，低八度）
            (-5, 4, 'L'),    # 左手五音（so）
            (0, 1, 'L'),     # 左手高八度根音（do）
            (2, 1, 'R'),     # 右手九音（re）
            (4, 2, 'R'),     # 右手三音（mi）
            (7, 3, 'R'),     # 右手五音（so）
            (12, 5, 'R'),    # 右手高八度根音（do）
        ],
        'range': (-12, 12),
    },
]


def is_white(pitch):
    return pitch % 12 in WHITE_INDEX


def white_name(pitch):
    return WHITE_NAMES[WHITE_INDEX[pitch % 12]]


def normalize_start(start):
    """若起始音是黑键，向左补齐其白键锚点，避免首个黑键悬空。"""
    return start - 1 if not is_white(start) else start


def count_whites(start, end):
    start = normalize_start(start)
    return sum(1 for p in range(start, end + 1) if is_white(p))


def draw_chromatic_keyboard(svg, x0, y0, start, end, highlights, mode='sharp'):
    """绘制一段半音键盘，返回 {pitch: (cx, cy)} 供指法圆点定位。"""
    start = normalize_start(start)

    white_pitches = [p for p in range(start, end + 1) if is_white(p)]
    white_index = {p: i for i, p in enumerate(white_pitches)}
    centers = {}

    # 白键
    for p in white_pitches:
        wx = x0 + white_index[p] * WHITE_W
        fill = PRESS_FILL if p in highlights else 'white'
        svg.append(f'<rect x="{wx}" y="{y0}" width="{WHITE_W}" height="{WHITE_H}" fill="{fill}" stroke="#ccc" stroke-width="1"/>')
        svg.append(f'<text x="{wx + WHITE_W/2}" y="{y0 + WHITE_H + 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#666">{white_name(p)}{p // 12 - 1}</text>')
        centers[p] = (wx + WHITE_W / 2, y0 + WHITE_H * 0.55)

    # 黑键
    names = SHARP_NAMES if mode == 'sharp' else FLAT_NAMES
    for p in range(start, end + 1):
        if is_white(p):
            continue
        if p % 12 not in names:
            continue
        left_white = p - 1
        if left_white not in white_index:
            continue
        bx = x0 + white_index[left_white] * WHITE_W + BLACK_X_OFFSET
        fill = PRESS_FILL if p in highlights else '#333'
        svg.append(f'<rect x="{bx}" y="{y0}" width="{BLACK_W}" height="{BLACK_H}" fill="{fill}" stroke="#111" stroke-width="1" rx="2"/>')
        svg.append(f'<text x="{bx + BLACK_W/2}" y="{y0 + BLACK_H/2 + 4}" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#fff">{names[p % 12]}{p // 12 - 1}</text>')
        centers[p] = (bx + BLACK_W / 2, y0 + BLACK_H / 2)

    return centers


def finger_dot(svg, cx, cy, color, label):
    r = 13
    svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}" stroke="white" stroke-width="2"/>')
    svg.append(f'<text x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" font-weight="bold" fill="white">{label}</text>')


# 单图布局常量
MARGIN = 30
TITLE_Y = 28
SUBTITLE_Y = 47
KEY_Y = 62
NOTE_Y = KEY_Y + WHITE_H + 18      # 白键音名
DEGREE_Y = KEY_Y + WHITE_H + 40    # 音级标注（根音/九音/三音/五音）
LEGEND_Y = KEY_Y + WHITE_H + 62    # 底部图例
H = KEY_Y + WHITE_H + 74           # 画布总高


def draw_hand(svg, W, tonic_name, hand):
    offset, mode = TONIC_INFO[tonic_name]

    title = f'{tonic_name} Add9 · {hand["label"]}（{hand["sub"]}）'
    svg.append(f'<text x="{W/2}" y="{TITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#2c3e50">{title}</text>')
    svg.append(f'<text x="{W/2}" y="{SUBTITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#888">{hand["desc"]}</text>')

    # 计算实际音高与键盘展示范围
    start = BASE + offset + hand['range'][0]
    end = BASE + offset + hand['range'][1]
    notes = [(BASE + offset + rel, finger, side) for rel, finger, side in hand['notes']]
    highlights = {p for p, _, _ in notes}

    n_white = count_whites(start, end)
    x0 = (W - n_white * WHITE_W) / 2
    centers = draw_chromatic_keyboard(svg, x0, KEY_Y, start, end, highlights, mode)

    # 指法圆点 + 音级标注
    for rel, finger, side in hand['notes']:
        p = BASE + offset + rel
        cx, cy = centers[p]
        if not is_white(p):
            cy = KEY_Y + BLACK_H - 16  # 黑键圆点下移，避免遮挡黑键音名
        color = LEFT_STROKE if side == 'L' else RIGHT_STROKE
        finger_dot(svg, cx, cy, color, str(finger))
        deg = {0: '根音', 2: '九音', 4: '三音', 7: '五音'}[rel % 12]
        svg.append(f'<text x="{cx:.1f}" y="{DEGREE_Y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="{color}">{deg}</text>')

    draw_legend(svg, x0, LEGEND_Y)


def draw_legend(svg, x, y):
    """底部图例：绿色=按下键，红色=左手，蓝色=右手"""
    svg.append(f'<rect x="{x}" y="{y - 12}" width="14" height="14" rx="3" fill="{PRESS_FILL}" stroke="#ccc" stroke-width="1"/>')
    svg.append(f'<text x="{x + 20}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#555">按下的键</text>')
    svg.append(f'<circle cx="{x + 96}" cy="{y - 5}" r="7" fill="{LEFT_STROKE}" stroke="white" stroke-width="1.5"/>')
    svg.append(f'<text x="{x + 108}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#555">左手</text>')
    svg.append(f'<circle cx="{x + 152}" cy="{y - 5}" r="7" fill="{RIGHT_STROKE}" stroke="white" stroke-width="1.5"/>')
    svg.append(f'<text x="{x + 164}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#555">右手</text>')
    svg.append(f'<text x="{x + 210}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#999">（圆点内数字 = 指法编号）</text>')


def build_single_svg(tonic_name, hand, idx):
    """为一个根音的一种手型生成单张 SVG。"""
    offset, mode = TONIC_INFO[tonic_name]
    start = BASE + offset + hand['range'][0]
    end = BASE + offset + hand['range'][1]
    n_white = count_whites(start, end)
    W = int(2 * MARGIN + n_white * WHITE_W)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    draw_hand(svg, W, tonic_name, hand)
    svg.append('</svg>')

    path = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'add9-chords' / f'{tonic_name}-hand-shape-{idx}.svg'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(svg), encoding='utf-8')
    print(f'{tonic_name}-hand-shape-{idx}.svg done')


if __name__ == '__main__':
    for tonic_name in TONICS:
        for i, hand in enumerate(HANDS, start=1):
            build_single_svg(tonic_name, hand, i)
    print('All 24 add9 SVGs generated!')
