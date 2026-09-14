from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[2]
out=root/'_shots/tempest_duo_0913'
log=(out/'test_fl_final.log').read_text(encoding='utf-8-sig')
assert '============================================'in log,'suite has not finished'
failure_lines=[s.strip()for s in log.splitlines()if s.strip().startswith('ASSERT FAIL:')]
base=(root/'docs/qa/codex_takeover_0913_failures.txt').read_text(encoding='utf-8-sig').splitlines()
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s.strip())
new=[s for s in failure_lines if norm(s)not in {norm(s)for s in base}]
gone=[s for s in base if norm(s)not in {norm(s)for s in failure_lines}]
probe=json.loads((out/'results.json').read_text(encoding='utf-8'))
validation={'date':'2026-09-13','suite':{'passed':sum(s.startswith('  ok  ')for s in log.splitlines()),
    'failed':len(failure_lines),'exitCode':1 if failure_lines else 0,'newFailureNames':new,
    'baselineFailureNamesNotPresent':gone,'failureNames':failure_lines},
    'browser':probe,'reviewedSourceCommit':'f936f106d85d935aaf518fbac5ab34756bc26724',
    'files':[{'path':str(p.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in [root/'assets/game.js',root/'_BUILD_SOURCE/test_fl.js',root/'assets/game/bosses/tempest/tlvb_hull.png',root/'assets/game/bosses/tempest/tlvb_hull_damaged.png']],
    'video':{'path':'_shots/tempest_duo_0913/BulletsOfFury_Stage6_TempestBrothers.mp4',
        'fps':30,'source':'real index.html renderer through Boss Mode warning/spawn route',
        'driver':'invincible pilot with real input and accelerated native hitSubBoss health gates',
        'audio':'frame-stamped game sound replay through OfflineAudioContext'}}
target=root/'docs/qa/tempest_brothers_0913.json';target.write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps({'suite':{k:v for k,v in validation['suite'].items()if k!='failureNames'},'browserPassed':sum(c['pass']for c in probe['checks']),'browserFailed':[c for c in probe['checks']if not c['pass']],'browserErrors':probe['errors']},indent=2))
