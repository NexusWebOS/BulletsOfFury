#!/usr/bin/env python3
"""
inf_unbox_0917b.py - take the empty level-tag box off four element badges.

Mike, 0917b: "they shouldnt have a box at all in the icon". Four of the nine inf_* badges came back
from generation with a dark tag box sitting over the hex's bottom apex (dark, kinetic, toxic, water);
fire, ice, chrome, lightning and prism are clean, and are the reference for what the bottom should be.

The hex is vertically symmetric (65 rows, apex at 0 and 64), so the covered area is rebuilt from the
badge's OWN top apex: for each pixel under the box, the mirrored row gives the silhouette and the
frame/interior split (the first dark pixel inside the lit rim run is the frame's inner edge).
  - frame pixels take the mirror, re-toned by the per-channel gain between the visible bottom rim
    and its mirror (the top rim is lit, the bottom is not - a straight copy would glow);
  - interior pixels continue the interior just above the box and fade into the badge's darkest
    interior over five rows, so the glyph above is never copied down.
Originals: _BUILD_SOURCE/_backups/infusion_0917_boxed/.
"""
import os, sys
from PIL import Image
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
DIR=os.path.join(ROOT,'assets','game','ui','infusion_0917')
SRC=os.path.join(ROOT,'_BUILD_SOURCE','_backups','infusion_0917_boxed')
BOX={'dark':(17,49,37),'kinetic':(16,50,37),'toxic':(16,50,37),'water':(15,49,37)}   # x0, y0, x1 (exclusive); to the bottom

def lit(p): return p[3]>40 and max(p[:3])>=60

def spans(px,W,y):
    xs=[x for x in range(W) if px[x,y][3]>40]
    if not xs: return None
    L,R=xs[0],xs[-1]
    # inner edge: skip the outline, walk the lit rim, stop at the first dark pixel
    def walk(start,step):
        x=start
        while 0<=x<W and not lit(px[x,y]) and px[x,y][3]>40 and abs(x-start)<3: x+=step
        while 0<=x<W and lit(px[x,y]): x+=step
        return x
    return L,R,walk(L,1),walk(R,-1)

def fix(e):
    im=Image.open(os.path.join(SRC,'inf_'+e+'.png')).convert('RGBA'); W,H=im.size
    src=im.load(); out=im.copy(); px=out.load()
    x0,y0,x1=BOX[e]
    # tone gain: visible bottom rim (outside the box) against its mirror
    acc=[0,0,0];ref=[0,0,0]
    for y in range(y0,H):
        for x in list(range(0,x0))+list(range(x1,W)):
            p=src[x,y];q=src[x,H-1-y]
            if lit(p) and lit(q):
                for c in range(3): acc[c]+=p[c]; ref[c]+=q[c]
    gain=[acc[c]/max(1,ref[c]) for c in range(3)]
    # deepest interior colour: the darkest opaque pixel on the row above the box, inside the rim
    row=[src[x,y0-2] for x in range(x0,x1) if src[x,y0-2][3]>200]
    deep=min(row,key=lambda p:sum(p[:3])) if row else (8,8,12,255)
    for y in range(y0,H):
        m=H-1-y; sp=spans(src,W,m)
        # interior samples beside the box on THIS row
        lc=src[x0-1,y]; rc=src[x1,y]
        for x in range(x0,x1):
            q=src[x,m]
            if not sp or x<sp[0] or x>sp[1]: px[x,y]=(0,0,0,0); continue
            if sp[2]<=x<=sp[3] and sp[2]<sp[3]:
                # the interior just above the box, fading into the badge's own deepest interior
                a=src[x,y0-2]; k=min(1.0,(y-y0+1)/5.0)
                px[x,y]=tuple(int(a[c]*(1-k)+deep[c]*k) for c in range(3))+(255,)
            elif lit(q):
                px[x,y]=tuple(min(255,int(q[c]*gain[c])) for c in range(3))+(q[3],)
            else:
                px[x,y]=q
    out.save(os.path.join(DIR,'inf_'+e+'.png'))
    print(e,'gain',[round(g,2) for g in gain])

for e in BOX: fix(e)
