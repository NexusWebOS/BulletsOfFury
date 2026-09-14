from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_cloud_0914';D=R/'docs'
s=(O/'suite.log').read_text(encoding='utf-8');assert 'FAILED —'in s
fail=[x.strip()for x in s[s.index('FAILED —'):].splitlines()if'ASSERT FAIL:'in x]
baseline=json.loads((D/'qa/furyship_live_0914.json').read_text(encoding='utf-8'))['suite']['failureNames']
new=sorted(set(fail)-set(baseline));missing=sorted(set(baseline)-set(fail));passed=len(re.findall(r'^  ok  ',s,re.M))
assert passed==3850 and len(fail)==60 and not new
native=json.loads((O/'native.json').read_text());retained=json.loads((O/'retained.json').read_text())
assert len(native['checks'])==11 and all(c['pass']for c in native['checks'])and not native['errors']
assert retained['noRebuild']and retained['size']==48 and len(retained['plumes'])==2 and not retained['errors']and not retained['error']
game=(R/'assets/game.js').read_bytes();test=(R/'_BUILD_SOURCE/test_fl.js').read_bytes();sha=hashlib.sha256(game).hexdigest()
assert sha==native['runtimeSha256']==retained['runtimeSha256']
assert b'\r\n'not in game and test==(O/'test.before.js').read_bytes()
assert b'\n'not in test.replace(b'\r\n',b'')
movie=Path(native['video']);assert movie.is_file()and native['fullDecodeExitCode']==0
out={'runtimeSha256':sha,'suite':{'passed':passed,'failed':len(fail),'exitCode':1,'finalSummaryReached':True,'newFailingAssertionNames':new,'missingBaselineFailureNames':missing,'failureNames':fail,'baseline':'docs/qa/furyship_live_0914.json','testFileUnchanged':True},'native':{k:v for k,v in native.items()if k!='timeline'},'retained':retained,'timelineSamples':native['timeline'][::90],'videoSha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'lineEndings':{'runtime':'LF','suite':'CRLF'}}
(D/'qa/furyship_cloud_intro_0914.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=D/'REQUEST_CHECKLIST_0914.json';data=json.loads(p.read_text(encoding='utf-8'))
for x in data['items']:
 if x['id']=='SPACE-12':
  x['request']='New ship, 12 enlarged assembly pieces from 30 authored component views, eight roll poses and twelve somersault poses are integrated. Remaining: generated silhouette/wingspan consistency, exact component fit and smoother intermediate turns.';x['evidence']='FURYSHIP_CLOUD_INTRO_0914.md'
 if x['id']=='SPACE-13':
  x['request']='Revised intro: sustained fast sky flight, dense clouds with gaps, moving cloud-framed assembly clearing, smaller local energy effect and full white fade into the completed ship in space. Speed effects and animated thrusters integrated.';x['evidence']='FURYSHIP_CLOUD_INTRO_0914.md'
data['latestBatch']={'description':'Reworked the Stage 5 intro to twelve larger assembly pieces, extended sky/cloud travel at constant speed, a cloud clearing, smaller local fusion effects and a full white fade revealing space. Native scene 11/0 plus retained-fighter checks; full suite 3,850/60 (exit 1, no new failure names); 26-second video with game sound.','evidence':'FURYSHIP_CLOUD_INTRO_0914.md','completed':[]}
p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
note='''

## Codex update — September 14: cloud-flight intro revision

Mike rejected the small six-piece assembly and slow sweep. Read docs/FURYSHIP_CLOUD_INTRO_0914.md and docs/qa/furyship_cloud_intro_0914.json. The new Stage-5 intro now stays at 420px/s through sky, clouds, clearing, assembly, white fade and countdown. Twelve independent pieces use the existing authored kit; full-size loose cells draw at 194.7px around a 118px cinematic hull. The local energy ring is smaller. Space replaces sky only under opaque white, which also covers HQ and scanlines. Latest request explicitly supersedes the old no-fade rule for this intro. Retained new fighters skip rebuilding and stay 48px; other stages/legacy route unchanged.

Native full launch from t=0 including all HQ dialogue: 11/0; separate retained/animated-exhaust probe passed; zero page/console/loop errors. Full suite 3,850/60 exit1, final summary, no new failure names. Historical random sand-tank assertion passed; no fix claimed. Test file unchanged. Runtime SHA256 3d55604968cc2af62926ed8ef7ed296a03cf051c57d87686ad6434d9405e2978. LF/CRLF preserved. Video _shots/furyship_cloud_0914/BulletsOfFury_Cloud_Transformation_0914.mp4 (26 seconds, game sound effects, fully decoded). Sources _BUILD_SOURCE/furyship_cloud_0914; do not reapply prior integrators over this build.

Tally still 135: 51 complete / 11 partial / 73 pending. SPACE-12 retains art consistency/fit/perspective refinement; SPACE-13 evidence updated for the revised staging. No commit/push/atlas edits/user-data deletion/background automation.
'''
for p in [R/'HANDOFF_CODEX.md',R/'CLAUDE.md']:
 b=p.read_bytes()
 if b'## Codex update \xe2\x80\x94 September 14: cloud-flight intro revision'not in b:
  nl='\r\n'if b'\r\n'in b else'\n';p.write_bytes(b+note.replace('\n',nl).encode('utf-8'))
p=D/'FURYSHIP_LIVE_0914.md';s=p.read_text(encoding='utf-8')
if '## Later cloud-flight revision'not in s:p.write_text(s+'\n\n## Later cloud-flight revision\n\nMike revised the staging after reviewing this video. The current twelve-piece, sustained-speed cloud intro and full-white reveal are documented in [FURYSHIP_CLOUD_INTRO_0914.md](FURYSHIP_CLOUD_INTRO_0914.md).\n',encoding='utf-8')
print('Saved: native 11/0 + retained; suite',passed,'/',len(fail),'exit 1; no new failures;',sha)
