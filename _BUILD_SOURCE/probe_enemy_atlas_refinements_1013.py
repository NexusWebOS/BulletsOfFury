import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path(os.environ.get('BOF_ATLAS_QA_OUTPUT',str(Path(__file__).resolve().parents[1]/'_shots'/'enemy_atlas_controls_1013')));out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(channel='chrome',args=['--mute-audio']);g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)))
 g.goto('http://127.0.0.1:8767/index.html?bossmode=1&enemyAtlas=1',wait_until='load',timeout=120000);g.wait_for_function('window.BOF_ENEMY_ATLAS?.ready',timeout=60000)
 checks=[]
 storage=g.evaluate("""()=>{localStorage.setItem('atlas-ephemeral','temporary');localStorage.clear();return localStorage.getItem('atlas-ephemeral')===null;}""");checks.append(['ephemeral clear',storage])
 e={'id':'guide-replay','spawn':{'method':'enemy','type':'s1jetdelta','stage':1},'stages':[1]};g.evaluate('e=>BOF_ENEMY_ATLAS.start(e)',e);g.evaluate('BOF_ENEMY_ATLAS.mute(false)');g.wait_for_timeout(8000)
 snap=g.evaluate('BOF_ENEMY_ATLAS.snapshot()');checks.append(['automatic replay loaded',snap['actor'] is not None and not snap['error']]);checks.append(['replay retains sound',not snap['muted']]);checks.append(['replay restarted native unit',snap['elapsed']<6]);
 e={'id':'guide-carrier','spawn':{'method':'encounter','kind':'warhive','stage':6,'role':'boss'},'stages':[6]};g.evaluate('e=>BOF_ENEMY_ATLAS.start(e)',e);checks.append(['module health labelled',g.evaluate('BOF_ENEMY_ATLAS.snapshot().healthControl')==False]);
 g.evaluate('BOF_ENEMY_ATLAS.pause(true)');f=g.evaluate('BOF_ENEMY_ATLAS.snapshot().frames');g.wait_for_timeout(300);checks.append(['paused native frame remains fixed',g.evaluate('BOF_ENEMY_ATLAS.snapshot().frames')==f]);g.evaluate('BOF_ENEMY_ATLAS.step()');g.wait_for_timeout(100);checks.append(['step one native frame',g.evaluate('BOF_ENEMY_ATLAS.snapshot().frames')==f+1]);
 result={'checks':checks,'pageErrors':errors,'replay':snap};(out/'atlas_refinements_1013.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));b.close()
