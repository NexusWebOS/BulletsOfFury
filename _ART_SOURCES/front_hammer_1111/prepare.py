from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;B=W.parent;OLD=B/'heavy_hammer_1111';R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['assets/game.js','assets/whole_hammer_1110.js','assets/boss_animation_1109.js','assets/overhead_slam_art_1111.js']
before={n:sha(R/n)for n in names};(W/'before').mkdir(exist_ok=True)
for n in names:
 if Path(n).name!='game.js':shutil.copy2(R/n,W/'before'/Path(n).name)
s=(R/'assets/whole_hammer_1110.js').read_text();assert 'const FH1111='not in s;(W/'whole_hammer_1110.js').write_text(s+(W/'runtime-front.js').read_text())
(W/'installation-plan.json').write_text(json.dumps(dict(before=before,coreUnchanged=True),indent=2))
shutil.copy2(OLD/'author.lua',W/'author.lua')
source=(R/'assets/hammer_acting_art_1021.js').read_text();d=json.JSONDecoder().raw_decode(source[source.index('{'):])[0]
evidence={n:dict(frames=len(d['banks'][n]),sheet=d['sheets'][d['banks'][n][0]['sheet']],sha=sha(R/d['sheets'][d['banks'][n][0]['sheet']]['path']))for n in ['blue_slam','blue_side','blue_slam_armor','blue_side_armor','corrupt_slam','corrupt_side']}
evidence['passwordOwner']='assets/hammer_time_0927.js HT27_BASE.hammerTick/draw; HAMA is excluded by c25Own, so its cue/dance owners remain intact.'
(W/'earlier-animation-evidence.json').write_text(json.dumps(evidence,indent=2))
for stage in [5,8]:
 s=(B/f'verify_heavy_stage{stage}.py').read_text().replace('outputs/Heavy-hammer-motion','outputs/Front-facing-hammer').replace('from heavy_record_loaded import record_loaded','from front_record_loaded import record_loaded')
 if stage==5:s=s.replace("for mat in ['regular','chrome']:","for mat in ['regular','chrome','red']:")
 (B/f'verify_front_stage{stage}.py').write_text(s)
s=(B/'heavy_record_loaded.py').read_text().replace('outputs/Heavy-hammer-motion','outputs/Front-facing-hammer').replace('reference-led heavy hammer motion','front-facing hammer motion / regular + Chromium')
(B/'front_record_loaded.py').write_text(s)
print('Prepared frontal routing; normal/Chromium/red variants, depth windups and red preload. Earlier attack provenance recorded.')
