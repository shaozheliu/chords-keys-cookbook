# 钢琴即兴 · 和弦与键盘手册（前端站点）

本目录即 GitHub Pages 的站点根目录，前置说明见仓库根部的 [`README.md`](../README.md)。

## 站点入口

| 模块 | 入口 |
|------|------|
| 首页（四模块分流） | [`index.html`](./index.html) |
| 和弦库 | [`chords/`](./chords/) |
| 每日练习 | [`practice/`](./practice/) |
| 和弦进行 | [`progressions/`](./progressions/) |
| 曲目拆解 | [`songs/`](./songs/) |

## 目录约定

```
docs/
├── index.html          # 首页
├── app/                # 公共前端资源
│   ├── css/app.css     # 浅色极简设计系统（设计令牌 + 组件样式）
│   └── js/app.js       # 数据加载 / SVG 路径 / 卡片与导航渲染
├── data/               # JSON 数据层
│   ├── chords.json       # 和弦家族与 9 种和弦定义、12 调映射
│   ├── practice.json     # 周维度轮动分组与练习步骤
│   ├── progressions.json # 和弦进行与逐小节手位
│   └── songs.json        # 曲目五维度拆解
├── chords/             # 和弦库（index / family / detail + js/chords.js）
├── practice/           # 每日练习
├── progressions/       # 和弦进行
├── songs/              # 曲目拆解
├── assets/images/      # 预生成 SVG（键盘图 / 手型图 / 进行图 / 节奏型）
└── 1-基础篇 ~ 4-实战篇/ # 理论 Markdown，作为内容储备，暂未接入导航
```

## 本地预览

`fetch()` 需要 HTTP 环境：

```bash
npx serve docs        # 或
python -m http.server 8000 --directory docs
```

## 内部约定

- **路由**：静态服务器会把 `xxx.html` 301 到无扩展名路径并丢弃查询串，因此模块内部统一用 hash 传参
  （`detail.html#slug=c-major`、`family.html#type=sevenths`、`progressions/#4566`）。
- **资源命名**：卡片图 `card-keys/{slug}-{list|hero}.svg`；手型图 `{folder}/{调名}-hand-shape-{id}.svg`；
  进行图 `{folder}/{调名}-progression.svg`。`major` / `minor` 后缀用连字符（`c-major`），其余直接拼接（`c7`、`csus4`）。
- **模块解耦**：练习与进行只存 `chordId`，曲目只存 `progressionId`，运行时查表渲染。
