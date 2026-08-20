#!/usr/bin/env python3
"""Derive the production wordmark assets from the FROZEN masters (read-only).

Owner rulings 2026-08-19:
  * the swash tail is REMOVED — a tester read it as a snake, and the risk landed worse than predicted;
  * removing it alone left the s's lower arm as a blunt diagonal stub, so the TERMINAL IS REDRAWN:
    the arm is cut across its full width at the letter's own left sidebearing, instead of diving
    below the baseline to a point.

The frozen masters are NEVER written. Every derived asset is produced here, so provenance is one
command: `python3 scripts/finish-wordmark.py`.

Note the teal lived ONLY inside the tail group, so removing the tail also removes the last teal from
the wordmark — the earlier navy-S raster recolour is superseded by this re-render.
"""
import re, sys, pathlib

FROZEN = pathlib.Path("/Users/phillipapuzzio/Documents/professor_paws_brand/APPROVED_LOCKED_2026-08-18/svg_masters")
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wordmark-out")
OUT.mkdir(parents=True, exist_ok=True)

CUT_X = 215.6          # cut where the lower arm still carries full stroke width (~5.7 units)
OLD_TERMINAL = (211.94, 4.59)

def endp(c, n):
    return (n[0], n[1]) if c in "ML" else ((n[2], n[3]) if c == "Q" else None)

def finish_s(d: str) -> str:
    """Remove the tail lead-in from the s outline and cut a proper terminal, preserving curves."""
    cmds = [(m.group(1), [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(2))])
            for m in re.finditer(r"([MLQZ])([^MLQZ]*)", d)]
    i_cut = next(i for i, (c, n) in enumerate(cmds)
                 if endp(c, n) and abs(endp(c, n)[0] - OLD_TERMINAL[0]) < .01
                 and abs(endp(c, n)[1] - OLD_TERMINAL[1]) < .01)
    upper = [(c, n) for c, n in cmds[:i_cut] if endp(c, n) and endp(c, n)[0] >= CUT_X]
    lower = [(c, n) for c, n in cmds[i_cut:] if c != "Z" and endp(c, n) and endp(c, n)[0] >= CUT_X]
    yi, yo = endp(*upper[-1])[1], endp(*lower[0])[1]     # natural stroke width — never clamped
    parts  = [c + " " + " ".join(f"{v:.2f}" for v in n) for c, n in upper]
    parts += [f"L {CUT_X:.2f} {yi:.2f}", f"L {CUT_X:.2f} {yo:.2f}"]
    parts += [c + " " + " ".join(f"{v:.2f}" for v in n) for c, n in lower]
    return " ".join(parts) + " Z"

def derive(name: str) -> pathlib.Path:
    src = (FROZEN / f"{name}.svg").read_text()
    assert src.count('id="tail"') == 1, f"{name}: expected exactly one tail group"
    assert src.count("#14AAA3") == 1, f"{name}: expected exactly one teal fill"
    out = re.sub(r'<g id="tail">.*?</g>', "", src, flags=re.S)          # 1. drop the swash
    sm = next(m for m in re.finditer(r'<path[^>]*?\bd="([^"]*)"[^>]*?/>', out)
              if f"{OLD_TERMINAL[0]} {OLD_TERMINAL[1]}" in m.group(1))   # 2. find the s by its terminal
    out = out[:sm.start(1)] + finish_s(sm.group(1)) + out[sm.end(1):]    # 3. redraw the terminal
    assert "#14AAA3" not in out, f"{name}: teal survived"
    assert 'id="tail"' not in out, f"{name}: tail survived"
    p = OUT / f"{name}.svg"; p.write_text(out); return p

if __name__ == "__main__":
    for n in ["A_wordmark", "B_primary_horizontal_lockup", "D_wordmark_one_line"]:
        p = derive(n)
        print(f"  {n:32} -> {p}  ({p.stat().st_size} bytes)")
