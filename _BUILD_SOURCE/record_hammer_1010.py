"""Save measured Hammer QA and a guide drop, without touching staged work."""
from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'_shots/hammer_1010'
native=json.loads((out/'report.json').read_text())
log=(out/'regression_final.log').read_text()
assert native['fail']==0 and not native['errors']
assert '==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in log
count=len(re.findall(r'^  ok ',log,re.M))
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
report={
 'date':'2026-10-10','baseRevision':revision,'scope':'Hammer background dive, committed jump, absorptive Chromium and authored shield/core/side swing/spike frames',
 'syntax':{'assets/game.js':'pass','assets/hammer_1010.js':'pass','assets/furious_review_0927.js':'pass','assets/gameplay_repair_1004.js':'pass'},
 'regression':{'command':'node _BUILD_SOURCE/test_fl.js','pass':count,'fail':0,'exitCode':0,'finalSummary':'FALVA/LIZZIE BUILD OK, 0 ERRORS','preHammerBaseline':8079,'addedAssertions':count-8079},
 'native':{'command':'python _BUILD_SOURCE/probe_hammer_1010.py','pass':native['pass'],'fail':native['fail'],'exitCode':0,'errors':native['errors'],'checks':native['checks'],'screenshots':native['screenshots'],'videos':native['videos']},
 'art':{'mode':'built-in image_gen edit','frames':96,'banks':6,'framesPerBank':16,'owner':'_BUILD_SOURCE/build_hammer_1010.py','prompts':'_ART_SOURCES/hammer_1010/prompts.json','provenance':'_ART_SOURCES/hammer_1010/generation_manifest.json','registration':'_ART_SOURCES/hammer_1010/registration.json','shippingManifest':'assets/game/levels/stage_05/boss/hammer_1010/manifest.json','evenFixedCanvases':True,'atlasChanges':False},
 'review':'_shots/hammer_1010/review.html',
 'visualReview':'All native contact sheets reviewed. Complete head/two arms, full feet/hammer, no neighboring poses in left cuts, corrected reactor pivots and common body scale. Formation, both releases, orbital depth and spikes inspected in timed native gameplay captures.',
 'limitations':['Protected captures verify behavior and pixels, not a human campaign clear or difficulty balance.'],
 'publication':'Local working tree only; pre-existing staged guide changes preserved.'
}
(ROOT/'docs/qa/hammer_1010.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
entry=f'''# 2026-10-10 - LOCAL: Hammer depth, commitment and Chromium

Mike requested depth-safe background dives, committed jump strikes, absorptive
Chromium and Neo Geo shield/core/spike/side swing animation. Player contact now
uses the drawn orbital scale; early descent cannot collide before scale 1.
Missiles no longer cancel/reflect the dive. Hammer depletion and the 8% emergency
reserve wait for the strike; the reserve still restores 38% then resumes rage.
Chromium body shots are absorbed with no hostile copies; the exposed healing
hammer and break/stun windows remain. Six built-in image_gen banks add 96 actual
frames (16 each), even fixed canvases and measured chest/hammer/foot pivots.
Complete heads and two arms; generated wall shatter and independently animated
reactor through hit flashes. Owning builder: _BUILD_SOURCE/build_hammer_1010.py;
runtime: assets/hammer_1010.js, loaded after existing incoming/siege layers.
Full suite {count:,}/0, final summary, exit 0; native {native['pass']}/0 including keyboard
BOSS5, four difficulties, live contact/armor, commitment, recovery, wall shatter
and hit-flash core. Zero page/console/asset errors. Native pixels/timed clips
inspected; protected fixtures do not establish human-clear balance. See
[the drop](docs/HAMMER_1010.md), [QA](docs/qa/hammer_1010.json) and
_shots/hammer_1010/review.html. Existing staged/untracked work preserved.
Local only; no commit/push.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=ROOT/name;s=p.read_bytes();anchor=b'# 2026-10-10 - GitHub 7539951 merged with local siege tanks'
 assert s.count(anchor)==1
 heading=b'# 2026-10-10 - LOCAL: Hammer depth, commitment and Chromium'
 if heading in s:
  start=s.index(heading);end=s.index(anchor,start);p.write_bytes(s[:start]+entry.encode()+s[end:])
 else:p.write_bytes(s.replace(anchor,entry.encode()+anchor,1))
print(f'Saved QA and local guide drop: {count} regression / {native["pass"]} native passes.')
