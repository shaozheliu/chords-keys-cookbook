# 各层级卡片用的标准琴键图。
# 固定 13 白键（C→下一组 A），样式对齐参考图。
# 列表 228×128，详情主图 360×202。
# 示例：A 大三和弦（A - C♯ - E）。

from pathlib import Path

from piano_svg import CARD_HERO, CARD_LIST, write_card_svg

# C4=60 起的标准 13 白键：C4…A5
# A 大三：A4=69, C#5=73, E5=76；再标高八度 A5=81 更完整
A_MAJOR = {69, 73, 76, 81}

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'card-keys'


def main():
    list_w, list_h = CARD_LIST
    hero_w, hero_h = CARD_HERO
    # 列表卡字小，仍保留标签；主图同样标准 13 键
    write_card_svg(OUT / 'a-major-list.svg', list_w, list_h, A_MAJOR, start_c=60, show_labels=True)
    write_card_svg(OUT / 'a-major-hero.svg', hero_w, hero_h, A_MAJOR, start_c=60, show_labels=True)
    print(f'a-major-list.svg {list_w}×{list_h}  whites=13')
    print(f'a-major-hero.svg {hero_w}×{hero_h}  whites=13')


if __name__ == '__main__':
    main()
