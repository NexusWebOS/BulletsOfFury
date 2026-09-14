from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_solid_0914';D=R/'docs'
s=(O/'suite_final.log').read_text(encoding='utf-8');assert 'FAILED —'in s
fail=[x.strip()for x in s[s.index('FAILED —'):].splitlines()if'ASSERT FAIL:'in x]
base=json.loads((D/'qa/furyship_live_0914.json').read_text(encoding='utf-8'))['suite']['failureNames']
passed=len(re.findall(r'^  ok  ',s,re.M));assert passed==3849 and len(fail)==61 and set(fail)==set(base)
n=json.loads((O/'native.json').read_text());a=json.loads((O/'part_audit.json').read_text())
assert len(n['checks'])==17 and all(x['pass']for x in n['checks'])and not n['errors']
g=(R/'assets/game.js').read_bytes();t=(R/'_BUILD_SOURCE/test_fl.js').read_bytes();sha=hashlib.sha256(g).hexdigest()
assert sha==n['runtimeSha256']and b'\r\n'not in g and t==(O/'test.before.js').read_bytes()
assert b'\n'not in t.replace(b'\r\n',b'')
movie=Path(n['video']);assert movie.is_file()and n['fullDecodeExitCode']==0
proof={'runtimeSha256':sha,'suite':{'passed':passed,'failed':len(fail),'exitCode':1,'finalSummaryReached':True,'failureNames':fail,'newFailingAssertionNames':[],'baseline':'docs/qa/furyship_live_0914.json','testFileUnchanged':True},'native':{k:v for k,v in n.items()if k!='timeline'},'partAudit':a,'timelineSamples':n['timeline'][::90],'videoSha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'lineEndings':{'runtime':'LF','suite':'CRLF'}}
(D/'qa/furyship_solid_assembly_0914.json').write_text(json.dumps(proof,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=D/'REQUEST_CHECKLIST_0914.json';data=json.loads(p.read_text(encoding='utf-8'))
for x in data['items']:
 if x['id']=='SPACE-12':
  x['request']='New ship and flight reels integrated. Twelve large solid top-view components rise from below individually with sound, then rotate and orbit without fades or mirrored perspective tricks. Remaining: flight-reel silhouette/wingspan consistency and exact final component fit.';x['evidence']='FURYSHIP_SOLID_ASSEMBLY_0914.md'
 if x['id']=='SPACE-13':
  x['request']='Intro sustains 1,000 px/s vertical travel through a finite cloud deck and clearing. Travelling top/bottom caps removed; fixed side banks remain. Compact assembly energy, full white reveal, speed effects and animated exhaust integrated.';x['evidence']='FURYSHIP_SOLID_ASSEMBLY_0914.md'
data['latestBatch']={'description':'Removed part fades/perspective flipping; twelve solid top-view pieces arrive from below one at a time with individual sounds, then rotate in evenly spaced orbits. Increased intro speed to 1,000 px/s; removed repeating top/bottom cloud caps. Native 17/0; suite 3,849/61 (exit 1, exact baseline failure names); 26-second gameplay video with sound.','evidence':'FURYSHIP_SOLID_ASSEMBLY_0914.md','completed':[]}
p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
note='''

## Codex update — September 14: solid parts, individual arrivals and faster sky

Mike rejected part fades, perspective flips and travelling top/bottom clouds. Read docs/FURYSHIP_SOLID_ASSEMBLY_0914.md and docs/qa/furyship_solid_assembly_0914.json. Parts now use opaque top plates only, rotated in evenly spaced orbits. Twelve individual bottom entrances begin in the cloud section, 0.54s apart, each with the new game-engine furyPartArrival sound. Incoming kit draws above clouds, plane beneath the holes. Entire kit stays opaque until the full white transition hides the completed-hull substitution. No per-part fade or mirrored transform. Side banks hold fixed positions; the central cloud deck passes once and does not wrap. Intro speed 1,000px/s, no braking. Flight roll/somersault frames unchanged.

Native full-launch checks 17/0, actual draw opacity/key/transform and twelve sound-cue timing audit passed; zero page/console/loop errors. Video _shots/furyship_solid_0914/BulletsOfFury_Solid_Assembly_0914.mp4 (26 seconds, game sound, full decode passed). Full suite 3,849/61 exit1, final summary, exact failure names from furyship_live_0914 baseline. Historical random sand-tank assertion failed. Test file unchanged; LF/CRLF preserved. Runtime SHA256 5150c9c4134da494bec2d2789b9e7fecfd4c022f8647302a470945f4072109b5. Sources _BUILD_SOURCE/furyship_solid_0914. Do not reapply old integrators over this build.

Checklist remains 51 complete / 11 partial / 73 pending. SPACE-12's assembly perspective blending is superseded by the opaque top-view rotation requirement; flight silhouette consistency and exact fit remain. No new bitmap/atlas/manifest changes, commit, push, user-data deletion or automation.
'''
for p in [R/'CLAUDE.md',R/'HANDOFF_CODEX.md']:
 b=p.read_bytes()
 if b'solid parts, individual arrivals and faster sky'not in b:
  nl='\r\n'if b'\r\n'in b else'\n';p.write_bytes(b+note.replace('\n',nl).encode('utf-8'))
p=D/'FURYSHIP_CLOUD_INTRO_0914.md';s=p.read_text(encoding='utf-8')
if '## Later solid-assembly revision'not in s:p.write_text(s+'\n\n## Later solid-assembly revision\n\nThe current faster intro, opaque top-view parts, individual bottom entrances and removal of travelling cloud caps are documented in [FURYSHIP_SOLID_ASSEMBLY_0914.md](FURYSHIP_SOLID_ASSEMBLY_0914.md).\n',encoding='utf-8')
print('Verified native 17/0; suite 3849/61 exit1, no new failures;',sha)
