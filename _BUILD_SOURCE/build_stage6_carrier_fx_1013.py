"""Normalize authored beam frames and reuse the actual Furnace muzzle drawings."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
if not (ROOT/'assets/game.js').exists(): ROOT=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
GEN=ROOT/'_ART_SOURCES/stage6_carrier_1013'
source=GEN/'exec-12a42842-3e73-4deb-b398-4c1a6bbb04a8.png'
if not source.exists(): source=Path(r'C:\Users\Mike\.codex\generated_images\01a13451-d0ca-74d1-b34a-2880fcad6a35\exec-12a42842-3e73-4deb-b398-4c1a6bbb04a8.png')
OUT=ROOT/'_shots/stage6_carrier_1013/fx_build';OUT.mkdir(parents=True,exist_ok=True)
beam=Image.open(source).convert('RGBA'); scale=512/beam.height
# Fixed measured axes translate authored frames onto one pivot, no per-frame fit.
axes=[177,483,789,1096]; cropw=300
sheet=Image.new('RGBA',(512,512))
for i,axis in enumerate(axes):
    frame=beam.crop((axis-cropw//2,0,axis+cropw//2,beam.height))
    size=(round(cropw*scale),512);frame=frame.resize(size,Image.Resampling.NEAREST)
    sheet.alpha_composite(frame,(i*128+(128-size[0])//2,0))
sheet.save(OUT/'red_beams.png',optimize=True)
muzzle=Image.new('RGBA',(512,128)); sources=[]
for i in range(4):
    p=ROOT/f'assets/game/levels/stage_02/boss/bosses/furnace/eye_laser_0924/muzzle_{i}.png';sources.append(str(p.relative_to(ROOT)))
    im=Image.open(p).convert('RGBA').crop((0,80,544,624)).resize((128,128),Image.Resampling.NEAREST)
    muzzle.alpha_composite(im,(i*128,0))
muzzle.save(OUT/'muzzles.png',optimize=True)
vents=[[493,221,37,9],[493,233,37,9],[493,245,37,9],[493,257,37,9],[493,269,37,9],[493,281,37,9]]
hull=Image.open(ROOT/'assets/game/levels/stage_06/boss/siege_carrier_1013/hull.png').convert('RGBA')
lights=Image.new('RGBA',(240,12))
for i,(x,y,w,h) in enumerate(vents):lights.alpha_composite(hull.crop((x,y,x+w,y+h)),(40*i+1,1))
lights.save(OUT/'front_lights.png',optimize=True)
meta={'tool':'built-in image_gen for red beam; existing authored Furnace bank for muzzle','beam':{'source':str(Path('_ART_SOURCES/stage6_carrier_1013')/source.name),'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'frame':[128,512],'pivot':[64,0],'sourceAxes':axes,'commonSourceCrop':[300,1240],'commonScale':scale,'solidBodyWidth':80,'fringeWidth':12,'frames':4,'fps':16,'render':'uniform scale from solidBodyWidth; clipped vertical tiles; no beam-axis stretching'},'muzzle':{'sources':sources,'crop':[0,80,544,624],'frame':[128,128],'pivot':[64,64],'commonScale':128/544,'frames':4,'fps':18},'lights':{'source':'hull.png existing cyan reactor lens/vent pixels','ventRects':[[493,221,37,9],[493,233,37,9],[493,245,37,9],[493,257,37,9],[493,269,37,9],[493,281,37,9]],'sequence':'Each vent follows matching gun 0..5, amber/red precharge flicker, hot red firing, cyan recovery; no free-running clock'},'checks':{}}
for p in OUT.glob('*.png'):
    im=Image.open(p);meta['checks'][p.stem]={'size':list(im.size),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/'fx_manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
if '--install' in sys.argv:
    dest=ROOT/'assets/game/levels/stage_06/boss/siege_carrier_1013'
    for name in ['red_beams.png','muzzles.png','front_lights.png','fx_manifest.json']:shutil.copy2(OUT/name,dest/name)
    GEN.mkdir(parents=True,exist_ok=True)
    if source.parent!=GEN:shutil.copy2(source,GEN/source.name)
print(json.dumps(meta['checks']))
