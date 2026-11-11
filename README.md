# 🎹 和弦 Keys CookBook

> 钢琴弹唱 Cookbook — 从和弦到伴奏再到曲目的系统练习手册

在线阅读：[shaozheliu.github.io/chords-keys-cookbook](https://shaozheliu.github.io/chords-keys-cookbook/)

---

## 项目简介

零构建、零依赖的原生前端小站：JSON 驱动页面，`docs/` 目录直接作为 GitHub Pages 发布根。

| 模块 | 入口 | 说明 |
|------|------|------|
| **和弦库** | `docs/chords/` | 和弦类型 × 12 调：卡片键盘图 + 手型详解 |
| **每日练习** | `docs/practice/` | 五度圈轮动；和弦练习与进行练习（节奏型 + 按拍手型） |
| **和弦进行** | `docs/progressions/` | 进行介绍、组合与 Practice Kit（节奏型 + 按拍手型） |
| **曲目拆解** | `docs/songs/` | 曲目与进行关联（逐步补齐） |

进行练习 **不** 再使用四拍「进行总览长图」，只保留 **节奏型 X 谱** 与 **`measures[]` 引用的手型小图**。

---

## 目录结构

GitHub Pages 发布 **`/docs`**，仓库根只放说明与构建脚本。

```
chords-keys-handbook/
├── README.md                    # 本文件：结构说明、维护入口
├── scripts/                     # Python：生成 SVG、迁移布局、理论链修复
│   ├── asset_paths.py           # 产物路径约定（手型 / 节奏 / 卡片）
│   ├── migrate_asset_layout.py    # 一次性迁移动产目录（可重复运行）
│   ├── gen_*_hand_groups.py       # 手型图 → hands/by-tonic/…
│   ├── gen_card_keyboard.py       # 卡片图 → cards/
│   └── fix_theory_asset_links.py  # 理论 Markdown 内图片路径
│
└── docs/                        # ★ 站点根（用户浏览器访问的根）
    ├── index.html               # 首页
    ├── app/                     # 全站 JS / CSS（数据加载、路径拼接、Practice Kit）
    ├── chords/ practice/        # 各模块 HTML + 模块 JS
    │   progressions/ songs/
    │
    ├── data/                    # 索引层：运行时 fetch 的 JSON
    │   ├── chords.json          # 和弦类型、手型 id、folder→手型色彩映射
    │   ├── practice.json        # 每日练习分组与步骤
    │   ├── progressions.json    # 进行、节奏模板、combos.measures（按拍手型）
    │   └── songs.json
    │
    ├── materials/               # 素材层：源稿与说明（模型主要改这里）
    │   ├── README.md
    │   ├── rhythm/              # 节奏型 YAML、拍型表、index.json
    │   │   ├── cells/
    │   │   ├── by-progression/{id}/score.yaml
    │   │   └── index.json
    │   ├── hands/ README.md     # 手型命名约定
    │   ├── cards/ README.md     # 卡片图约定
    │   └── theory/ README.md    # 理论文（正文在 1–4 篇目录）
    │
    ├── assets/images/           # 产物层：线上引用的 SVG
    │   ├── rhythm/by-progression/{id}/   # X 谱节奏型
    │   ├── hands/by-tonic/{调}/{色彩}/shape-{n}.svg
    │   └── cards/{slug}-{list|hero}.svg
    │
    ├── 1-基础篇/ … 4-实战篇/     # 理论 Markdown（未全接入导航）
    └── staff-scores/            # 五线谱相关（曲目扩展用）
```

### 各层职责（一句话）

| 层 | 路径 | 谁改 | 干什么 |
|----|------|------|--------|
| 表现 | `app/`、各模块 HTML/JS | 功能迭代 | 页面与交互 |
| 索引 | `data/*.json` | 内容迭代 | id、文案、**指向图片的模板**、`measures` 手型引用 |
| 素材 | `materials/` | 你 / Agent | 节奏 YAML、维护说明、拍型表 |
| 产物 | `assets/images/` | **构建脚本** | 浏览器实际请求的 SVG URL |
| 工具 | `scripts/`（仓库根） | 工具链 | 生成与迁移产物 |

### 图片命名（产物 URL）

| 类型 | 路径模式 | 用于 |
|------|----------|------|
| 节奏型 | `rhythm/by-progression/{进行id}/rhythm.svg`（级数谱，每条进行一张） | 练习 / 进行 Practice Kit |
| 手型 | `hands/by-tonic/{调}/{色彩}/shape-{n}.svg` | 和弦详情、按拍指法格 |
| 卡片 | `cards/{slug}-list.svg` · `-hero.svg` | 和弦库列表与详情头图 |

`chords.json` 中的 `folder`（如 `m7-chords`）仍表示手型 **色彩**；`app.js` 映射到 `hands/…/m7/`。

节奏型构建：`.cursor/skills/handbook-rhythm-pattern/`（本地 Agent Skill）；清单见 `docs/materials/rhythm/index.json`。

---

## 本地预览

```bash
python3 -m http.server 8765 --directory docs
# 或 npx serve docs
```

需 HTTP 环境才能 `fetch()` JSON。

---

## 数据维护

- **和弦 / 手型**：改 `chords.json` 或运行 `scripts/gen_*_hand_groups.py`
- **进行**：改 `progressions.json` 的 `combos.measures`（`chordId` + `tonic` + `handShapeId`）与 `rhythmSvgTemplate`
- **节奏源稿**：`docs/materials/rhythm/by-progression/` → 构建写入 `assets/images/rhythm/…`

模块间通过 id 引用：`measures` 只存 `chordId`，不重复和弦定义。

---

## 更新日历

| 日期 | 范围 | 摘要 |
|------|------|------|
| 2026-03-11 | 工程结构 | 素材层 `materials/`；产物分 `rhythm` / `hands` / `cards`；移除进行总览图与 `*-progressions/` |

（后续由 Automation 或手工在此追加。）
