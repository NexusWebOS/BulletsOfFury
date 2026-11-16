from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/forge';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'ok':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);c=b.new_context(viewport={'width':1440,'height':1000});p=c.new_page();p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 def boot():p.goto('http://127.0.0.1:8765/index.html?release-forge=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 boot();p.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False});p.evaluate("()=>{BOFOnline.submitScore=()=>{};debugFight=null;run.mode='campaign';diffKey='hard';run.ngplus=false;run.forge={};run.forgeForms={};run.forgeElems=Object.fromEntries(Object.keys(INFUSIONS).filter(k=>k!=='dark').map(k=>[k,1]));run.wvars=[];run.loadout=[0,1,2,3,4,5];run._respecBase23=true;delete run._forgeBudget23;campaign.rank={};campaign.unlockedMax=1;campaign.stageX1004=null;campaign.cityRescue16=null;hf23Budget();}")
 for stage in range(1,10):
  q=p.evaluate("""n=>{run.stage=n;setState(GS.PLAY);const before=run.forgeCombos;setState(GS.STAGECLEAR);campaign.rank[n]='A';campaign.unlockedMax=Math.min(9,n+1);const earned=run.forgeCombos;forgeStart(()=>{});forgeStart(()=>{});const after=run.forgeCombos,el=Object.keys(INFUSIONS).filter(k=>k!=='dark'),free=[];for(const w of [0,1,2,3,4,5,6,7])for(const e of el)if(!run.forgeForms[w]?.[e])free.push([w,e]);const a=forgeCombine(...free[0]),bb=forgeCombine(...free[1]),third=forgeCombine(...free[2]);return{before,earned,after,a,b:bb,third,left:run.forgeCombos,cleared:hf23Budget().cleared.slice(),write:campWriteSlot(0),snapshot:campReadSlot(0)?.forgeCombos};}""",stage)
  ck(f'Stage{stage} clear grants exactly two combinations; repeat Forge visits grant none',q['earned']==q['before']+2 and q['after']==q['earned'],q)
  ck(f'Stage{stage} two combinations persist and the third is refused',q['a']==q['b']=='ok'and q['third']=='spent'and q['left']==q['snapshot']==0 and q['write'],q)
 # This fixture tests post-clear economy, not native boss completion.
 boot();q=p.evaluate("()=>{const s=campReadSlot(0),ok=campApply(s);ensureForgeForms();return{ok,left:run.forgeCombos,count:Object.values(run.forgeForms).reduce((n,x)=>n+Object.keys(x).length,0),cleared:hf23Budget().cleared,levels:[...new Set(Object.values(run.forgeForms).flatMap(x=>Object.values(x).map(q=>q.lv)))]};}")
 ck('fresh browser load preserves all18 forged forms, zero spent balance and normalized tier1',q['ok']and q['left']==0 and q['count']==18 and q['levels']==[1]and q['cleared']==list(range(1,10)),q)
 # Native combat selection: Maverick's homing lances remain separate from Laser/Firewhip.
 p.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False})
 for pilot in p.evaluate('PILOTS.map(p=>p.key)'):
  q=p.evaluate("""pk=>{run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);PILOTMOD={...PILOTS[pilotIndex]};run.ngplus=false;run.weapon=3;run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);run.forge={};run.forgeForms={3:{fire:{elem:'fire',lv:1}}};run.wvars=[];run.infusion=null;special=null;run._primary1003b='mg';player.reset();player.fireCd=0;enemies=[];boss=subBoss=null;bossActive=subBossActive=false;pBullets=[];const selected=weaponFormSelect(3,{kind:'forge',elem:'fire'});pShoot();return{selected,variant:heldVariant(3),infusion:run.infusion?.elem,kinds:pBullets.map(b=>b.kind)};}""",pilot)
  ck(pilot+' native Firewhip selection emits Firewhip rather than the wrong primary',q['selected']=='ok'and q['variant']=='firewhip'and'firewhip'in q['kinds']and'mavlaser'not in q['kinds'],q)
 # Save no QA scores to connected leaderboards; verify readable real Forge pixels.
 p.evaluate('()=>{run.mode="campaign";forgeStart(()=>{});}')
 for i in range(20):p.evaluate(shoot.STEP,6);p.wait_for_timeout(1)
 p.screenshot(path=str(O/'forge-native.png'))
 ck('no page or console errors',not errors,errors);b.close()
(O/'report.json').write_text(json.dumps({'scope':'Prepared completed-stage checkpoints and native Forge/save/weapon-selection APIs. Does not represent nine natural boss victories or all live combat damage combinations.','checks':checks,'errors':errors},indent=2),encoding='utf8')
sys.exit(any(not q['ok']for q in checks))
