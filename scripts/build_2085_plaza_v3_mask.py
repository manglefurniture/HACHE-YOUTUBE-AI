#!/usr/bin/env python3
"""Build a ComfyUI inpaint mask for eye-level Plaza V3I/J from V2E.

White: remove rooftop terrace / generate ground-level public square and natural tree.
Black: protect approved futuristic skyline and overhead architecture.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib
import sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path.cwd()
dir=root/"assets"/"2085"/"references"
src=dir/"HACHE_2085_PLAZA_V2E_TREE_00001_.png"
dst=dir/"plaza_v3ij_ground_mask.png"
with Image.open(src) as pic:
    if pic.size != (1344,768): raise SystemExit("Unexpected image size")
if dst.exists(): raise SystemExit("Refusing overwrite: "+str(dst))
m=Image.new("L",(1344,768),0)
d=ImageDraw.Draw(m)
# Replace the roof deck, rails, rooftop walls and elevated foreground as one continuous paved square.
d.polygon([(0,305),(175,305),(350,345),(470,390),(580,410),(1000,420),(1344,410),(1344,768),(0,768)],fill=255)
# Blend old unnatural clipped dome into a broad ancient canopy while masking no top skyline towers.
d.ellipse((520,195,1110,575),fill=255)
# Anchor naturally branching trunk and root spread in pedestrian pavement.
d.polygon([(680,365),(780,365),(800,540),(855,720),(610,720),(655,555)],fill=255)
m=m.filter(ImageFilter.GaussianBlur(radius=12))
m.save(dst)
b=dst.read_bytes()
fraction=sum(v*n for v,n in enumerate(m.histogram()))/(255*1344*768)
print("MASK",dst,"bytes",len(b),"sha256",hashlib.sha256(b).hexdigest(),"coverage",round(fraction,4))
