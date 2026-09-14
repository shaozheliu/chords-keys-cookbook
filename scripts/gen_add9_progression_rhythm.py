#!/usr/bin/env python3
"""为 add9 的 12 调「和弦进行」生成「具体和弦名」标注的节奏型图。

进行骨架：IVsus2 → Vsus4 → viadd9 → viadd9（4 个小节），每小节上方标注该调的具体和弦名。
节奏型沿用 8 个八分音符 + 跨拍连音。

输出: docs/assets/images/rhythm-patterns/{主音}-add9-rhythm.svg
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_add9_progression import TONIC_INFO, TONICS, note_name
from gen_rhythm_patterns import render


def build_chords(tonic):
    off, mode = TONIC_INFO[tonic]
    vi = f"{note_name((off + 9) % 12, mode)}madd9"
    return [
        f"{note_name((off + 5) % 12, mode)}sus2",
        f"{note_name((off + 7) % 12, mode)}sus4",
        vi,
        vi,
    ]


if __name__ == '__main__':
    for tonic in TONICS:
        chords = build_chords(tonic)
        pattern = {
            'title': f'节奏型 · {tonic} 大调 IV-V-vi',
            'out': f'{tonic}-add9-rhythm.svg',
            'fixed_units': [0, 2, 4, 6, 8, 10, 12, 14],
            'fixed_lines': [(1, 0, 2), (1, 4, 6), (1, 8, 10), (1, 12, 14)],
            'variants': {'': ([], [])},
            'bars': [(c, '') for c in chords],
            'ties': [(6, 8)],
        }
        render(pattern)
    print('All 12 add9 progression rhythm SVGs generated!')
