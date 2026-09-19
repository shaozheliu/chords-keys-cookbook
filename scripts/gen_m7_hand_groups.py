# ============================================================
# 十二调小七和弦（m7）手型图生成器
# 按五度圈顺序，为 12 个根音逐个生成两张独立 SVG（共 24 张）。
# 每张：和弦标题 + 一张连续键盘（左右手合并）+ 红蓝指法圆点数字。
# 小七和弦 = 根音 + 小三度 + 纯五度 + 小七度，可拆解为「根音 + 三音上的大三和弦」。
#   手型一：左手 3-1指 根音-五音 ｜ 右手 1-2-4指 七音-三音-五音
#   手型二：左手 5-2-1指 根音-五音-高八度根音 ｜ 右手 1-2-3-5指 三音-五音-七音-高八度三音
# 命名：{根音}-hand-shape-{1|2}.svg，如 C-hand-shape-1.svg。
# ============================================================

from pathlib import Path

from piano_svg import write_hand_svg

# 配色（与大三/挂留/大七脚本保持一致）
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
# 小七和弦的三音（小三度）、七音（小七度）为降号音，故按「根音小调」的调号决定 sharp/flat：
#   根音小调带降号（C/G/D/F/Db/Ab/Eb/Bb）用 flat，带升号或自然（A/E/B/F#）用 sharp。
TONIC_INFO = {
    'C': (0, 'flat'), 'G': (7, 'flat'), 'D': (2, 'flat'), 'A': (9, 'sharp'),
    'E': (4, 'sharp'), 'B': (11, 'sharp'), 'F#': (6, 'sharp'),
    'F': (5, 'flat'), 'Db': (1, 'flat'), 'Ab': (8, 'flat'),
    'Eb': (3, 'flat'), 'Bb': (10, 'flat'),
}

# 十二调顺序（五度圈顺时针）
TONICS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

# 主音参考音高（C4=60），所有音高叠加该基准，保证为正
BASE = 60

# 小七和弦音级 -> 名称
DEGREE_NAMES = {0: '根音', 3: '三音', 7: '五音', 10: '七音'}

# 手型定义：notes 为 (相对主音半音, 指法编号, 手别 L/R)，range 为键盘展示范围
HANDS = [
    {  # 手型一：左手根音-五音 + 右手七音-三音-五音（三音上的大三和弦第二转位）
        'label': '手型一',
        'desc': '左手 3-1指 根音-五音 ｜ 右手 1-2-4指 七音-三音-五音',
        'notes': [
            (-12, 3, 'L'),   # 左手根音 do（低八度）
            (-5, 1, 'L'),    # 左手五音 so
            (-2, 1, 'R'),    # 右手七音 降xi
            (3, 2, 'R'),     # 右手三音 降mi
            (7, 4, 'R'),     # 右手五音 so
        ],
        'range': (-12, 12),
    },
    {  # 手型二：左手根音-五音-高八度根音 + 右手三音-五音-七音-高八度三音（三音上的大三和弦原位加高八度根音）
        'label': '手型二',
        'desc': '左手 5-2-1指 根音-五音-高八度根音 ｜ 右手 1-2-3-5指 三音-五音-七音-高八度三音',
        'notes': [
            (-12, 5, 'L'),   # 左手根音 do（低八度）
            (-5, 2, 'L'),    # 左手五音 so
            (0, 1, 'L'),     # 左手高八度根音 do
            (3, 1, 'R'),     # 右手三音 降mi
            (7, 2, 'R'),     # 右手五音 so
            (10, 3, 'R'),    # 右手七音 降xi
            (15, 5, 'R'),    # 右手高八度三音 降mi
        ],
        'range': (-12, 16),
    },
]

DEGREE = {0: '根音', 3: '三音', 7: '五音', 10: '七音'}
OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'm7-chords'


def build_single_svg(tonic_name, hand, idx):
    sub = hand.get('sub')
    title = f'{tonic_name} m7 · {hand["label"]}'
    path = OUT / f'{tonic_name}-hand-shape-{idx}.svg'
    write_hand_svg(path, title, hand['desc'], tonic_name, hand, DEGREE, TONIC_INFO, BASE)
    print(f'{path.name} done')


if __name__ == '__main__':
    for tonic_name in TONICS:
        for i, hand in enumerate(HANDS, start=1):
            build_single_svg(tonic_name, hand, i)
