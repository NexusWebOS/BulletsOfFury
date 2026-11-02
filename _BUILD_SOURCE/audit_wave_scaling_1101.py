"""Read live regular-wave plans and encounter pools before shared-rule migration."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/waves_all_1101';O.mkdir(parents=True,exist_ok=True);errors=[];rows=[]
label=sys.argv[1]if len(sys.argv)>1 else'before'
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 for stage in range(1,10):
  p.evaluate('s=>EA11.setup(s,"furious")',stage)
  q=p.evaluate('''()=>{bossWarned=false;subBossDone=subBossTriggered=aminiTriggered=true;const waves=stagePlan.map((w,i)=>({i,t:w.t,meta:Object.fromEntries(Object.entries(w).filter(([k])=>k!=='fn')),fnMeta:{...w.fn},source:String(w.fn).slice(0,300)}));return{stage:run.stage,name:curStage.name,length:curStage.length,boss:curStage.boss,mini:SUBBOSS[run.stage],waves};}''')
  q['pools']=[]
  for diff in ['normal','hard','furious']:
   for role in ['mini','boss']:
    z=p.evaluate('''q=>{diffKey=q.diff;DIFF=difficultyForRun(run.mode,diffKey);bossActive=subBossActive=false;bossWarned=false;boss=subBoss=null;story=thaw=fb2Talk=null;enemies=[];if(q.role==='mini'){const d=SUBBOSS[run.stage];if(!d)return null;spawnSubBoss(d.kind);}else spawnBoss(curStage.boss);const b=q.role==='mini'?subBoss:boss;if(!b)return null;const seen=new Set(),pools={};function visit(o,path,depth){if(!o||typeof o!=='object'||seen.has(o)||depth>6)return;seen.add(o);for(const[k,v]of Object.entries(o)){if(k.startsWith('_bof')||k==='owner'||k==='base'||k==='source')continue;const pp=path?path+'.'+k:k;if(typeof v==='number'&&Number.isFinite(v)&&/hp|maxhp|coremax|energy|shield|maxshield|armormax|gunmax/i.test(k))pools[pp]=v;else if(v&&typeof v==='object'&&!ArrayBuffer.isView(v)&&!(v instanceof HTMLCanvasElement)&&!(v instanceof HTMLImageElement))visit(v,pp,depth+1);}}visit(b,'',0);return{diff:q.diff,role:q.role,kind:b.kind,max:b.maxhp,hp:b.hp,pools};}''',dict(diff=diff,role=role))
    if z:q['pools'].append(z)
  rows.append(q);(O/('audit-'+label+'.json')).write_text(json.dumps(dict(rows=rows,errors=errors),indent=2));print('Stage',stage,q['name'],'waves',len(q['waves']),'pools',[(z['diff'],z['role'],z.get('max'))for z in q['pools']],flush=True)
 b.close()
print('Wave entries',sum(len(q['waves'])for q in rows),'errors',errors)
