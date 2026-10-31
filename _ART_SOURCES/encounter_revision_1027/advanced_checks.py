from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html?debug=1',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF)
  p.evaluate('run.stage=7;stageLoadBegin(7)');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=180000)
  out=p.evaluate('''()=>{
   const checks={},data={};function ok(k,v){checks[k]=(checks[k]??true)&&!!v;}
   function spawn(ng=false){diffKey='furious';debugStartFight({stage:7,role:'boss',kind:'sludgeemperor'},{pilot:'cole'});run.ngplus=ng;spawnBoss('sludgeemperor');s7mInit(boss);return boss;}
   let b=spawn(false),M=b._s7mod,normal={core:M.coreMax,shield:M.shieldMax,total:b.maxhp,cans:M.er28Canisters.map(c=>c.max)};
   b=spawn(true);M=b._s7mod;ng27Health(b);ng27Health(M);const plus={core:M.coreMax,shield:M.shieldMax,total:b.maxhp,cans:M.er28Canisters.map(c=>c.max)};
   data.health={normal,plus};ok('canister-budget-not-duplicated',Math.abs(plus.cans.reduce((s,v)=>s+v,0)-plus.shield)<.01);ok('ngplus-canisters-scale-once',plus.cans.every((v,i)=>Math.abs(v-normal.cans[i]*1.25)<.01));ok('ngplus-total-hp25',Math.abs(plus.total-normal.total*1.25)<1);
   run.ngplus=false;s7mSet(b,'er28-guns');M.t=M.warn+.1;M.er28.cd=.5;const list=ng27Clocks(b),old=M.er28.cd;s7mTick(b,1/60);const native=old-M.er28.cd;ng27Advance(list);ok('ngplus-ias15-once',Math.abs((old-M.er28.cd)/native-1.15)<.001);
   const c=M.er28Canisters[0],hp=c.hp;s7mHit(b,10,0,0,c.id);const pulse=c.flash;for(let i=0;i<30;i++)s7mTick(b,1/60);ok('canister-local-hit-flash-expires',pulse>0&&c.flash===0&&c.hp===hp-10);
   M.parts.forEach(p=>{if(p.id.startsWith('front')||p.id.startsWith('rear'))p.hp=0;});M.er28Canisters.forEach(c=>s7mHit(b,c.hp+1,0,0,c.id));s7mSet(b,'er28-bounce');
   let worst=0,px=b.x,py=b.y,landings=0;for(let i=0;i<240;i++){s7mTick(b,1/60);worst=Math.max(worst,Math.hypot(b.x-px,b.y-py));if(M.height<.01){landings++;ok('landings-stay-in-middle',Math.abs(b.x-worldWidth()/2)<1);}px=b.x;py=b.y;}data.maxBounceStep=worst;ok('continuous-bounce-no-ground-teleport',worst<22);
   // A normal stage keeps its original timed arrival and route sequence.
   run.stage=6;boss=null;subBoss=null;bossActive=subBossActive=bossDefeated=false;debugFight=null;subBossDone=false;s6Opening=null;s6WingInit();stageTimer=13;s6WingTick(1/60);ok('normal-stage-before-arrival',s6Wing.beats===0);stageTimer=14;s6WingTick(1/60);ok('normal-stage-first-arrival14',s6Wing.beats===1);subBossDone=true;stageTimer=41;s6WingTick(1/60);ok('normal-stage-second-arrival41',s6Wing.beats===2);stageTimer=52;s6WingTick(1/60);ok('normal-stage-full-wing52',s6Wing.all);
   return{checks,data};
  }''')
  b.close()
finally:stop()
out['errors']=errors;out['checks']['noRuntimeErrors']=not errors;(W/'advanced-checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
