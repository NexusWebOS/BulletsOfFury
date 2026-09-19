"""Build all nine pilot avatars from current portrait faces and one approved box frame."""
from colorsys import rgb_to_hsv,hsv_to_rgb
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
FACES=ROOT/'assets/game/pilot_portraits'
OUT=ROOT/'assets/game/pilot_avatars'
FRAME=Image.open(OUT/'avatar_frame_template_0919.png').convert('RGBA')
ACCENTS={'axel':0.59,'cole':0.32,'decker':0.08,'falva':0.78,'freezer':0.52,
         'juggernaut':0.11,'lizzie':0.92,'maverick':0.25,'yuri':0.005}
assert FRAME.size==(256,256)
def recolor_frame(hue):
    pixels=[]
    for r,g,b,a in FRAME.get_flattened_data():
        h,s,v=rgb_to_hsv(r/255,g/255,b/255)
        if a and .48<h<.71 and s>.22 and b>r+10:
            nr,ng,nb=hsv_to_rgb(hue,s,v)
            r,g,b=round(nr*255),round(ng*255),round(nb*255)
        pixels.append((r,g,b,a))
    out=Image.new('RGBA',FRAME.size);out.putdata(pixels)
    return out
for pilot,hue in ACCENTS.items():
    face=Image.open(FACES/(pilot+'-idle.png')).convert('RGBA')
    assert face.size==(256,256)
    face=face.crop((17,17,239,239)).resize((202,212),Image.Resampling.NEAREST)
    panel=Image.new('RGBA',(256,256),(7,11,19,255))
    panel.alpha_composite(face,(27,27))
    panel.alpha_composite(recolor_frame(hue))
    panel.save(OUT/('pav_'+pilot+'.png'))
