"""Requested PixelLab smoothing. Uploads exact registered whole-body keys;
credentials and upload refs are never printed. Canonical weapon is baked later.
"""
from pathlib import Path
import json,re
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import upload,content
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_motion_1025';J=D/'jobs';J.mkdir(exist_ok=True)
spec=[]
for mat in ['regular','chrome']:
 # The original GPT profile faces right; the registered key7 is the left-facing
 # whole-plate version. Keep both endpoints for actual opposite torso twists.
 p=D/'seeds'/('motion_'+mat+'_7.png');im=Image.open(p).transpose(Image.Transpose.FLIP_LEFT_RIGHT);im.save(D/'seeds'/('right_'+mat+'.png'))
 for name,first,last,frames,action in [
 ('takeoff',f'motion_{mat}_0',f'motion_{mat}_2',16,'Bend both knees deeply, compress the hips, push off, tuck both knees into an upward jump. Keep the marked closed weapon fist low and OUTSIDE the same hip, with a balancing free arm. No raising the weapon arm.'),
 ('land',f'motion_{mat}_2',f'motion_{mat}_3',16,'Unfold the tucked legs from an airborne jump and absorb a landing into a low crouch. Keep the marked closed weapon fist low outside the hip. Smooth knees, hips and torso weight transfer.'),
 ('windup',f'motion_{mat}_3',f'motion_{mat}_5',16,'Spring from the crouch into a second jump, bend the knees airborne, then lift the ONE marked weapon fist up and back above the shoulder into a powerful overhead windup. Twist hips and shoulders; free hand balances separately. Do not clasp both hands together.'),
 ('strike',f'motion_{mat}_5',f'motion_{mat}_6',16,'Swing the marked weapon fist FORCEFULLY DOWN from behind the head across the body to knee height. Rotate shoulders and hips, pitch the torso forward, extend then brace the knees. One continuous connected heavy overhead strike, visible whole body rotation and recoil.'),
 ('retract',f'motion_{mat}_6',f'motion_{mat}_0',16,'Recover from the low overhead strike into the supplied one-handed side guard. Pull the marked weapon fist back toward its outside hip, straighten the knees, uncoil the torso and brace into a stable hovering return pose. Smooth connected arm and leg motion with no jumping pose swaps.'),
 ('left',f'motion_{mat}_0',f'motion_{mat}_7',16,'Turn the WHOLE ROBOT strongly toward screen LEFT into the supplied side-profile endpoint. Twist hips, planted feet, torso, helmet and shoulders together, not just the arm. Sweep the marked closed weapon fist outward from its low side guard through a broad leftward strike arc. Clear anticipation then powerful follow-through.'),
 ('right',f'motion_{mat}_0',f'right_{mat}',16,'Turn the WHOLE ROBOT strongly toward screen RIGHT into the supplied side-profile endpoint. Twist hips, feet, torso, helmet and shoulders together. Sweep the same marked weapon fist outward through a broad rightward strike arc, keeping the other hand separate. Clear anticipation then forceful follow-through.'),
 ('shield',f'power_{mat}_0',f'power_{mat}_1',16,'Brace the planted legs and extend the FREE OPEN PALM forward to project a shield. The marked closed weapon fist remains lowered OUTSIDE its hip, perfectly stable, holding its imaginary grip. Animate only connected arm joints, torso bracing and the free open palm. No energy shield is drawn in this body clip.'),
 ('palm',f'power_{mat}_0',f'power_{mat}_1',16,'Animate ONLY this robot extending its empty free arm from its chest to the supplied open-palm endpoint. Deliberate smooth elbow extension and wrist opening, with a small shoulder turn and planted legs. The OTHER marked closed fist stays low outside the hip. Every frame contains ONLY the robot on transparent background. NO circles, discs, fields, particles, glow, floor, scenery or effects. Do not add any object. Finish with the exact supplied open palm. Keep its original dark metal or silver material.'),
 ('aura',f'power_{mat}_2',f'power_{mat}_3',24,'Explosive anime super-warrior power transformation. Start hunched with both fists clenched and knees wide. Body trembles under strain; head lifts, shoulders brace, chest reactor surges. An enormous golden-white flame aura ERUPTS and streams violently UPWARD around him, cyan lightning lashes between plates, pressure ripples pulse outward. Flames must FLOW and flicker continuously, not crossfade a still aura. Keep robot solid and readable and all anatomy connected. Marked weapon fist stays low outside hip; never raise it. Match final powered pose.'),
 ]:spec.append(dict(name=name+'_'+mat,first=first,last=last,frames=frames,action=action))
spec.append(dict(name='activation',first='power_regular_2',last='power_chrome_3',frames=24,action='Actual explosive armor takeover: dark robot braces wide, fists clenched low, trembles and strains upward like a super-warrior charging power. A golden-white flame aura builds from his boots then ERUPTS upward, with animated cyan lightning. Reflective SILVER CHROMIUM plating physically spreads over shoulders, chest, forearms and shins as he straightens into the supplied final plated form. Clear progressive material takeover and moving flame tongues, not an alpha fade or static glow. Marked weapon fist remains low OUTSIDE the same hip throughout. All body parts stay connected. No face, helmet, scale or weapon changes.'))
(D/'motion-spec.json').write_text(json.dumps(spec,indent=2)+'\n',encoding='utf8')
c=PixelLab()
try:
 raw=content(c.call('get_upload_url',{}));url=re.search(r'https://[^\s"<>]+',raw).group(0);refs={}
 for q in spec:
  p=J/(q['name']+'.json')
  if p.exists() and not json.loads(p.read_text()).get('isError'):continue
  if p.exists():p.rename(p.with_suffix('.attempt'+str(len(list(J.glob(q['name']+'.attempt*')))+1)+'.json'))
  for key in [q['first'],q['last']]:
   if key not in refs:refs[key]=upload(c,D/'seeds'/(key+'.png'),url)
  args=dict(first_frame_url=refs[q['first']],last_frame_url=refs[q['last']],frame_count=q['frames'],no_background=True,seed=1025000+spec.index(q),direction='south',view='side',subject_description='one intact armored Chronos robot with pointed helmet, cyan chest reactor, blue visor, closed marked weapon fist and separate free hand, NO WEAPON',initial_pose='the exact supplied initial whole-robot pose on a fixed transparent256 canvas',enhance_prompt=False,description='FRAME FORMAT256x256 transparent, reactor128,116, same scale/camera and robot. All anatomy connected. Tiny magenta mark tracks the same closed fist. NO WEAPON, shaft or new objects; real hammer attached later. No zoom or fade. '+q['action'])
  result=c.call('animate_image_pixminimax',args);p.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');txt=content(result);m=re.search(r'job_id[:"\s]+([\w-]{20,})',txt);print(json.dumps(dict(bank=q['name'],error=result.get('isError',False),job=m.group(1) if m else None,summary=txt[:220] if result.get('isError') else 'submitted')),flush=True)
finally:c.close()
