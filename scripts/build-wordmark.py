"""Professor P[paw]ws — deterministic one-line website wordmark.

Letters are converted to OUTLINES from Nunito (OFL) so no webfont is shipped
and rendering is identical everywhere. The paw is constructed geometrically
(5 rounded shapes), sized to occupy the advance slot of the lowercase 'a' it
replaces, so the word still reads "Paws".
"""
import re, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

# Nunito, SIL Open Font License 1.1 — google/fonts @ 8c6a9bb9732545b9ed53f29ec5e1ab0ff53c4e6f
# sha256 bb55a5ca5c2042335b3991af27c4d0705d0ef41cac6164ac737fd8f2a1e85207
# The font is used ONLY to generate outlines here; no webfont is shipped for the logo.
FONT = "/Users/phillipapuzzio/dev/brand-experiments/toolchain/fonts/nunito/Nunito[wght].ttf"
WEIGHT = 800
ORANGE = "#F59A23"
GOLD_FILL = "#FFC233"      # kidTheme `yellow` — existing app token
GOLD_EDGE = "#B8791F"      # theme `amber`   — existing app token

BEFORE = "Professor P"     # orange
AFTER  = "ws"              # orange
SLOT   = "a"               # replaced by the paw

font = instancer.instantiateVariableFont(TTFont(FONT), {"wght": WEIGHT})
gs = font.getGlyphSet()
cmap = font.getBestCmap()
hmtx = font["hmtx"]
upm = font["head"].unitsPerEm


def gname(ch):
    return cmap[ord(ch)]


def adv(ch):
    return hmtx[gname(ch)][0]


def kern_pairs():
    pairs = {}
    if "kern" in font:
        try:
            for st in font["kern"].kernTables:
                pairs.update(st.kernTable)
        except Exception:
            pass
    return pairs


KERN = kern_pairs()


def layout(text):
    """(glyph, d, x_offset) with kerning; returns list + total advance."""
    out, x = [], 0.0
    prev = None
    for ch in text:
        g = gname(ch)
        if prev is not None:
            x += KERN.get((prev, g), 0)
        pen = SVGPathPen(gs)
        gs[g].draw(pen)
        out.append((g, pen.getCommands(), x))
        x += adv(ch)
        prev = g
    return out, x


# ── lay out: BEFORE + [a-slot] + AFTER, kerned across the seam as if 'a' were present
full = BEFORE + SLOT + AFTER
placed, total_adv = layout(full)
slot_index = len(BEFORE)
slot_x = placed[slot_index][2]
slot_adv = adv(SLOT)

# vertical extents of the real 'a' -> the paw matches its optical footprint
bp = BoundsPen(gs)
gs[gname(SLOT)].draw(bp)
a_xmin, a_ymin, a_xmax, a_ymax = bp.bounds
a_w = a_xmax - a_xmin
a_h = a_ymax - a_ymin

letter_paths = []
for i, (g, d, x) in enumerate(placed):
    if i == slot_index:
        continue                      # the 'a' itself is never drawn
    letter_paths.append(f'<path d="{d}" transform="translate({x:.2f} 0)"/>')

# ── the paw, built in the 'a' slot ────────────────────────────────────────────
# Sized to the 'a' ink box, nudged slightly wider/taller so it holds the same
# optical weight as a letter rather than reading as a small icon.
PAW_W = a_w * 1.26
PAW_H = a_h * 1.22
cx = slot_x + a_xmin + a_w / 2.0
cy = a_ymin + a_h / 2.0

def ellipse(ex, ey, rx, ry, rot=0.0):
    return (f'<ellipse cx="{ex:.2f}" cy="{ey:.2f}" rx="{rx:.2f}" ry="{ry:.2f}"'
            + (f' transform="rotate({rot:.1f} {ex:.2f} {ey:.2f})"' if rot else '') + '/>')

# MAIN PAD — a deliberately WIDE ellipse (rx well above ry) so it reads as a paw
# pad, not an egg. Sits in the lower half of the slot.
pad = ellipse(cx, cy - PAW_H * 0.185, PAW_W * 0.425, PAW_H * 0.270)

# FOUR TOES — inner pair upright and high, outer pair dropped and splayed.
toe_rx = PAW_W * 0.147
toe_ry = PAW_H * 0.163
toes = [
    ellipse(cx - PAW_W * 0.372, cy + PAW_H * 0.140, toe_rx, toe_ry, -26),
    ellipse(cx - PAW_W * 0.140, cy + PAW_H * 0.285, toe_rx, toe_ry, -9),
    ellipse(cx + PAW_W * 0.140, cy + PAW_H * 0.285, toe_rx, toe_ry, 9),
    ellipse(cx + PAW_W * 0.372, cy + PAW_H * 0.140, toe_rx, toe_ry, 26),
]

# ── emit ──────────────────────────────────────────────────────────────────────
PAD = upm * 0.06
xmin = -PAD
# right edge: ink extent of the last glyph, not its advance (avoids a phantom gap)
bp2 = BoundsPen(gs)
gs[placed[-1][0]].draw(bp2)
right_ink = placed[-1][2] + bp2.bounds[2]
vb_w = right_ink + 2 * PAD

# vertical: cap height down to descender of 'P'/'f' etc — measure the whole set
ys = []
for g, d, x in placed:
    b = BoundsPen(gs); gs[g].draw(b)
    if b.bounds:
        ys += [b.bounds[1], b.bounds[3]]
ys += [cy - PAW_H / 2, cy + PAW_H / 2]
ymin, ymax = min(ys), max(ys)
vb_h = (ymax - ymin) + 2 * PAD

# SVG y-down: flip via a scale(1,-1) wrapper
STROKE = upm * 0.020
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{xmin:.2f} {-(ymax + PAD):.2f} {vb_w:.2f} {vb_h:.2f}" role="img" aria-label="Professor Paws">
  <g transform="scale(1 -1)">
    <g fill="{ORANGE}">
      {chr(10).join('      ' + p for p in letter_paths).strip()}
    </g>
    <g fill="{GOLD_FILL}" stroke="{GOLD_EDGE}" stroke-width="{STROKE:.2f}" stroke-linejoin="round">
      {pad}
      {chr(10).join('      ' + t for t in toes).strip()}
    </g>
  </g>
</svg>
'''
out = str(pathlib.Path(__file__).resolve().parent.parent / "assets/brand/wordmark.svg")
open(out, "w").write(svg)
print("wrote", out)
print(f"viewBox {xmin:.2f} {-(ymax+PAD):.2f} {vb_w:.2f} {vb_h:.2f}   aspect {vb_w/vb_h:.3f}")
print(f"'a' slot: x={slot_x:.1f} advance={slot_adv} ink_w={a_w:.1f} ink_h={a_h:.1f}")
print(f"paw: w={PAW_W:.1f} ({PAW_W/a_w*100:.0f}% of 'a' ink width)  h={PAW_H:.1f}")
