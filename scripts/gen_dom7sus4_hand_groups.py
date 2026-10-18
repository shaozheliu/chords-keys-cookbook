# ============================================================
# 十二调属七挂四（dom7sus4 / 7sus4）手型图 — 属七三音换四音
# ============================================================

from pathlib import Path

from piano_svg import write_hand_svg

TONIC_INFO = {
    'C': (0, 'sharp'), 'G': (7, 'sharp'), 'D': (2, 'sharp'), 'A': (9, 'sharp'),
    'E': (4, 'sharp'), 'B': (11, 'sharp'), 'F': (5, 'flat'), 'F#': (6, 'sharp'),
    'Db': (1, 'flat'), 'Ab': (8, 'flat'), 'Eb': (3, 'flat'), 'Bb': (10, 'flat'),
}

TONICS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']
BASE = 60

HANDS = [
    {
        'label': '收缩型',
        'sub': '手型一',
        'desc': '左手 3指(根音) ｜ 右手 1-2-4指 五音-降七-四音',
        'notes': [
            (-12, 3, 'L'),
            (-5, 1, 'R'),
            (-2, 2, 'R'),
            (5, 4, 'R'),
        ],
        'range': (-12, 12),
    },
    {
        'label': '扩张型',
        'sub': '手型二',
        'desc': '左手 5-2-1指 根音-五音-降七 ｜ 右手 1-2-3-5指 根音-四音-五音-高八度根音',
        'notes': [
            (-12, 5, 'L'),
            (-5, 2, 'L'),
            (-2, 1, 'L'),
            (0, 1, 'R'),
            (5, 2, 'R'),
            (7, 3, 'R'),
            (12, 5, 'R'),
        ],
        'range': (-12, 12),
    },
]

DEGREE = {0: '根音', 5: '四音', 7: '五音', 10: '七音'}
OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'dom7sus4-chords'


def build_single_svg(tonic_name, hand, idx):
    title = f'{tonic_name}7sus4 · {hand["label"]}（{hand["sub"]}）'
    path = OUT / f'{tonic_name}-hand-shape-{idx}.svg'
    write_hand_svg(path, title, hand['desc'], tonic_name, hand, DEGREE, TONIC_INFO, BASE)
    print(f'{path.name} done')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for tonic_name in TONICS:
        for i, hand in enumerate(HANDS, start=1):
            build_single_svg(tonic_name, hand, i)
    print('All 12 dom7sus4 hand SVGs generated!')
