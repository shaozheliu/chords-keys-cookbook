#!/usr/bin/env python3
"""为 12 个小七和弦（以它为三级）生成「具体和弦名」标注的节奏型图。

每个小七对应一个所属大调，节奏型沿用 8 个八分音符 + 跨拍连音（4 小节），
每小节上方标注该调 1add9/3m7/4sus2/5sus4 的「具体和弦名」（三级用降号命名）。

输出: docs/assets/images/rhythm-patterns/{所属大调}-progression-rhythm.svg
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_m7_progression import TONIC_INFO, note_name, M7_FLAT_NAME
from gen_rhythm_patterns import render

# 12 个小七（用户分组顺序）→ 所属大调
UNITS = [
    ('Fm7', 'Db'), ('Cm7', 'Ab'), ('Gm7', 'Eb'),   # 周一
    ('Dm7', 'Bb'), ('Am7', 'F'), ('Em7', 'C'),      # 周二
    ('Bm7', 'G'), ('F#m7', 'D'), ('Dbm7', 'A'),     # 周三~四
    ('Abm7', 'E'), ('Ebm7', 'B'), ('Bbm7', 'F#'),   # 周五~六
]

SFX = {'1': 'add9', '3': 'm7', '4': 'sus2', '5': 'sus4'}
DEG_OFFSET = {1: 0, 3: 4, 4: 5, 5: 7}


def build_chords(tonic):
    off, mode = TONIC_INFO[tonic]
    names = {d: note_name((off + DEG_OFFSET[d]) % 12, mode) for d in [1, 3, 4, 5]}
    chords = []
    for d in ['1', '3', '4', '5']:
        if d == '3' and tonic in M7_FLAT_NAME:
            chords.append(M7_FLAT_NAME[tonic])
        else:
            chords.append(f"{names[int(d)]}{SFX[d]}")
    return chords


if __name__ == '__main__':
    for m7, tonic in UNITS:
        chords = build_chords(tonic)
        pattern = {
            'title': f'节奏型 · {m7} 作三级',
            'out': f'{tonic}-progression-rhythm.svg',
            'fixed_units': [0, 2, 4, 6, 8, 10, 12, 14],
            'fixed_lines': [(1, 0, 2), (1, 4, 6), (1, 8, 10), (1, 12, 14)],
            'variants': {'': ([], [])},
            'bars': [(c, '') for c in chords],
            'ties': [(6, 8)],
        }
        render(pattern)
    print('All 12 m7 progression rhythm SVGs generated!')
