"""Rear-leg push poses use the existing Warden's rigid authored upper/lower anatomy.
No source-pixel stretching. All world cells share a 320 canvas and hip pivot.
"""
from pathlib import Path
import json,math,subprocess
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_07/boss/warden_lunge_1028';D.mkdir(parents=True,exist_ok=True)
cmd="const fs=require('fs'),vm=require('vm'),s={};vm.createContext(s);vm.runInContext(fs.readFileSync('assets/stage78_review_art_1025.js','utf8')+';this.a=R25_ART;',s);process.stdout.write(JSON.stringify(s.a));"
A=json.loads(subprocess.check_output(['node','-e',cmd],cwd=R,text=True));out={}
def transform(im,source,target,angle,k=.64):
 c=math.cos(angle);s=math.sin(angle);sx,sy=source;tx,ty=target
 return im.transform((320,320),Image.Transform.AFFINE,(c/k,s/k,sx-(c*tx+s*ty)/k,-s/k,c/k,sy+(s*tx-c*ty)/k),Image.Resampling.NEAREST)
for name in ['rearL','rearR']:
 meta=A['legs'][name];side=-1 if name.endswith('L') else 1;src=Image.open(R/A['sheets']['leg_'+name]['path']).convert('RGBA').crop((0,0,256,256)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 hip=np.array([meta['pivot'][0],256-meta['pivot'][1]],float);knee=np.array([130 if side<0 else 126,111],float);foot=np.array([meta['frames'][0]['foot'][0],256-meta['frames'][0]['foot'][1]],float)
 upper=src.copy();upper.paste((0,0,0,0),(0,0,256,104));lower=src.copy();lower.paste((0,0,0,0),(0,124,256,256))
 l1=np.linalg.norm(knee-hip);l2=np.linalg.norm(foot-knee);poses=[];sheet=Image.new('RGBA',(320*8,320*6))
 for f in range(48):
  # First 16 brace, next 16 push, last 16 recover. Angles come from the actual bones.
  if f<16:u=f/15;lat=70+(45-70)*u;back=100+(20-100)*u
  elif f<32:u=(f-16)/15;lat=45;back=20+70*u
  else:u=(f-32)/15;lat=45+(70-45)*u;back=90+10*u
  target=np.array([side*lat,-back])/.64;d=np.linalg.norm(target);d=min(d,l1+l2-1);direction=target/np.linalg.norm(target);along=(l1*l1-l2*l2+d*d)/(2*d);height=math.sqrt(max(0,l1*l1-along*along));perp=np.array([-direction[1],direction[0]])
  joint=direction*along+perp*height*side;goal=direction*d
  a1=math.atan2(joint[1],joint[0])-math.atan2(*(knee-hip)[::-1]);a2=math.atan2((goal-joint)[1],(goal-joint)[0])-math.atan2(*(foot-knee)[::-1])
  frame=Image.new('RGBA',(320,320));frame.alpha_composite(transform(upper,hip,[160,160],a1));frame.alpha_composite(transform(lower,knee,np.array([160,160])+joint*.64,a2))
  sheet.paste(frame,((f%8)*320,(f//8)*320));point=(np.array([160,160])+goal*.64).tolist();poses.append(dict(foot=point,target=point,knee=(np.array([160,160])+joint*.64).tolist()))
 sheet.save(D/(name+'.png'));hit=Image.new('RGBA',sheet.size,(255,255,255,0));hit.putalpha(sheet.getchannel('A'));hit.save(D/(name+'_hit.png'))
 out[name]=dict(key='wl39_'+name,path=(D/(name+'.png')).relative_to(R).as_posix(),cw=320,ch=320,cols=8,frames=48,pivot=[160,160],poses=poses)
 out[name+'_hit']={**out[name], 'key':'wl39_'+name+'_hit','path':(D/(name+'_hit.png')).relative_to(R).as_posix()}
# Exact authored core silhouette for the airborne ground shadow; original alpha retained.
core=Image.open(R/'assets/game/shared/combat/encounter_revision_1027/core.png').convert('RGBA')
shadow=Image.new('RGBA',core.size,(0,0,0,0));shadow.putalpha(core.getchannel('A'));shadow.save(D/'core_shadow.png')
out['coreShadow']=dict(key='wl39_core_shadow',path=(D/'core_shadow.png').relative_to(R).as_posix(),cw=168,ch=190,cols=4,frames=16,pivot=[84,95],source='er28_core')
(D/'manifest.json').write_text(json.dumps(dict(banks=out,source='R25 authored rear legs, rigid source-preserving hinge poses',builder='_BUILD_SOURCE/build_warden_lunge_1028.py'),indent=2))
(R/'assets/warden_lunge_art_1028.js').write_text('"use strict";\nconst WL39_ART='+json.dumps(out,separators=(',',':'))+';\n',encoding='utf8')
print('rear push banks: 48 fixed hip poses per leg')

# Register this standalone bank with its owning builder; preserve existing catalogue bytes.
tax=R/'assets/data/ART_TAXONOMY.json';raw=tax.read_text(encoding='utf8')
if '"wl39_"' not in raw:
 entry=dict(role='warden_rear_leg_push',owner='_BUILD_SOURCE/build_warden_lunge_1028.py',manifest='assets/game/levels/stage_07/boss/warden_lunge_1028/manifest.json',note='October28: 48 rigid source-pixel hinge poses, 320 cells, shared hip pivots, actual alpha targets and native hit flashes. Front/claw/body/HP ownership unchanged.')
 tax.write_text('{\n  "wl39_": '+json.dumps(entry,separators=(',',':'))+','+raw[1:],encoding='utf8')
