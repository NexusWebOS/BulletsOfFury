"""Export real PixelLab cloak poses with one shared pad, canvas and pivot."""
from pathlib import Path
import base64,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/stealth_1019';D=R/'assets/game/shared/combat/stealth_1019';O=R/'_shots/overnight_combat_1019'
D.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
JOBS={'loop':('65fb9a91-ca47-4ea9-ab35-11f4f48a140f',32),'in':('0569ade1-e52b-470d-82d2-bc6221903923',32),'out':('0569ade1-e52b-470d-82d2-bc6221903923',32)}
for f in (O/'raw').glob('cloak_*.b64'):(S/(f.stem+'.png')).write_bytes(base64.b64decode(f.read_text()))
art={'fps':18,'canvas':[160,192],'pivot':[80,96],'sourceCanvas':[128,160],'pad':[16,16],'sourceScale':1,'banks':{}}
audit={}
for bank,(job,count) in JOBS.items():
    poses=[];records=[];ink=[];sourceIndices=[];last=None
    for i in (range(count-1,-1,-1) if bank=='out' else range(count)):
        # The separately generated out clip hallucinated an aircraft outline.
        # Reject it. Dissipation reverses the accepted genuine forming poses;
        # it never draws an invented aircraft or synthesizes warp frames.
        name='loop' if bank=='loop' else 'in32'
        im=Image.open(S/f'cloak_{name}_{i+1:02}.png').convert('RGBA');assert im.size==(128,160),(bank,i,im.size)
        # Remove only identical generated hold frames. No warp, interpolation,
        # duplicated padding poses or per-pose fitting is introduced.
        digest=hashlib.sha256(im.tobytes()).hexdigest()
        if bank!='loop' and digest==last:continue
        last=digest;sourceIndices.append(i+1);outIndex=len(poses)
        pose=Image.new('RGBA',(160,192));pose.alpha_composite(im,(16,16));bbox=pose.getbbox()
        if bbox:assert bbox[0]>=16 and bbox[1]>=16 and bbox[2]<=144 and bbox[3]<=176
        f=D/f'{bank}_{outIndex:02}.png';pose.save(f,optimize=True);poses.append(pose);ink.append(int((np.array(pose)[:,:,3]>0).sum()))
        records.append({'key':f'sk19_{bank}_{outIndex:02}','path':f.relative_to(R).as_posix(),'w':160,'h':192,'pivot':[80,96],'sourceIndex':i+1})
    count=len(poses)
    sheet=Image.new('RGBA',(160*8,192*((count+7)//8)),(7,13,24,255));onions=sheet.copy()
    for i,im in enumerate(poses):
        at=(i%8*160,i//8*192);sheet.alpha_composite(im,at)
        for j in [max(0,i-1),min(count-1,i+1)]:
            g=poses[j].copy();g.putalpha(g.getchannel('A').point(lambda a:round(a*.22)));onions.alpha_composite(g,at)
        onions.alpha_composite(im,at)
    sheet.save(O/f'cloak-{bank}-registration.png');onions.save(O/f'cloak-{bank}-onions.png')
    poses[0].save(O/f'cloak-{bank}.webp',save_all=True,append_images=poses[1:],duration=56,loop=0,lossless=True)
    unique=len({hashlib.sha256(p.tobytes()).hexdigest() for p in poses});assert unique>=16 and count>=16,(bank,unique,count)
    art['banks'][bank]=records;audit[bank]={'job':job,'reverseSourceSequence':bank=='out','frames':count,'unique':unique,'sourceIndices':sourceIndices,'canvas':[160,192],'pivot':[80,96],'sharedTranslation':[16,16],'scale':1,'inkPixels':ink}
audit['rejected']=[{'job':'579ba49d-8f3e-4f07-9b1d-896a82c14c8f','reason':'Hallucinated a fighter outline in the supposedly aircraft-free effect. Never shipped.'},{'job':'06a6810e-5643-477e-a088-bd042b420354','reason':'16-pose clip held four blank frames; longer generation selected.'},{'job':'67eb748d-765b-4b5f-86e0-9931c3c22a3a','reason':'16-pose clip held six blank frames; insufficient distinct motion.'}]
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(S/'registration.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
(R/'assets/stealth_art_1019.js').write_text('"use strict";\n// Owned by build_stealth_1019.py.\nconst SK19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
tax=R/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8-sig'))
data['sk19_']={'role':'optical_stealth_refraction_form_loop_dissipate','sheet':None,'note':'PixelLab32 source poses each for form/loop/dissipate; only identical generated holds removed, exact delivered counts in manifest.160x192/pivot80,96, common16px pad and source scale1. No aircraft generated or uploaded. Runtime stealth_1019.js; owner build_stealth_1019.py.'}
data['sg19_']={'role':'rime_permanent_shoulder_cavity_pixel_charge','sheet':None,'note':'32 existing PixelLab frost-charge poses clipped to each measured authored Rime cavity.80x80/pivot40,40, fixed0.4 proportional source scale. Low idle light and stepped charge; no extra hull/rim. Owner build_shoulder_glow_1019.py; runtime shoulder_glow_1019.js.'}
tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(audit,indent=2))
