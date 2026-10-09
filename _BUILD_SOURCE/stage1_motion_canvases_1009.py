"""Reference-only edit canvases: repeat approved native parts without redrawing."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/stage1_motion_1009/live_reference'
DEST=ROOT/'_ART_SOURCES/stage1_motion_1009/edit_canvas'
DEST.mkdir(exist_ok=True)
for name,count in [('overhaul_tank_1_hull',8),('overhaul_tank_1_turret',4),('s1truckmissile',8)]:
    im=Image.open(SRC/(name+'.png')).convert('RGBA')
    if name=='s1truckmissile':
        box=im.getbbox();im=im.crop((box[0]-8,box[1]-8,box[2]+8,box[3]+8))
    slot=400
    k=min(360/im.width,460/im.height)
    im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',(slot*count,512))
    for i in range(count):canvas.alpha_composite(im,(i*slot+(slot-im.width)//2,(512-im.height)//2))
    canvas.save(DEST/(name+'.png'))
print('Prepared three approved live source edit canvases.')
