import math
from pathlib import Path

# SVG canvas
w, h = 500, 500
cx, cy = w/2, h/2
r = 170
font_size = 30

# 12 keys clockwise from top (C at 12 o'clock)
keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F\u266f', 'D\u266d', 'A\u266d', 'E\u266d', 'B\u266d', 'F']

svg_parts = []
svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')
svg_parts.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')

# Circle outline
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#333" stroke-width="2"/>')

# Center dot
svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#333"/>')

# Title
svg_parts.append(f'<text x="{cx}" y="{cy-8}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#888">\u4e94\u5ea6\u5708</text>')
svg_parts.append(f'<text x="{cx}" y="{cy+12}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#aaa">Circle of Fifths</text>')

# Place keys
for i, key in enumerate(keys):
    angle_deg = -90 + i * 30
    angle = math.radians(angle_deg)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    svg_parts.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="central" font-family="Arial,sans-serif" font-size="{font_size}" font-weight="bold" fill="#2c3e50">{key}</text>')

# Clockwise arrow (+P5): curves from C toward G (top-right)
arrow_r = r + 55
start_angle = math.radians(-80)
end_angle = math.radians(-50)
ax1 = cx + arrow_r * math.cos(start_angle)
ay1 = cy + arrow_r * math.sin(start_angle)
ax2 = cx + arrow_r * math.cos(end_angle)
ay2 = cy + arrow_r * math.sin(end_angle)

svg_parts.append(f'<path d="M {ax1:.1f} {ay1:.1f} A {arrow_r} {arrow_r} 0 0 0 {ax2:.1f} {ay2:.1f}" fill="none" stroke="#e74c3c" stroke-width="2.5" marker-end="url(#arrowRed)"/>')

# Counter-clockwise arrow (+P4): curves from C toward F (top-left)
start_angle2 = math.radians(-100)
end_angle2 = math.radians(-130)
bx1 = cx + arrow_r * math.cos(start_angle2)
by1 = cy + arrow_r * math.sin(start_angle2)
bx2 = cx + arrow_r * math.cos(end_angle2)
by2 = cy + arrow_r * math.sin(end_angle2)

svg_parts.append(f'<path d="M {bx1:.1f} {by1:.1f} A {arrow_r} {arrow_r} 0 0 1 {bx2:.1f} {by2:.1f}" fill="none" stroke="#3498db" stroke-width="2.5" marker-end="url(#arrowBlue)"/>')

# Arrow markers
svg_parts.append('<defs>')
svg_parts.append('<marker id="arrowRed" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#e74c3c"/></marker>')
svg_parts.append('<marker id="arrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#3498db"/></marker>')
svg_parts.append('</defs>')

# Arrow labels
lx = cx + (arrow_r + 25) * math.cos(math.radians(-65))
ly = cy + (arrow_r + 25) * math.sin(math.radians(-65))
svg_parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" font-family="Arial,sans-serif" font-size="12" fill="#e74c3c">+P5</text>')

lx2 = cx + (arrow_r + 25) * math.cos(math.radians(-115))
ly2 = cy + (arrow_r + 25) * math.sin(math.radians(-115))
svg_parts.append(f'<text x="{lx2:.1f}" y="{ly2:.1f}" text-anchor="middle" dominant-baseline="central" font-family="Arial,sans-serif" font-size="12" fill="#3498db">+P4</text>')

svg_parts.append('</svg>')

svg_content = '\n'.join(svg_parts)

output_path = Path(__file__).resolve().parent.parent / 'docs' / 'assets' / 'images' / 'common' / 'circle-of-fifths.svg'
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(svg_content, encoding='utf-8')

print(f'Generated: {output_path}')
