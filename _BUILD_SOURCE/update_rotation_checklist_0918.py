from pathlib import Path
import json

p=Path(__file__).resolve().parents[1]/'docs/REQUEST_CHECKLIST_0914.json'
d=json.loads(p.read_text(encoding='utf-8'))
items=d['items']
by={x['id']:x for x in items}
for iid in ('S1-16','S1-17'):
    q=by[iid];q['status']='complete';q['evidence']='ROTATION_SHIELD_STAGE2_REPAIR_0918.md'
    for k in ('workOrder','difficulty','difficultyBand'):q.pop(k,None)

new=[
 {'id':'UI-24','group':'Pause, saving, title and pilot selection','status':'complete','request':'Use the graphical arcade dialogue font and letter-by-letter centered banner for item, ammunition and upgrade acquisition messages instead of basic floating text.','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md','dependency':''},
 {'id':'UI-25','group':'Pause, saving, title and pilot selection','status':'complete','request':'Replace the HP-like shield gauge with a distinct rectangular energy-shield frame, straight fill well and connected SHIELD box whose baked label is centered horizontally and vertically.','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md','dependency':''},
 {'id':'ENG-21','group':'Shared combat, warnings and targeting','status':'pending','request':'Complete a vehicle-wide authored direction-frame audit for all remaining tanks and jets; remove live canvas rotation where it produces warped or wonky turns, while retaining correct pivots, shadows and weapon mounts.','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md','dependency':'','difficulty':5,'difficultyBand':'Broad asset and engine conversion'},
 {'id':'ENG-22','group':'Shared combat, warnings and targeting','status':'complete','request':'Give pickup families authored turn strips, select frames at runtime, and remove the ugly additive glow discs from the new bombs and score bullets.','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md','dependency':''},
 {'id':'S1-19','group':'Stage 1: fodder, Razorback and jungle chopper','status':'complete','request':'Show two independent miniboss bars for the Hard Razorback Duo, one for each tank, and flash the targetable center turret during opening-phase hits.','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md','dependency':''},
 {'id':'S2-12','group':'Stage 2: lava hazards, Magma Ward and Furnace Tyrant','status':'complete','request':'Confine hostile fire geysers to the left/right lava gutters, keep them off the mountain, add dedicated warning/eruption audio, and play the firewall pass cue as it crosses the player.','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md','dependency':''},
 {'id':'S2-13','group':'Stage 2: lava hazards, Magma Ward and Furnace Tyrant','status':'complete','request':'Use individual authored direction frames for Furnace Tyrant body and destructible arm/turret states, with arm mounts locked to the boss spin angle.','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md','dependency':''},
]
for q in new:
    if q['id'] not in by:items.append(q)

pending=sorted((x for x in items if x.get('status')!='complete'),key=lambda x:x.get('workOrder',9999))
for n,q in enumerate(pending):q['workOrder']=n
d['updated']='2026-09-18'
d['latestBatch']={'description':'0918 authored pickup/Furnace turns, rectangular shield gauge, dual Razorback bars and Stage 2 fire-hazard repair','evidence':'ROTATION_SHIELD_STAGE2_REPAIR_0918.md'}
p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\r\n')
print(len(items),'items',len(pending),'pending')
