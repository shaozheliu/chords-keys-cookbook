# 素材层（materials）

本目录存放 **可编辑源稿与说明**，不直接作为 GitHub Pages 的默认 URL 根。浏览器加载的 SVG 在 `../assets/images/`；站点逻辑在 `../data/` 与 `../app/`。

| 子目录 | 用途 |
|--------|------|
| [`rhythm/`](./rhythm/) | 节奏型 X 谱：按和弦进行分的 YAML 与构建索引 |
| [`hands/`](./hands/) | 手型说明与约定（图在 `assets/images/hands/`） |
| [`cards/`](./cards/) | 和弦库卡片键盘图说明（图在 `assets/images/cards/`） |
| [`theory/`](./theory/) | 理论文章储备（正文暂在 `../1-基础篇`～`../4-实战篇`） |

维护顺序：改素材 → 跑 `scripts/` 或 rhythm skill 构建 → 更新 `data/*.json`（若路径或 id 变化）→ 本地 `python -m http.server --directory docs` 预览。
