"""Build an honest per-encounter review; never turn form visits into full clears."""
from pathlib import Path
import json,collections,csv,hashlib,html
R=Path(__file__).resolve().parents[1];D=R/'_shots/maneuver_safety_1007';Q=R/'docs/qa';Q.mkdir(exist_ok=True)
names=['baseline_a','baseline_b','native_screen','learned_screen','prepared_screen','final_a','final_b','variants','equipped','tactics','tactics_ram_candidate','tactics_ram_final_candidate','tactics_after','release_affected']
groups={}
for name in names:
 p=D/name/'report.json'
 if p.exists():
  d=json.loads(p.read_text(encoding='utf-8'));groups[name]={'runs':[{k:q[k] for k in ['c','t','outcome','alive','deaths','lives','initialHP','remainingHP','pools','peakBullets','rolls','flips','hits','diagnostics'] if k in q} for q in d['runs']],'errors':d['errors'],'candidateOverlay':d.get('candidateOverlay'),'runtimeSHA256':d.get('runtimeSHA256')}
def runkey(c):
 return 'FULLFINAL' if c.get('sequence') else ('STAGE'+str(c['stage'])) if c.get('fullStage') else c.get('variant') or c.get('code')
# Replace the affected broad-screen rows with the same profile on the final build.
rechecked={(runkey(r['c']),r['c']['diff']) for r in groups.get('release_affected',{}).get('runs',[])}
rows={}
for group in ['final_a','final_b','variants','release_affected']:
 for r in groups.get(group,{}).get('runs',[]):
  c=r['c'];key=runkey(c)
  if group in ['final_a','final_b'] and (key,c['diff']) in rechecked:continue
  row=rows.setdefault(key,{'key':key,'stage':c['stage'],'scope':'complete stage' if c.get('fullStage') else 'complete finale' if c.get('sequence') else 'carrier phase' if c.get('variant')=='harrier' else 'form/phase visit' if c.get('form') is not None else 'encounter','difficulties':{}})
  a=row['difficulties'].setdefault(c['diff'],{'trials':0,'clears':0,'visitsSurvived':0,'timeouts':0,'deaths':0,'outcomes':[],'source':group})
  clear=r['outcome'] in ['encounter-defeated','phase-depleted','stageclear','flyover','victory']
  # The carrier zero-HP trigger precedes the ace. This is only its carrier phase.
  if key=='harrier':clear=r['outcome']=='encounter-defeated'
  # Warden's completed death/portal sequence hands Stage 7 to Stage 8's entry.
  if c.get('fullStage') and c['stage']==7 and r['outcome']=='warpentry':clear=True
  # A sequence is complete only once all pools are empty or the finale truly ends.
  if c.get('sequence'):clear=r['outcome'] in ['stageclear','flyover','victory'] or (r['outcome'] in ['encounter-defeated','phase-depleted'] and r.get('pools') and all(x<=0 for x in r['pools']['hp']))
  alive=r.get('alive',False);clear=bool(clear and alive)
  survived=alive and (clear or r['outcome']=='form-transition')
  a['trials']+=1;a['clears']+=clear;a['visitsSurvived']+=survived;a['timeouts']+=r['outcome']=='time-limit';a['deaths']+=r['deaths'];a['outcomes'].append(r['outcome'])
def row_order(item):
 r=item[1];k=r['key']
 forms=['HOST8','HELI8','FURN8','CRYO8','STORM8','KNIGHT','ACE8','WARD8','HAMR8']
 rank=0 if k.startswith('STAGE') else 1 if k.startswith('MINI') else 2 if k.startswith('ALT') else 3 if k.startswith('BOSS') else 4 if k in ['harrier','ace'] else 5 if k in ['FINAL1','FINAL2','FINAL3'] else 6 if k in forms else 7
 return (r['stage'],rank,forms.index(k) if k in forms else k)
rows=dict(sorted(rows.items(),key=row_order))
for row in rows.values():
 for a in row['difficulties'].values():a['clearPercent']=round(100*a['clears']/a['trials'],1);a['visitSurvivalPercent']=round(100*a['visitsSurvived']/a['trials'],1)
metrics={}
for name in ['warning_before','warning_after','warning_final','clock','clock_final','ram_before','ram_candidate','ram_render_candidate','ram_after']:
 p=D/name/'report.json'
 if p.exists():metrics[name]=json.loads(p.read_text(encoding='utf-8'))
payload={'status':'Human survival and learning targets are not certified. Zero-clear screens remain open findings.','method':'One seed per difficulty, unboosted Juggernaut, level III primary, 250 ms observation delay, 10 Hz decisions, 60 Hz simulation and 10 Hz drawing; real stock, deaths and weapon loss. Variants use two seeds. The broad screen includes the clock/ground-warning fixes; Stage 4, its boss and the Sovereign copy were repeated after the ram fix. Full Stage 8/finale results retain the earlier ram build. Simulated replay percentages are not human survival probabilities.','groups':groups,'matrix':list(rows.values()),'mechanical':metrics,'runtimeSHA256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'assets/game.js',R/'assets/maneuver_safety_1007.js',R/'assets/feedback_1002.js',R/'assets/encounters_0926.js',R/'index.html']}}
(Q/'maneuver_safety_1007.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
with (Q/'maneuver_safety_1007_matrix.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['encounter','stage','scope','difficulty','clears','trials','clear_percent','visit_survivals','visit_survival_percent','deaths','outcomes','source_group'])
 for row in rows.values():
  for diff,a in row['difficulties'].items():w.writerow([row['key'],row['stage'],row['scope'],diff,a['clears'],a['trials'],a['clearPercent'],a['visitsSurvived'],a['visitSurvivalPercent'],a['deaths'],' / '.join(a['outcomes']),a['source']])
table=['| Encounter | Scope | Easy | Normal | Hard | Furious |','|---|---|---:|---:|---:|---:|']
for row in rows.values():
 cells=[]
 for diff in ['easy','normal','hard','furious']:
  a=row['difficulties'].get(diff);cells.append('pending' if not a else f"{a['clearPercent']:g}% ({a['clears']}/{a['trials']})"+(' + visit survived' if a['visitsSurvived']>a['clears'] else ''))
 table.append('| '+row['key']+' | '+row['scope']+' | '+' | '.join(cells)+' |')
(Q/'maneuver_safety_1007_matrix.md').write_text('# Measured replay completion rates\n\n'+payload['method']+'\n\nForm transitions are surviving a visit, not clearing that form pool or the complete finale. Carrier is the hull phase only. Full-stage flyover is the post-boss exit; Stage 7 warpentry follows the defeated Warden into Stage 8.\n\n'+'\n'.join(table)+'\n',encoding='utf-8')
human=[]
for row in rows.values():
 for diff in ['easy','normal','hard','furious']:
  for attempt in [1,2,3]:human.append([row['key'],row['scope'],diff,attempt,'','','','','','','','','','',''])
with (Q/'maneuver_human_trials_1007.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['encounter','scope','difficulty','attempt','player_id','experience','pilot','weapon_and_level','speed_level','clear_yes_no','deaths','tell_understood_1_to_5','fairness_1_to_5','reward_1_to_5','notes']);w.writerows(human)
page='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BOF maneuverability review</title><style>
body{font:16px/1.55 system-ui;margin:0;background:#0d131c;color:#eaf0fa}main{max-width:1250px;margin:auto;padding:32px}h1{font-size:32px;margin:0}p{max-width:1000px;color:#bdcadb}a{color:#88d8ff}button,select{font:inherit;background:#19293c;color:white;padding:9px;border:1px solid #56718d;border-radius:6px}table{width:100%;border-collapse:collapse;margin-top:20px}th,td{text-align:left;padding:12px;border-bottom:1px solid #28394d}th{position:sticky;top:0;background:#192333}td small{display:block;color:#bdcadb}.bad{color:#ffac97}.good{color:#98e5b6}.visit{color:#f5d487}.cards{display:flex;gap:16px;flex-wrap:wrap;margin:24px 0}.card{background:#192333;padding:18px;border-radius:10px;min-width:180px}.card strong{display:block;font-size:24px}details{margin:22px 0;background:#192333;padding:16px;border-radius:8px}pre{white-space:pre-wrap;font:13px/1.5 monospace}footer{margin:32px 0;color:#a6b5c8}.scroll{overflow:auto}</style><main>
<h1>Bullets of Fury · maneuverability review</h1><p>Mechanical safety checks and real-engine scripted attempts across Easy, Normal, Hard and Furious. <b>Balance is not signed off:</b> several encounters still have zero clears in these screens. Human learning, enjoyment and win rates remain unmeasured.</p>
<div class="cards"><div class="card"><strong>180 / 180</strong>Delayed ground-warning escapes</div><div class="card"><strong>24 / 24</strong>Delayed Stage 4 ram escapes</div><div class="card"><strong>47 / 47</strong>Browser timing / input checks</div></div>
<p>Percentages below mean completed scripted replays, with the sample size shown. A surviving form transition does not count as a clear. A single successful replay does not imply a 100% human success rate.</p>
<label>Show <select id="filter"><option value="all">All measured encounters</option><option value="red">Rows with zero clears</option><option value="stage">Complete-stage attempts</option><option value="final">Stage 8 phases and forms</option></select></label>
<div class="scroll"><table><thead><tr><th>Encounter / scope</th><th>Easy</th><th>Normal</th><th>Hard</th><th>Furious</th></tr></thead><tbody id="body"></tbody></table></div>
<details><summary>What the test pilot can and cannot do</summary><p id="method"></p><p>The pilot recognizes delayed visible bullets, warnings, beam lanes, some boss body shapes, ring arcs and pickups. It uses ordinary eight-way movement, real rolls/somersaults and limited manual missiles. It does not reproduce human pattern recognition or the complete special-ability arsenal. A zero-clear row is a review priority, not proof that a person cannot win.</p><p>Optional Stage X rematch progression, co-op and human replay improvement remain outside this pass. Stage 6 carrier-phase and blue-ace trials are listed separately.</p></details>
<details><summary>Corrections and evidence</summary><p>The combat loop uses fixed 60 Hz updates so frame-based movement and projectiles agree with second-based attack timers. Yellow ground reticles now coincide with actual aim commitment and leave reaction plus travel room. The Sovereign ram now visibly warns for its generators and swept path. All 20 centered ground-warning controls and 16 of 24 ram controls still take real damage; eight unshielded edge starts are outside the ram path.</p><p><a href="../../docs/MANEUVER_SAFETY_1007.md">Read the complete report</a> · <a href="../../docs/qa/maneuver_safety_1007_matrix.csv">Download matrix</a> · <a href="../../docs/qa/maneuver_human_trials_1007.csv">Human replay worksheet</a> · <a href="../../docs/qa/maneuver_safety_1007.json">Raw measurements</a></p></details><footer>Each difficulty keeps its authored HP, damage, rewards and resources. No invulnerability or forced boss damage is used in completion attempts.</footer></main><script>
const data=__DATA__;document.querySelector('#method').textContent=data.method;
function draw(){const value=document.querySelector('#filter').value;document.querySelector('#body').innerHTML=data.matrix.filter(r=>value==='all'||value==='red'&&Object.values(r.difficulties).some(a=>a.clears===0)||value==='stage'&&r.scope==='complete stage'||value==='final'&&r.stage===8).map(r=>'<tr><td><b>'+r.key+'</b><small>'+r.scope+'</small></td>'+['easy','normal','hard','furious'].map(d=>{const a=r.difficulties[d];if(!a)return'<td>Pending</td>';return'<td class="'+(a.clears?'good':a.visitsSurvived?'visit':'bad')+'">'+a.clearPercent+'% ('+a.clears+'/'+a.trials+')<small>'+a.deaths+' deaths'+(a.visitsSurvived>a.clears?' · survived visit':'')+'</small></td>'}).join('')+'</tr>').join('')}document.querySelector('#filter').onchange=draw;draw();
</script>'''
page=page.replace('__DATA__',json.dumps({'matrix':list(rows.values()),'method':payload['method']}).replace('<','\\u003c'))
(D/'review.html').write_text(page,encoding='utf-8')
print('Wrote',len(rows),'matrix rows; groups', {k:len(v['runs']) for k,v in groups.items()})
