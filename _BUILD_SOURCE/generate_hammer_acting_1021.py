"""PixelLab Hammerboss motion requests, seeded only from approved game exports."""
from pathlib import Path
import json,re,sys,concurrent.futures
from pixellab_intro_1021 import upload
from pixellab_mcp import PixelLab
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/hammer_acting_1021';D.mkdir(exist_ok=True)
s=(R/'assets/hammer_redesign_art_1020.js').read_text();art=json.loads(s[s.index('{'):s.rindex('}')+1])
def txt(v):return '\n'.join(x['text'] for x in v.get('content',[]) if x['type']=='text')
identity=dict(blue='the same bulky black and silver armored humanoid robot, cyan circular chest reactor, blue shoulder and knee lights, black horned helmet and massive cylindrical blue energy hammer on its long black handle',corrupt='the same lean demonic alien machine humanoid, black violet spiked armor, horned head, orange furnace heart, purple luminous hammer on its long dark shaft')
actions={
 'slam':'With both hands gripping the long hammer shaft, lift the entire hammer high ABOVE the head, hold briefly with its head clearly visible above the helmet, then swing the hammer forcefully straight DOWN in front, ending with its head extended well below the knees at ground impact. The hammer must project well outside the body silhouette. Feet planted, whole shaft visible. No spin, no extra hammer, no detached weapon. End in the low impact pose.',
 'jump':'Crouch deeply, pull the hammer up behind and above the head, tuck the knees in a jumping attack pose, then extend the legs for landing while striking the hammer down in front. Animate the BODY POSE around its fixed chest pivot; gameplay supplies world travel. End with bent knees, both hands on the shaft and hammer head clearly extended below the body. No camera travel.',
 'side':'Wind the long hammer to the left across the shoulder, rotate the torso into a powerful horizontal SIDE SWING to the right, and extend both arms fully. At the impact pose the shaft is almost horizontal and the entire massive hammer HEAD sticks out far to the RIGHT beyond the body silhouette. Hold that extended impact pose, then recover. Exactly two arms and one hammer, not a swirling energy ribbon.',
 'hold':'Bring the hammer high over the head in both hands, arms lifted, then HOLD the hammer above the helmet while its energy head pulses brighter. Final half remains in that same raised-hammer pose, with subtle charged energy flowing inside the hammer and chest. Whole weapon stays visible and attached, no swing or release. Keep feet planted and fixed chest anchor.',
 'throw':'Wind the hammer back over the right shoulder, step forward and extend both arms into a powerful hammer THROW toward the viewer and down. Open hands at the release pose and finish with EMPTY hands extended forward, then braced unarmed recovery. After release do not draw the flying hammer anywhere; the game renders the detached weapon separately. Exactly two arms, no second hammer.',
 'cast':'Keep the hammer gripped in the left hand beside the body. Raise the free right arm, open its palm toward the viewer and cast a spell with a clear outstretched hand. Lean into the casting gesture, hold the palm outward, small energy gathering in the palm and chest. No giant effect, no beam or projectile baked into the sprite. Finish with hand clearly extended.',
 'beam':'Brace both feet wide, lean back slightly, spread both arms to either side and aim the bright circular chest core forward and down toward the player for a sustained laser beam. Chest core opens and pulses intensely while the head stays above it. Hold the braced firing posture for the last half. No beam or scenery baked into sprite; the game owns the actual laser. Keep hammer held to one side, visible entire shaft.',
 'rage':'Clench the free fist, pull the hammer beside the shoulder, lean forward and ROAR in rage, shoulders and chest heaving. The reactor and existing armor lights flare fiercely in their authored colors, then settle into an aggressive ready stance with hammer fully visible. Two arms, same metal armor, no fire covering the silhouette.',
 'chromium':'Charge with arms and hammer raised, then reflective CHROMIUM armor physically plates over the existing shoulders, torso, arms and legs in a clear takeover transformation. Finish as the exact same humanoid and hammer wearing brilliant reflective silver chromium armor with sharp white metal highlights and the ORIGINAL colored chest core, armor lights and hammer. Chromium is real solid plated armor, not a translucent aura, not a giant circular shield. Keep same size and limbs; hold the complete transformed armored pose for final half.'}
actions['spin']='Spin the complete same humanoid body around its upright chest axis while gripping the long hammer shaft in both hands with arms extended. Show actual front, side, back, opposite side and front views in one full turn. The solid hammer HEAD must sweep a full circle OUTSIDE the body silhouette on its long handle. Exactly one hammer and two arms, no detached spinning head, no energy spiral substituting for the body. Return to the original front-facing pose.'
header='FRAME FORMAT: 256 x 256 transparent pixels per frame. Identical canvas, one common proportional scale and fixed CHEST pivot128,112 in EVERY frame. Keep the current body scale and view. Reserve transparent margins for the full extended hammer; keep limbs and weapon unclipped. Crisp arcade pixel art, no scenery, text, UI, extra limbs, duplicate weapons, camera zoom or perspective changes. '
refs_file=D/'upload-refs.json'
if refs_file.exists():refs=json.loads(refs_file.read_text())
else:
 c=PixelLab();url=re.search(r'https://[^\s"<>]+',txt(c.call('get_upload_url',{}))).group(0)
 refs={v:upload(c,R/art['banks'][v+'_idle'][0]['path'],url) for v in ['blue','corrupt']};c.close();refs_file.write_text(json.dumps(refs,indent=2)+'\n')
plan={}
for variant in ['blue','corrupt']:
 source=refs[variant]
 for i,(name,action) in enumerate(actions.items()):
  key=variant+'_'+name;plan[key]=dict(description=header+action,first_frame_url=source,frame_count=16,no_background=True,subject_description=identity[variant],initial_pose='standing facing the viewer with hammer held low diagonally in both hands, chest at pixel128,112',view='low top-down',direction='south',seed=10212100+(0 if variant=='blue' else 100)+i)
extra={'blue_throw_raised':D/'raw/blue_throw/06.png','blue_empty':R/art['banks']['blue_empty'][0]['path'],'corrupt_empty':R/art['banks']['corrupt_unarmed'][0]['path'],'blue_ship':D/'references/blue_ship.png','blue_ball':D/'references/blue_ball.png','corrupt_ball':R/art['banks']['corrupt_ball'][0]['path']}
if any(n not in refs for n in extra):
 c=PixelLab();url=re.search(r'https://[^\s"<>]+',txt(c.call('get_upload_url',{}))).group(0)
 for n,path in extra.items():
  if n not in refs:refs[n]=upload(c,path,url)
 c.close();refs_file.write_text(json.dumps(refs,indent=2)+'\n')
for j,v in enumerate(['blue','corrupt']):
 for action in ['to_ball','from_ship']:
  args=dict(frame_count=16,no_background=True,view='low top-down',direction='south',seed=10212300+j*10+(action=='from_ship'))
  if action=='to_ball':args.update(first_frame_url=refs[v],last_frame_url=refs[v+'_ball'],subject_description=identity[v],initial_pose='standing facing the viewer gripping the long hammer',description=header+'Fold the arms and legs INTO the torso, armor panels folding mechanically together, then transform THIS SAME humanoid into the exact supplied SPIKED BALL endpoint. The helmet, chest core and hammer fold inside solid armor panels; spikes extend outward. One connected body, no duplicate robot or separate sphere. Fixed central anchor; end as the exact complete supplied ball.')
  else:args.update(first_frame_url=refs['blue_ship'],last_frame_url=refs[v],subject_description='the actual black silver Hammerboss combat ship with blue nose reactor, transforming into '+identity[v],initial_pose='the exact supplied Hammerboss spacecraft facing down toward the viewer',description=header+'The actual supplied ship mechanically unfolds INTO the exact supplied humanoid endpoint. Preserve this precise aircraft silhouette, blue nose core, wings and metal palette at the start. Wings fold into shoulders and arms, fuselage splits into torso and legs, the chest core stays centered and the long hammer deploys into both hands. End in the supplied complete humanoid ready pose. No generic substitute jet, no duplicate ship, no camera travel. Gameplay supplies fly-in movement.')
  plan[v+'_'+action]=args
for v,action in [('blue','cast'),('blue','beam'),('blue','rage'),('corrupt','beam'),('corrupt','rage')]:
 args=dict(plan[v+'_'+action]);args['first_frame_url']=refs[v+'_empty'];args['seed']+=500
 motion={'cast':'Extend the right open hand forward to cast a spell, lean into the gesture while the left arm stays braced and open. Hold the casting hand clearly outstretched. Small energy in palm only, no large baked effect.', 'beam':'Spread both empty arms wide, brace feet, lean backward and open the bright circular chest reactor panels toward the viewer. Hold that symmetrical braced posture with subtly pulsing light contained entirely INSIDE the circular chest aperture. All light stays inside the body outline. Empty transparent space all around the character.', 'rage':'Clench BOTH EMPTY fists, pull shoulders back and roar furiously, chest reactor and existing armor lights flare, then finish leaning forward in a threatening unarmed combat stance.'}[action]
 args['description']=header+'UNARMED version of this exact robot. The hammer has been destroyed: absolutely NO hammer, shaft, gun or extra weapon. Exactly TWO arms. '+motion
 args['subject_description']=identity[v].split(', and massive')[0].split(', purple luminous hammer')[0]+' with empty hands and no weapon'
 args['initial_pose']='the exact supplied unarmed humanoid facing the viewer, empty hands, chest fixed at128,112'
 plan[v+'_'+action+'_empty']=args
args=dict(plan['blue_throw']);args.update(first_frame_url=refs['blue_throw_raised'],last_frame_url=refs['blue_empty'],seed=10212900,initial_pose='the exact robot holding its hammer raised above the head',description=header+'Throw the hammer AWAY from the robot: extend both arms FORWARD, OPEN the hands and LET GO of the handle. The hammer flies away and is completely ABSENT by the middle of the clip. Finish in the exact supplied EMPTY-HANDED pose. DO NOT swing the hammer to the ground. DO NOT keep gripping it. No ground strike. Only the body remains after release; gameplay renders the independent flying weapon.')
plan['blue_throw_release']=args
for action in ['cast','beam','rage']:
 args=dict(plan['blue_'+action+'_empty']);args['seed']+=700
 args['subject_description']='a bulky black and silver armored humanoid robot with blue armor lights, cyan circular chest reactor, black horned helmet and two empty open hands'
 args['initial_pose']='standing with two empty open hands beside the torso, as supplied in the reference'
 motion={'cast':'Lift the right arm and extend the right OPEN PALM forward in a clear casting gesture, while the left empty hand stays beside the torso. All fingers and both empty palms remain visible. Finish with the right arm straight and palm facing the viewer. Subtle contained blue light inside that palm only.', 'beam':'Brace both feet wide and spread both empty arms to the sides, leaning backward with the chest aperture aimed toward the viewer. The circular reactor panels open, subtle blue light pulses only INSIDE the chest aperture. Hold this powerful braced posture.', 'rage':'Clench both empty hands into fists, pull the shoulders back and roar, flare the existing blue chest and armor lights briefly, then lean forward with both fists braced beside the torso.'}[action]
 args['description']=header.replace('full extended hammer','full body')+'Animate the robot BODY ONLY, completely empty-handed throughout. '+motion+' Only this single body on transparency. Keep all surrounding space completely empty. No props, no scenery, no additional objects, no separate effects.'
 plan['blue_'+action+'_clean']=args
plan['corrupt_stun']=dict(first_frame_url=refs['corrupt_empty'],frame_count=16,no_background=True,view='low top-down',direction='south',seed=10214000,subject_description='the same black violet armored demonic humanoid with horned head, orange heart and two empty hands',initial_pose='the exact supplied unarmed humanoid standing facing the viewer',description='FRAME FORMAT: 256 x256 transparent pixels, common scale and fixed floor contact at pixel128,200. Same exact character, palette, proportions and crisp arcade pixels, empty background. Recoil from a hard hit, buckle at the knees and collapse onto ONE KNEE, the opposite empty fist braced on the floor, head hanging LOW in exhaustion. The chest naturally drops as the knee bends. Hold that clear deeply KNEELING defeated pose for the final half of the animation. Keep both feet/floor contacts at the same baseline, no jumping or camera movement. Exactly two arms and empty hands; this single whole body only, nothing else.')
(D/'requests.json').write_text(json.dumps(plan,indent=2)+'\n')
def start(item):
 name,args=item;p=D/(name+'-job.json')
 if p.exists() and not json.loads(p.read_text()).get('isError'):return
 c=PixelLab()
 try:
  result=c.call('animate_image_pixminimax',args);p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(bank=name,error=result.get('isError',False),receipt=txt(result)[:1800])),flush=True)
 finally:c.close()
if __name__=='__main__':
 names=sys.argv[1:] or list(plan)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(start,[(n,plan[n]) for n in names]))
