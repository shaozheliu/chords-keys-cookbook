
\version "2.24.0"

\header {
  title = "出现又离开 · 主歌（一）前八句（小样）"
  subtitle = "A 大调 · 4/4 · ♩≈80 ｜ 和弦记号 + 柱式 voicing + 歌词（旋律待补）"
  tagline = ##f
}

\paper {
  indent = 0
  ragged-last = ##f
  page-breaking = #ly:one-line-auto-height-breaking
  % LilyPond ≥ 2.25.4 字体新语法（set-global-fonts 已移除）
  fonts.roman = "Songti SC"
  fonts.sans = "PingFang SC"
}

chordNames = \chordmode {
  a1 e/gis fis:m a:sus2/e d a d e
}

staffVoice = {
  \key a \major
  \time 4/4
  \tempo 4 = 80
  <a cis' e'>1 <gis b e'>1 <fis a cis'>1 <e a b>1 <d fis a>1 <a cis' e'>1 <d fis a>1 <e gis b>1
  \bar "|."
}

verseWords = \lyricmode {
  我2 和4 你4 本2 应4 该4 各2 自4 好4 各2 自4 坏4 各2 自4 生4 活4 的4 自2 在2 毫2 无4 关4 联4 的4 存2 在2
}

\score {
  <<
    \new ChordNames \chordNames
    \new Staff \staffVoice
    \new Lyrics \verseWords
  >>
  \layout { }
}
