#!/usr/bin/env python3
"""Build a localized non-destructive inpainting mask for City V3 (2085).
White pixels are regenerated; black pixels preserve the approved city architecture.
No secrets, requests, server paths or private photos are used.
"""
import argparse
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--image", type=Path, required=True, help="Approved City V3 PNG")
    p.add_argument("--output", type=Path, required=True, help="Local grayscale ComfyUI mask PNG")
    args = p.parse_args()
    with Image.open(args.image) as im:
        width, height = im.size
    if (width, height) != (1344, 768):
        raise SystemExit(f"Unexpected reference dimensions: {width}x{height}")
    mask = Image.new("L", (width, height), 0)
    d = ImageDraw.Draw(mask)
    # Old plaza and pedestrian paving across the lower civic green area.
    d.polygon([(410, 635), (485, 520), (600, 478), (780, 460),
               (1070, 458), (1344, 488), (1344, 768), (345, 768)], fill=255)
    # Room for an ancient spreading tree and its branches within the square.
    d.ellipse((635, 310, 1210, 630), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=17))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite existing mask: {args.output}")
    mask.save(args.output)
    b = args.output.read_bytes()
    print(f"mask={args.output} dimensions={width}x{height} sha256={hashlib.sha256(b).hexdigest()}")
    print(f"masked_fraction={sum(mask.convert('L').getdata())/(255*width*height):.3f}")

if __name__ == "__main__":
    main()
