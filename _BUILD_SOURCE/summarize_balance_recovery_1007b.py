from pathlib import Path
import json,csv,re,hashlib
R=Path(__file__).resolve().parents[1];Q=R/'_shots/maneuver_safety_1007';D=R/'docs/qa'
names={
 'tactical_before':'Paired bosses / before', 'tactical_after':'Paired bosses / after',
 'credit_stages_hard':'Equipped full stages / Hard / finite credits',
 'credit_stages_furious':'Equipped full stages / Furious / finite credits',
 'world_stage2_candidate':'Stage 2 / hazard-aware / before environmental pacing',
 'world_stage2_pacing':'Stage 2 / hazard-aware / after environmental pacing',
 'world_stage2_release':'Playable build / hazard-aware Hard Stage 2',
 'credit_bosses_release':'Playable build / slow-pilot bosses / finite credits',
 'sovereign_ram_budget':'Uninstalled helper-pause experiment / Hard and Furious',
 'finale_v3':'Historical v3 candidate / equipped full finale / starting lives',
 'finale_release':'Playable build / equipped full Easy finale / starting lives'}
rows=[];sources={}
for name,label in names.items():
 p=Q/name/'report.json'
 if not p.exists():continue
 d=json.loads(p.read_text(encoding='utf-8'))
 sources[name]={k:d.get(k) for k in ['method','browser','overlay','runtimeSHA256','errors','interrupted','sourceNote']}
 sources[name]['path']=str(p.relative_to(R))
 for q in d['runs']:
  c=q['c'];state=q.get('diagnostics',{}).get('state');pools=q.get('pools') or {};sequence=c.get('sequence',False)
  if sequence:clear=state in ['stageclear','victory'] and pools.get('encounter')==2 and len(pools.get('hp',[]))==9 and all(v<=0 for v in pools['hp'])
  elif c.get('fullStage'):clear=q['outcome'] in ['stageclear','flyover','warpentry','victory']
  else:clear=q['outcome']=='encounter-defeated'
  rows.append(dict(group=name,profile=label,id=c['id'],stage=c['stage'],difficulty=c['diff'],pilot=c['pilot'],primary=c.get('weapon',0),level=c.get('level'),speed=c.get('speed',0),seed=c['seed'],reaction=c.get('reaction'),decision=c.get('decision'),kind='full-finale' if sequence else 'full-stage' if c.get('fullStage') else 'boss',clear=clear,outcome=q['outcome'],state=state,seconds=round(q['t'],2),deaths=q['deaths'],credits_used=q.get('creditsUsed',0 if not c.get('useContinues') else None),credit_limit=q.get('creditLimit'),reserves=q['lives'],remaining_hp=round(q['remainingHP'],2) if isinstance(q['remainingHP'],(int,float)) else q['remainingHP'],mini_clears=[x['kind'] for x in q.get('milestones',[]) if x['type']=='miniboss-clear'],pools=pools))
probes={}
for n in ['whirl_comparison','final_candidate_probe2','pacing_candidate_probe','release_probe','release_firefox','release_webkit']:
 p=Q/n/'report.json'
 if p.exists():probes[n]=json.loads(p.read_text(encoding='utf-8'))
log=Q/'balance_release_suite.log';suite={}
if log.exists():
 s=log.read_text(encoding='utf-8',errors='replace');suite={'assertions':len(re.findall(r'^  ok ',s,re.M)),'finalBanner':'==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in s,'path':str(log.relative_to(R))}
runtime={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'index.html',R/'assets/game.js',R/'assets/balance_recovery_1007b.js',R/'assets/maneuver_safety_1007.js',R/'_BUILD_SOURCE/test_fl.js'] if p.exists()}
out={'scope':'Balance recovery continuation. Recorded controller attempts; not human survival estimates. Profiles and credit use remain separate.','rows':rows,'sources':sources,'native':probes,'suite':suite,'runtimeSHA256':runtime}
D.mkdir(exist_ok=True)
(D/'balance_recovery_1007b.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
fields=[k for k in rows[0] if k!='pools']
with (D/'balance_recovery_1007b.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in rows:w.writerow({k:', '.join(r[k]) if isinstance(r[k],list) else r[k] for k in fields})
md=['# Recorded balance-recovery attempts','', 'Each row is one controller attempt. Credits are spent through the real Continue screen; limits include naturally earned Continue Ups. Historical candidates and different controllers/loadouts are separate groups. Zero clears are retained.','']
for name,label in names.items():
 rs=[r for r in rows if r['group']==name]
 if not rs:continue
 md+=['## '+label,'','| Encounter | Difficulty | Clear | Time | Deaths | Continues used / available | Result |','|---|---|---:|---:|---:|---:|---|']
 for r in rs:
  credit=str(r['credits_used'])+(' / '+str(r['credit_limit']) if r['credit_limit'] is not None else '')
  md.append(f"| {r['id']} | {r['difficulty']} | {'Yes' if r['clear'] else 'No'} | {r['seconds']:.1f} s | {r['deaths']} | {credit} | {r['outcome']} |")
 md+=['',f"Observed clears: **{sum(r['clear'] for r in rs)}/{len(rs)} attempts**. This is not a human success percentage.",'']
(D/'balance_recovery_1007b_matrix.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
doc=(R/'_BUILD_SOURCE/balance_recovery_report_template_1007b.md').read_text(encoding='utf-8')
lines=[]
for group in ['tactical_before','tactical_after','credit_stages_hard','credit_stages_furious','world_stage2_candidate','world_stage2_pacing','world_stage2_release','credit_bosses_release','finale_release']:
 rs=[r for r in rows if r['group']==group]
 if not rs:continue
 clears=[f"{r['difficulty'].title()} Stage {r['stage']} ({r['kind']}, {r['credits_used']} continues)" for r in rs if r['clear']]
 lines.append(f"- **{names[group]}:** {sum(r['clear'] for r in rs)}/{len(rs)} observed clears."+(' Cleared: '+ '; '.join(clears)+'.' if clears else ' No clear was recorded.'))
if suite:lines+=['',f"Final playable-build regression: **{suite['assertions']:,} assertions**, final success banner **{'received' if suite['finalBanner'] else 'missing'}**. See the retained log and native probe results in QA JSON."]
if 'release_probe' in probes:
 p=probes['release_probe'];lines.append(f"Native playable-build verification: **{sum(bool(v) for v in p['checks'].values())}/{len(p['checks'])} checks**, **{len(p['errors'])} browser errors**.")
native_names=[n for n in ['release_probe','release_firefox','release_webkit'] if n in probes]
if len(native_names)==3:
 lines.append('Across Chromium, Firefox and WebKit: **'+str(sum(sum(bool(v) for v in probes[n]['checks'].values()) for n in native_names))+'/'+str(sum(len(probes[n]['checks']) for n in native_names))+' native checks passed**, **'+str(sum(len(probes[n]['errors']) for n in native_names))+' recorded browser errors**. This is functional verification, not an FPS benchmark.')
lines+=['','Hard/Furious encounters without clears remain open. The full-stage screens also record miniboss defeats separately in CSV/JSON; a miniboss kill does not count as a full-stage clear. Fresh repeated human attempts are still needed to establish learning and reward quality.']
doc=doc.replace('<!-- RESULTS -->','\n'.join(lines)).replace('its hull, generators and helpers remain solid and attached','its hull and surviving attachments remain solid and connected')
(R/'docs/BALANCE_RECOVERY_1007B.md').write_text(doc,encoding='utf-8',newline='\n')
print('Wrote portable evidence:',len(rows),'attempts,',len(probes),'native datasets. Suite:',suite)
