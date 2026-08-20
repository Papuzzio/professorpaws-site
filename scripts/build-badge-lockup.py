#!/usr/bin/env python3
"""Add the BOARD'S BADGE DEVICE to the lockups — teal disc + white ring behind the mascot.

The owner's brand board shows the head sitting in a teal circle with a thick white ring
(clearest on the dark-background lockup). The board's own dog is an AI-generated retriever with
a collar and tag; it is NOT the approved mascot, and the owner's instruction with the board was
"keep the existing dog", restated as "put my dog in that spot instead". So this reproduces the
board's DEVICE and puts the FROZEN mascot inside it. The mascot bytes are never touched — the
badge is two vector shapes inserted BEHIND the existing <image>, which is left byte-identical.

The frozen wordmark letterforms are deliberately NOT redrawn: the board's 3D navy PROFESSOR and
brush-script Paws differ from the approved, frozen wordmark, and changing that needs its own
owner ruling (see APP ICON / wordmark freeze). Flagged in the report, not silently actioned.

    python3 scripts/build-badge-lockup.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEAL, WHITE, NAVY = '#14AAA3', '#FFFFFF', '#14213D'

# the mascot canvas carries transparent padding; the DOG occupies this fraction of it, measured
# from the alpha channel — the badge must be concentric with the dog, not with the canvas.
DOG_X0, DOG_X1, DOG_Y0, DOG_Y1 = 0.0850, 0.9141, 0.0977, 0.8818
# board proportions, measured off the dark-background lockup crop
# The mascot is WIDER than tall (850x804) and is not a circle, so sizing the disc off the larger
# side alone let the chest ruff spill across the ring. These are tuned so the whole frozen mascot
# sits INSIDE the disc, as the board shows — the artwork is contained, never clipped.
DISC_OVER_HEAD, RING_OVER_HEAD = 1.30, 1.41

def badge(svg_text, ring_fill):
    m = re.search(r'<image id="mascot" x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg_text)
    if not m:
        raise SystemExit('mascot <image> not found — refusing to guess')
    x, y, w, h = (float(g) for g in m.groups())
    dx0, dx1 = x + DOG_X0 * w, x + DOG_X1 * w
    dy0, dy1 = y + DOG_Y0 * h, y + DOG_Y1 * h
    cx, cy = (dx0 + dx1) / 2, (dy0 + dy1) / 2
    head = max(dx1 - dx0, dy1 - dy0)
    r_disc = head * DISC_OVER_HEAD / 2
    r_ring = head * RING_OVER_HEAD / 2
    shapes = (f'<g id="badge" data-role="badge">'
              f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r_ring:.2f}" fill="{ring_fill}"/>'
              f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r_disc:.2f}" fill="{TEAL}"/>'
              f'</g>')
    out = svg_text.replace('<image id="mascot"', shapes + '<image id="mascot"', 1)
    return out, cx, cy, r_ring

def widen(svg_text, cx, cy, r):
    """The ring can reach past the artboard; grow the viewBox rather than crop the badge."""
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg_text)
    vx, vy, vw, vh = (float(g) for g in m.groups())
    nx0, ny0 = min(vx, cx - r), min(vy, cy - r)
    nx1, ny1 = max(vx + vw, cx + r), max(vy + vh, cy + r)
    pad = 1.0
    nx0, ny0, nx1, ny1 = nx0 - pad, ny0 - pad, nx1 + pad, ny1 + pad
    return re.sub(r'viewBox="[^"]+"',
                  f'viewBox="{nx0:.2f} {ny0:.2f} {nx1-nx0:.2f} {ny1-ny0:.2f}"', svg_text, 1), (nx1-nx0)/(ny1-ny0)

# light lockups get a white ring; the dark-background ones get a white ring too (as on the board)
TARGETS = {
    'logo-horizontal-color.svg': WHITE,
    'logo-stacked-color.svg':    WHITE,
    'logo-light-bg.svg':         WHITE,
    'logo-dark-bg.svg':          WHITE,
    'logo-stacked-dark-bg.svg':  WHITE,
}

for name, ring in TARGETS.items():
    p = ROOT / 'assets' / 'logo' / name
    if not p.exists():
        print(f'  skip {name} (absent)'); continue
    s = p.read_text()
    # idempotent: strip any badge from a previous run so proportions can be re-tuned
    s = re.sub(r'<g id="badge".*?</g>', '', s, flags=re.S)
    before_img = s.count('<image')
    s, cx, cy, r = badge(s, ring)
    s, ratio = widen(s, cx, cy, r)
    assert s.count('<image') == before_img, 'mascot image count changed — refusing'
    p.write_text(s)
    print(f'  {name}: badge at ({cx:.1f},{cy:.1f}) r={r:.1f}  aspect {ratio:.3f}')
print('done — mascot artwork untouched in every file')
