#!/usr/bin/env python3
"""Build the whole production logo family from the FROZEN masters (read-only).

Owner rulings 2026-08-19:
  * the swash TAIL IS REMOVED (a tester read it as a snake) and the s TERMINAL IS REDRAWN — removal alone
    left a blunt stub, which reads as a rendering fault;
  * the brand board sets PROFESSOR navy + Paws ORANGE, teal as a supporting accent;
  * KEEP THE EXISTING DOG — the canonical mascot is never redrawn or re-traced. Masters that embed it keep
    their <image> untouched; the mascot rides as-is.

Frozen masters are NEVER written. One command reproduces every derived asset.
"""
import re, sys, pathlib, collections

FROZEN = pathlib.Path("/Users/phillipapuzzio/Documents/professor_paws_brand/APPROVED_LOCKED_2026-08-18/svg_masters")
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/logo-system"); OUT.mkdir(parents=True, exist_ok=True)

NAVY, ORANGE, CREAM, BLACK, WHITE = "#14213D", "#FF8C42", "#FBF7EF", "#000000", "#FFFFFF"
CUT_X, OLD_TERM = 215.6, (211.94, 4.59)

def endp(c, n): return (n[0], n[1]) if c in "ML" else ((n[2], n[3]) if c == "Q" else None)

def finish_s(d):
    cmds = [(m.group(1), [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(2))])
            for m in re.finditer(r"([MLQZ])([^MLQZ]*)", d)]
    i = next(k for k, (c, n) in enumerate(cmds) if endp(c, n)
             and abs(endp(c, n)[0]-OLD_TERM[0]) < .01 and abs(endp(c, n)[1]-OLD_TERM[1]) < .01)
    up = [(c, n) for c, n in cmds[:i] if endp(c, n) and endp(c, n)[0] >= CUT_X]
    lo = [(c, n) for c, n in cmds[i:] if c != "Z" and endp(c, n) and endp(c, n)[0] >= CUT_X]
    yi, yo = endp(*up[-1])[1], endp(*lo[0])[1]          # natural stroke width, never clamped
    P  = [c+" "+" ".join(f"{v:.2f}" for v in n) for c, n in up]
    P += [f"L {CUT_X:.2f} {yi:.2f}", f"L {CUT_X:.2f} {yo:.2f}"]
    P += [c+" "+" ".join(f"{v:.2f}" for v in n) for c, n in lo]
    return " ".join(P) + " Z"

def recolour(svg, group, colour):
    """Set the fill of every path inside one semantic group."""
    m = re.search(rf'<g id="{group}">(.*?)</g>', svg, re.S)
    if not m: return svg
    body = re.sub(r'fill="[^"]*"', f'fill="{colour}"', m.group(1))
    return svg[:m.start(1)] + body + svg[m.end(1):]

def corrected(name, paws, professor=None):
    """Tail removed, terminal redrawn, colours applied. The mascot <image> is untouched."""
    s = (FROZEN / f"{name}.svg").read_text()
    imgs = s.count("<image")
    s = re.sub(r'<g id="tail">.*?</g>', "", s, flags=re.S)
    sm = next((m for m in re.finditer(r'<path[^>]*?\bd="([^"]*)"[^>]*?/>', s)
               if f"{OLD_TERM[0]} {OLD_TERM[1]}" in m.group(1)), None)
    if sm: s = s[:sm.start(1)] + finish_s(sm.group(1)) + s[sm.end(1):]
    s = recolour(s, "paws", paws)
    if professor: s = recolour(s, "professor", professor)
    assert 'id="tail"' not in s and "#14AAA3" not in s, f"{name}: tail/teal survived"
    assert s.count("<image") == imgs, f"{name}: mascot image count changed"
    return s

FULL   = [("A_wordmark","wordmark-color"), ("B_primary_horizontal_lockup","logo-horizontal-color"),
          ("C_stacked_lockup","logo-stacked-color"), ("D_wordmark_one_line","wordmark-one-line-color"),
          ("G_primary_lockup_light","logo-light-bg"), ("G_wordmark_light","wordmark-light-bg")]
DARK   = [("H_primary_lockup_dark","logo-dark-bg"), ("H_stacked_lockup_dark","logo-stacked-dark-bg"),
          ("H_wordmark_dark","wordmark-dark-bg")]
if __name__ == "__main__":
    made = []
    for src, out in FULL:                       # navy PROFESSOR + orange Paws
        (OUT/f"{out}.svg").write_text(corrected(src, ORANGE, NAVY)); made.append(out)
    for src, out in DARK:                       # cream PROFESSOR + orange Paws, for dark grounds
        (OUT/f"{out}.svg").write_text(corrected(src, ORANGE, CREAM)); made.append(out)
    base = corrected("A_wordmark", NAVY, NAVY)  # monochrome family, from the SAME corrected geometry
    for out, col in [("wordmark-monochrome-ink", NAVY), ("wordmark-monochrome-black", BLACK),
                     ("wordmark-reversed-white", WHITE)]:
        (OUT/f"{out}.svg").write_text(recolour(recolour(base, "paws", col), "professor", col)); made.append(out)
    for n in made: print(f"  {n}.svg  ({(OUT/(n+'.svg')).stat().st_size} bytes)")
