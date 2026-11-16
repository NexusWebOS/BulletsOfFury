from pathlib import Path
from PIL import Image
import json,hashlib,shutil,sys,struct,zlib,math
R=Path('D:/BOF-Downloads/2026-11-14/RevG-source');S=R/'_ART_SOURCES/stage_frame_1115';O=R/'_shots/stage_frame_1115';A=R/'assets/game/shared/campaign/stage_frame_1115'
for p in [S,O,A]:p.mkdir(parents=True,exist_ok=True)
metaFile=Path(__file__).with_name('stage_frame_1115_generation.json')
if not metaFile.exists():metaFile=S/'generation.json'
meta=json.loads(metaFile.read_text(encoding='utf8'))
if not(S/'generation.json').exists():shutil.copyfile(metaFile,S/'generation.json')
master=S/'generated-frame-kit.png'
if not master.exists():shutil.copyfile(meta['generationOutput'],master)
raw=Image.open(master).convert('RGBA');assert raw.height%3==0
slots=[raw.crop((0,i*raw.height//3,raw.width,(i+1)*raw.height//3))for i in range(3)];bounds=[p.getbbox()for p in slots]
l=max(0,min(b[0]for b in bounds)-4)//2*2;t=max(0,min(b[1]for b in bounds)-4)//2*2;rr=min(raw.width,math.ceil((max(b[2]for b in bounds)+4)/2)*2);bb=min(slots[0].height,math.ceil((max(b[3]for b in bounds)+4)/2)*2);crop=[l,t,rr,bb]
k=min(912/(rr-l),300/(bb-t));size=[round((rr-l)*k),round((bb-t)*k)];at=[(912-size[0])//2,(300-size[1])//2];frames=[]
for p in slots:
 im=p.crop(crop).resize(size,Image.Resampling.NEAREST);c=Image.new('RGBA',(912,300));c.alpha_composite(im,tuple(at));frames.append(c)
TIMES=[1000]*3
old=(R/'_BUILD_SOURCE/pursuit_trace_1115_build.py').read_text(encoding='utf8');defs=old[old.index('def string('):old.index("M={'version'")].replace('16,456,256','3,912,300').replace('0,15,0,0,bytes','0,2,0,0,bytes').replace('Traced frame rim','Generated briefing frame').replace('Selected green-white pulse','Reserved overlay - empty').replace('selected-green-white','mission-priority-clear');exec(compile(defs,'aseprite-source-functions','exec'))
source=S/'stage-frames.aseprite';author='--author'in sys.argv or not source.exists()
if author:aseprite(source,frames[0],[(f,Image.new('RGBA',(912,300)))for f in frames])
decoded=decode_visible(source)
if author:assert all(a.tobytes()==b.tobytes()for a,b in zip(frames,decoded))
frames=decoded;M={**meta,'sourceMasterSha256':hashlib.sha256(master.read_bytes()).hexdigest(),'sourceCrop':crop,'sourceSlot':[raw.width,raw.height//3],'proportionalExportScale':k,'exportSize':size,'offset':at,'logicalRect':{'x':12,'y':338,'w':456,'h':150},'textSafe':{'title':[64,24,328,22],'body':[40,63,376,57]},'images':{}}
for name,im in zip(meta['variants'],frames):
 path=A/(name+'.png');im.save(path);assert im.size==(912,300);M['images'][name]={'key':'map15_frame_'+name,'path':str(path.relative_to(R)).replace('\\','/'),'w':912,'h':300,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};im.save(O/(name+'-frame.png'))
(S/'manifest.json').write_text(json.dumps(M,indent=2),encoding='utf8',newline='\n');(R/'assets/stage_frame_art_1115.js').write_text('"use strict";\nconst MBR15_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(O/'asset-qa.json').write_text(json.dumps({'frames':3,'sourceRoundtrip':True,'source':str(source.relative_to(R)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'manifest':M,'scope':'Generated blank frame variants, one proportional direct-master export and fixed2x UI density. Source-format writer/decoder; editor GUI/CLI unavailable, not claimed.'},indent=2),encoding='utf8')
print(json.dumps({'variants':list(M['images']),'source':raw.size,'crop':crop,'scale':k,'export':size,'cell':[912,300]},indent=2))
