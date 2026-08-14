# ============================================================
# sus4 和弦进行 GIF 生成器（C 大调 F-G-C）
# 用 Pillow 直接绘制三帧（Pillow 无法光栅化 SVG），合成循环 GIF：
#   帧1  Fsus2 · 扩张型（IV）
#   帧2  Gsus4 · 扩张型（V）
#   帧3  C 大三 · 紧凑型（I，收缩的大三）
# 三帧共用同一段键盘（C2~C5），便于眼睛追踪和弦变化。
# 输出：docs/assets/images/sus4-chords/F-G-C-progression.gif
# 自包含，不 import 其他脚本。
# ============================================================

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# 配色（与 SVG 脚本保持一致）
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

# 固定键盘范围（三帧一致）：C3(MIDI 48) ~ C6(MIDI 84)
# 最高音为 Fsus2 扩张型的二音高八度 G5(79)，故上界取到 C6。
START = 48
END = 84
BASE = 60

# 布局
MARGIN = 30
TITLE_Y = 34
KEY_Y = 66
DEGREE_Y = KEY_Y + WHITE_H + 40
LEGEND_Y = KEY_Y + WHITE_H + 68
H = KEY_Y + WHITE_H + 88


def load_font(size):
    """优先加载 Windows 中文字体，失败则回退默认位图字体。"""
    for path in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/msyh.ttf', 'C:/Windows/Fonts/simhei.ttf']:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def is_white(pitch):
    return pitch % 12 in WHITE_INDEX


def white_name(pitch):
    return WHITE_NAMES[WHITE_INDEX[pitch % 12]]


def draw_keyboard(draw, fonts, x0, highlights, mode):
    """绘制固定范围的半音键盘，返回 {pitch: (cx, cy)} 供圆点定位。"""
    white_pitches = [p for p in range(START, END + 1) if is_white(p)]
    white_index = {p: i for i, p in enumerate(white_pitches)}
    centers = {}

    # 白键
    for p in white_pitches:
        wx = x0 + white_index[p] * WHITE_W
        fill = PRESS_FILL if p in highlights else '#ffffff'
        draw.rectangle([wx, KEY_Y, wx + WHITE_W - 1, KEY_Y + WHITE_H - 1],
                       fill=fill, outline='#cccccc', width=1)
        draw.text((wx + WHITE_W / 2, KEY_Y + WHITE_H + 16),
                  f'{white_name(p)}{p // 12 - 1}', font=fonts['note'], fill='#666666', anchor='mm')
        centers[p] = (wx + WHITE_W / 2, KEY_Y + WHITE_H * 0.55)

    # 黑键
    names = SHARP_NAMES if mode == 'sharp' else FLAT_NAMES
    for p in range(START, END + 1):
        if is_white(p):
            continue
        if p % 12 not in names:
            continue
        left_white = p - 1
        if left_white not in white_index:
            continue
        bx = x0 + white_index[left_white] * WHITE_W + BLACK_X_OFFSET
        fill = PRESS_FILL if p in highlights else '#333333'
        draw.rectangle([bx, KEY_Y, bx + BLACK_W - 1, KEY_Y + BLACK_H - 1],
                       fill=fill, outline='#111111', width=1)
        draw.text((bx + BLACK_W / 2, KEY_Y + BLACK_H / 2),
                  f'{names[p % 12]}{p // 12 - 1}', font=fonts['black_note'], fill='#ffffff', anchor='mm')
        centers[p] = (bx + BLACK_W / 2, KEY_Y + BLACK_H / 2)

    return centers


def draw_legend(draw, fonts, x):
    y = LEGEND_Y
    draw.rectangle([x, y - 11, x + 14, y + 3], fill=PRESS_FILL, outline='#cccccc', width=1)
    draw.text((x + 20, y - 4), '按下的键', font=fonts['legend'], fill='#555555', anchor='lm')
    draw.ellipse([x + 96 - 7, y - 12, x + 96 + 7, y + 2], fill=LEFT_STROKE, outline='#ffffff', width=2)
    draw.text((x + 108, y - 4), '左手', font=fonts['legend'], fill='#555555', anchor='lm')
    draw.ellipse([x + 152 - 7, y - 12, x + 152 + 7, y + 2], fill=RIGHT_STROKE, outline='#ffffff', width=2)
    draw.text((x + 164, y - 4), '右手', font=fonts['legend'], fill='#555555', anchor='lm')
    draw.text((x + 212, y - 4), '（圆点内数字 = 指法编号）', font=fonts['legend'], fill='#999999', anchor='lm')


def draw_frame(frame):
    """根据帧配置绘制一帧，返回 PIL.Image。"""
    n_white = len([p for p in range(START, END + 1) if is_white(p)])
    W = int(2 * MARGIN + n_white * WHITE_W)
    x0 = (W - n_white * WHITE_W) / 2

    fonts = {
        'title': load_font(22),
        'note': load_font(12),
        'black_note': load_font(10),
        'finger': load_font(13),
        'degree': load_font(12),
        'legend': load_font(12),
    }

    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    draw.text((W / 2, TITLE_Y), frame['title'], font=fonts['title'], fill='#2c3e50', anchor='mm')

    offset = frame['offset']
    notes = [(BASE + offset + rel, finger, side) for rel, finger, side in frame['notes']]
    highlights = {p for p, _, _ in notes}
    centers = draw_keyboard(draw, fonts, x0, highlights, frame['mode'])

    for rel, finger, side in frame['notes']:
        p = BASE + offset + rel
        cx, cy = centers[p]
        if not is_white(p):
            cy = KEY_Y + BLACK_H - 16  # 黑键圆点下移，避免遮挡黑键音名
        color = LEFT_STROKE if side == 'L' else RIGHT_STROKE
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=color, outline='#ffffff', width=2)
        draw.text((cx, cy), str(finger), font=fonts['finger'], fill='#ffffff', anchor='mm')

        deg = frame['degrees'][rel % 12]
        draw.text((cx, DEGREE_Y), deg, font=fonts['degree'], fill=color, anchor='mm')

    draw_legend(draw, fonts, x0)
    return img


FRAMES = [
    {  # 帧1：Fsus2 · 扩张型（IV）
        'title': 'Fsus2 · 扩张型（IV）',
        'offset': 5,
        'mode': 'sharp',
        'notes': [
            (-12, 5, 'L'), (-5, 2, 'L'), (0, 1, 'L'),   # 左手 do-so-do
            (2, 1, 'R'), (7, 2, 'R'), (14, 5, 'R'),     # 右手 re-so-re
        ],
        'degrees': {0: '根音', 2: '二音', 7: '五音'},
    },
    {  # 帧2：Gsus4 · 扩张型（V）
        'title': 'Gsus4 · 扩张型（V）',
        'offset': 7,
        'mode': 'sharp',
        'notes': [
            (-12, 5, 'L'), (-5, 2, 'L'),                 # 左手 do-so
            (0, 1, 'R'), (5, 2, 'R'), (7, 3, 'R'), (12, 5, 'R'),  # 右手 do-fa-so-do
        ],
        'degrees': {0: '根音', 5: '四音', 7: '五音'},
    },
    {  # 帧3：C 大三 · 紧凑型（I，收缩的大三）
        'title': 'C 大三 · 紧凑型（I）',
        'offset': 0,
        'mode': 'sharp',
        'notes': [
            (-12, 3, 'L'),                               # 左手根音
            (-5, 1, 'R'), (0, 2, 'R'), (4, 4, 'R'),      # 右手 so-do-mi
        ],
        'degrees': {0: '根音', 4: '三音', 7: '五音'},
    },
]


if __name__ == '__main__':
    frames = [draw_frame(f) for f in FRAMES]
    # 结束后明显停顿：追加一帧复用最后一帧（C 大三），延长其显示时间再循环。
    hold = frames[-1].copy()
    all_frames = frames + [hold]
    durations = [1800, 1800, 1800, 3000]  # 前三帧放慢，末帧停顿
    for f, d in zip(all_frames, durations):
        f.info['duration'] = d

    path = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'sus4-chords' / 'F-G-C-progression.gif'
    path.parent.mkdir(parents=True, exist_ok=True)
    all_frames[0].save(path, save_all=True, append_images=all_frames[1:], loop=0)
    print(f'F-G-C-progression.gif done ({len(all_frames)} frames)')
