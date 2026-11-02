"""Complete coverage, actual difficulty gates, native pools and movie receipts."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_comparison_1102';out=dict(checks=[],tracks={},dracodia={},storms={})
def ck(name,passed,data=None):out['checks'].append(dict(name=name,passed=bool(passed),data=data));print('PASS'if passed else'FAIL',name,flush=True)
expected={f'stage{s}-{r}'for s in range(1,10)for r in ['mini','boss']}|{'stage6-rough-riders'}
for diff in ['normal','hard','furious']:
 state=json.loads((O/diff/'batch.json').read_text());jobs=state['jobs'];good=[j for j in jobs.values()if j.get('passed')];out['tracks'][diff]=dict(complete=len(good),seconds=sum(j.get('seconds',0)for j in good),fpsMin=min(j.get('nativeFps',0)for j in good),fpsMean=sum(j.get('nativeFps',0)for j in good)/max(1,len(good)))
 ck(diff+' has all19 complete decoded audible source-stable fights',set(jobs)==expected and len(good)==19 and all(all(j['checks'].values())for j in good))
 reports={k:json.loads((R/j['folder']/'report.json').read_text())for k,j in jobs.items()if j.get('passed')}
 ck(diff+' recordings retain native difficulty and labelled invulnerability',all(r['setup']['difficulty']==diff and r['invulnerable']and r['completed']for r in reports.values()))
 ck(diff+' every movie file and receipt exists',all((R/j['path']).is_file()and(R/j['folder']/'report.json').is_file()for j in good))
 if 'stage8-boss'in reports:
  t=reports['stage8-boss']['timeline'];forms={q['form']for q in t if q.get('phase')==2 and q.get('mode')=='fight'};rebirth=any('rebirth'in str(q.get('mode','')).lower()for q in t);unlocked=any(q.get('dracodia')and q['dracodia'].get('unlocked')for q in t);protected=[q for q in t if q.get('phase')==2 and q.get('form')==0 and q.get('mode')=='fight'and q.get('dracodia')and not q['dracodia'].get('unlocked')]
  out['dracodia'][diff]=dict(forms=sorted(forms),rebirth=rebirth,finalUnlocked=unlocked,protectedRows=len(protected));ck(diff+' Dracodia film includes native rebirth, all4copies and final body',{0,1,2,6,8}<=forms and rebirth and unlocked,out['dracodia'][diff]);ck(diff+' Dracodia protected base retains its complete pool',bool(protected)and all(abs(q['hp']-q['maxhp'])<.01 for q in protected))
 if diff=='furious':
  for key,kind in [('stage6-mini','razorwake'),('stage6-boss','thunderhead')]:
   r=reports.get(key);rows=[q for q in r['timeline']if q.get('storm')]if r else[];attacks={q['storm']['attack']for q in rows if q['storm']['phase']=='attack'};out['storms'][key]=sorted(a for a in attacks if a);ck(key+' retains actual Fury identity and complete pool',bool(r)and r['setup']['entry']['kind']==kind and all(abs(q['hp']-q['storm']['core']-sum(p['hp']for p in q['storm']['parts']))<.01 for q in rows if q.get('hp')is not None));ck(key+' shows the complete initial attack book',({'guns','pass','shear','vortex'}if key.endswith('mini')else{'guns','gates','rail','vortex','eye'})<=attacks,sorted(a for a in attacks if a))
  r=reports.get('stage7-mini');ck('Furious Stage7 film shows two independent Sumpjaw actors',bool(r)and any(q.get('sumpjaw')and len(q['sumpjaw']['actors'])==2 for q in r['timeline']))
(O/'collection-checks.json').write_text(json.dumps(out,indent=2));print('SUMMARY',sum(c['passed']for c in out['checks']),'/',len(out['checks']));sys.exit(0 if all(c['passed']for c in out['checks'])else 1)
