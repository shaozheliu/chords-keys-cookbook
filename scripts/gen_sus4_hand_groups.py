# ============================================================
# 十二调挂留四和弦手型图生成器
# 按五度圈顺序，为 12 个根音逐个生成一张独立 SVG（共 12 张）。
# 每张：和弦标题 + 一张连续键盘（左右手合并）+ 红蓝指法圆点数字。
# sus4 只需掌握扩张型（手型二）：
#   左手 5-2指 根音-五音 ｜ 右手 1-2-3-5指 根音-四音-五音-高八度根音
# 命名：{根音}-hand-shape-2.svg，如 C-hand-shape-2.svg。
# sus4 = 根音 + 纯四度（+5）+ 纯五度（+7），四音替代三音。
# ============================================================

from pathlib import Path

from piano_svg import write_hand_svg

# 配色（与大三/挂留二脚本保持一致）
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
# sus4 的四音为纯四度；F 的四音是 Bb（黑键），故 F 用降号标注。
# 其余升号调的四音均为白键，沿用 sharp；降号调本就为 flat。
TONIC_INFO = {
    'C': (0, 'sharp'), 'G': (7, 'sharp'), 'D': (2, 'sharp'), 'A': (9, 'sharp'),
    'E': (4, 'sharp'), 'B': (11, 'sharp'), 'F': (5, 'flat'), 'F#': (6, 'sharp'),
    'Db': (1, 'flat'), 'Ab': (8, 'flat'), 'Eb': (3, 'flat'), 'Bb': (10, 'flat'),
}

# 十二调顺序（五度圈顺时针）
TONICS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

# 主音参考音高（C4=60），所有音高叠加该基准，保证为正
BASE = 60

# 手型定义：notes 为 (相对主音半音, 指法编号, 手别 L/R)，range 为键盘展示范围
HANDS = [
    {  # 扩张型（手型二）：左手根音+五音 + 右手 根音-四音-五音-高八度根音
        'label': '扩张型',
        'sub': '手型二',
        'desc': '左手 5-2指 根音-五音 ｜ 右手 1-2-3-5指 根音-四音-五音-高八度根音',
        'notes': [
            (-12, 5, 'L'),   # 左手根音（do，低八度）
            (-5, 2, 'L'),    # 左手五音（so）
            (0, 1, 'R'),     # 右手根音（do）
            (5, 2, 'R'),     # 右手四音（fa）
            (7, 3, 'R'),     # 右手五音（so）
            (12, 5, 'R'),    # 右手高八度根音（do）
        ],
        'range': (-12, 12),
    },
]

DEGREE = {0: '根音', 5: '四音', 7: '五音'}
OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'sus4-chords'


def build_single_svg(tonic_name, hand, idx):
    sub = hand.get('sub')
    extra = f'（{sub}）' if sub else ''
    title = f'{tonic_name} Sus4 · {hand["label"]}{extra}'
    path = OUT / f'{tonic_name}-hand-shape-{idx}.svg'
    write_hand_svg(path, title, hand['desc'], tonic_name, hand, DEGREE, TONIC_INFO, BASE)
    print(f'{path.name} done')


if __name__ == '__main__':
    # sus4 只掌握扩张型，文件名固定为 hand-shape-2。
    for tonic_name in TONICS:
        for hand in HANDS:
            build_single_svg(tonic_name, hand, 2)
