import os, sys
import numpy as np
from PIL import Image, ImageDraw

def to_hsv(rgb):
    r,g,b=[rgb[...,i]/255.0 for i in range(3)]
    mx=np.max(rgb,axis=-1)/255.0; mn=np.min(rgb,axis=-1)/255.0
    d=mx-mn
    h=np.zeros_like(mx)
    m=(d>1e-6)&(mx==r); h[m]=((g[m]-b[m])/d[m])%6
    m=(d>1e-6)&(mx==g); h[m]=((b[m]-r[m])/d[m])+2
    m=(d>1e-6)&(mx==b); h[m]=((r[m]-g[m])/d[m])+4
    h=(h*60)%360
    s=np.where(mx>0,d/np.maximum(mx,1e-6),0)
    return h,s,mx
def to_rgb(h,s,v):
    c=v*s; x=c*(1-np.abs((h/60.0)%2-1)); m=v-c
    z=np.zeros_like(h)
    r,g,b=[z.copy() for _ in range(3)]
    for lo,hi,rr,gg,bb in ((0,60,c,x,z),(60,120,x,c,z),(120,180,z,c,x),
                           (180,240,z,x,c),(240,300,x,z,c),(300,360,c,z,x)):
        k=(h>=lo)&(h<hi); r[k]=rr[k]; g[k]=gg[k]; b[k]=bb[k]
    return np.clip(np.dstack([(r+m),(g+m),(b+m)])*255,0,255)

def goldify(a, s_gamma=0.20, v_gamma=0.66, hue_pull=1.0, target_hue=44.0,
            white_sat=0.16, ink_floor=0.10):
    """Mike, 0909: 'palette swap lizzie's brown to be more Golden, the white remains.'
       Pack Lizzie measures sat 0.53 / val 0.45 against the in-game gold's 0.86 / 0.57 — same
       hue family (both ~45 deg), just desaturated and dark. The constants are SOLVED, not picked:
       s_gamma 0.20 / v_gamma 0.66 lands the recoloured ink on sat 0.88 val 0.57 hue 44, against
       her existing gold hull's measured 0.86 / 0.57 / 45. So this lifts saturation and value and nudges the
       hue toward gold, and touches NOTHING that is already near-white or near-black: the white
       livery (sat<=0.16) and the outline (val<0.10) are left exactly as drawn."""
    out=a.copy().astype(float)
    rgb=out[...,:3]
    h,s,v=to_hsv(rgb)
    opaque=out[...,3]>40
    warm=(h<95)|(h>330)                 # the brown/gold family only; blue+purple accents untouched
    m = opaque & warm & (s>white_sat) & (v>=ink_floor)
    h2=h.copy(); s2=s.copy(); v2=v.copy()
    h2[m]=h[m]+(target_hue-np.where(h[m]>330,h[m]-360,h[m]))*hue_pull
    s2[m]=np.clip(s[m]**s_gamma,0,1)
    v2[m]=np.clip(v[m]**v_gamma,0,1)
    new=to_rgb(h2%360,s2,v2)
    out[...,:3]=np.where(m[...,None], new, rgb)
    return out.astype(np.uint8), int(m.sum()), int(opaque.sum())

if __name__=='__main__':
    tot=0; ink=0
    for i in range(8):
        p='cutframes/lizzie_%d.png'%i
        a=np.array(Image.open(p).convert('RGBA'))
        b,n,o=goldify(a); tot+=n; ink+=o
        Image.fromarray(b,'RGBA').save('cutframes/lizzie_gold_%d.png'%i)
    print('recoloured %d of %d ink px across 8 frames (%.0f%%)'%(tot,ink,100*tot/ink))
    # before / after / in-game reference
    Z=2
    befores=[Image.open('cutframes/lizzie_%d.png'%i).convert('RGBA') for i in range(8)]
    afters =[Image.open('cutframes/lizzie_gold_%d.png'%i).convert('RGBA') for i in range(8)]
    CW=260; CH=250
    sh=Image.new('RGBA',(CW*8+20,60+CH*2),(22,23,28,255)); dr=ImageDraw.Draw(sh)
    dr.text((14,14),'LIZZIE — pack sheet #78 as generated (top) vs goldified (bottom). White and outline untouched.',fill=(255,210,140,255))
    for r,row in enumerate((befores,afters)):
        for i,im in enumerate(row):
            f=min((CW-16)/im.width,(CH-30)/im.height)
            t=im.resize((max(1,int(im.width*f)),max(1,int(im.height*f))),Image.NEAREST)
            x=10+i*CW; y=44+r*CH
            sh.alpha_composite(t,(x+(CW-t.width)//2,y))
            dr.text((x+8,y+CH-22),'%s br%d'%('was' if r==0 else 'GOLD',i),
                    fill=(180,180,190,255) if r==0 else (255,215,120,255))
    sh.save('lizzie_gold.png'); print('saved lizzie_gold.png',sh.size)
