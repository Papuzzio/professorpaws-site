#!/usr/bin/env python3
"""App-icon family + mascot-only mark, from the FROZEN canonical icon (read-only).

Owner: KEEP THE EXISTING DOG. The mascot is never redrawn or re-traced — only the flat background
field is re-laid. The frozen icon is a vector-style render on a flat teal field, so a soft matte on
the background colour swaps the ground without touching a pixel of the dog's own artwork.
"""
import sys, pathlib
import numpy as np
from PIL import Image

FROZEN = pathlib.Path("/Users/phillipapuzzio/Documents/professor_paws_icon/professor_paws_icon_FINAL.png")
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/app-icons"); OUT.mkdir(parents=True, exist_ok=True)
TEAL   = np.array([0x14, 0xAA, 0xA3], float)     # the frozen ground
ORANGE = np.array([0xFF, 0x8C, 0x42], float)     # brand-board app-icon ground
SIZES  = [1024, 180, 120, 60, 40, 32, 16]

def matte(img):
    """Soft 0..1 mask of the flat teal ground. 1 = ground, 0 = dog."""
    a = np.asarray(img.convert("RGB"), float)
    d = np.linalg.norm(a - TEAL, axis=-1)
    return np.clip(1.0 - (d - 8.0) / 26.0, 0.0, 1.0)   # narrow band: edges are ~1-2px on this render

def main():
    src = Image.open(FROZEN)
    m = matte(src)[..., None]
    rgb = np.asarray(src.convert("RGB"), float)
    orange = rgb * (1 - m) + ORANGE * m                # ground re-laid, dog untouched where m==0
    Image.fromarray(orange.clip(0, 255).astype("uint8")).save(OUT / "app-icon-1024.png")
    base = Image.open(OUT / "app-icon-1024.png")
    for s in SIZES[1:]:
        base.resize((s, s), Image.LANCZOS).save(OUT / f"app-icon-{s}.png")
    # mascot only, transparent ground — for use on cream/dark surfaces
    rgba = np.dstack([rgb, (1 - m[..., 0]) * 255])
    Image.fromarray(rgba.clip(0, 255).astype("uint8"), "RGBA").save(OUT / "mascot-only.png")
    for s in SIZES: print(f"  app-icon-{s}.png")
    print("  mascot-only.png (transparent)")
    print(f"  dog pixels untouched: {int((m[...,0] < 0.02).sum()):,} of {m.size:,}")

if __name__ == "__main__":
    main()
