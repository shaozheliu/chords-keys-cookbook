# 按 Figma 三级页面生成和弦目录站：
#   docs/chords/            和弦大全
#   docs/chords/<family>/   分类列表
#   docs/chords/<slug>/     和弦详情
# 同时写出卡片琴键图（固定 13 个白键）。

import html
from pathlib import Path
from urllib.parse import quote

from piano_svg import CARD_HERO, CARD_LIST, write_card_svg

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
CHORDS = DOCS / 'chords'
KEYS = DOCS / 'assets' / 'images' / 'card-keys'

TONICS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']
TONIC_PC = {
    'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11,
    'F#': 6, 'Db': 1, 'Ab': 8, 'Eb': 3, 'Bb': 10, 'F': 5,
}
SLUG_TONIC = {
    'C': 'c', 'G': 'g', 'D': 'd', 'A': 'a', 'E': 'e', 'B': 'b',
    'F#': 'f-sharp', 'Db': 'd-flat', 'Ab': 'a-flat', 'Eb': 'e-flat',
    'Bb': 'b-flat', 'F': 'f',
}
CN = {
    'C': 'C', 'G': 'G', 'D': 'D', 'A': 'A', 'E': 'E', 'B': 'B',
    'F#': '升F', 'Db': '降D', 'Ab': '降A', 'Eb': '降E', 'Bb': '降B', 'F': 'F',
}

LETTER_INDEX = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
PC_OF = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
LETTERS = 'CDEFGAB'
LETTER_STEPS = {0: 0, 2: 1, 3: 2, 4: 2, 5: 3, 7: 4, 9: 5, 10: 6, 11: 6}


def spell(root, interval):
    letter = LETTERS[(LETTER_INDEX[root[0]] + LETTER_STEPS[interval]) % 7]
    diff = ((TONIC_PC[root] + interval) % 12 - PC_OF[letter]) % 12
    if diff > 6:
        diff -= 12
    return letter + {0: '', 1: '#', 2: '##', -1: 'b', -2: 'bb'}[diff]


def pitches(root, intervals):
    pcs = {(TONIC_PC[root] + i) % 12 for i in intervals}
    return {p for p in range(60, 82) if p % 12 in pcs}


def e(text):
    return html.escape(str(text), quote=True)


KINDS = {
    'major': {
        'section': '大三和弦',
        'type_name': '大三和弦',
        'intervals': (0, 4, 7),
        'formula': '1 - 3 - 5',
        'tone': '明亮、开阔、稳定',
        'style': '流行 / 民谣 / 乡村',
        'folder': 'major-triads',
        'suffix': 'major',
        'symbol': lambda t: t,
        'title': lambda t: f'{CN[t]}大调和弦',
        'hands': [
            (1, '手型一 · 紧凑型', '左手 3 指弹根音，右手 1-2-4 指弹三音和弦。'),
            (2, '手型二 · 丰满型', '左手 5 指与 2 指弹根音和五音，右手 1-2-3-5 指弹四音和弦。'),
        ],
    },
    'minor': {
        'section': '小三和弦',
        'type_name': '小三和弦',
        'intervals': (0, 3, 7),
        'formula': '1 - ♭3 - 5',
        'tone': '柔和、内敛、暗淡',
        'style': '抒情 / 民谣 / 流行',
        'folder': 'minor-triads',
        'suffix': 'minor',
        'symbol': lambda t: f'{t}m',
        'title': lambda t: f'{CN[t]}小调和弦',
        'hands': [
            (1, '手型一 · 紧凑型', '左手 3 指弹根音，右手 1-2-4 指弹五音、根音、降三音。'),
            (2, '手型二 · 扩张型', '左手 5 指与 2 指弹根音和五音，右手 1-2-3-5 指弹根音、降三音、五音和高八度根音。'),
        ],
    },
    'dom7': {
        'section': '属七和弦',
        'type_name': '属七和弦',
        'intervals': (0, 4, 7, 10),
        'formula': '1 - 3 - 5 - ♭7',
        'tone': '紧张、有推动力',
        'style': '布鲁斯 / 流行 / 爵士',
        'folder': 'dom7-chords',
        'suffix': '7',
        'symbol': lambda t: f'{t}7',
        'title': lambda t: f'{CN[t]}属七和弦',
        'hands': [
            (1, '手型一', '左手 3 指与 1 指弹根音和五音，右手 1-2-4 指弹七音、三音、五音。'),
            (2, '手型二', '左手 5-3-1 指弹根音、五音、七音，右手 1-2-3-5 指弹根音、三音、五音和高八度根音。'),
        ],
    },
    'm7': {
        'section': '小七和弦',
        'type_name': '小七和弦',
        'intervals': (0, 3, 7, 10),
        'formula': '1 - ♭3 - 5 - ♭7',
        'tone': '柔和、流动',
        'style': '流行 / R&B / 爵士',
        'folder': 'm7-chords',
        'suffix': 'm7',
        'symbol': lambda t: f'{t}m7',
        'title': lambda t: f'{CN[t]}小七和弦',
        'hands': [
            (1, '手型一', '左手 3 指与 1 指弹根音和五音，右手 1-2-4 指弹七音、三音、五音。'),
            (2, '手型二', '左手 5-2-1 指弹根音、五音和高八度根音，右手 1-2-3-5 指弹三音、五音、七音和高八度三音。'),
        ],
    },
    'maj7': {
        'section': '大七和弦',
        'type_name': '大七和弦',
        'intervals': (0, 4, 7, 11),
        'formula': '1 - 3 - 5 - 7',
        'tone': '明亮、梦幻',
        'style': '流行 / 爵士 / 民谣',
        'folder': 'maj7-chords',
        'suffix': 'maj7',
        'symbol': lambda t: f'{t}maj7',
        'title': lambda t: f'{CN[t]}大七和弦',
        'hands': [
            (1, '手型一 · 收缩型', '左手 3 指弹根音，右手 1-2-4 指弹五音、七音、三音。'),
            (2, '手型二 · 中间型', '左手 5 指与 1 指弹根音和高八度根音，右手 1-2-4 指弹三音、五音、七音。'),
            (3, '手型三 · 扩张型', '左手 5-2-1 指弹根音、五音和高八度根音，右手 1-2-3-5 指弹三音、五音、七音和高八度三音。'),
        ],
    },
    'sus2': {
        'section': '挂二和弦',
        'type_name': '挂二和弦',
        'intervals': (0, 2, 7),
        'formula': '1 - 2 - 5',
        'tone': '开放、悬置',
        'style': '流行 / 民谣',
        'folder': 'sus2-chords',
        'suffix': 'sus2',
        'symbol': lambda t: f'{t}sus2',
        'title': lambda t: f'{CN[t]}挂二和弦',
        'hands': [
            (1, '手型一 · 紧凑型', '左手 3 指弹根音，右手 1-2-3 指弹五音、根音、二音。'),
            (2, '手型二 · 扩张型', '左手 5-2-1 指弹根音、五音和高八度根音，右手 1-2-5 指弹二音、五音和高八度二音。'),
        ],
    },
    'sus4': {
        'section': '挂四和弦',
        'type_name': '挂四和弦',
        'intervals': (0, 5, 7),
        'formula': '1 - 4 - 5',
        'tone': '悬置、等待解决',
        'style': '流行 / 摇滚',
        'folder': 'sus4-chords',
        'suffix': 'sus4',
        'symbol': lambda t: f'{t}sus4',
        'title': lambda t: f'{CN[t]}挂四和弦',
        'hands': [
            (2, '手型二 · 扩张型', '左手 5 指与 2 指弹根音和五音，右手 1-2-3-5 指弹根音、四音、五音和高八度根音。'),
        ],
    },
    'add9': {
        'section': '加九和弦',
        'type_name': '加九和弦',
        'intervals': (0, 2, 4, 7),
        'formula': '1 - 2 - 3 - 5',
        'tone': '明亮、带色彩',
        'style': '流行 / 民谣',
        'folder': 'add9-chords',
        'suffix': 'add9',
        'symbol': lambda t: f'{t}add9',
        'title': lambda t: f'{CN[t]}加九和弦',
        'hands': [
            (1, '手型一 · 收缩型', '左手 3 指弹根音，右手 1-2-3-4 指弹五音、根音、九音、三音。'),
            (2, '手型二 · 扩张型', '左手 5-4-1 指弹根音、五音和高八度根音，右手 1-2-3-5 指弹九音、三音、五音和高八度根音。'),
        ],
    },
    'maj6': {
        'section': '六和弦',
        'type_name': '六和弦',
        'intervals': (0, 4, 7, 9),
        'formula': '1 - 3 - 5 - 6',
        'tone': '温暖、复古',
        'style': '爵士 / 流行 / 民谣',
        'folder': 'maj6-chords',
        'suffix': '6',
        'symbol': lambda t: f'{t}6',
        'title': lambda t: f'{CN[t]}六和弦',
        'hands': [
            (1, '手型一 · 收缩型', '左手 3 指与 1 指弹根音和五音，右手 1-2-4 指弹六音、根音、三音。'),
            (2, '手型二 · 扩张型', '左手 5 指与 2 指弹根音和五音，右手 1-2-3-4 指弹根音、三音、五音、六音。'),
        ],
    },
}

FAMILIES = [
    {
        'id': 'triads',
        'title': '三和弦',
        'lead': '共 2 个子类型，24 个和弦。大三与小三是钢琴即兴最常用的基础色彩。',
        'kinds': ['major', 'minor'],
        'chips': [
            ('major', '大三和弦 (12)', '#major'),
            ('minor', '小三和弦 (12)', '#minor'),
            ('suspended', '挂留和弦 (24)', '../suspended/'),
            ('added', '加音和弦 (24)', '../added/'),
        ],
    },
    {
        'id': 'sevenths',
        'title': '七和弦',
        'lead': '共 3 个子类型，36 个和弦。属七负责推动，小七与大七负责色彩。',
        'kinds': ['dom7', 'm7', 'maj7'],
        'chips': [
            ('dom7', '属七和弦 (12)', '#dom7'),
            ('m7', '小七和弦 (12)', '#m7'),
            ('maj7', '大七和弦 (12)', '#maj7'),
            ('triads', '三和弦 (24)', '../triads/'),
        ],
    },
    {
        'id': 'suspended',
        'title': '挂留和弦',
        'lead': '共 2 个子类型，24 个和弦。挂二更开放，挂四更倾向于解决。',
        'kinds': ['sus2', 'sus4'],
        'chips': [
            ('sus2', '挂二和弦 (12)', '#sus2'),
            ('sus4', '挂四和弦 (12)', '#sus4'),
            ('triads', '三和弦 (24)', '../triads/'),
            ('added', '加音和弦 (24)', '../added/'),
        ],
    },
    {
        'id': 'added',
        'title': '加音和弦',
        'lead': '共 2 个子类型，24 个和弦。加九与六和弦都在三和弦上加一个色彩音。',
        'kinds': ['add9', 'maj6'],
        'chips': [
            ('add9', '加九和弦 (12)', '#add9'),
            ('maj6', '六和弦 (12)', '#maj6'),
            ('triads', '三和弦 (24)', '../triads/'),
            ('suspended', '挂留和弦 (24)', '../suspended/'),
        ],
    },
]


def slug_of(kind_id, tonic):
    kind = KINDS[kind_id]
    suffix = kind['suffix']
    base = SLUG_TONIC[tonic]
    if suffix == '7':
        return f'{base}7'
    if suffix in ('m7', 'maj7', 'sus2', 'sus4', 'add9'):
        return base + suffix
    if suffix == '6':
        return f'{base}6'
    return f'{base}-{suffix}'


def chord(kind_id, tonic, symbol=None, title=None):
    kind = KINDS[kind_id]
    return {
        'kind': kind_id,
        'tonic': tonic,
        'slug': slug_of(kind_id, tonic),
        'symbol': symbol or kind['symbol'](tonic),
        'title': title or kind['title'](tonic),
        'notes': ' - '.join(spell(tonic, i) for i in kind['intervals']),
    }


def asset_name(name):
    return quote(name, safe='')


def shell(title, depth, body):
    up = '../' * depth
    home = up or './'
    chords = '../' * (depth - 1) if depth > 1 else './'
    css = '../' * (depth - 1) + 'site.css' if depth > 1 else 'site.css'
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)} — 钢琴即兴</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎹</text></svg>">
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="{home}">钢琴即兴</a>
    <nav class="site-nav">
      <a href="{home}">首页</a>
      <a class="active" href="{chords}">和弦</a>
    </nav>
  </header>
  <main class="page">
{body}
  </main>
  <footer class="site-footer">
    <div>钢琴即兴 · 自学手册</div>
    <nav>
      <a href="{home}">首页</a>
      <a href="{chords}">和弦</a>
    </nav>
    <div>© 2026 Chords &amp; Keys Handbook</div>
  </footer>
</body>
</html>
'''


def crumb(items):
    parts = []
    for label, href in items[:-1]:
        parts.append(f'<a href="{href}">{e(label)}</a>')
    parts.append(e(items[-1][0]))
    return '<p class="crumb">' + ' / '.join(parts) + '</p>'


def chips(items, active):
    out = ['<div class="chips">']
    for cid, label, href in items:
        cls = 'chip active' if cid == active else 'chip'
        out.append(f'<a class="{cls}" href="{href}">{e(label)}</a>')
    out.append('</div>')
    return '\n'.join(out)


def card_html(item, img_prefix, href_prefix):
    src = f'{img_prefix}card-keys/{item["slug"]}-list.svg'
    href = f'{href_prefix}{item["slug"]}/'
    return f'''<a class="chord-card" href="{href}">
  <div class="chord-copy"><strong>{e(item["symbol"])}</strong><span>{e(item["title"])}</span></div>
  <img src="{src}" alt="{e(item["title"])}键盘" width="228" height="128">
</a>'''


def section_html(title, cards, img_prefix, href_prefix, anchor, more=None):
    more_html = f'<a href="{more}">查看全部 →</a>' if more else '<span></span>'
    grid = '\n'.join(card_html(c, img_prefix, href_prefix) for c in cards)
    return f'''<section class="section" id="{anchor}">
  <div class="section-head"><h2>{e(title)}</h2>{more_html}</div>
  <div class="card-grid">
{grid}
  </div>
</section>'''


def write_page(path, title, depth, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(shell(title, depth, body), encoding='utf-8')


def write_images():
    list_w, list_h = CARD_LIST
    hero_w, hero_h = CARD_HERO
    for kind_id, kind in KINDS.items():
        for tonic in TONICS:
            item = chord(kind_id, tonic)
            notes = pitches(tonic, kind['intervals'])
            write_card_svg(KEYS / f'{item["slug"]}-list.svg', list_w, list_h, notes)
            write_card_svg(KEYS / f'{item["slug"]}-hero.svg', hero_w, hero_h, notes)


def write_index():
    img = '../assets/images/'
    preview = {
        'major': [
            chord('major', t) for t in ('A', 'Bb', 'B', 'C', 'Db', 'D')
        ],
        'sevenths': [
            chord('dom7', 'A'),
            chord('m7', 'A'),
            chord('maj7', 'C'),
            chord('dom7', 'D'),
            chord('m7', 'E'),
            chord('dom7', 'G'),
        ],
        'suspended': [
            chord('sus2', 'A'),
            chord('sus4', 'A'),
            chord('sus2', 'D'),
            chord('sus4', 'D'),
            chord('sus4', 'E'),
            chord('sus4', 'G'),
        ],
    }
    # 列表页与 Figma 一致：这一张预览写成升C，详情页仍用降D记谱。
    for item in preview['major']:
        if item['tonic'] == 'Db':
            item['symbol'] = 'C#'
            item['title'] = '升C大调和弦'
    body = [
        crumb([('首页', '../'), ('和弦', None)]),
        '<h1>钢琴和弦大全</h1>',
        '<p class="lead">和弦是钢琴即兴的基础。每个和弦都配有键盘图、构成说明和练习建议。</p>',
        chips([
            ('triads', '三和弦 (24)', '#triads'),
            ('sevenths', '七和弦 (36)', '#sevenths'),
            ('suspended', '挂留和弦 (24)', '#suspended'),
            ('added', '加音和弦 (24)', 'added/'),
        ], 'triads'),
        section_html('三和弦', preview['major'], img, '', 'triads', 'triads/'),
        section_html('七和弦', preview['sevenths'], img, '', 'sevenths', 'sevenths/'),
        section_html('挂留和弦', preview['suspended'], img, '', 'suspended', 'suspended/'),
    ]
    write_page(CHORDS / 'index.html', '钢琴和弦大全', 1, '\n'.join(body))


def write_family(family):
    img = '../../assets/images/'
    blocks = []
    for kind_id in family['kinds']:
        kind = KINDS[kind_id]
        cards = [chord(kind_id, t) for t in TONICS]
        blocks.append(section_html(kind['section'], cards, img, '../', kind_id))
    body = '\n'.join([
        crumb([('首页', '../../'), ('和弦', '../'), (family['title'], None)]),
        f'<h1>{e(family["title"])}</h1>',
        f'<p class="lead">{e(family["lead"])}</p>',
        chips(family['chips'], family['kinds'][0]),
        *blocks,
    ])
    write_page(CHORDS / family['id'] / 'index.html', family['title'], 2, body)


def write_detail(kind_id, tonic):
    kind = KINDS[kind_id]
    item = chord(kind_id, tonic)
    family = next(f for f in FAMILIES if kind_id in f['kinds'])
    img = '../../assets/images/'
    hero = f'{img}card-keys/{item["slug"]}-hero.svg'
    rows = [
        ('根音', tonic),
        ('和弦类型', kind['type_name']),
        ('组成音', item['notes']),
        ('音程关系', kind['formula']),
        ('音色特征', kind['tone']),
        ('适用风格', kind['style']),
    ]
    info = '\n'.join(
        f'<div class="info-row"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in rows
    )
    hands = []
    for idx, label, sentence in kind['hands']:
        filename = f'{tonic}-hand-shape-{idx}.svg'
        path = DOCS / 'assets' / 'images' / kind['folder'] / filename
        if not path.exists():
            continue
        src = img + kind['folder'] + '/' + asset_name(filename)
        hands.append(f'''<div class="hand-block">
  <h3>{e(label)}</h3>
  <p>{e(sentence)}</p>
  <img src="{src}" alt="{e(item["title"])} {e(label)}" width="640" height="360">
</div>''')
    body = f'''{crumb([
        ('首页', '../../'),
        ('和弦', '../'),
        (family['title'], f'../{family["id"]}/'),
        (item['symbol'], None),
    ])}
<article class="detail-layout">
  <div class="detail-main">
    <div class="hero-card">
      <div>
        <h1 class="hero-symbol">{e(item["symbol"])}</h1>
        <p class="hero-name">{e(item["title"])}</p>
      </div>
      <img src="{hero}" alt="{e(item["title"])}键盘" width="360" height="202">
    </div>
    <section>
      <h2 class="block-title">和弦信息</h2>
      <div class="info">
{info}
      </div>
    </section>
    <section class="practice">
      <h2 class="block-title">练习建议</h2>
      {''.join(hands)}
    </section>
  </div>
  <aside class="related">
    <h2>相关歌曲</h2>
    <div class="placeholder">敬请期待</div>
  </aside>
</article>'''
    write_page(CHORDS / item['slug'] / 'index.html', item['title'], 2, body)


def main():
    write_images()
    write_index()
    for family in FAMILIES:
        write_family(family)
    count = 0
    for kind_id in KINDS:
        for tonic in TONICS:
            write_detail(kind_id, tonic)
            count += 1
    print(f'cards written to {KEYS}')
    print(f'detail pages: {count}')
    print(f'catalog: {CHORDS}')


if __name__ == '__main__':
    main()
