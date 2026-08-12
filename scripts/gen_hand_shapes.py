import math

# ============================================================
# Piano keyboard drawing helpers
# ============================================================

WHITE_W = 40
WHITE_H = 150
BLACK_W = 26
BLACK_H = 90

# White key x positions (C D E F G A B on one octave)
WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
WHITE_X = [0, 40, 80, 120, 160, 200, 240]
KEYBOARD_W = 280  # 7 white keys
KEYBOARD_H = WHITE_H

# Black key positions (relative to white keys)
BLACK_KEYS = ['C#', 'D#', None, 'F#', 'G#', 'A#', None]
BLACK_X_OFFSET = 27  # black key starts 27px from white left edge

def draw_keyboard(svg, x0, y0):
    """Draw one octave of piano keys (C to B)"""
    # White keys
    for i, (label, wx) in enumerate(zip(WHITE_KEYS, WHITE_X)):
        rect_x = x0 + wx
        svg.append(f'<rect x="{rect_x}" y="{y0}" width="{WHITE_W}" height="{WHITE_H}" fill="white" stroke="#999" stroke-width="1"/>')
        # Label below key
        svg.append(f'<text x="{rect_x + WHITE_W/2}" y="{y0 + WHITE_H + 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#666">{label}</text>')

    # Black keys
    for i, (label, wx) in enumerate(zip(BLACK_KEYS, WHITE_X)):
        if label is None:
            continue
        bx = x0 + wx + BLACK_X_OFFSET
        svg.append(f'<rect x="{bx}" y="{y0}" width="{BLACK_W}" height="{BLACK_H}" fill="#333" stroke="#111" stroke-width="1" rx="2"/>')
        # Label on black key
        svg.append(f'<text x="{bx + BLACK_W/2}" y="{y0 + BLACK_H/2 + 4}" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#fff">{label}</text>')

def finger_dot(svg, x, y, color, label):
    """Draw a finger position dot"""
    r = 13
    svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" fill-opacity="0.85" stroke="{color}" stroke-width="1.5"/>')
    svg.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" font-weight="bold" fill="white">{label}</text>')

# ============================================================
# Generate hand_shape_1.svg — 手型一
# ============================================================

svg1 = []
w1, h1 = 700, 330
svg1.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w1} {h1}" width="{w1}" height="{h1}">')
svg1.append(f'<rect width="{w1}" height="{h1}" fill="#ffffff"/>')

# Title
svg1.append(f'<text x="{w1/2}" y="28" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#2c3e50">手型一：左手根音 + 右手三音和弦</text>')
svg1.append(f'<text x="{w1/2}" y="48" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#888">左手 3指(根音) ｜ 右手 1-2-4指 (以 Do-Mi-So 排列为例)</text>')

# Left hand keyboard (lower octave, C3)
lx0, ly0 = 30, 110
svg1.append(f'<text x="{lx0 + KEYBOARD_W/2}" y="{ly0 - 12}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#999">左手</text>')
draw_keyboard(svg1, lx0, ly0)

# Right hand keyboard (middle octave, C4)
rx0, ry0 = 390, 110
svg1.append(f'<text x="{rx0 + KEYBOARD_W/2}" y="{ry0 - 12}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#999">右手</text>')
draw_keyboard(svg1, rx0, ry0)

# Mark left hand: 3rd finger on C (white key 0, middle of key)
lx_c = lx0 + WHITE_X[0] + WHITE_W/2
ly_mid = ly0 + WHITE_H * 0.55
finger_dot(svg1, lx_c, ly_mid, "#e74c3c", "3")
# Label
svg1.append(f'<text x="{lx_c}" y="{ly0 - 30}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#e74c3c">根音 Do</text>')

# Mark right hand: Do-Mi-So = C-E-G (white keys 0,2,4)
# Left to right: 1(thumb) on C, 2(index) on E, 4(ring) on G
rx_c1 = rx0 + WHITE_X[0] + WHITE_W/2  # C - 1
rx_e2 = rx0 + WHITE_X[2] + WHITE_W/2  # E - 2
rx_g4 = rx0 + WHITE_X[4] + WHITE_W/2  # G - 4
ry_rmid = ry0 + WHITE_H * 0.55

finger_dot(svg1, rx_c1, ry_rmid, "#3498db", "1")
finger_dot(svg1, rx_e2, ry_rmid, "#2ecc71", "2")
finger_dot(svg1, rx_g4, ry_rmid, "#9b59b6", "4")

# Labels for right hand notes
svg1.append(f'<text x="{rx_c1}" y="{ry0 - 30}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#3498db">Do</text>')
svg1.append(f'<text x="{rx_e2}" y="{ry0 - 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#2ecc71">Mi</text>')
svg1.append(f'<text x="{rx_g4}" y="{ry0 - 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#9b59b6">So</text>')

# Legend
legend_x = 30
legend_y = h1 - 30
items = [("#e74c3c", "左手 3指"), ("#3498db", "右手 1指(拇指)"), ("#2ecc71", "右手 2指(食指)"), ("#9b59b6", "右手 4指(无名指)")]
for i, (color, text) in enumerate(items):
    ox = legend_x + i * 135
    svg1.append(f'<circle cx="{ox + 6}" cy="{legend_y - 4}" r="7" fill="{color}" fill-opacity="0.85"/>')
    svg1.append(f'<text x="{ox + 18}" y="{legend_y}" font-family="Arial,sans-serif" font-size="11" fill="#555">{text}</text>')

svg1.append('</svg>')
with open(r'd:\Githubprojects\chords-keys-cookbook\docs\practice\hand-shape-1.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg1))
print("hand-shape-1.svg done")

# ============================================================
# Generate hand_shape_2.svg — 手型二
# ============================================================

svg2 = []
w2, h2 = 700, 330
svg2.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w2} {h2}" width="{w2}" height="{h2}">')
svg2.append(f'<rect width="{w2}" height="{h2}" fill="#ffffff"/>')

# Title
svg2.append(f'<text x="{w2/2}" y="28" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#2c3e50">手型二：左手根音+五音 + 右手四音和弦</text>')
svg2.append(f'<text x="{w2/2}" y="48" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#888">左手 5指(根音) + 2指(五音) ｜ 右手 1-2-3-5指 Do-Mi-So-Do</text>')

# Left hand keyboard
lx0, ly0 = 30, 110
svg2.append(f'<text x="{lx0 + KEYBOARD_W/2}" y="{ly0 - 12}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#999">左手</text>')
draw_keyboard(svg2, lx0, ly0)

# Right hand keyboard
rx0, ry0 = 390, 110
svg2.append(f'<text x="{rx0 + KEYBOARD_W/2}" y="{ry0 - 12}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#999">右手</text>')
draw_keyboard(svg2, rx0, ry0)

# Mark left hand: 5 on C (low), 2 on G
lx_c5 = lx0 + WHITE_X[0] + WHITE_W/2        # C - 5th finger
lx_g2 = lx0 + WHITE_X[4] + WHITE_W/2        # G - 2nd finger
ly_lmid = ly0 + WHITE_H * 0.55

finger_dot(svg2, lx_c5, ly_lmid, "#e74c3c", "5")
finger_dot(svg2, lx_g2, ly_lmid, "#f39c12", "2")

svg2.append(f'<text x="{lx_c5}" y="{ly0 - 30}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#e74c3c">根音 Do</text>')
svg2.append(f'<text x="{lx_g2}" y="{ly0 - 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#f39c12">五音 So</text>')

# Draw a subtle bracket/brace between C and G in left hand
svg2.append(f'<line x1="{lx_c5}" y1="{ly0+100}" x2="{lx_g2}" y2="{ly0+100}" stroke="#ddd" stroke-width="1" stroke-dasharray="4,3"/>')

# Mark right hand: Do-Mi-So-Do = C-E-G-C (white keys 0,2,4,0)
# 1 on C, 2 on E, 3 on G, 5 on high C
rx_c1 = rx0 + WHITE_X[0] + WHITE_W/2     # C - 1st finger
rx_e2 = rx0 + WHITE_X[2] + WHITE_W/2     # E - 2nd finger
rx_g3 = rx0 + WHITE_X[4] + WHITE_W/2     # G - 3rd finger
rx_c5 = rx_c1 + WHITE_W * 7               # High C (next octave, same position)

ry_rmid = ry0 + WHITE_H * 0.55

finger_dot(svg2, rx_c1, ry_rmid, "#3498db", "1")
finger_dot(svg2, rx_e2, ry_rmid, "#2ecc71", "2")
finger_dot(svg2, rx_g3, ry_rmid, "#f39c12", "3")
finger_dot(svg2, rx_c5, ry_rmid, "#9b59b6", "5")

# Draw a subtle right-hand octave bracket
svg2.append(f'<line x1="{rx_c1}" y1="{ry0+100}" x2="{rx_c5}" y2="{ry0+100}" stroke="#ddd" stroke-width="1" stroke-dasharray="4,3"/>')
svg2.append(f'<text x="{(rx_c1+rx_c5)/2}" y="{ry0+116}" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#bbb">纯八度</text>')

# Labels for right hand
svg2.append(f'<text x="{rx_c1}" y="{ry0 - 30}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#3498db">Do</text>')
svg2.append(f'<text x="{rx_e2}" y="{ry0 - 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#2ecc71">Mi</text>')
svg2.append(f'<text x="{rx_g3}" y="{ry0 - 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#f39c12">So</text>')
svg2.append(f'<text x="{rx_c5}" y="{ry0 - 30}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#9b59b6">Do</text>')

# Also draw the high C key area
# Add extra white keys to complete the octave view
# We need to extend the right keyboard to show high C
# Actually high C is at the same white key position as the next octave's C
# Let's add a visual hint - draw one extra white key for the high C
high_c_x = rx0 + WHITE_W * 7
svg2.append(f'<rect x="{high_c_x}" y="{ry0}" width="{WHITE_W}" height="{WHITE_H}" fill="white" stroke="#999" stroke-width="1" opacity="0.4"/>')
svg2.append(f'<text x="{high_c_x + WHITE_W/2}" y="{ry0 + WHITE_H + 18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#bbb">C</text>')

# Legend
legend_x = 30
legend_y = h2 - 30
items2 = [("#e74c3c", "左手 5指(小指)"), ("#f39c12", "左手 2指 / 右手 3指"), ("#3498db", "右手 1指(拇指)"), ("#2ecc71", "右手 2指(食指)"), ("#9b59b6", "右手 5指(小指)")]
for i, (color, text) in enumerate(items2):
    ox = legend_x + i * 120
    svg2.append(f'<circle cx="{ox + 6}" cy="{legend_y - 4}" r="7" fill="{color}" fill-opacity="0.85"/>')
    svg2.append(f'<text x="{ox + 18}" y="{legend_y}" font-family="Arial,sans-serif" font-size="10" fill="#555">{text}</text>')

svg2.append('</svg>')
with open(r'd:\Githubprojects\chords-keys-cookbook\docs\practice\hand-shape-2.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg2))
print("hand-shape-2.svg done")

print("All SVGs generated!")
