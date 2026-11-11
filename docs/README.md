# 钢琴即兴 · 和弦与键盘手册（前端站点）

本目录即 **GitHub Pages 站点根**。仓库级说明见根部 [`README.md`](../README.md)。

## 站点入口

| 模块 | 路径 |
|------|------|
| 首页 | [`index.html`](./index.html) |
| 和弦库 | [`chords/`](./chords/) |
| 每日练习 | [`practice/`](./practice/) |
| 和弦进行 | [`progressions/`](./progressions/) |
| 曲目 | [`songs/`](./songs/) |

## 站内分层

| 目录 | 用途 |
|------|------|
| [`app/`](./app/) | 公共 `app.js` / `app.css` |
| [`data/`](./data/) | 四个 JSON 索引 |
| [`materials/`](./materials/) | 节奏 YAML、维护说明（非线上 URL） |
| [`assets/images/`](./assets/images/) | 节奏 / 手型 / 卡片 SVG |

资源路径约定：

- 卡片：`assets/images/cards/{slug}-{list|hero}.svg`
- 手型：`assets/images/hands/by-tonic/{调}/{色彩}/shape-{id}.svg`
- 节奏：`assets/images/rhythm/by-progression/{进行id}/…`

## 本地预览

```bash
python3 -m http.server 8765 --directory .
```
