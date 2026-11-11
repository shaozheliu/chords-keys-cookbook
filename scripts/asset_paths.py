# 站点 SVG 产物路径约定（docs/ 为 GitHub Pages 根）
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
ASSETS = DOCS / "assets" / "images"
MATERIALS = DOCS / "materials"

CARDS_DIR = ASSETS / "cards"
HANDS_ROOT = ASSETS / "hands" / "by-tonic"
RHYTHM_ROOT = ASSETS / "rhythm" / "by-progression"
RHYTHM_MATERIALS = MATERIALS / "rhythm"

# 生成脚本旧目录名 → 手型色彩目录（hands/by-tonic/{调}/{kind}/）
HAND_IMAGE_FOLDER_TO_KIND: dict[str, str] = {
    "major-triads": "major",
    "minor-triads": "minor",
    "dom7-chords": "dom7",
    "dom7sus4-chords": "dom7sus4",
    "m7-chords": "m7",
    "maj7-chords": "maj7",
    "sus2-chords": "sus2",
    "sus4-chords": "sus4",
    "add9-chords": "add9",
    "maj6-chords": "maj6",
    "maj69-chords": "maj69",
}


def hand_shape_svg(kind: str, tonic_name: str, shape_id: int | str) -> Path:
    return HANDS_ROOT / tonic_name / kind / f"shape-{shape_id}.svg"


def rhythm_svg(progression_id: str, tonic: str | None = None) -> Path:
    base = RHYTHM_ROOT / progression_id
    if tonic:
        return base / f"{tonic}-rhythm.svg"
    return base / "rhythm.svg"
