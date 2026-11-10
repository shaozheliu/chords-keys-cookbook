#!/usr/bin/env python3
"""2516251 · rhythm-score/1 + layout v2 → docs/.../2516251-rhythm.svg"""

from __future__ import annotations

from gen_rhythm_patterns import render_rhythm_score_v2

SCORE_2516251 = [
    {
        "chords": [(1, "2m7"), (3, "5⁷")],
        "beats": ["two-eighth", "two-sixteenth-eighth", "two-eighth", "quarter"],
    },
    {
        "chords": [(1, "1maj7"), (3, "6⁷")],
        "beats": ["two-eighth", "quarter", "two-eighth", "two-eighth"],
    },
    {
        "chords": [(1, "2m7"), (3, "5⁷sus4")],
        "beats": ["two-eighth", "four-sixteenth", "two-eighth", "two-sixteenth-eighth"],
    },
    {
        "chords": [(1, "1maj7")],
        "chord_holds": [2, 3, 4],
        "beats": ["quarter", "rest", "rest", "rest"],
    },
]


def main() -> None:
    render_rhythm_score_v2("2516251", "2516251-rhythm.svg", SCORE_2516251)
    print("2516251 rhythm SVG (v2) generated.")


if __name__ == "__main__":
    main()
