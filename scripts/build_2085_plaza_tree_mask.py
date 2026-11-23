#!/usr/bin/env python3
"""Create a local SDXL inpaint mask to add a historic shade tree to Plaza V2C."""
import argparse
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--image", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    with Image.open(a.image) as im:
        if im.size != (1344, 768):
            raise SystemExit(f"Unexpected canvas: {im.size}")
    if a.output.exists():
        raise SystemExit(f"Refusing to overwrite: {a.output}")
    m = Image.new("L", (1344, 768), 0)
    d = ImageDraw.Draw(m)
    # Broad canopy above existing pedestrian space, next to chess area.
    d.ellipse((515, 240, 1015, 535), fill=255)
    # Connect canopy to a substantial trunk and roots integrated in paving.
    d.polygon([(690, 425), (800, 430), (827, 710),
               (664, 738), (650, 655)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(14))
    a.output.parent.mkdir(parents=True, exist_ok=True)
    m.save(a.output)
    b = a.output.read_bytes()
    coverage = sum(v*n for v, n in enumerate(m.histogram())) / (255*1344*768)
    print(f"mask={a.output} sha256={hashlib.sha256(b).hexdigest()} coverage={coverage:.3f}")

if __name__ == "__main__":
    main()
