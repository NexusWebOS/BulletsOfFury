"""Publish observations against the immutable original Furious recordings."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/furious_789_1025'
# Times are MP4 elapsed time, not the in-game BOSS clock.
ISSUES=[
 (7,33.4,36.3,'P1','Gait','Legs swing as rigid plates; toes slide with the chassis instead of planting, pushing, lifting and stepping.','Confirmed visually; distance-driven articulated walking is being implemented.'),
 (7,36.3,43.0,'P2','Body rotation','Swipes and gun bracing tilt the entire top-down actor; the feet do not establish a new support stance. This reads as rocking a card.','Confirmed visually; turn and stance changes are being implemented.'),
 (7,42.9,308.9,'P2','Attack repetition','21 jump states occupy 79.3 seconds. Dedicated chase/crawl states total only 8.5 seconds, so the spider spends little of this recording visibly walking.','Measured from native timeline; adding walking between attack groups while retaining warned jumps.'),
 (7,134.7,296.4,'P2','Damaged stance','After the first front leg breaks at 02:14.7, the chassis leans while the surviving legs keep the same sliding gait. Front pair ends at 03:39.5; rear pair ends at 04:56.3.','Confirmed visually and in native part timeline; surviving-leg stance is being implemented.'),
 (7,308.9,351.0,'P1','Hit readability','Sustained hits refresh the core white overlay almost continuously, hiding the faceplate and attack detail. HP is still decreasing.','Confirmed visually and in flash owner; keep actual hit feedback and restore color between pulses.'),
 (8,7.0,138.4,'P2','Living arena','The organic background reads as a still picture. Existing very slow drift and faint code layers do not make its veins feel alive.','Visual/design finding; animate the existing authored background on an independent clock.'),
 (8,14.3,16.7,'P1','Eye beam','The thin red beam does not fill the red eye aperture. The final socket override uses boss center rather than the visible eye in the current pose.','Confirmed visually and in owner; measured eye socket plus animated aperture flare is being implemented.'),
 (8,17.5,21.3,'P1','Claw warnings and shots','Claw FOV starts at a previous pose while shots use the moving raised claws. No distinct claw muzzle flash links each release to the arm. Repeats throughout the first host.','Confirmed visually and in owner; use one committed raised pose/socket for warnings, missiles and projectiles.'),
 (8,70.3,104.6,'P1','Arm destruction','Destroyed right arm stays attached and darkened at 01:10.3; left arm at 01:44.2. Neither breaks off or shatters.','Current implementation was intentional under an older art rule; Mike explicitly replaces it with exploding detached arms.'),
 (8,104.6,138.4,'P1','Ball traversal','Ball movement stops during every horizontal beam tell/fire. Its route clock advances only while moving, leaving much of its four-point route unfinished before recovery. First active movement also jumps to the path start.','Confirmed visually and in code; continuous full-field route with warned dropped code bombs is being implemented.'),
 (8,104.6,138.4,'P2','Code bomb pressure','Bombs only appear after every second stopped laser cycle. This yields sparse aimed bombs instead of the requested trail left by a moving ball.','Confirmed visually and in owner; regular drops with native shootable bombs, reaction time and bounded active count.'),
 (8,14.6,137.5,'P1','Host hit flash','Whole humanoid/ball becomes a solid white silhouette under repeated shots, masking pose, dead-arm state and attack details.','Confirmed visually; localized arm feedback and visible separated pulse windows are being implemented.'),
 (8,138.4,142.4,'P2','Falling host explosion','The falling explosion works, but the body produces no recognizable armor fragments moving away from it.','Mike requested enhancement; preserve the existing fall/explosion owner and add actual alpha-cut authored debris.'),
 (8,152.4,164.0,'P1','Download transformation','The rebirth resolves into a fully solid held pose before the reveal. There is no visible accumulating data reconstruction or completion beat.','Confirmed visually; digital scan reconstruction, spin, increasing completion and a final light release are being implemented.'),
 (8,155.4,164.0,'P1','Lightning identity','The alleged lightning is a curved blue pinwheel/ring, including the same shapes in Mike\'s screenshots. It does not read as branching electrical bolts.','Confirmed visually and in actual asset; replace this scene\'s ring effects with inspected authored lightning bolts.'),
 (8,196.7,256.5,'P2','Final form hit readability','White whole-body hit plates also hide the final main form during attack tells. Copied Hammer, helicopter, brain and Volcano forms exhibit the same problem later.','Confirmed visually across forms; preserve their flash timers while giving the overlay a visible pulse envelope.'),
 (8,203.0,215.7,'P2','Effect congestion','Portal, duplicate silhouettes, download helpers, FOV and large pickup labels overlap the main actor. 03:29–03:33 is a clear example.','Visual/readability follow-up; authored final-form attack composition retained in this pass.'),
 (8,470.0,538.0,'P1','Volcano visibility','Repeated corner passes leave the Volcano mostly beyond the screen edge while large diagonal FOV fields remain visible. Examples: 07:51, 08:07–08:15, 08:27–08:29 and 08:49–08:59.','Confirmed visually; separate later-form choreography issue, outside Mike\'s first-host/rebirth redesign.'),
 (8,571.0,573.5,'P2','Hammer copy aura','The Hammer copy\'s red rage aura forms a hard rectangular-looking field around the body at 09:31. It obscures the silhouette.','Confirmed visually; Stage8 copy retains its independent native owner; Stage5 fixes do not automatically apply here.'),
 (9,3.0,85.2,'P2','Twin progress readability','No health display during the entire twins fight. The first disabled sentinel dims but remains present; progress is difficult to judge amid the nebula and supply drops.','Intentional source contract: health appears only after fusion, disabled twins wait at 1 HP. Readability proposal, not a stuck/immortal-boss bug.'),
 (9,27.0,43.0,'P2','Projectile contrast','Purple sentinel rounds compete with bright purple nebula branches and glowing supply drops; several shot lanes are hard to read at normal size.','Visual/readability finding; a human dodge test is still needed before making a balance claim.'),
 (9,85.2,87.7,'P3','Fusion presentation','Fusion succeeds and both sentinels converge, but supply crates remain in front of the reveal. The center crate competes with the new hull.','Confirmed visually; presentation polish proposal, native fusion logic works.'),
 (9,93.0,135.0,'P2','Final-form staging','Tidal Sovereign spends most of its approximately 50-second fight near upper center; volleys change more than body choreography. Pickup labels repeatedly cover the attack field.','Visual/design finding; no evidence of a stalled state machine.'),
 (9,3.0,85.2,'P3','Rotated hit overlay','Twin base hull is rotated by w.spin, but its blue hit overlay is drawn axis-aligned in the draw owner. This can create offset edges.','Source-confirmed transform mismatch; visible severity needs a controlled native hit-frame probe.'),
]

def fmt(t):return f'{int(t)//60:02}:{int(t)%60:02}'
def main():
    rows=[dict(id=f'S{s}-{i+1:02}',stage=s,start=a,end=b,priority=p,category=c,finding=f,status=z) for i,(s,a,b,p,c,f,z) in enumerate(ISSUES)]
    resolved={
      'Gait':'Implemented: four eight-pose leg banks, alternating diagonal support and planted world-space toes; native alpha targets verified.',
      'Body rotation':'Implemented: bounded continuous steering; body, native melee tips, guns, projectiles and warnings share one transform.',
      'Attack repetition':'Implemented: walking between groups and fewer automatic swipe-to-jump continuations; native HP and warning windows retained.',
      'Damaged stance':'Implemented: surviving legs retain the planted gait; destroyed parts remain absent from rendering and native targets.',
      'Hit readability':'Implemented: visible white hit pulses with authored color returning between sustained-hit pulses; native timers and expiry retained.',
      'Living arena':'Implemented: moving organic tissue bands, brightness pulses and native code layers on an independent clock.',
      'Eye beam':'Implemented: measured eye sockets in all 45 poses and an eight-frame red/white flare covering the eye, rooted to the native animated laser.',
      'Claw warnings and shots':'Implemented: raised claw pose, exact shared FOV/muzzle sockets, visible native muzzle flashes and alternating shootable physical rockets/ordinary projectiles.',
      'Arm destruction':'Implemented per Mike\'s new approval: arms explode, break away and shatter into actual authored alpha fragments. Native part HP and protected core retained.',
      'Ball traversal':'Implemented: continuous full-field paths, smooth start, one permanent fold and no stopped horizontal beam cycles.',
      'Code bomb pressure':'Implemented: regularly dropped native shootable code bombs, four-active cap, 112-unit target spacing and native 1.8-second Furious reaction time.',
      'Host hit flash':'Implemented: damaged arm/core pixels flash separately; ball pulses retain detail between hits. Native timers are preserved.',
      'Falling host explosion':'Implemented: preserve the loved falling explosion and supplement it with opaque authored armor fragments; final native destruction also gets fragments.',
      'Download transformation':'Implemented: actual fusion plate reconstructs in digital scan bands while spinning, shows increasing download completion and settles upright at 100% before native whiteout/reveal.',
      'Lightning identity':'Implemented: inspected authored branching blue bolts replace the rejected wheel in rebirth; exactly 24 accelerating native beats remain.',
      'Final form hit readability':'Partly improved: final main plate and Volcano now use readable hit pulses. Hammer, helicopter and brain native hit/effect composition remains a documented follow-up.',
      'Rotated hit overlay':'Implemented: native blue overlay now shares hull rotation, fusion scale and disabled opacity; hidden twin HP and fusion rules remain intact.'}
    for q in rows:
        if q['category']in resolved:q['status']=resolved[q['category']]
    data=dict(timeBasis='Elapsed MP4 time in the original Oct25 recordings; not the BOSS HUD clock.',method='All three continuous native Furious recordings inspected in chronological 2-second frame samples, targeted sub-second sequences, and source-owner audit. Cole invulnerability/input aiming enabled: footage does not prove dodge difficulty or player lethality.',reference='https://youtu.be/1oj6zi1ZfNw?t=172',issues=rows)
    (OUT/'findings.json').write_text(json.dumps(data,indent=2),encoding='utf8')
    qa=ROOT/'docs/qa/furious_789_review_1025.json';qa.parent.mkdir(exist_ok=True)
    qa.write_text(json.dumps(data,indent=2),encoding='utf8')
    text=['# Furious Stage 7, 8 and 9 review — October 25','',data['timeBasis'],'',data['method'],'','Reference inspected: [Raiden II, 02:52](https://youtu.be/1oj6zi1ZfNw?t=172). Its useful motion cues are planted feet, bent-knee recovery, alternating support and a stable body heading. Preserve the Warden\'s own authored armor and anatomy.','']
    for s in (7,8,9):
        text+= [f'## Stage {s}','','| MP4 time | Priority / area | Observation and disposition |','|---|---|---|']
        for q in rows:
            if q['stage']==s:text.append(f"| {fmt(q['start'])}–{fmt(q['end'])} | {q['priority']} · {q['category']} | {q['finding']} **{q['status']}** |")
        text.append('')
    text+=['## Interpretation and scope','','The protected opening dialogue, portal entrance, symbiote rebirth, final-arena monologue, disabled Stage9 sentinel, hidden twin health and debug boss-mode exit are authored behavior. Do not report them as broken combat. The late bot\'s occasional missed targeting and weapon pickups are recording conditions. No browser/console or asset failures occurred in the three captures.','','Mike explicitly authorized analysis and implementation in this pass. The requested Warden gait and Dracodia first-host/background/ball/rebirth revisions are the implementation scope. Later copied-form choreography and Stage9 presentation proposals remain documented follow-ups.','','Original recordings are preserved under `_shots/furious_789_1025/`; the local review includes clickable findings. Implementation and native verification are tracked in `docs/STAGE78_REVIEW_1025.md`.','']
    (ROOT/'docs/FURIOUS_789_REVIEW_1025.md').write_text('\n'.join(text),encoding='utf8')
    print(json.dumps({'findings':len(rows),'report':'docs/FURIOUS_789_REVIEW_1025.md'}))
if __name__=='__main__':main()
