"""展开 docs/rhythm-patterns/cells/canon.yaml 单拍型 → 小节 flat unit（layout v2）。"""

from __future__ import annotations

from typing import Any


def _base(beat_1based: int) -> int:
    return (beat_1based - 1) * 4


def expand_beat(cell_id: str, beat_1based: int) -> dict[str, Any]:
    """返回 xs / underlines / quarters / rest_beats（至多其一作主）。"""
    b = _base(beat_1based)
    out: dict[str, Any] = {
        "xs": [],
        "underlines": [],
        "quarters": [],
        "rest_beats": [],
    }

    if cell_id in ("quarter", "q"):
        out["quarters"] = [beat_1based]
        return out
    if cell_id in ("rest", "r"):
        out["rest_beats"] = [beat_1based]
        return out

    if cell_id == "two-eighth":
        out["xs"] = [b + 0, b + 2]
        out["underlines"] = [(1, b + 0, b + 2)]
    elif cell_id == "two-sixteenth-eighth":
        # 十六八 16+16+8：前两个 X 两道线，第三个 X 一道线
        out["xs"] = [b + 0, b + 1, b + 2]
        out["underlines"] = [(2, b + 0, b + 1), (1, b + 2, b + 2)]
    elif cell_id == "eighth-two-sixteenth":
        # 八十六 8+16+16：第一个 X 一道线（占 0–1 格），后两个 X 两道线
        out["xs"] = [b + 0, b + 2, b + 3]
        out["underlines"] = [(1, b + 0, b + 1), (2, b + 2, b + 3)]
    elif cell_id == "four-sixteenth":
        out["xs"] = [b + 0, b + 1, b + 2, b + 3]
        out["underlines"] = [(2, b + 0, b + 3)]
    else:
        raise ValueError(f"unknown rhythm cell: {cell_id}")

    return out


def merge_beat_specs(specs: list[dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {
        "xs": [],
        "underlines": [],
        "quarters": [],
        "rest_beats": [],
    }
    for s in specs:
        for key in merged:
            merged[key].extend(s.get(key, []))
    return merged
