# ============================================================
# 十二调大七和弦（maj7）手型图生成器
# 按五度圈顺序，为 12 个根音逐个生成三张独立 SVG（共 36 张）。
# 每张：和弦标题 + 一张连续键盘（左右手合并）+ 红蓝指法圆点数字。
# 大七和弦 = 根音 + 大三度 + 纯五度 + 大七度，可拆解为「根音 + 三音上的小三和弦」。
#   收缩型（手型一）：左手 3指 根音 ｜ 右手 1-2-4指 五音-七音-三音
#   中间型（手型二）：左手 5-1指 根音-高八度根音 ｜ 右手 1-2-4指 三音-五音-七音
#   扩张型（手型三）：左手 5-2-1指 根音-五音-高八度根音 ｜ 右手 1-2-3-5指 三音-五音-七音-高八度三音
# 命名：{根音}-hand-shape-{1|2|3}.svg，如 C-hand-shape-1.svg。
# ============================================================

from pathlib import Path

from piano_svg import write_hand_svg

# 配色（与大三/挂留脚本保持一致）
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
# 大七度音：升号调的大七度为白键（C→B、F→E）或升号黑键（G→F#、D→C#、A→G#、E→D#、B→A#），
# 降号调的大七度均为白键（Db→C、Ab→G、Eb→D、Bb→A），故沿用大调的 sharp/flat 配置即可。
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
    {  # 收缩型（手型一）：左手根音 + 右手 so-xi-mi（三音上的小三和弦第一转位）
        'label': '收缩型',
        'sub': '手型一',
        'desc': '左手 3指(根音) ｜ 右手 1-2-4指 五音-七音-三音',
        'notes': [
            (-12, 3, 'L'),   # 左手根音 do（低八度）
            (-5, 1, 'R'),    # 右手五音 so
            (-1, 2, 'R'),    # 右手七音 xi
            (4, 4, 'R'),     # 右手三音 mi
        ],
        'range': (-12, 12),
    },
    {  # 中间型（手型二）：左手八度根音 + 右手 mi-so-xi（三音上的小三和弦原位）
        'label': '中间型',
        'sub': '手型二',
        'desc': '左手 5-1指 根音-高八度根音 ｜ 右手 1-2-4指 三音-五音-七音',
        'notes': [
            (-12, 5, 'L'),   # 左手根音 do（低八度）
            (0, 1, 'L'),     # 左手高八度根音 do
            (4, 1, 'R'),     # 右手三音 mi
            (7, 2, 'R'),     # 右手五音 so
            (11, 4, 'R'),    # 右手七音 xi
        ],
        'range': (-12, 12),
    },
    {  # 扩张型（手型三）：左手 do-so-do + 右手 mi-so-xi-mi（三音上的小三和弦原位加高八度根音）
        'label': '扩张型',
        'sub': '手型三',
        'desc': '左手 5-2-1指 根音-五音-高八度根音 ｜ 右手 1-2-3-5指 三音-五音-七音-高八度三音',
        'notes': [
            (-12, 5, 'L'),   # 左手根音 do（低八度）
            (-5, 2, 'L'),    # 左手五音 so
            (0, 1, 'L'),     # 左手高八度根音 do
            (4, 1, 'R'),     # 右手三音 mi
            (7, 2, 'R'),     # 右手五音 so
            (11, 3, 'R'),    # 右手七音 xi
            (16, 5, 'R'),    # 右手高八度三音 mi
        ],
        'range': (-12, 16),
    },
]

DEGREE = {0: '根音', 4: '三音', 7: '五音', 11: '七音'}
OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'maj7-chords'


def build_single_svg(tonic_name, hand, idx):
    sub = hand.get('sub')
    extra = f'（{sub}）' if sub else ''
    title = f'{tonic_name} Maj7 · {hand["label"]}{extra}'
    path = OUT / f'{tonic_name}-hand-shape-{idx}.svg'
    write_hand_svg(path, title, hand['desc'], tonic_name, hand, DEGREE, TONIC_INFO, BASE)
    print(f'{path.name} done')


if __name__ == '__main__':
    for tonic_name in TONICS:
        for i, hand in enumerate(HANDS, start=1):
            build_single_svg(tonic_name, hand, i)
