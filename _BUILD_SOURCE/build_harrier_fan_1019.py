"""Export PixelLab's exact native-rotor animation, keeping hub/rim untouched."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/harrier_fan_1019';D=R/'assets/game/levels/stage_08/boss/harrier_fan_1019';O=R/'_shots/overnight_combat_1019'
D.mkdir(parents=True,exist_ok=True)
sheet=Image.open(S/'workbench-full.png').convert('RGBA');assert sheet.size==(1280,384)
ref=np.array(Image.open(S/'candidate_00.png').convert('RGBA'));yy,xx=np.indices((192,160));d=(xx-80)**2+(yy-96)**2
outside=d>25**2;hub=d<4**2
yy,xx=np.indices((64,64));radius=(xx-32)**2+(yy-32)**2;mask=(radius<=23**2)&(radius>6**2)
poses=[];records=[];audits=[];pal=set(map(tuple,ref.reshape(-1,4)))
dark=min((tuple(int(n) for n in v) for v in ref[(d<=23**2)&(ref[:,:,3]==255)]),key=lambda v:sum(v[:3]))
for i in range(16):
    frame=sheet.crop(((i%8)*160,(i//8)*192,(i%8+1)*160,(i//8+1)*192));a=np.array(frame)
    assert np.array_equal(a[outside],ref[outside]),('housing moved',i)
    assert np.array_equal(a[hub],ref[hub]),('axle moved',i)
    assert set(map(tuple,a.reshape(-1,4)))<=pal,('palette drift',i)
    cut=np.array(frame.crop((48,64,112,128)));blank=(cut[:,:,3]==0)&mask
    cut[blank]=dark;cut[~mask]=0
    pose=Image.fromarray(cut);path=D/f'rotor_{i:02}.png';pose.save(path,optimize=True);poses.append(pose)
    records.append(dict(key=f'hf19_rotor_{i:02}',path=path.relative_to(R).as_posix(),w=64,h=64,pivot=[32,32],degrees=i*22.5))
    audits.append(dict(frame=i,fixedHousing=True,fixedHub=True,paletteExact=True,filledCavityPixels=int(blank.sum()),sha256=hashlib.sha256(cut.tobytes()).hexdigest()))
assert len({a['sha256'] for a in audits})==16
art=dict(canvas=[64,64],pivot=[32,32],fps=20,referenceScale=.38,frames=records,mounts={'fanL':{'sourceSize':[350,390],'sourceAxle':[153,174]},'fanR':{'sourceSize':[351,392],'sourceAxle':[198,178]}})
contact=Image.new('RGBA',(64*8,64*2),(7,12,22,255));onion=contact.copy()
for i,pose in enumerate(poses):
    at=(i%8*64,i//8*64);contact.alpha_composite(pose,at)
    for j in [(i-1)%16,(i+1)%16]:
        ghost=poses[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda a:round(a*.2)));onion.alpha_composite(ghost,at)
    onion.alpha_composite(pose,at);ImageDraw.Draw(contact).text((at[0]+2,at[1]+2),str(i),fill='#ffffff')
contact.resize((1024,256),Image.Resampling.NEAREST).save(O/'harrier-fan-accepted.png');onion.resize((1024,256),Image.Resampling.NEAREST).save(O/'harrier-fan-onions.png')
poses[0].save(O/'harrier-fan-accepted.webp',save_all=True,append_images=poses[1:],duration=50,loop=0,lossless=True)
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(S/'accepted-registration.json').write_text(json.dumps(dict(source='Current native fmc_harrier fanL',workbench='7995aab4-ca2d-4951-8b8a-674edf4af50d',method='PixelLab exact workbench copies the authored rotor through 16 rigid 22.5-degree axial positions. Housing and hub protected. No generated flame/color changes accepted.',sourceCanvas=[160,192],sourcePivot=[80,96],sharedCrop=[48,64,64,64],canvas=[64,64],pivot=[32,32],annulus=[6,23],sourceScale=.38,frames=audits,rejected={'job':'374fdcfa-03f1-4d57-ad83-0250a7fbe0da','reason':'AI clip added flames, changed purple to orange and blinked instead of turning. Only its unchanged input frame is used as the exact workbench source.'}),indent=2)+'\n',encoding='utf-8')
(R/'assets/harrier_fan_art_1019.js').write_text('"use strict";\n// Owned by build_harrier_fan_1019.py.\nconst HF19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
tax=R/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8-sig'));data['hf19_']={'role':'stage8_harrier_native_turbine_interior','sheet':None,'note':'16 PixelLab exact-workbench rotor frames from the actual authored Harrier fan.64x64/pivot32,32, shared annular mask. Native housing/hub retained; no AI flame candidate shipped. Owner build_harrier_fan_1019.py; runtime harrier_fan_1019.js.'};tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(frames=16,unique=16,canvas=[64,64],pivot=[32,32],housingExact=True,hubExact=True,paletteExact=True,nativeDark=dark)))
