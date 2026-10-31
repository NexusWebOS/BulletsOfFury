from pathlib import Path
import shutil,json,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');S=R/'_ART_SOURCES/dracodia_eyes_1023';O=R/'_shots/dracodia_eyes_1023';O.mkdir(parents=True,exist_ok=True)
q=json.loads((W/'review/report.json').read_text());assert q['failed']==0 and q['passed']>=39;assert not json.loads((W/'review/record-errors.json').read_text());assert 'BUILD OK, 0 ERRORS' in(W/'core.log').read_text(encoding='utf-8')
for p in(W/'review').iterdir():
 if p.is_file():shutil.copy2(p,O/p.name)
for name in ['selection-notes.json','NOTES.md','finalize.py']:shutil.copy2(W/name,S/name)
for name in ['native','core','record']:shutil.copy2(W/(name+'.log'),O/(name+'-verified.log'))
for stem in ['probe','record']:
 text=(W/(stem+'.py')).read_text(encoding='utf-8').replace("R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=W/'review'","R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/dracodia_eyes_1023';O=R/'_shots/dracodia_eyes_1023'")
 (R/'_BUILD_SOURCE'/f'{stem}_dracodia_eyes_1023.py').write_text(text,encoding='utf-8')
# Keep the earlier broad encounter probe in step with moving, frame-measured
# eye origins. Its old invariant wrongly required static eye coordinates.
p=R/'_BUILD_SOURCE/probe_dracodia_brain_1023.py';text=p.read_text(encoding='utf-8').replace('eyes:nb23Eyes(B),sockets:sockets23','eyes:B._r30.v18.attack.eyes,liveEyes:nb23Eyes(B),sockets:sockets23').replace("row['eyes']==row['sockets']","row['eyes']==row['liveEyes']").replace('fixed eye sockets','frame-measured eye sockets');p.write_text(text,encoding='utf-8')
shutil.copy2(W/'review/report.json',R/'docs/qa/dracodia_eyes_1023.json');shutil.copy2(W/'NOTES.md',R/'docs/DRACODIA_EYES_1023.md')
note=f'''## October23 — Neural Archon face follows body, charge glow and16-frame lasers

Mike spotted a frozen rectangular eye patch. Removed the seed face paste from
all9 idle poses; whole PixelLab faces now move naturally. Each idle/charge/focus
cell has measured eyes, shared by visible laser origins and actual-pixel contact.
New PixelLab8-pose whole-brain eye/socket/brow charge,3 bright focus poses and
reverse recovery; authored white hit partners. New16-frame beam flow at24fps
through6 baked expansion widths. Warning fields sit behind the charged actor.
179 even cells/22 sheets. No runtime visual glow/tint/scale/rotation/fade added.
Cloud/geysers/timing/HP/Retina/native forms/death unchanged. Native{q['passed']}/0,
zero page/asset errors; face-source pixels compared, emitter alignment, actual
charge/beam blits, hit expiry and decoded audio verified. Focused native movie
saved. Full required core BUILD OK/0errors/actual exit0. Credits4.16->4.10USD.
Owning rebuild scripts repaired and archived. docs/DRACODIA_EYES_1023.md,
qa JSON, _shots/dracodia_eyes_1023/index.html. No commit/push.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;text=p.read_text(encoding='utf-8')
 if not text.startswith('## October23 — Neural Archon face follows body'):p.write_text(note+text,encoding='utf-8')
p=R/'assets/data/ART_TAXONOMY.json';a=json.loads(p.read_text(encoding='utf-8'));a['nb23_']['note']+='179 cells/22 sheets; final39 native checks. See docs/DRACODIA_EYES_1023.md.';p.write_text(json.dumps(a,indent=2),encoding='utf-8')
preview=Path(r'C:/Users/Mike/Documents/New project/BOF-Hammer-Tactical-1023/review')
for p in(W/'review').iterdir():
 if p.is_file():shutil.copy2(p,preview/p.name)
m=json.loads((W/'shipping/manifest.json').read_text());assert all(hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256']for s in m['sheets'].values());print(json.dumps({'checks':q['passed'],'errors':q['errors'],'cells':sum(map(len,m['banks'].values())),'sheets':len(m['sheets']),'preview':'http://127.0.0.1:53815/index.html?neural-eyes-1023'}))
