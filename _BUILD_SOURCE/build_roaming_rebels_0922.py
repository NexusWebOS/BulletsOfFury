"""Package the generated Roaming Rebels concept and five south-facing ship masters."""
from pathlib import Path
import json,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/game/roaming_rebels_0922'
for sub in ['masters','ships','portraits']:(OUT/sub).mkdir(parents=True,exist_ok=True)
meta=ROOT/'_shots/portraits_rebels_0922/rebel_generations.json'
rows=json.loads(meta.read_text()) if meta.exists() else json.loads((OUT/'provenance.json').read_text())['assets']
for r in rows:
    p=OUT/'masters'/(r['name']+'.png')
    if 'generated' in r and Path(r['generated']).resolve()!=p.resolve():shutil.copy2(r['generated'],p)
    r['master']=p.relative_to(ROOT).as_posix();r.pop('generated',None)
    if r['name']=='roaming_rebels_roster':continue
    im=Image.open(p).convert('RGBA');alpha=im.getchannel('A');assert alpha.getextrema()==(0,255),(r['name'],'missing alpha')
    bbox=alpha.getbbox();assert bbox
    sprite=im.crop(bbox);sprite.thumbnail((320,384),Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',(352,416));canvas.alpha_composite(sprite,((352-sprite.width)//2,(416-sprite.height)//2))
    dest=OUT/'ships'/(r['name']+'.png');canvas.save(dest)
    r.update(sprite=dest.relative_to(ROOT).as_posix(),facing='south',view='overhead',alphaBounds=list(bbox))
poster=Image.open(OUT/'masters/roaming_rebels_roster.png').convert('RGBA')
# Measured authored portrait interiors; labels stay on the poster, not dialogue cells.
boxes=[(58,715,292,920),(354,715,589,920),(652,715,887,920),(950,715,1183,920),(1245,715,1479,920)]
names=['voss','nyx','rook','kaia','jace']
for name,box in zip(names,boxes):
    cell=poster.crop(box);cell.thumbnail((256,256),Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',(256,256),(6,9,16,255));canvas.alpha_composite(cell,((256-cell.width)//2,(256-cell.height)//2));canvas.save(OUT/'portraits'/(name+'.png'))
(OUT/'provenance.json').write_text(json.dumps({'generator':'built-in image_gen','date':'2026-09-22','assets':rows},indent=2)+'\n')
roster=[
 {'key':'voss','name':'Darius Voss','role':'Leader','sex':'male','ship':'voss_iron_vulture','shipName':'Iron Vulture','color':'#b92335'},
 {'key':'nyx','name':'Nyx Calder','role':'Infiltrator','sex':'female','ship':'nyx_ghostknife','shipName':'Ghostknife','color':'#a45bde'},
 {'key':'rook','name':'Rook Mercer','role':'Enforcer','sex':'male','ship':'rook_breachhammer','shipName':'Breachhammer','color':'#df7a29'},
 {'key':'kaia','name':'Kaia Vane','role':'Signal Hacker','sex':'female','ship':'kaia_signal_wraith','shipName':'Signal Wraith','color':'#29c3be'},
 {'key':'jace','name':'Jace Riven','role':'Interceptor','sex':'male','ship':'jace_razorjack','shipName':'Razorjack','color':'#d34743'}]
(OUT/'roster.json').write_text(json.dumps({'name':'The Roaming Rebels','alignment':'Independent hostile hacker/militia group; opposes every organization, including Fury HQ.','status':'Art roster; names are working concepts. Five members including the male leader. Existing Stage 6 three-ship encounter is unchanged.','pilots':roster},indent=2)+'\n')
print('Packaged five alpha ships, five portrait crops and the roster concept.')
