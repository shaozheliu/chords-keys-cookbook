#!/usr/bin/env python3
"""为 sus4 的 12 调「和弦进行」生成「具体和弦名」标注的节奏型图。

进行骨架：IVsus2 → Vsus4 → I（3 个小节），每小节上方标注该调的具体和弦名。
节奏型沿用 8 个八分音符 + 跨拍连音。

输出: docs/assets/images/rhythm-patterns/{主音}-sus4-rhythm.svg
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_sus4_progression import TONIC_INFO, TONICS, note_name
from gen_rhythm_patterns import render


def build_chords(tonic):
    off, mode = TONIC_INFO[tonic]
    return [
        f"{note_name((off + 5) % 12, mode)}sus2",
        f"{note_name((off + 7) % 12, mode)}sus4",
        note_name(off % 12, mode),
    ]


if __name__ == '__main__':
    for tonic in TONICS:
        chords = build_chords(tonic)
        pattern = {
            'title': f'节奏型 · {tonic} 大调 IV-V-I',
            'out': f'{tonic}-sus4-rhythm.svg',
            'fixed_units': [0, 2, 4, 6, 8, 10, 12, 14],
            'fixed_lines': [(1, 0, 2), (1, 4, 6), (1, 8, 10), (1, 12, 14)],
            'variants': {'': ([], [])},
            'bars': [(c, '') for c in chords],
            'ties': [(6, 8)],
        }
        render(pattern)
    print('All 12 sus4 progression rhythm SVGs generated!')
