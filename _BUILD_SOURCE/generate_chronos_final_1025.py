"""Pinned whole-body rotation and overhead chromium takeover, via PixelLab."""
from pathlib import Path
from PIL import Image
import json,re
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import upload,content
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_final_1025';S=D/'seeds';S.mkdir(exist_ok=True)
im=Image.open(D/'spin-keys.png').convert('RGBA')
# One scale for all six poses. Reactor-aligned; no per-frame fitting.
cores=[(397,201),(843,206),(1394,203),(165,679),(657,683),(1137,678)]
for i,(cx,cy) in enumerate(cores):
 x=i%3*512;y=i//3*512;tile=im.crop((x,y,x+512,y+512)).resize((180,180),Image.Resampling.NEAREST)
 out=Image.new('RGBA',(256,256));out.alpha_composite(tile,(round(128-(cx-x)*180/512),round(116-(cy-y)*180/512)));out.save(S/f'spin-{i}.png')
for mat in ['regular','chrome']:
 Image.open(R/f'_ART_SOURCES/chronos_motion_1025/frames/windup_{mat}/16.png').save(S/f'raised-{mat}.png')
spec=[
 dict(name='spin_a',first='spin-0',last='spin-3',frames=16,action='Rotate the WHOLE connected robot CLOCKWISE through left profile into the rear view. His ONE weapon arm stays FULLY EXTENDED STRAIGHT at shoulder height throughout; the long hammer points OUTWARD beyond his straight elbow. Helmet, shoulders, hips, knees and boots all visibly turn together through a 180-degree half spin. Maintain rigid weapon geometry; no wrist-only circle and no bending the arm across his body. Smooth airborne combat turn, no walking. Finish in exact rear pose.'),
 dict(name='spin_b',first='spin-3',last='spin-0',frames=16,action='Continue the WHOLE robot CLOCKWISE from rear view through right profile back to front view. ONE weapon arm remains FULLY EXTENDED STRAIGHT at shoulder height, its long hammer points OUTWARD beyond his fist. Helmet, shoulders, hips, knees and boots turn TOGETHER through remaining180degrees. Finish EXACT supplied original front pose for seamless combat spin. No wrist-only rotation, no hammer crossing his chest, no walking.'),
 dict(name='overhead_activation',first='raised-regular',last='raised-chrome',frames=24,action='The robot HOLDS HIS MARKED WEAPON FIST STRAIGHT UP ABOVE HIS HEAD throughout the full charge. Keep the fist continuously raised. Electrical blue-white energy pours into his raised fist and travels down arm into chest; reflective SILVER CHROMIUM armor spreads progressively from shoulders over torso then arms and legs. He braces and trembles under power. Animate crawling blue electricity, metallic plates locking in order, actual physical movement. NO yellow/gold/red flames, no Super Saiyan aura. Preserve fixed pose/camera/scale and close with fully chrome armor and same raised fist. NO HAMMER or new weapon: actual hammer is baked into frames later.')]
(D/'motion-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
c=PixelLab()
try:
 raw=content(c.call('get_upload_url',{}));url=re.search(r'https://[^\s"<>]+',raw).group(0);refs={};J=D/'jobs';J.mkdir(exist_ok=True)
 for i,q in enumerate(spec):
  p=J/(q['name']+'.json')
  if p.exists():continue
  for k in [q['first'],q['last']]:
   if k not in refs:refs[k]=upload(c,S/(k+'.png'),url)
  result=c.call('animate_image_pixminimax',dict(first_frame_url=refs[q['first']],last_frame_url=refs[q['last']],frame_count=q['frames'],no_background=True,seed=1025250+i,direction='south',view='side',enhance_prompt=False,subject_description='One complete intact Chronos robot, dark graphite armor or silver chromium, blue visor, round cyan reactor, pointed helmet',initial_pose='Exact supplied complete robot pose, fixed256x256 transparent canvas, reactor128,116',description='FRAME FORMAT256x256, same camera/scale, all anatomy connected, no scenery, no fading, no parts separated. '+q['action']))
  p.write_text(json.dumps(result,indent=2)+'\n');print(q['name'], 'error' if result.get('isError') else 'submitted',flush=True)
finally:c.close()
