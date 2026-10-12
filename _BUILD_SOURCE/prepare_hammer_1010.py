"""Export approved whole-body seeds and a fixed-grid reference; no repainting."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_ART_SOURCES/hammer_1010/reference'
OUT.mkdir(parents=True,exist_ok=True)
im=Image.open(ROOT/'assets/game/levels/stage_05/boss/stage5_archmage_0916/combat_0926/hammer_strike_v2.png').convert('RGBA')
for name,r,pivot in [('idle',(0,0,392,362),(194,173)),('raised',(1080,0,1448,362),(1277,201))]:
    cell=Image.new('RGBA',(512,512))
    cell.alpha_composite(im.crop(r),(256-(pivot[0]-r[0]),224-(pivot[1]-r[1])))
    cell.save(OUT/(name+'.png'))
grid=Image.new('RGBA',(2048,2048))
grid.alpha_composite(Image.open(OUT/'idle.png'),(0,0))
grid.save(OUT/'shield_edit_canvas.png')
print('Approved seeds on even 512px cells, reactor pivot 256,224.')
