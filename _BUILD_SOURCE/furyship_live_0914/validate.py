"""Save measured suite/native/video evidence without hiding the inherited red suite."""
from pathlib import Path
import json,re,hashlib,collections
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_live_0914'
s=(O/'suite_final.log').read_text(encoding='utf-8');assert 'FAILED —' in s
fails=[x.strip()for x in s[s.index('FAILED —'):].splitlines()if 'ASSERT FAIL:'in x]
baseline=json.loads((R/'docs/qa/supply_audit_0914.json').read_text())['suite']['failureNames']
passed=len(re.findall(r'^  ok  ',s,re.M));assert passed==3849 and len(fails)==61
new=sorted(set(fails)-set(baseline));missing=sorted(set(baseline)-set(fails));assert not new and not missing
native=json.loads((O/'native.json').read_text());assert len(native['checks'])==26 and all(x['pass']for x in native['checks'])and not native['errors']
runtime=(R/'assets/game.js').read_bytes();tests=(R/'_BUILD_SOURCE/test_fl.js').read_bytes();sha=hashlib.sha256(runtime).hexdigest()
assert native['runtimeSha256']==sha
assert b'\r\n'not in runtime and b'\n'not in tests.replace(b'\r\n',b'')
video=json.loads((O/'video/report.json').read_text());assert video['runtimeSha256']==sha and len(video['takes'])==2
assert sum(x['seconds']for x in video['takes'])==26
assert all(not x['audio']['errs']and 0<x['audio']['exportPeak']<=.85 for x in video['takes'])
movie=O/'video/BulletsOfFury_Furyship_0914.mp4';assert movie.stat().st_size>1000000
out={'runtimeSha256':sha,'testSha256':hashlib.sha256(tests).hexdigest(),
 'suite':{'passed':passed,'failed':len(fails),'exitCode':1,'finalSummaryReached':True,'section309Passed':10,'failureNames':fails,'newFailingAssertionNames':new,'missingBaselineFailureNames':missing,'baseline':'docs/qa/supply_audit_0914.json'},
 'native':native,'video':{**video,'file':str(movie.relative_to(R)).replace('\\','/'),'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'fullDecodeExitCode':0},
 'lineEndings':{'runtime':'LF','suite':'CRLF'},
 'limits':['Native fixture skips completed HQ reading and boss entrance; invincibility is capture-only. This is visual integration proof, not a full balance run.','Generated somersault wingspan still varies 98-112 pixels versus 90 for the approved base. Component view blends and final socket silhouette remain refinement work.','Video sound effects follow the captured game event log; constant export gain controls peaks. Runtime audio mix is unchanged.','Other unfinished encounter, asset and achievement work remains in the request checklist.']}
(R/'docs/qa/furyship_live_0914.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Suite',passed,'passed /',len(fails),'baseline failures (exit 1); native 26/0; video 26 seconds; matching runtime',sha)
