#!/usr/bin/env python3
"""节奏型 SVG 批量入口（仅 v2 / rhythm-score 管线）。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent
PYTHON = sys.executable

TARGETS: dict[str, list[str]] = {
    "exercise-1": [],
    "1564-12": ["gen_1564_progression_rhythm.py"],
    "2516251": ["gen_2516251_rhythm.py"],
}

ALL_ORDER = ["exercise-1", "1564-12", "2516251"]


def _run(script: str) -> None:
    path = SKILL_SCRIPTS / script
    if not path.is_file():
        raise FileNotFoundError(path)
    subprocess.run([PYTHON, str(path)], cwd=str(SKILL_SCRIPTS), check=True)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: build_rhythm_patterns.py <target|all>\n"
            "Targets: " + ", ".join(ALL_ORDER),
            file=sys.stderr,
        )
        sys.exit(1)

    arg = sys.argv[1].strip().lower()
    if arg == "all":
        keys = ALL_ORDER
    elif arg in TARGETS:
        keys = [arg]
    else:
        print(f"Unknown target: {arg}", file=sys.stderr)
        sys.exit(1)

    for key in keys:
        if key == "exercise-1":
            subprocess.run(
                [PYTHON, str(SKILL_SCRIPTS / "gen_rhythm_patterns.py"), "exercise-1"],
                cwd=str(SKILL_SCRIPTS),
                check=True,
            )
            continue
        for script in TARGETS[key]:
            _run(script)


if __name__ == "__main__":
    main()
