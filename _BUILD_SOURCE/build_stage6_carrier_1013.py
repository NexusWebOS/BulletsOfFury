from PIL import Image
from pathlib import Path
import json, hashlib, shutil, sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/stage6_carrier_1013/build'; OUT.mkdir(parents=True,exist_ok=True)
GEN=ROOT/'_ART_SOURCES/stage6_carrier_1013'
ASSETS=OUT/'assets'; ASSETS.mkdir(exist_ok=True)
hull=Image.open(GEN/'exec-3a8b6129-9415-4cc7-a171-16fb474e0039.png').convert('RGBA')
# Uniform scale, transparent even canvas, preserving original source proportions.
scale=992/hull.width
size=(round(hull.width*scale),round(hull.height*scale))
canvas=Image.new('RGBA',(1024,512)); canvas.alpha_composite(hull.resize(size,Image.Resampling.LANCZOS),(16,(512-size[1])//2))
canvas.save(ASSETS/'hull.png',optimize=True)
# The generated row has four identical-width cells; do not fit states individually.
tur=Image.open(GEN/'exec-3855b3e4-8ddd-434d-b980-1dd5d7747061.png').convert('RGBA')
cw=tur.width//4; ts=144/tur.height; sz=(round(cw*ts),144)
sheet=Image.new('RGBA',(512,160))
for i in range(4):
    frame=Image.new('RGBA',(128,160))
    frame.alpha_composite(tur.crop((i*cw,0,(i+1)*cw,tur.height)).resize(sz,Image.Resampling.LANCZOS),((128-sz[0])//2,8))
    sheet.alpha_composite(frame,(i*128,0))
sheet.save(ASSETS/'turrets.png',optimize=True)
manifest={'name':'Warhive Siege Carrier','frameRules':{'uniformScale':True,'transparentMargins':True},'hull':{'file':'hull.png','size':[1024,512],'pivot':[512,256],'source':str(GEN/'exec-3a8b6129-9415-4cc7-a171-16fb474e0039.png'),'scale':scale,'sockets':[[269, 366], [347, 366], [426, 366], [600, 366], [679, 366], [759, 366]]},'turrets':{'file':'turrets.png','frame':[128,160],'pivot':[64,60],'muzzle':[64,144],'frames':['idle','charging','firing','wreck'],'source':str(GEN/'exec-3855b3e4-8ddd-434d-b980-1dd5d7747061.png'),'scale':ts}}
for p in ASSETS.glob('*.png'):
    im=Image.open(p); manifest[p.stem+'Checks']={'size':list(im.size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'transparentCorners':all(im.getpixel(q)[3]==0 for q in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)])}
(ASSETS/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
if '--install' in sys.argv:
    dest=ROOT/'assets/game/levels/stage_06/boss/siege_carrier_1013'; dest.mkdir(parents=True,exist_ok=True)
    for p in ASSETS.iterdir(): shutil.copy2(p,dest/p.name)
print(json.dumps({'assets':str(ASSETS),'totalBytes':sum(p.stat().st_size for p in ASSETS.iterdir()),'installed':'--install' in sys.argv}))
