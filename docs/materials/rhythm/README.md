# 节奏型素材

按 **和弦进行 id** 分子目录，每进行包含：

- `README.md`（可选）：练习讲法、与 `progressions.json` 的对应关系  
- `score.yaml`：`rhythm-score/1` 源稿  

共用拍型表：`cells/canon.yaml`。构建清单：`index.json`。

产物路径：`docs/assets/images/rhythm/by-progression/{进行id}/`，站点通过 `progressions.json` 的 `rhythmSvgTemplate` 引用。
