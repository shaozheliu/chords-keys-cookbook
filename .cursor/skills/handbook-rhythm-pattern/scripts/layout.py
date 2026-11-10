"""布局 v2：固定小节框 + unit 网格；首尾 slot 到竖线等距，与音符时值无关。"""

from __future__ import annotations

SLOT_W = 18
BEAT_GAP = 16
BAR_GAP = 0
BAR_PAD_LEFT = 18
BAR_PAD_RIGHT = 18
SUBS_PER_BEAT = 4
BEAT_INNER = SUBS_PER_BEAT * SLOT_W
RHYTHM_W = 4 * BEAT_INNER + 3 * BEAT_GAP
BAR_OUTER = BAR_PAD_LEFT + RHYTHM_W + BAR_PAD_RIGHT

BAR_INNER = BAR_OUTER


def unit_to_beat_slot(unit: int) -> tuple[int, int]:
    beat = unit // SUBS_PER_BEAT
    slot = unit % SUBS_PER_BEAT
    return beat, slot


def measure_left(page_left: float, bar_index: int) -> float:
    return page_left + bar_index * BAR_OUTER


def measure_right(page_left: float, bar_index: int) -> float:
    return measure_left(page_left, bar_index) + BAR_OUTER


def rhythm_grid_left(page_left: float, bar_index: int) -> float:
    return measure_left(page_left, bar_index) + BAR_PAD_LEFT


def x_center(grid_left: float, unit: int) -> float:
    beat, slot = unit_to_beat_slot(unit)
    beat_x = grid_left + beat * (BEAT_INNER + BEAT_GAP)
    return beat_x + slot * SLOT_W + SLOT_W / 2


def beat_first_unit(beat_1based: int) -> int:
    """该拍第一个十六分 slot。"""
    return (beat_1based - 1) * SUBS_PER_BEAT


def beat_last_unit(beat_1based: int) -> int:
    """该拍最后一个十六分 slot。"""
    return beat_first_unit(beat_1based) + (SUBS_PER_BEAT - 1)


def beat_center(grid_left: float, beat_1based: int) -> float:
    """拍心（和弦延长线「—」等辅助标记用，不占节奏行首尾间距）。"""
    beat = beat_1based - 1
    beat_x = grid_left + beat * (BEAT_INNER + BEAT_GAP)
    return beat_x + BEAT_INNER / 2


def quarter_unit(beat_1based: int) -> int:
    """已弃用绘制：四分节奏符改用 beat_center（与和弦行、整拍休止一致）。"""
    return beat_first_unit(beat_1based) + 2


def rhythm_quarter_x(grid_left: float, beat_1based: int) -> float:
    return beat_center(grid_left, beat_1based)


def rhythm_rest_x(grid_left: float, beat_1based: int) -> float:
    """整拍休止「—」：拍心，与和弦行对齐；小节右 inset 由固定 BAR_OUTER 保证。"""
    return beat_center(grid_left, beat_1based)


def content_edge_inset_px() -> float:
    return BAR_PAD_LEFT + SLOT_W / 2


def symbol_x_chord(grid_left: float, beat_1based: int) -> float:
    """和弦行与节奏行「每一拍」纵轴对齐：落拍心（整拍列水平中线）。"""
    return beat_center(grid_left, beat_1based)


def symbol_x_rhythm(grid_left: float, unit: int) -> float:
    """节奏行：X 与 — 均按 unit 取 x，四分/十六分/休止不另算边距。"""
    return x_center(grid_left, unit)


def assert_measure_padding(page_left: float, bar_index: int) -> None:
    """小节框内网格：unit 0、unit 15 到左右竖线等距。"""
    ml = measure_left(page_left, bar_index)
    mr = measure_right(page_left, bar_index)
    gx = rhythm_grid_left(page_left, bar_index)
    inset = content_edge_inset_px()
    if abs((x_center(gx, 0) - ml) - inset) > 0.01:
        raise ValueError(f"bar {bar_index} left inset {x_center(gx,0)-ml} != {inset}")
    if abs((mr - x_center(gx, 15)) - inset) > 0.01:
        raise ValueError(f"bar {bar_index} right inset {mr-x_center(gx,15)} != {inset}")


def barline_xs(page_left: float, n_bars: int) -> list[float]:
    """相邻小节共用竖线：measure_right(i) == measure_left(i+1)。"""
    if n_bars <= 0:
        return [page_left]
    xs: list[float] = []
    for i in range(n_bars):
        xs.append(measure_left(page_left, i))
    end = measure_right(page_left, n_bars - 1)
    if not xs or abs(xs[-1] - end) > 0.01:
        xs.append(end)
    return xs


def bar_width(n_bars: int, left: float, right_pad: float) -> float:
    if n_bars <= 0:
        return left + right_pad
    return left + n_bars * BAR_OUTER + right_pad


def bar_x(left: float, bar_index: int) -> float:
    return rhythm_grid_left(left, bar_index)
