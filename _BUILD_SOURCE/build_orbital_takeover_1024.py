"""Owns fixed-cell orbital cinematic exports and their registrations."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/orbital_takeover_1024'
D=R/'assets/game/shared/cinematics/orbital_takeover_1024'
D.mkdir(parents=True,exist_ok=True)
art={}
def reg(name,im,pivot,**extra):
    assert im.width%2==0 and im.height%2==0
    path=D/(name+'.webp');im.save(path,lossless=True)
    art[name]={'key':'ot24_'+name,'path':path.relative_to(R).as_posix(),'w':im.width,'h':im.height,'pivot':pivot,'sourceScale':1,**extra}
    art[name]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
sheet=Image.open(S/'satellite_pair.png').convert('RGBA')
# Shared square canvas/pivot, one proportional export scale for both plates.
cw=sheet.width//2;ch=sheet.height;k=min(512/cw,512/ch)
for i,name in enumerate(['satellite','infected']):
    im=sheet.crop((i*cw,0,(i+1)*cw,ch));im=im.resize((round(cw*k),round(ch*k)),Image.Resampling.NEAREST)
    cell=Image.new('RGBA',(512,512));cell.alpha_composite(im,((512-im.width)//2,(512-im.height)//2));reg(name,cell,[256,256])
reg('signal',Image.open(S/'signal.png').convert('RGBA'),[32,0])
source_files=sorted((S/'fluid').glob('*.png'))
# Reject generated disappearance/shrink frames 20-35; use the stable full-size motion run.
selected=list(range(20))
frames=[Image.open(source_files[i]).convert('RGBA')for i in selected]
assert len(frames)==20 and all(im.size==(128,128)for im in frames)
cols=8;atlas=Image.new('RGBA',(cols*128,((len(frames)+cols-1)//cols)*128))
for i,im in enumerate(frames):atlas.alpha_composite(im,(i%cols*128,i//cols*128))
reg('fluid',atlas,[64,64],frames=len(frames),columns=cols,cellWidth=128,cellHeight=128,sourceFrameIndices=selected)
# The renderer reads fixed cell dimensions; sheet geometry is separate metadata.
art['fluid']['sheetWidth']=atlas.width;art['fluid']['sheetHeight']=atlas.height
art['fluid']['w']=128;art['fluid']['h']=128
physical=sorted((S/'physical').glob('*.png'))
if physical:
    assert len(physical)==41
    bank=Image.new('RGBA',(8*256,6*256))
    for i,path in enumerate(physical):
        im=Image.open(path).convert('RGBA');assert im.size==(256,256)
        bank.alpha_composite(im,(i%8*256,i//8*256))
    reg('takeover',bank,[128,128],frames=41,columns=8,cellWidth=256,cellHeight=256)
    art['takeover']['sheetWidth']=bank.width;art['takeover']['sheetHeight']=bank.height
    art['takeover']['w']=256;art['takeover']['h']=256
art['earth']={'key':'ot24_earth','path':'assets/game/shared/cinematics/homecoming_1010/earth.png','w':1672,'h':942,'pivot':[836,471],'sourceScale':1}
(D/'manifest.json').write_text(json.dumps({'owner':'build_orbital_takeover_1024.py','art':art},indent=2),encoding='utf8')
(R/'assets/orbital_takeover_art_1024.js').write_text('"use strict";\nconst OT24_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
taxonomy=R/'assets/data/ART_TAXONOMY.json'
data=json.loads(taxonomy.read_text(encoding='utf8'))
data['ot24_']={'owner':'_BUILD_SOURCE/build_orbital_takeover_1024.py','manifest':'assets/game/shared/cinematics/orbital_takeover_1024/manifest.json','purpose':'Paired 512px stable satellite plates; faceless animated liquid symbiote and authored Earth downlink packets. No face-bearing remnant, no warped hull frames.'}
taxonomy.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
print('Exported',len(frames),'faceless fluid cells; paired 512px plates, signal and Earth registration.')
