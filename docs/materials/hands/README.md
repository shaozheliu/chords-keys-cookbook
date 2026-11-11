# 手型素材

练习与进行按拍展示 **单和弦指法小图**，路径规则：

`assets/images/hands/by-tonic/{调}/{色彩}/shape-{1|2|3}.svg`

`{色彩}` 与 `chords.json` 里和弦类型的 `folder` 对应（如 `m7-chords` → `m7`）。详见仓库根 `scripts/asset_paths.py` 中的 `HAND_IMAGE_FOLDER_TO_KIND`。

生成：`scripts/gen_*_hand_groups.py`。
