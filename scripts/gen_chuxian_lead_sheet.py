# ============================================================
# 《出现又离开》弹唱谱小样生成器（主歌一·前八句）
#
# 流程：Python 生成 .ly 源文件 → 调用 lilypond（SVG 后端）→ 输出 SVG。
# 小样内容 = 和弦记号 + 单谱表柱式 voicing + 中文歌词（不含旋律，旋律待用户
# 以简谱文本提供后填入 MELODY 变量，并在 score 块中启用旋律声部）。
#
# 依赖：brew install lilypond
# 输出：docs/assets/images/songs/chuxian-you-likai-ver1.{ly,svg}
# 自包含，不 import 其他脚本。
# ============================================================

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ------------------------------------------------------------
# 数据：主歌（一）前八句（用户提供和弦，歌词见 2-出现又离开.md 弹唱谱表）
# 每小节一个和弦；voicing 为紧凑把位（半音移调只改 CHORDS/VOICINGS 即可）。
# ------------------------------------------------------------
KEY = 'a'          # A 大调
TIME = '4/4'
TEMPO = '4 = 80'

CHORDS = [
    'a1',          # 我和你
    'e/gis',       # 本应该
    'fis:m',       # 各自好
    'a:sus2/e',    # 各自坏（用户指定 Asus2/E，与文档表格的 E 不同）
    'd',           # 各自生活的
    'a',           # 自在
    'd',           # 毫无关联的
    'e',           # 存在
]

# 单谱表柱式 voicing（LilyPond 音名：小字组 a3~e4 一带，突出 A→G#→F# 低音级进）
VOICINGS = [
    "<a cis' e'>1",    # A
    "<gis b e'>1",     # E/G#
    "<fis a cis'>1",   # F#m
    "<e a b>1",        # Asus2/E
    "<d fis a>1",      # D
    "<a cis' e'>1",    # A
    "<d fis a>1",      # D
    "<e gis b>1",      # E
]

# 歌词：时值仅用于把音节均匀摆进小节（2+4+4 或 2+2），不代表真实节奏
LYRICS = (
    '我2 和4 你4 本2 应4 该4 各2 自4 好4 各2 自4 坏4 '
    '各2 自4 生4 活4 的4 自2 在2 毫2 无4 关4 联4 的4 存2 在2'
)

# macOS 中文歌词字体候选（Fontconfig 按名查找，命中第一个可用项由 LilyPond 决定）
SERIF_FONT = 'Songti SC'
SANS_FONT = 'PingFang SC'

TITLE = '出现又离开 · 主歌（一）前八句（小样）'
SUBTITLE = 'A 大调 · 4/4 · ♩≈80 ｜ 和弦记号 + 柱式 voicing + 歌词（旋律待补）'

LY_TEMPLATE = r"""
\version "2.24.0"

\header {
  title = "%(title)s"
  subtitle = "%(subtitle)s"
  tagline = ##f
}

\paper {
  indent = 0
  ragged-last = ##f
  page-breaking = #ly:one-line-auto-height-breaking
  %% LilyPond ≥ 2.25.4 字体新语法（set-global-fonts 已移除）
  fonts.roman = "%(serif)s"
  fonts.sans = "%(sans)s"
}

chordNames = \chordmode {
  %(chords)s
}

staffVoice = {
  \key %(key)s \major
  \time %(time)s
  \tempo %(tempo)s
  %(voicings)s
  \bar "|."
}

verseWords = \lyricmode {
  %(lyrics)s
}

\score {
  <<
    \new ChordNames \chordNames
    \new Staff \staffVoice
    \new Lyrics \verseWords
  >>
  \layout { }
}
"""


def build_ly():
    return LY_TEMPLATE % {
        'title': TITLE,
        'subtitle': SUBTITLE,
        'serif': SERIF_FONT,
        'sans': SANS_FONT,
        'chords': ' '.join(CHORDS),
        'key': KEY,
        'time': TIME,
        'tempo': TEMPO,
        'voicings': ' '.join(VOICINGS),
        'lyrics': LYRICS,
    }


def main():
    lilypond = shutil.which('lilypond')
    if lilypond is None:
        sys.exit('未找到 lilypond，请先执行：brew install lilypond')

    out_dir = (
        Path(__file__).resolve().parent.parent
        / 'docs' / 'assets' / 'images' / 'songs'
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    ly_path = out_dir / 'chuxian-you-likai-ver1.ly'
    ly_path.write_text(build_ly(), encoding='utf-8')

    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [lilypond, '-dbackend=svg',
             '-o', str(Path(tmp) / 'out'), str(ly_path)],
            capture_output=True, text=True,
        )
        # LilyPond 的进度/字体告警走 stderr，原样透出便于诊断
        sys.stderr.write(result.stderr)
        if result.returncode != 0:
            sys.exit(f'lilypond 编译失败（退出码 {result.returncode}）')
        svg_src = Path(tmp) / 'out.svg'
        if not svg_src.exists():
            sys.exit('lilypond 未产出 SVG')
        svg_dst = out_dir / 'chuxian-you-likai-ver1.svg'
        shutil.move(str(svg_src), svg_dst)

    # SVG 后端只写通用族名（serif/sans），替换为 LilyPond 排版时实际使用的
    # 具体字体（保留通用族名兜底），避免浏览器回退到度量不一致的字体
    svg = svg_dst.read_text(encoding='utf-8')
    svg = svg.replace('font-family="serif"', f'font-family="{SERIF_FONT}, serif"')
    svg = svg.replace('font-family="sans"', f'font-family="{SANS_FONT}, sans-serif"')
    svg_dst.write_text(svg, encoding='utf-8')

    print(f'done: {svg_dst}')


if __name__ == '__main__':
    main()
