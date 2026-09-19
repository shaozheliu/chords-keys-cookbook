# ============================================================
# 十二调大三和弦手型图
# 画布 640×360，配色见 piano_svg.py（白键 / 黑键 / 按下浅灰）。
# 命名：{调名}-hand-shape-{1|2}.svg
# ============================================================

from pathlib import Path

from piano_svg import write_hand_svg

TONIC_INFO = {
    'C': (0, 'sharp'), 'G': (7, 'sharp'), 'D': (2, 'sharp'), 'A': (9, 'sharp'),
    'E': (4, 'sharp'), 'B': (11, 'sharp'), 'F': (5, 'sharp'), 'F#': (6, 'sharp'),
    'Db': (1, 'flat'), 'Ab': (8, 'flat'), 'Eb': (3, 'flat'), 'Bb': (10, 'flat'),
}

TONICS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']
BASE = 60
DEGREE = {0: '根音', 4: '三音', 7: '五音'}

HANDS = [
    {
        'label': '紧凑型',
        'sub': '手型一',
        'desc': '左手 3指(根音) ｜ 右手 1-2-4指 五音-根音-三音',
        'notes': [
            (-12, 3, 'L'),
            (-5, 1, 'R'),
            (0, 2, 'R'),
            (4, 4, 'R'),
        ],
        'range': (-12, 12),
    },
    {
        'label': '扩张型',
        'sub': '手型二',
        'desc': '左手 5指(根音)+2指(五音) ｜ 右手 1-2-3-5指 根音-三音-五音-高八度根音',
        'notes': [
            (-12, 5, 'L'),
            (-5, 2, 'L'),
            (0, 1, 'R'),
            (4, 2, 'R'),
            (7, 3, 'R'),
            (12, 5, 'R'),
        ],
        'range': (-12, 12),
    },
]

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'major-triads'


def build_single_svg(tonic_name, hand, idx):
    sub = hand.get('sub')
    extra = f'（{sub}）' if sub else ''
    title = f'{tonic_name} Major · {hand["label"]}{extra}'
    path = OUT / f'{tonic_name}-hand-shape-{idx}.svg'
    write_hand_svg(path, title, hand['desc'], tonic_name, hand, DEGREE, TONIC_INFO, BASE)
    print(f'{path.name} done')


if __name__ == '__main__':
    for tonic_name in TONICS:
        for i, hand in enumerate(HANDS, start=1):
            build_single_svg(tonic_name, hand, i)
    print('All major-triad hand shapes generated.')
