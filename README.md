# 🎹 和弦 Keys CookBook

> 钢琴弹唱 Cookbook — 从和弦到伴奏再到曲目的系统练习手册

在线阅读：[shaozheliu.github.io/chords-keys-cookbook](https://shaozheliu.github.io/chords-keys-cookbook/)

---

## 项目简介

一个零构建、零依赖的原生前端应用，由 JSON 数据层驱动，托管于 GitHub Pages。

围绕钢琴弹唱的四条主线组织：

| 模块 | 入口 | 说明 |
|------|------|------|
| **和弦库** | `docs/chords/` | 9 种和弦类型 × 12 调 × 1~3 手型，三级路由（大全 → 分类 → 详情） |
| **每日练习** | `docs/practice/` | 五度圈周维度轮动，纵向 → 横向 → 视唱三段式练习步骤 |
| **和弦进行** | `docs/progressions/` | 4 条经典进行的级数序列、手型表与节奏型 |
| **曲目拆解** | `docs/songs/` | 经典弹唱曲目的和声分析、段落拆解、伴奏手法与练习要点 |

## 技术栈

- **前端**：原生 HTML5 + ES6+ JavaScript，无框架、无构建步骤
- **样式**：单文件浅色极简设计系统 `docs/app/css/app.css`（沿用原站 `site.css` 的设计令牌与组件语言），无 UI 框架、无外部字体/CDN 依赖
- **数据层**：4 个静态 JSON（`docs/data/`），通过 `fetch()` 异步加载
- **资源**：533 张预生成 SVG 键盘图 / 手型图 / 进行图 / 节奏型（`docs/assets/images/`）
- **部署**：GitHub Pages 直接托管 `docs/` 目录

### 设计语言

以 `#fafafa` 底色、`#0a0a0a` 墨色、`#e5e5e5` 细线与 16px 圆角卡片构成的浅色极简界面：

- 顶部固定导航栏：左侧品牌，中间居中文案导航（当前模块以墨色下划线标示）
- 内容区：「分类筛选 chips → 区块标题 → 三栏卡片网格」的稳定节奏
- 详情区：左侧主内容（hero 卡 / 信息表 / 手位图）+ 右侧相关栏
- 键盘图统一以白底卡片呈现，形成视觉焦点

## 目录结构

```
├── docs/                      # GitHub Pages 根目录
│   ├── index.html             # 首页，四个模块入口
│   ├── app/                   # 公共前端资源（app.js / app.css）
│   ├── data/                  # JSON 数据层（chords / practice / progressions / songs）
│   ├── chords/                # 和弦库（index / family / detail + js）
│   ├── practice/              # 每日练习模块
│   ├── progressions/          # 和弦进行模块
│   ├── songs/                 # 曲目拆解模块
│   ├── assets/images/         # SVG 资源
│   └── 1-基础篇 ~ 4-实战篇/    # 理论 Markdown（内容储备，暂未接入导航）
└── scripts/                   # Python SVG 与静态页生成脚本
```

## 本地预览

`fetch()` 需要 HTTP 环境，直接双击 HTML 无法加载数据。任选一种方式起本地服务：

```bash
npx serve docs        # 或
python -m http.server 8000 --directory docs
```

然后访问 `http://localhost:3000/`（serve 默认端口）或 `http://localhost:8000/`。

## 数据维护

所有内容集中在 `docs/data/` 下的 4 个 JSON 文件：

- `chords.json` — 和弦家族、9 种和弦定义（音程 / 公式 / 音色 / 手型 / 声部排列）、12 调与 slug 映射
- `practice.json` — 周维度轮动分组与各和弦的练习步骤
- `progressions.json` — 和弦进行的小节定义（通过 `chordId` 引用 `chords.json`）
- `songs.json` — 曲目五维度数据（通过 `progressionId` 关联进行）

模块间通过 id 引用解耦：练习与进行只存 `chordId`，曲目只存 `progressionId`，运行时查表渲染。

## SVG 生成

`scripts/` 下的 Python 脚本负责生成 `docs/assets/images/` 中的全部 SVG。命名约定：

- 卡片图：`card-keys/{slug}-{list|hero}.svg`
- 手型图：`{folder}/{调名}-hand-shape-{手型id}.svg`
- 进行图：`{folder}/{调名}-progression.svg`
- 节奏型：`rhythm-patterns/{名称}.svg`
