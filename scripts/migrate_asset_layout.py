#!/usr/bin/env python3
"""将 assets 迁到 rhythm/hands/cards 新布局；删除进行总览目录。可重复运行（跳过已迁文件）。"""
from __future__ import annotations

import shutil
from pathlib import Path

from asset_paths import (
    ASSETS,
    CARDS_DIR,
    HAND_IMAGE_FOLDER_TO_KIND,
    HANDS_ROOT,
    RHYTHM_ROOT,
)

ROOT = Path(__file__).resolve().parent.parent
IMG = ASSETS
RP = IMG / "rhythm-patterns"
CK = IMG / "card-keys"

PROG_OVERVIEW_DIRS = [
    "1564-progressions",
    "dom7-progressions",
    "m7-progressions",
    "add9-progressions",
    "sus4-progressions",
]


def migrate_hands() -> int:
    n = 0
    for folder, kind in HAND_IMAGE_FOLDER_TO_KIND.items():
        src_dir = IMG / folder
        if not src_dir.is_dir():
            continue
        for f in list(src_dir.glob("*-hand-shape-*.svg")):
            parts = f.stem.split("-hand-shape-")
            if len(parts) != 2:
                continue
            tonic, idx = parts[0], parts[1]
            dest = HANDS_ROOT / tonic / kind / f"shape-{idx}.svg"
            if dest.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            f.rename(dest)
            n += 1
        if src_dir.is_dir() and not any(src_dir.iterdir()):
            src_dir.rmdir()
    return n


def migrate_rhythm() -> int:
    n = 0
    if not RP.is_dir():
        return n

    d1564 = RHYTHM_ROOT / "1564"
    d1564.mkdir(parents=True, exist_ok=True)
    for f in list(RP.glob("*-1564-rhythm.svg")):
        tonic = f.name.replace("-1564-rhythm.svg", "")
        dest = d1564 / f"{tonic}-rhythm.svg"
        if not dest.exists():
            f.rename(dest)
            n += 1

    d251 = RHYTHM_ROOT / "2516251"
    d251.mkdir(parents=True, exist_ok=True)
    src251 = RP / "2516251-rhythm.svg"
    if src251.is_file():
        dest = d251 / "rhythm.svg"
        if not dest.exists():
            src251.rename(dest)
            n += 1

    dex = RHYTHM_ROOT / "exercise-1"
    dex.mkdir(parents=True, exist_ok=True)
    demo = RP / "lianxi-1-demo.svg"
    if demo.is_file():
        dest = dex / "demo.svg"
        if not dest.exists():
            demo.rename(dest)
            n += 1

    legacy = {
        "dom7-turnaround.svg": ("dom7-turnaround", "rhythm.svg"),
        "maj7-4-88-4-1616-8.svg": ("maj7-demos", "maj7-4-88-4-1616-8.svg"),
        "add9-m7-8x8-tie.svg": ("add9-demos", "add9-m7-8x8-tie.svg"),
    }
    for name, (pid, out_name) in legacy.items():
        src = RP / name
        if not src.is_file():
            continue
        dest_dir = RHYTHM_ROOT / pid
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / out_name
        if not dest.exists():
            src.rename(dest)
            n += 1

    for f in list(RP.glob("*-progression-rhythm.svg")):
        tonic = f.name.split("-progression-rhythm")[0]
        dest_dir = RHYTHM_ROOT / "m7-turnaround"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{tonic}-rhythm.svg"
        if not dest.exists():
            f.rename(dest)
            n += 1

    for pat, pid in [("*-add9-rhythm.svg", "add9-drill"), ("*-sus4-rhythm.svg", "sus4-drill")]:
        dest_dir = RHYTHM_ROOT / pid
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in list(RP.glob(pat)):
            tonic = f.name.split("-")[0]
            dest = dest_dir / f"{tonic}-rhythm.svg"
            if not dest.exists():
                f.rename(dest)
                n += 1

    if RP.is_dir() and not any(RP.iterdir()):
        RP.rmdir()
    return n


def migrate_cards() -> int:
    n = 0
    if not CK.is_dir():
        return n
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    for f in list(CK.glob("*.svg")):
        dest = CARDS_DIR / f.name
        if dest.exists():
            continue
        f.rename(dest)
        n += 1
    if CK.is_dir() and not any(CK.iterdir()):
        CK.rmdir()
    return n


def remove_progression_overviews() -> int:
    n = 0
    for name in PROG_OVERVIEW_DIRS:
        d = IMG / name
        if d.is_dir():
            shutil.rmtree(d)
            n += 1
    return n


def main() -> None:
    print("hands:", migrate_hands())
    print("rhythm:", migrate_rhythm())
    print("cards:", migrate_cards())
    print("removed overview dirs:", remove_progression_overviews())


if __name__ == "__main__":
    main()
