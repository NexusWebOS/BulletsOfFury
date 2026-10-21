from pathlib import Path
from PIL import Image
import json,shutil,hashlib
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent
A=R/'_ART_SOURCES/holoscan_1021';D=R/'assets/game/shared/ui/holoscan_1021';Q=R/'_shots/holoscan_1021'
for d in [A,D,Q]:d.mkdir(parents=True,exist_ok=True)
gen=Path(r'C:/Users/Mike/.codex/generated_images/01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f/exec-0debf39e-eb53-4a10-9f4f-2eef83f590f7.png')
if not gen.exists():gen=A/'empty-frame-master.png'
approved=R/'_ART_SOURCES/menu_heart_1021/concept_2.png'
if gen.resolve()!=(A/'empty-frame-master.png').resolve():shutil.copy2(gen,A/'empty-frame-master.png')
shutil.copy2(approved,A/'approved-concept-02.png')
raw=Image.open(gen).convert('RGB');ref=Image.open(approved).convert('RGB');assert raw.size==(1536,1024) and ref.size==(1519,1035),(raw.size,ref.size)
assets={}
for name,source,rect in [('frame',raw,(18,14,1518,1008)),('grid',raw,(124,178,380,434)),('floor',raw,(44,700,1494,916)),('dais',ref,(282,612,488,658))]:
 im=source.crop(rect);assert im.width%2==im.height%2==0;path=D/(name+'.webp');im.save(path,lossless=True,method=6);assets[name]=dict(path=path.relative_to(R).as_posix(),width=im.width,height=im.height,sourceRect=rect,bytes=path.stat().st_size)
for name in ['holoscan_dossier_1021.js','holoscan_dossier_1021.css']:
 source=W/name if (W/name).exists() else R/'assets'/name
 if source.resolve()!=(R/'assets'/name).resolve():shutil.copy2(source,R/'assets'/name)
p=R/'assets/instructor_bob_1020.js';s=p.read_text(encoding='utf-8')
if 'const BOB20_SPEC=' not in s:
 shutil.copy2(p,A/'previous-instructor-owner.js')
 s=s.replace('const IC20={',"const BOB20_SPEC=Object.freeze({missile:Object.freeze({hp:90,element:null}),cannon:Object.freeze({hp:110,element:null}),core:Object.freeze({hp:240,element:'ice',missileMultiplier:2})});\nconst IC20={",1)
 assert "mode==='exam'?({core:240,missile:90,cannon:110}[id])" in s
 s=s.replace("mode==='exam'?({core:240,missile:90,cannon:110}[id])","mode==='exam'?BOB20_SPEC[id].hp")
 assert "id==='core'&&G.mode==='exam'&&missile?2:1" in s
 s=s.replace("id==='core'&&G.mode==='exam'&&missile?2:1","id==='core'&&G.mode==='exam'&&missile?BOB20_SPEC.core.missileMultiplier:1")
 assert 'go=Input.menuConfirm();' in s
 s=s.replace('go=Input.menuConfirm();','go=Input.menuConfirm()||!!L._hsConfirm;L._hsConfirm=false;',1)
 p.write_text(s,encoding='utf-8',newline='\n')
p=R/'index.html';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n'
if b'holoscan_dossier_1021.css' not in b:b=b.replace(b'</head>',b'<link rel="stylesheet" href="assets/holoscan_dossier_1021.css?v=holoscan-1021-1">'+nl+b'</head>',1)
if b'holoscan_dossier_1021.js' not in b:b=b.replace(b'</body>',b'<script src="assets/holoscan_dossier_1021.js?v=holoscan-1021-1"></script>'+nl+b'</body>',1)
b=b.replace(b'assets/instructor_bob_1020.js?v=instructor-bob-fit-black-red-1020',b'assets/instructor_bob_1020.js?v=holoscan-1021-3').replace(b'holoscan-1021-1',b'holoscan-1021-3').replace(b'holoscan-1021-2',b'holoscan-1021-3')
p.write_bytes(b)
p=R/'AGENTS.md';s=p.read_text(encoding='utf-8')
old='- Five boss-preview concepts in `_shots/menu_heart_1021/review.html` await Mike’s choice; do not install an unchosen concept or copy Overdrive’s card again. Bind the chosen design to actual BOF models and live stats.'
new='- Mike selected concept02, Holoscan / Exploded View, on October21. Its live owner is `assets/holoscan_dossier_1021.js`: actual authored turntables, shared BOB20_SPEC stats, readable responsive text and native tutorial input/clocks. Preserve the selected cyan/black material, fixed frame pivots and all four part views. Do not reintroduce the Overdrive card or concept-only weapon/size statistics.'
if old in s:p.write_text(s.replace(old,new),encoding='utf-8',newline='\n')
manifest={'selectedConcept':2,'name':'Holoscan / Exploded View','source':'Built-in image_gen clean frame from approved concept; current PixelLab B.O.B. turntables reused without regeneration.','assets':assets,'runtimeBytes':sum(a['bytes'] for a in assets.values()),'newAnimationGenerations':0,'statsOwner':'BOB20_SPEC in assets/instructor_bob_1020.js','font':'Existing corrected BOF Iron Signal Bold TTF','notes':'Frame uses 72px nine-slice corners. Grid/floor/dais are authored image crops. New UI clocks are owned by the native tutorial; no extra animation loop.'}
(A/'asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(A/'request.json').write_text(json.dumps({'request':'Implement the selected Holoscan B.O.B. concept using actual modules and live statistics.','approvedReference':str(approved),'generation':'Clean empty cyan/navy pixel metal window. Remove all robots/text/cards from approved concept; retain grid/floor and frame. No new character generations.','frameMaster':str(gen)},indent=2),encoding='utf-8')
for name in ['build_holoscan_1021.py']:
 if (W/name).resolve()!=(R/'_BUILD_SOURCE'/name).resolve():shutil.copy2(W/name,R/'_BUILD_SOURCE'/name)
# The original source-rectangle observer watched only the gameplay canvas. The
# dossier now renders into its real DOM canvases; keep the same four-bank / four
# yaw assertion while observing the selected thumbnail's actual drawImage calls.
p=R/'_BUILD_SOURCE/probe_instructor_bob_1020.py';s=p.read_text(encoding='utf-8')
if 'const surface=HS21.root.querySelector' not in s:
 shutil.copy2(p,A/'previous-instructor-probe.py');start=s.index("  rotations=p.evaluate(");end=s.index("''')",start)+4;part=s[start:end]
 assert 'const calls=[],draw=ctx.drawImage;' in part
 part=part.replace('const calls=[],draw=ctx.drawImage;',"const surface=HS21.root.querySelector('[data-part=\"'+i+'\"] canvas').getContext('2d');HS21.dirty=true;const calls=[],draw=surface.drawImage;").replace('ctx.drawImage','surface.drawImage')
 s=s[:start]+part+s[end:];p.write_text(s,encoding='utf-8',newline='\n')
print(json.dumps(manifest,indent=2))
