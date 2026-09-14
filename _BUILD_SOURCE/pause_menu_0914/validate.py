from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'_shots/pause_menu_0914'
log=(out/'tests.log').read_text(encoding='utf-8');assert '============================================'in log
fails=[l.strip()for l in log.splitlines()if 'ASSERT FAIL:'in l]
base=json.loads((ROOT/'docs/qa/stage_1_5_0914.json').read_text(encoding='utf-8'))['suite']['failureNames']
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s)
assert {norm(x)for x in fails}=={norm(x)for x in base},'failure names'
passed=len(re.findall(r'^  ok  ',log,re.M));assert passed==3756 and len(fails)==61,(passed,len(fails))
sec=log[log.index('=== 302.'):log.index('============================================',log.index('=== 302.'))]
assert len(re.findall(r'^  ok  ',sec,re.M))==11,'section 302'
browser=json.loads((out/'results.json').read_text(encoding='utf-8'))
assert len(browser['checks'])==14 and all(c['pass']for c in browser['checks'])and not browser['errors']and not browser['details']['error'],'browser'
art={'newBitmapAssets':False,'verification':'Existing green menu cursor and authored font inspected in native screenshots. Buttons use existing chrome drawing helpers.'}
runtime=(ROOT/'assets/game.js').read_bytes();tests=(ROOT/'_BUILD_SOURCE/test_fl.js').read_bytes()
assert runtime==(out/'game.expected.js').read_bytes(),'runtime reproduction'
assert b'\r\n'not in runtime and tests.count(b'\n')==tests.count(b'\r\n'),'line endings'
sha=lambda b:hashlib.sha256(b).hexdigest()
report={'suite':{'passed':passed,'failed':len(fails),'exitCode':1,'finalSummaryReached':True,'section302Passed':11,'baseline':'docs/qa/stage_1_5_0914.json','failureNames':fails,'newFailingAssertionNames':[],'randomBaselineNote':'Sand-tank assertion failed again after passing the preceding run; not a new regression.'},'browser':browser,'art':art,'runtime':{'sha256':sha(runtime),'beforeSha256':sha((out/'game.before.js').read_bytes()),'testSha256':sha(tests),'LF':True,'testsCRLF':True},'autosave':{'backend':'browser localStorage','names':['Autosav01.json','Autosav02.json','Autosav03.json'],'separateFromManualSlots':True,'readbackVerified':True},'pending':'Requested SpriteCook bitmap button production, missile tiers, achievements, modes and remaining encounter work remain pending.'}
(ROOT/'docs/qa/pause_menu_0914.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('3756/61 exit1; baseline names matched; section302 11/0; Chromium14/0.')
