#!/usr/bin/env python3
"""更新 4-实战篇 内嵌图片路径（手型 / 节奏）；去掉进行总览图引用。"""
from __future__ import annotations

import re
from pathlib import Path

from asset_paths import HAND_IMAGE_FOLDER_TO_KIND

DOCS = Path(__file__).resolve().parent.parent / "docs"
THEORY = DOCS / "4-实战篇"


def fix_hands(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        folder, tonic, n = m.group(1), m.group(2), m.group(3)
        kind = HAND_IMAGE_FOLDER_TO_KIND.get(folder)
        if not kind:
            return m.group(0)
        return f"assets/images/hands/by-tonic/{tonic}/{kind}/shape-{n}.svg"

    return re.sub(
        r"assets/images/([^/]+)/([A-Za-z#]+)-hand-shape-(\d+)\.svg",
        repl,
        text,
    )


def fix_rhythm(text: str) -> str:
    text = re.sub(
        r"assets/images/rhythm-patterns/dom7-turnaround\.svg",
        "assets/images/rhythm/by-progression/dom7-turnaround/rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm(?:-patterns)?/by-progression/1564/[A-Za-z#]+-rhythm\.svg",
        "assets/images/rhythm/by-progression/1564/rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/([A-Za-z#]+)-1564-rhythm\.svg",
        "assets/images/rhythm/by-progression/1564/rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/([A-Za-z#]+)-progression-rhythm\.svg",
        r"assets/images/rhythm/by-progression/m7-turnaround/\1-rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/2516251-rhythm\.svg",
        "assets/images/rhythm/by-progression/2516251/rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/C-progression-rhythm\.svg",
        "assets/images/rhythm/by-progression/m7-turnaround/C-rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/([A-Za-z#%]+)-add9-rhythm\.svg",
        r"assets/images/rhythm/by-progression/add9-drill/\1-rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/([A-Za-z#%]+)-sus4-rhythm\.svg",
        r"assets/images/rhythm/by-progression/sus4-drill/\1-rhythm.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/maj7-4-88-4-1616-8\.svg",
        "assets/images/rhythm/by-progression/maj7-demos/maj7-4-88-4-1616-8.svg",
        text,
    )
    text = re.sub(
        r"assets/images/rhythm-patterns/([A-Za-z#%]+)-progression-rhythm\.svg",
        r"assets/images/rhythm/by-progression/m7-turnaround/\1-rhythm.svg",
        text,
    )
    return text


def drop_overview_images(text: str) -> str:
    return re.sub(
        r"\n?!\[[^\]]*进行[^\]]*\]\([^)]*-progressions/[^)]+\)\n?",
        "\n",
        text,
    )


def main() -> None:
    for md in THEORY.rglob("*.md"):
        old = md.read_text(encoding="utf-8")
        new = drop_overview_images(fix_rhythm(fix_hands(old)))
        if new != old:
            md.write_text(new, encoding="utf-8")
            print("updated", md.relative_to(DOCS))


if __name__ == "__main__":
    main()
