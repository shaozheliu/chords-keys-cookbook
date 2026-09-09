# ============================================================
# 小七和弦「和弦进行」手位图生成器（12 调）
# 进行骨架：1add9 → 3m7 → 4sus2 → 5sus4（1-3-4-5 级数进行，小七落在三级）
# 统一骨架：左手 3-1指 根音-五音 ｜ 右手 1-2-4指 三个音
# 每张图：标题 + 四个和弦纵向堆叠（每个和弦一行键盘，红/蓝指法圆点）。
# 命名：{根音}-progression.svg，如 C-progression.svg。
# ============================================================

from pathlib import Path

# 配色（与 m7/大七等脚本保持一致）
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
# 黑键标注按「主音大调的调号」决定 sharp/flat（升号调用 sharp，降号调用 flat）。
TONIC_INFO = {
    'C': (0, 'sharp'), 'G': (7, 'sharp'), 'D': (2, 'sharp'), 'A': (9, 'sharp'),
    'E': (4, 'sharp'), 'B': (11, 'sharp'), 'F': (5, 'flat'), 'F#': (6, 'sharp'),
    'Db': (1, 'flat'), 'Ab': (8, 'flat'), 'Eb': (3, 'flat'), 'Bb': (10, 'flat'),
}

# 十二调顺序（五度圈顺时针）
TONICS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

# 主音参考音高（C4=60）
BASE = 60

# 三级小七的「降号命名覆盖」：这些大调的三级小七在教程里统一用降号记谱
# （例如 A 大调三级严格是 C♯m7，但教程按小七和弦视角记为 D♭m7，等音同键）。
M7_FLAT_NAME = {'A': 'Dbm7', 'E': 'Abm7', 'B': 'Ebm7', 'F#': 'Bbm7'}


def note_name(pc, mode):
    """半音级（0-11）-> 音名（不含八度），按 sharp/flat 风格标注黑键。"""
    if pc in WHITE_INDEX:
        return WHITE_NAMES[WHITE_INDEX[pc]]
    return (SHARP_NAMES if mode == 'sharp' else FLAT_NAMES).get(pc, '?')


def degree_note_names(offset, mode):
    """返回大调 1/3/4/5 级音名。"""
    return {
        1: note_name(offset % 12, mode),
        3: note_name((offset + 4) % 12, mode),
        4: note_name((offset + 5) % 12, mode),
        5: note_name((offset + 7) % 12, mode),
    }


# ---- 进行定义：四个和弦的 voicing ----
# notes 为 (相对主音半音, 指法编号, 手别 L/R, 音级名)
# 音级名 = 相对「该级和弦根音」的音级（用于键盘下方标注）
PROGRESSION = [
    {  # 1add9 = 1-3-5-9：右手九音-三音-五音
        'degree': '1add9',
        'notes': [
            (-12, 3, 'L', '根音'),   # 左手根音（低八度）
            (-5, 1, 'L', '五音'),    # 左手五音
            (2, 1, 'R', '九音'),     # 右手九音
            (4, 2, 'R', '三音'),     # 右手三音
            (7, 4, 'R', '五音'),     # 右手五音
        ],
        'range': (-12, 7),
    },
    {  # 3m7 = 1-b3-5-b7：右手三音-五音-七音（三音上的大三和弦原位）
        'degree': '3m7',
        'notes': [
            (-8, 3, 'L', '根音'),    # 左手根音（三级低八度）
            (-1, 1, 'L', '五音'),    # 左手五音
            (7, 1, 'R', '三音'),     # 右手三音
            (11, 2, 'R', '五音'),    # 右手五音
            (14, 4, 'R', '七音'),    # 右手七音
        ],
        'range': (-8, 14),
    },
    {  # 4sus2 = 1-2-5：右手二音-五音-六音
        'degree': '4sus2',
        'notes': [
            (-7, 3, 'L', '根音'),    # 左手根音（四级低八度）
            (0, 1, 'L', '五音'),     # 左手五音
            (7, 1, 'R', '二音'),     # 右手二音
            (12, 2, 'R', '五音'),    # 右手五音
            (14, 4, 'R', '六音'),    # 右手六音
        ],
        'range': (-7, 14),
    },
    {  # 5sus4 = 1-4-5：右手四音-五音-六音
        'degree': '5sus4',
        'notes': [
            (-5, 3, 'L', '根音'),    # 左手根音（五级低八度）
            (2, 1, 'L', '五音'),     # 左手五音
            (12, 1, 'R', '四音'),    # 右手四音
            (14, 2, 'R', '五音'),    # 右手五音
            (16, 4, 'R', '六音'),    # 右手六音
        ],
        'range': (-5, 16),
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


# ---- 纵向布局常量 ----
MARGIN = 30
TITLE_Y = 28
SUBTITLE_Y = 48
ROW_TITLE_Y = 22          # 每行「和弦标签」相对行顶的偏移
ROW_KEY_Y = 32            # 每行键盘顶部相对行顶的偏移
ROW_NOTE_Y = ROW_KEY_Y + WHITE_H + 18    # 白键音名
ROW_DEGREE_Y = ROW_KEY_Y + WHITE_H + 40  # 音级标注
ROW_H = ROW_KEY_Y + WHITE_H + 62         # 每行总高（含底部留白）
LEGEND_H = 40


def draw_progression_row(svg, W, tonic_name, chord, row_idx, names):
    offset, mode = TONIC_INFO[tonic_name]
    row_top = SUBTITLE_Y + 14 + row_idx * ROW_H

    # 和弦标签：级数代号 + 该调实际和弦名
    degree = chord['degree']
    suffix = {'1add9': 'add9', '3m7': 'm7', '4sus2': 'sus2', '5sus4': 'sus4'}[degree]
    dnum = {'1add9': '1', '3m7': '3', '4sus2': '4', '5sus4': '5'}[degree]
    if degree == '3m7' and tonic_name in M7_FLAT_NAME:
        chord_name = M7_FLAT_NAME[tonic_name]
        row_mode = 'flat'
    else:
        chord_name = f"{names[int(dnum)]}{suffix}"
        row_mode = mode
    svg.append(f'<text x="{MARGIN}" y="{row_top + ROW_TITLE_Y}" font-family="Arial,sans-serif" font-size="16" font-weight="bold" fill="#2c3e50">{degree} = {chord_name}</text>')

    start = BASE + offset + chord['range'][0]
    end = BASE + offset + chord['range'][1]
    notes = [(BASE + offset + rel, finger, side) for rel, finger, side, _ in chord['notes']]
    highlights = {p for p, _, _ in notes}

    n_white = count_whites(start, end)
    x0 = (W - n_white * WHITE_W) / 2
    centers = draw_chromatic_keyboard(svg, x0, row_top + ROW_KEY_Y, start, end, highlights, row_mode)

    # 指法圆点 + 音级标注
    for rel, finger, side, deg in chord['notes']:
        p = BASE + offset + rel
        cx, cy = centers[p]
        if not is_white(p):
            cy = row_top + ROW_KEY_Y + BLACK_H - 16  # 黑键圆点下移，避免遮挡黑键音名
        color = LEFT_STROKE if side == 'L' else RIGHT_STROKE
        finger_dot(svg, cx, cy, color, str(finger))
        svg.append(f'<text x="{cx:.1f}" y="{row_top + ROW_DEGREE_Y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="{color}">{deg}</text>')

    return x0


def draw_legend(svg, x, y):
    """底部图例：绿色=按下键，红色=左手，蓝色=右手"""
    svg.append(f'<rect x="{x}" y="{y - 12}" width="14" height="14" rx="3" fill="{PRESS_FILL}" stroke="#ccc" stroke-width="1"/>')
    svg.append(f'<text x="{x + 20}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#555">按下的键</text>')
    svg.append(f'<circle cx="{x + 96}" cy="{y - 5}" r="7" fill="{LEFT_STROKE}" stroke="white" stroke-width="1.5"/>')
    svg.append(f'<text x="{x + 108}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#555">左手</text>')
    svg.append(f'<circle cx="{x + 152}" cy="{y - 5}" r="7" fill="{RIGHT_STROKE}" stroke="white" stroke-width="1.5"/>')
    svg.append(f'<text x="{x + 164}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#555">右手</text>')
    svg.append(f'<text x="{x + 210}" y="{y}" font-family="Arial,sans-serif" font-size="11" fill="#999">（圆点内数字 = 指法编号）</text>')


def build_single_svg(tonic_name):
    offset, mode = TONIC_INFO[tonic_name]
    names = degree_note_names(offset, mode)

    # 宽度：取四个和弦里最宽的键盘
    max_white = 0
    for chord in PROGRESSION:
        s = BASE + offset + chord['range'][0]
        e = BASE + offset + chord['range'][1]
        max_white = max(max_white, count_whites(s, e))
    W = int(2 * MARGIN + max_white * WHITE_W)

    H = SUBTITLE_Y + 14 + ROW_H * len(PROGRESSION) + LEGEND_H + 6

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    svg.append(f'<text x="{W/2}" y="{TITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#2c3e50">{tonic_name} 大调 · 1add9 → 3m7 → 4sus2 → 5sus4</text>')
    svg.append(f'<text x="{W/2}" y="{SUBTITLE_Y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#888">左手 3-1指 根音-五音 ｜ 右手 1-2-4指</text>')

    first_x0 = None
    for i, chord in enumerate(PROGRESSION):
        x0 = draw_progression_row(svg, W, tonic_name, chord, i, names)
        if first_x0 is None:
            first_x0 = x0

    legend_y = SUBTITLE_Y + 14 + ROW_H * len(PROGRESSION) + LEGEND_H - 8
    draw_legend(svg, first_x0 if first_x0 else MARGIN, legend_y)
    svg.append('</svg>')

    path = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'm7-progressions' / f'{tonic_name}-progression.svg'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(svg), encoding='utf-8')
    print(f'{tonic_name}-progression.svg done')


if __name__ == '__main__':
    for tonic_name in TONICS:
        build_single_svg(tonic_name)
    print('All 12 m7 progression SVGs generated!')
