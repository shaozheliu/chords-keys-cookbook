# ============================================================
# 自动生成 docs/_sidebar.md 的脚本（支持：篇 → 章 → 分组/节 → 子节）
# 约定：
#   - docs 下每个顶层文件夹 = 一个「篇」，命名「N-篇名」，N 为数字决定顺序
#   - 篇内直接放置的 .md 文件 = 「章」（无节），其首个 # H1 作为章标题
#   - 篇内子文件夹 = 「章」，命名「N-章名」，章名作为章标题；
#     若子文件夹内有 README.md，则章条目链接到 README.md（作为目录页）
#   - 章内条目：
#     * 直接 .md 文件 = 「节」，其首个 # H1 作为节标题；
#       仅当无 README.md 时在侧栏展开，有 README.md 时由目录页自行导航
#     * 子文件夹 = 「分组」，命名「N-组名」，组名作为分组标题，
#       组内 .md 文件 = 「子节」，其首个 # H1 作为子节标题；分组始终展开
#   - 编号：篇 = 第X部分（中文）；章 = X.Y；节/组 = X.Y.Z；子节 = X.Y.Z.W
# 用法：
#   python scripts/gen_sidebar.py
# 输出：
#   docs/_sidebar.md（由本脚本生成，请勿手动编辑）
# ============================================================

import re
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / 'docs'
SIDEBAR_PATH = DOCS_DIR / '_sidebar.md'


def extract_h1(md_path: Path):
    """读取 markdown 文件的首个 H1 标题文本；找不到返回 None。"""
    text = md_path.read_text(encoding='utf-8-sig')
    for line in text.splitlines():
        m = re.match(r'^#\s+(.+?)\s*$', line)
        if m:
            return m.group(1).strip()
    return None


def leading_number(name: str):
    """从名称开头提取数字，用于排序；无数字则返回 None。"""
    m = re.match(r'^(\d+)', name)
    return int(m.group(1)) if m else None


def sort_key(name: str):
    """排序键：有数字前缀的按数字排，无数字的排到后面按名称排。"""
    n = leading_number(name)
    return (0, n, name) if n is not None else (1, 0, name)


def strip_prefix(name: str) -> str:
    """去掉名称开头的 'N-' 前缀，用于从文件夹/文件名推导标题。"""
    return re.sub(r'^\d+-', '', name)


def cn_num(n: int) -> str:
    """把 1~99 的整数转成中文数字，超范围回退阿拉伯数字。"""
    digits = '零一二三四五六七八九'
    if 1 <= n <= 10:
        return {1: '一', 2: '二', 3: '三', 4: '四', 5: '五',
                6: '六', 7: '七', 8: '八', 9: '九', 10: '十'}[n]
    if 11 <= n <= 19:
        return '十' + (digits[n - 10] if n - 10 else '')
    if 20 <= n <= 99:
        tens, ones = divmod(n, 10)
        return digits[tens] + '十' + (digits[ones] if ones else '')
    return str(n)


def is_md_file(path: Path) -> bool:
    """是否为需要纳入目录的 markdown 文件（排除下划线开头的内部文件）。"""
    return path.is_file() and path.suffix.lower() == '.md' and not path.name.startswith('_')


def collect_items(dir_path: Path):
    """收集目录下的条目：直接 .md 文件 + 带数字前缀的子文件夹，统一排序。"""
    items = []
    for child in dir_path.iterdir():
        if child.name.startswith('_'):
            continue
        if is_md_file(child):
            items.append(('file', child))
        elif child.is_dir() and leading_number(child.name) is not None:
            items.append(('dir', child))
    items.sort(key=lambda it: sort_key(it[1].name))
    return items


def collect_parts():
    """扫描 docs 生成节点树：[(篇标题, [章节点...])...]。

    节点为 ('file', 标题, md路径) 或 ('group', 标题, 链接|None, [子节点...])。
    """
    part_dirs = [p for p in DOCS_DIR.iterdir()
                 if p.is_dir() and leading_number(p.name) is not None]
    part_dirs.sort(key=lambda p: sort_key(p.name))

    parts = []
    for part_dir in part_dirs:
        part_title = strip_prefix(part_dir.name)

        chapters = []
        for kind, path in collect_items(part_dir):
            if kind == 'file':
                # 篇内直接 .md 文件 = 章（无节）
                chapters.append(('file', extract_h1(path) or path.stem, path))
            else:  # dir = 章
                title = strip_prefix(path.name)
                readme = path / 'README.md'
                link = readme if readme.exists() else None
                children = []
                for child_kind, child_path in collect_items(path):
                    if child_kind == 'file':
                        # 有 README（目录页）时，直接明细由目录页导航，侧栏不展开
                        if link is None:
                            children.append(('file', extract_h1(child_path) or child_path.stem, child_path))
                    else:  # 子文件夹 = 分组，始终展开
                        group_title = strip_prefix(child_path.name)
                        group_children = []
                        for md in sorted([f for f in child_path.iterdir() if is_md_file(f)],
                                         key=lambda f: sort_key(f.name)):
                            group_children.append(('file', extract_h1(md) or md.stem, md))
                        children.append(('group', group_title, None, group_children))
                chapters.append(('group', title, link, children))
        parts.append((part_title, chapters))
    return parts


def render_node(lines, node, nums, indent):
    """递归渲染单个节点（file 或 group）为侧栏行。"""
    pad = '  ' * indent
    kind = node[0]
    if kind == 'file':
        title, md_path = node[1], node[2]
        rel = md_path.relative_to(DOCS_DIR).as_posix()
        label = '.'.join(map(str, nums)) + ' ' + title
        lines.append(f'{pad}- [{label}]({rel})')
    else:  # group
        title, link, children = node[1], node[2], node[3]
        label = '.'.join(map(str, nums)) + ' ' + title
        if link is not None:
            rel = link.relative_to(DOCS_DIR).as_posix()
            lines.append(f'{pad}- [{label}]({rel})')
        else:
            lines.append(f'{pad}- {label}')
        for idx, child in enumerate(children, start=1):
            render_node(lines, child, nums + [idx], indent + 1)


def build_sidebar(parts):
    """根据篇结构生成 _sidebar.md 内容。"""
    lines = [
        '<!-- 本文件由 scripts/gen_sidebar.py 自动生成，请勿手动编辑 -->',
        '',
        '- [🏠 首页](/)',
    ]
    for part_idx, (part_title, chapters) in enumerate(parts, start=1):
        lines.append(f'- 第{cn_num(part_idx)}部分 {part_title}')
        for ch_idx, chapter in enumerate(chapters, start=1):
            render_node(lines, chapter, [part_idx, ch_idx], indent=1)
    return '\n'.join(lines) + '\n'


def count_files(nodes):
    """递归统计 file 节点（叶子文档）数量。"""
    total = 0
    for node in nodes:
        if node[0] == 'file':
            total += 1
        else:
            total += count_files(node[3])
    return total


def main():
    parts = collect_parts()
    content = build_sidebar(parts)
    SIDEBAR_PATH.write_text(content, encoding='utf-8')
    part_count = len(parts)
    chapter_count = sum(len(chapters) for _, chapters in parts)
    file_count = sum(count_files(chapters) for _, chapters in parts)
    print(f'已生成 {SIDEBAR_PATH}（{part_count} 篇 / {chapter_count} 章 / {file_count} 文档）')


if __name__ == '__main__':
    main()
