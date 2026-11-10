"""Resolve repository root for handbook-rhythm-pattern scripts."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve().parent
    for candidate in (here, *here.parents):
        if (candidate / "docs" / "assets" / "images" / "rhythm-patterns").is_dir():
            return candidate
        if (candidate / "docs" / "staff-scores").is_dir():
            return candidate
    raise RuntimeError("could not find repo root (docs/…/rhythm-patterns or staff-scores)")


def out_dir() -> Path:
    return repo_root() / "docs" / "assets" / "images" / "rhythm-patterns"


def repo_scripts_dir() -> Path:
    return repo_root() / "scripts"
