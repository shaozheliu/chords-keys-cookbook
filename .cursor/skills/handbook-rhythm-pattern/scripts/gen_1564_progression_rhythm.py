#!/usr/bin/env python3
"""1564 色彩进行 · 练习1 节奏型 → 12 调 {tonic}-1564-rhythm.svg"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import repo_scripts_dir

sys.path.insert(0, str(repo_scripts_dir()))
from gen_m7_progression import TONICS  # noqa: E402

from gen_rhythm_patterns import render_practice1_rhythm  # noqa: E402


def main() -> None:
    for tonic in TONICS:
        render_practice1_rhythm(
            title=f"1564 · {tonic} 大调",
            outfile=f"{tonic}-1564-rhythm.svg",
        )
    print("All 12 × 1564 rhythm SVGs generated.")


if __name__ == "__main__":
    main()
