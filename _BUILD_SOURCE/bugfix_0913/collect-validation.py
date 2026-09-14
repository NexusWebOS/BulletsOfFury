"""Save regression comparison, before/after browser evidence and native encounter results."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[2];out=root/'_shots/game_bugfix_0913'
log=(out/'test_fl.log').read_text(encoding='utf-8-sig')
assert '=== 297.'in log and '============================================'in log,'suite did not finish'
fail=[s.strip()for s in log.splitlines()if s.strip().startswith('ASSERT FAIL:')]
baseline=json.loads((root/'docs/qa/tempest_return_0913.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s.strip())
new=[s for s in fail if norm(s)not in {norm(s)for s in baseline['suite']['failureNames']}]
before=json.loads((out/'before/results.json').read_text(encoding='utf-8'))
after=json.loads((out/'after/results.json').read_text(encoding='utf-8'))
rz=(out/'razorback.log').read_text(encoding='utf-8-sig')
assert '19 ok / 0 fail'in rz and 'page errors ('not in rz,'Razorback native probe did not pass'
assert all(c['pass']for c in before['checks']) and not before['errors'],'baseline reproduction failed'
assert all(c['pass']for c in after['checks']) and not after['errors'],'after-change verification failed'
prehash=hashlib.sha256((out/'game.before.js').read_bytes()).hexdigest()
assert prehash==baseline['files'][0]['sha256'],'before snapshot differs from previous validated runtime'
unit_section=log[log.index('=== 297.'):log.index('============================================',log.index('=== 297.'))]
report={'date':'2026-09-13','suite':{'passed':sum(s.startswith('  ok  ')for s in log.splitlines()),
  'failed':len(fail),'exitCode':int(bool(fail)),'newFailureNames':new,'failureNames':fail,
  'newAssertionsPassed':sum(s.startswith('  ok  ')for s in unit_section.splitlines()),
  'baseline':'docs/qa/tempest_return_0913.json','log':'_shots/game_bugfix_0913/test_fl.log'},
  'beforeSnapshot':{'path':'_shots/game_bugfix_0913/game.before.js','sha256':prehash},
  'beforeBrowser':before,'afterBrowser':after,
  'nativeRazorback':{'passed':19,'failed':0,'pageConsoleErrors':0,'log':'_shots/game_bugfix_0913/razorback.log'},
  'files':[{'path':str(p.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    for p in [root/'assets/game.js',root/'_BUILD_SOURCE/test_fl.js',root/'_BUILD_SOURCE/bugfix_0913/beam.js',root/'_BUILD_SOURCE/tempest_source_0913/fighter.js',root/'_BUILD_SOURCE/tempest_source_0913/adapter.js']],
  'screenshots':'_shots/game_bugfix_0913/after/contact.png','audio':'_shots/game_bugfix_0913/after/cole_three_nukes.wav'}
(root/'docs/qa/game_bugfix_0913.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'suitePassed':report['suite']['passed'],'suiteFailed':len(fail),'newFailureNames':new,
  'newAssertionsPassed':report['suite']['newAssertionsPassed'],'browserChecksPassed':len(after['checks'])+19,
  'nuclearImpactsBefore':[e['accepted']for e in before['details']['nukes']],
  'nuclearImpactsAfter':[e['accepted']for e in after['details']['nukes']],
  'audio':after['details']['audio']},indent=2))
