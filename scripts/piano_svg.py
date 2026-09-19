# 钢琴图共用绘制。
# 手型图：640×360，左右手指法。
# 卡片琴键：固定 13 白键，样式对齐参考图（圆角、黑键阴影、薄荷绿按下）。

from pathlib import Path

# --- 配色 ---
BG = '#FFFFFF'
PAGE = '#FAFAFA'
WHITE_KEY = '#FFFFFF'
WHITE_EDGE = '#D4D4D8'
BLACK_KEY = '#171717'
INK = '#0A0A0A'
MUTED = '#71717A'
HINT = '#A1A1AA'

# 左右手（显著区分：红 / 蓝）
LEFT = '#DC2626'
RIGHT = '#2563EB'

# 按下态：鲜明绿色，和未按白键拉开对比
PRESS_TOP = '#6EE7B7'
PRESS_BOTTOM = '#A7F3D0'
PRESS_FILL = '#6EE7B7'
PRESS_EDGE = '#059669'
PRESS_TEXT = '#065F46'
PRESS_BLACK = '#10B981'

FONT = 'Arial, Helvetica, sans-serif'

HAND_W = 640
HAND_H = 360
CARD_LIST = (228, 128)
CARD_HERO = (360, 202)

# 标准卡片键盘：固定 13 个白键（C → 下一组 A）
CARD_WHITE_COUNT = 13

WHITE_INDEX = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
WHITE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
# 黑键标注：参考图用 Db/Eb/F#/Ab/Bb
BLACK_LABELS = {1: 'D♭', 3: 'E♭', 6: 'F♯', 8: 'A♭', 10: 'B♭'}

# 白键音级序列（从任意 C 起连续 13 个白键的半音偏移）
# C D E F G A B C D E F G A
_WHITE_STEPS = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21]


def is_white(pitch):
    return pitch % 12 in WHITE_INDEX


def white_name(pitch):
    return WHITE_NAMES[WHITE_INDEX[pitch % 12]]


def normalize_start(start):
    return start - 1 if not is_white(start) else start


def white_pitches(start, end):
    start = normalize_start(start)
    return [p for p in range(start, end + 1) if is_white(p)]


def card_white_pitches(start_c=60):
    """从某个 C 起，固定返回 13 个白键音高。"""
    return [start_c + s for s in _WHITE_STEPS]


def card_range(start_c=60):
    whites = card_white_pitches(start_c)
    return whites[0], whites[-1]


def white_label(pitch):
    """白键标签：仅 C 带八度号，其余只写音名。"""
    name = white_name(pitch)
    if name == 'C':
        return f'{name}{pitch // 12 - 1}'
    return name


def ensure_press_gradient(svg):
    svg.append(
        '<defs>'
        '<linearGradient id="pressGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{PRESS_TOP}"/>'
        f'<stop offset="100%" stop-color="{PRESS_BOTTOM}"/>'
        '</linearGradient>'
        '<filter id="blackShadow" x="-20%" y="-10%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="1.5" stdDeviation="1.2" flood-color="#000000" flood-opacity="0.28"/>'
        '</filter>'
        '</defs>'
    )


# ---------------------------------------------------------------------------
# 手型图键盘（可变白键数）
# ---------------------------------------------------------------------------

def draw_keyboard(svg, x, y, white_w, white_h, start, end, highlights, mode='sharp',
                  labels=True, label_size=11):
    start = normalize_start(start)
    whites = white_pitches(start, end)
    index = {p: i for i, p in enumerate(whites)}
    black_w = round(white_w * 0.62, 2)
    black_h = round(white_h * 0.62, 2)
    black_off = white_w - black_w / 2
    centers = {}

    for p in whites:
        wx = x + index[p] * white_w
        pressed = p in highlights
        fill = PRESS_FILL if pressed else WHITE_KEY
        stroke = PRESS_EDGE if pressed else WHITE_EDGE
        weight = 1.5 if pressed else 1
        svg.append(
            f'<rect x="{wx:.2f}" y="{y:.2f}" width="{white_w:.2f}" height="{white_h:.2f}" '
            f'rx="0" ry="0" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"/>'
        )
        if labels:
            color = PRESS_TEXT if pressed else MUTED
            svg.append(
                f'<text x="{wx + white_w / 2:.2f}" y="{y + white_h + label_size + 4:.2f}" '
                f'text-anchor="middle" font-family="{FONT}" font-size="{label_size}" fill="{color}">'
                f'{white_name(p)}{p // 12 - 1}</text>'
            )
        centers[p] = (wx + white_w / 2, y + white_h * 0.62)

    for p in range(start, end + 1):
        if is_white(p) or p % 12 not in BLACK_LABELS:
            continue
        left = p - 1
        if left not in index:
            continue
        bx = x + index[left] * white_w + black_off
        pressed = p in highlights
        fill = PRESS_BLACK if pressed else BLACK_KEY
        stroke = '#FFFFFF' if pressed else BLACK_KEY
        svg.append(
            f'<rect x="{bx:.2f}" y="{y:.2f}" width="{black_w:.2f}" height="{black_h:.2f}" '
            f'rx="{max(1.5, black_w * 0.08):.2f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        )
        if labels and black_w >= 14:
            svg.append(
                f'<text x="{bx + black_w / 2:.2f}" y="{y + black_h - 6:.2f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="8" fill="#FFFFFF">{BLACK_LABELS[p % 12]}</text>'
            )
        centers[p] = (bx + black_w / 2, y + black_h * 0.72)

    return centers, len(whites) * white_w, black_h


def finger_dot(svg, cx, cy, side, label, r=12):
    color = LEFT if side == 'L' else RIGHT
    svg.append(
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}" stroke="#FFFFFF" stroke-width="2"/>'
    )
    svg.append(
        f'<text x="{cx:.1f}" y="{cy + 4:.1f}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="11" font-weight="bold" fill="#FFFFFF">{label}</text>'
    )


def draw_legend(svg, x, y):
    svg.append(
        f'<rect x="{x}" y="{y - 10}" width="12" height="12" rx="2" fill="{PRESS_FILL}" '
        f'stroke="{PRESS_EDGE}" stroke-width="1"/>'
    )
    svg.append(
        f'<text x="{x + 16}" y="{y}" font-family="{FONT}" font-size="11" fill="{MUTED}">按下的键</text>'
    )
    svg.append(
        f'<circle cx="{x + 92}" cy="{y - 4}" r="6" fill="{LEFT}" stroke="#FFFFFF" stroke-width="1"/>'
    )
    svg.append(
        f'<text x="{x + 102}" y="{y}" font-family="{FONT}" font-size="11" fill="{MUTED}">左手</text>'
    )
    svg.append(
        f'<circle cx="{x + 148}" cy="{y - 4}" r="6" fill="{RIGHT}" stroke="#FFFFFF" stroke-width="1"/>'
    )
    svg.append(
        f'<text x="{x + 158}" y="{y}" font-family="{FONT}" font-size="11" fill="{MUTED}">右手</text>'
    )
    svg.append(
        f'<text x="{x + 198}" y="{y}" font-family="{FONT}" font-size="11" fill="{HINT}">圆点内为指法</text>'
    )


def build_hand_svg(title, desc, tonic_name, hand, degree_names, tonic_info, base=60):
    offset, mode = tonic_info[tonic_name]
    start = base + offset + hand['range'][0]
    end = base + offset + hand['range'][1]
    notes = [(base + offset + rel, finger, side) for rel, finger, side in hand['notes']]
    highlights = {p for p, _, _ in notes}

    n_white = len(white_pitches(start, end))
    margin = 20
    white_w = min(38, (HAND_W - margin * 2) / max(n_white, 1))
    white_h = 168
    board_w = n_white * white_w
    x0 = (HAND_W - board_w) / 2
    key_y = 62

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {HAND_W} {HAND_H}" '
        f'width="{HAND_W}" height="{HAND_H}">',
        f'<rect width="{HAND_W}" height="{HAND_H}" fill="{BG}"/>',
        f'<text x="{HAND_W / 2}" y="26" text-anchor="middle" font-family="{FONT}" '
        f'font-size="16" font-weight="bold" fill="{INK}">{title}</text>',
        f'<text x="{HAND_W / 2}" y="46" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" fill="{MUTED}">{desc}</text>',
    ]
    centers, _, black_h = draw_keyboard(
        svg, x0, key_y, white_w, white_h, start, end, highlights, mode, labels=True, label_size=11,
    )

    for rel, finger, side in hand['notes']:
        p = base + offset + rel
        cx, cy = centers[p]
        if not is_white(p):
            cy = key_y + black_h - 14
        finger_dot(svg, cx, cy, side, str(finger))
        deg = degree_names[rel % 12]
        color = LEFT if side == 'L' else RIGHT
        svg.append(
            f'<text x="{cx:.1f}" y="{key_y + white_h + 32}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="11" font-weight="bold" fill="{color}">{deg}</text>'
        )

    draw_legend(svg, x0, HAND_H - 16)
    svg.append('</svg>')
    return '\n'.join(svg)


def write_hand_svg(path, title, desc, tonic_name, hand, degree_names, tonic_info, base=60):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        build_hand_svg(title, desc, tonic_name, hand, degree_names, tonic_info, base),
        encoding='utf-8',
    )


# ---------------------------------------------------------------------------
# 卡片琴键：固定 13 白键，参考图样式
# ---------------------------------------------------------------------------

def draw_card_keyboard(svg, x, y, width, height, start_c, highlights, show_labels=True):
    """在矩形区域内画标准 13 白键键盘。"""
    whites = card_white_pitches(start_c)
    assert len(whites) == CARD_WHITE_COUNT
    white_w = width / CARD_WHITE_COUNT
    white_h = height
    black_w = white_w * 0.58
    black_h = white_h * 0.58
    radius = max(2.0, white_w * 0.12)
    black_radius = max(1.5, black_w * 0.18)
    index = {p: i for i, p in enumerate(whites)}
    white_set = set(whites)

    # 白键（底圆角）
    for i, p in enumerate(whites):
        wx = x + i * white_w
        pressed = p in highlights
        fill = 'url(#pressGrad)' if pressed else WHITE_KEY
        stroke = PRESS_EDGE if pressed else WHITE_EDGE
        weight = 1.5 if pressed else 1
        # 用 path 做底圆角
        r = radius
        path = (
            f'M {wx:.2f} {y:.2f} '
            f'H {wx + white_w:.2f} '
            f'V {y + white_h - r:.2f} '
            f'Q {wx + white_w:.2f} {y + white_h:.2f} {wx + white_w - r:.2f} {y + white_h:.2f} '
            f'H {wx + r:.2f} '
            f'Q {wx:.2f} {y + white_h:.2f} {wx:.2f} {y + white_h - r:.2f} '
            f'Z'
        )
        svg.append(f'<path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"/>')
        if show_labels:
            label = white_label(p)
            fs = max(8, min(12, white_w * 0.38))
            color = PRESS_TEXT if pressed else INK
            svg.append(
                f'<text x="{wx + white_w / 2:.2f}" y="{y + white_h - fs * 0.45:.2f}" '
                f'text-anchor="middle" font-family="{FONT}" font-size="{fs:.1f}" '
                f'font-weight="{"700" if pressed else "500"}" fill="{color}">{label}</text>'
            )

    # 黑键阴影 + 本体
    for p in range(whites[0], whites[-1] + 1):
        if is_white(p) or p % 12 not in BLACK_LABELS:
            continue
        left = p - 1
        if left not in index:
            # 黑键左侧必须是已画出的白键
            continue
        if left + 1 not in white_set and (left + 1) not in highlights:
            # 右邻白键也要在范围内（E-F / B-C 之间没有黑键，已由 BLACK_LABELS 过滤）
            pass
        bx = x + index[left] * white_w + white_w - black_w / 2
        # 裁掉超出左右边界的黑键
        if bx < x - 1 or bx + black_w > x + width + 1:
            continue
        pressed = p in highlights
        fill = PRESS_BLACK if pressed else BLACK_KEY
        br = black_radius
        stroke_attr = f' stroke="{PRESS_EDGE}" stroke-width="1.5"' if pressed else ''
        svg.append(
            f'<rect x="{bx:.2f}" y="{y:.2f}" width="{black_w:.2f}" height="{black_h:.2f}" '
            f'rx="{br:.2f}" ry="{br:.2f}" fill="{fill}" filter="url(#blackShadow)"{stroke_attr}/>'
        )
        if show_labels and black_w >= 10:
            fs = max(6, min(9, black_w * 0.42))
            svg.append(
                f'<text x="{bx + black_w / 2:.2f}" y="{y + black_h - fs * 0.35:.2f}" '
                f'text-anchor="middle" font-family="{FONT}" font-size="{fs:.1f}" '
                f'fill="#FFFFFF">{BLACK_LABELS[p % 12]}</text>'
            )


def build_card_svg(width, height, highlights, start_c=60, show_labels=True):
    """固定 13 白键卡片图。"""
    pad_x = 6
    pad_y = 6
    # 标签在键内，整块铺满
    board_w = width - pad_x * 2
    board_h = height - pad_y * 2
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
    ]
    ensure_press_gradient(svg)
    draw_card_keyboard(svg, pad_x, pad_y, board_w, board_h, start_c, set(highlights), show_labels)
    svg.append('</svg>')
    return '\n'.join(svg)


def write_card_svg(path, width, height, highlights, start_c=60, show_labels=True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        build_card_svg(width, height, highlights, start_c, show_labels),
        encoding='utf-8',
    )
