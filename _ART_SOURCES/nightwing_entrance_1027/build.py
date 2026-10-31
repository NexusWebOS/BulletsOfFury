from pathlib import Path
from PIL import Image,ImageDraw
import json,math,os,shutil,subprocess
W=Path(__file__).resolve().parent;R=W.parents[1];D=W/'compiled';D.mkdir(exist_ok=True)
im=Image.open(R/'assets/game/levels/stage_06/boss/sky_repair_1004i/ace.png').convert('RGBA');frames=[];groups={};size=272
def pad(q):
 c=Image.new('RGBA',(size,size));c.alpha_composite(q,((size-q.width)//2,(size-q.height)//2));return c
def native(i):return pad(im.crop((i*176,0,(i+1)*176,184)).resize((184,192),Image.Resampling.NEAREST))
def add(name,ff):groups[name]={'start':len(frames),'count':len(ff)};frames.extend(ff)
def thrust(q,i):
 c=Image.new('RGBA',(size,size));data=(R/'assets/director_art_0927.js').read_text(encoding='utf-8');da=json.loads(data[data.index('{'):data.rindex('}')+1]);r=da['reels']['exhaust']['frames'][i%6]
 sheet=Image.open(R/da['sheets']['specialist']['path']).convert('RGBA');f=sheet.crop((r[0],r[1],r[0]+256,r[1]+256)).resize((34,34),Image.Resampling.NEAREST)
 for side in[-1,1]:c.alpha_composite(f,(size//2+side*22-round(r[4]*34/256),size//2-57-round(r[5]*34/256)))
 c.alpha_composite(q);return c
add('south',[thrust(native(0),i)for i in range(8)]);add('damaged',[thrust(native(1),i)for i in range(8)]);add('inverted',[native(2)])
s=(R/'assets/part2_art_1010.js').read_text(encoding='utf-8');P=json.loads(s[s.index('{'):s.rindex('}')+1]);motions={}
for motion in ['roll','somer']:
 ff=[]
 for a in sorted((a for a in P['stealth_'+motion]if a['role']=='blue'),key=lambda a:a['pose']):ff.append(pad(Image.open(R/a['path']).convert('RGBA').resize((242,242),Image.Resampling.NEAREST)))
 motions[motion]=ff;add(motion,ff)
add('inverted_somer',[q.rotate(180)for q in motions['somer']]);add('bank_right',[motions['roll'][1]]);add('bank_left',[motions['roll'][15]]);add('north',[q.rotate(180)for q in frames[:8]]);add('death',[native(1).rotate(-i*360/32,Image.Resampling.NEAREST)for i in range(32)])
A={}
for hit in[False,True]:
 name='whole_hit'if hit else'whole';out=Image.new('RGBA',(size*8,size*math.ceil(len(frames)/8)))
 for i,q in enumerate(frames):
  if hit:c=Image.new('RGBA',q.size,(255,255,255,0));c.putalpha(q.getchannel('A'))
  else:c=q
  out.alpha_composite(c,(i%8*size,i//8*size))
 out.save(D/(name+'.png'),optimize=True);A[name]={'key':'nw28_'+name,'path':f'assets/game/levels/stage_06/boss/nightwing_entrance_1027/{name}.png','cw':size,'ch':size,'cols':8,'frames':len(frames),'pivot':[136,136]}
A['groups']=groups;(D/'manifest.json').write_text(json.dumps(A,indent=2),encoding='utf-8');(W/'nightwing_entrance_art_1027.js').write_text('"use strict";\nconst NW28_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8')
o=Image.new('RGBA',(size*3,size*2),(15,26,37,255));g=ImageDraw.Draw(o)
for i,name in enumerate(['south','north','damaged','roll','somer','death']):o.alpha_composite(frames[groups[name]['start']+(4 if name in['roll','somer','death'] else 0)],(i%3*size,i//3*size));g.text((i%3*size+9,i//3*size+9),name,fill='white')
o.save(W/'whole-poses.png');print(f'Authored {len(frames)} complete whole-ship poses with exhaust, matching white frames and fixed272px pivots.')

for key in ['whole','whole_hit']:
 a=A[key];target=R/a['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(D/(key+'.png'),target)
shutil.copy2(W/'nightwing_entrance_art_1027.js',R/'assets/nightwing_entrance_art_1027.js')
ase=os.environ.get('ASEPRITE_EXE')or shutil.which('aseprite')
if ase:subprocess.run([ase,'--batch',str(D/'whole.png'),'--save-as',str(W/'nightwing-whole.aseprite')],check=True,capture_output=True)
