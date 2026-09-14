from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'_shots/missile_supplies_0914'
log=(out/'tests.log').read_text(encoding='utf-8');assert '============================================'in log
fails=[l.strip()for l in log.splitlines()if 'ASSERT FAIL:'in l]
base=json.loads((ROOT/'docs/qa/stage_1_5_0914.json').read_text(encoding='utf-8'))['suite']['failureNames']
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s)
assert {norm(x)for x in fails}=={norm(x)for x in base},'failure names'
passed=len(re.findall(r'^  ok  ',log,re.M));assert passed==3745 and len(fails)==61,(passed,len(fails))
sec=log[log.index('=== 301.'):log.index('============================================',log.index('=== 301.'))]
assert len(re.findall(r'^  ok  ',sec,re.M))==12,'section 301'
browser=json.loads((out/'results.json').read_text(encoding='utf-8'))
assert len(browser['checks'])==11 and all(c['pass']for c in browser['checks'])and not browser['errors']and not browser['details']['error'],'browser'
art=json.loads((out/'inspection.json').read_text(encoding='utf-8'));assert not art['errors'],'art'
runtime=(ROOT/'assets/game.js').read_bytes();tests=(ROOT/'_BUILD_SOURCE/test_fl.js').read_bytes()
assert runtime==(out/'game.expected.js').read_bytes(),'runtime reproduction'
assert b'\r\n'not in runtime and tests.count(b'\n')==tests.count(b'\r\n'),'line endings'
sha=lambda b:hashlib.sha256(b).hexdigest()
report={'suite':{'passed':passed,'failed':len(fails),'exitCode':1,'finalSummaryReached':True,'section301Passed':12,'baseline':'docs/qa/stage_1_5_0914.json','failureNames':fails,'newFailingAssertionNames':[],'randomBaselineNote':'Sand-tank assertion failed again after passing the preceding run; not a new regression.'},'browser':browser,'art':art,'runtime':{'sha256':sha(runtime),'beforeSha256':sha((out/'game.before.js').read_bytes()),'testSha256':sha(tests),'LF':True,'testsCRLF':True},'pending':'Super/Ultra/Uber upgrades and their caps remain pending SpriteCook art; full pause menu and other overnight scope pending.'}
(ROOT/'docs/qa/missile_supplies_0914.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('3745/61 exit1; baseline names matched; section301 12/0; Chromium11/0.')
