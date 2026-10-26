from pathlib import Path
import json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/beta_priorities_1024';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(n,ok,data=None):
 checks.append(dict(name=n,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?debug=1');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for route in ['left','right']:
   row=p.evaluate("""route=>{run.mode='campaign';run.stage=6;run.score=100;campaign.rank={};campaign.unlockedMax=6;campaign.stageX1004=null;delete run._gp4StageX;P2M.active=null;s6WingInit();s6Wing.route=route;setState(GS.STAGECLEAR);const R={bonus:123,rank:'A'};scLeaveStage(R);if(BOFCinematicDirector.active)BOFCinematicDirector.finish();const snap=Rival24.save();window.clear24=R;return{state,stage:run.stage,score:run.score,route:campaign.stageX1004,focus:CF4.focus,flight:CF4.flight,snap,auto:campReadAuto()};}""",route)
   ck('Stage6 '+route+' offers opposite pursuit before Stage7',row['stage']==6 and row['state']=='stagesel' and row['focus'] and row['route']['route']!=route,row)
   ck('Pending pursuit survives save/load '+route,p.evaluate("s=>{Rival24.load(s);return !!cf4Pending()&&CF4.flight>=3.2}",row['snap']))
   p.evaluate("saved=>{campApply(saved);openStageSelect(7,{})}",row['auto'])
   p.wait_for_function('()=>{drawStageSelect(.05);return XART.rdy(CC21_ART.key)}')
   for batch in range(12):
    p.evaluate('()=>{for(let i=0;i<15;i++){stateT+=.05;drawStageSelect(.05)}}');p.wait_for_timeout(20)
   p.screenshot(path=str(O/('offered-pursuit-'+route+'.png')))
   flow=p.evaluate("""saved=>{const before=run.score,wasStage=run.stage;run.stage=6;scLeaveStage(clear24);run.stage=wasStage;const once=run.score===before;const restored=campApply(saved);openStageSelect(7,{});const pending=cf4Pending();sselBoot=0;sselZoom=null;riftReturn=null;_selFlash=null;campPause=null;cmap2.focus='map';CF4.focus=true;map4hLeaveX();const declined=!map4hXFocused()&&cf4Pending();CF4.focus=true;CF4.flight=3.3;Input.clearTaps();Input.injectTap(keybind.fire[0]);Rival24.mapInput();const launched=run._gp4StageX===campaign.stageX1004.route;ap10StageXReward();const reward=JSON.stringify([run.lives,run.bombs,run.forgeCombos]);ap10StageXReward();const rewardOnce=reward===JSON.stringify([run.lives,run.bombs,run.forgeCombos]);scLeaveStage({bonus:0,rank:'A'});const completed=campaign.stageX1004.done;scLeaveStage({bonus:0,rank:'A'});if(BOFCinematicDirector.active)BOFCinematicDirector.finish();const revisit=campaign.stageX1004.done&&!cf4Pending();return{restored,pending,once,declined,launched,rewardOnce,completed,revisit};}""",row['auto'])
   ck('Saved pursuit can be declined and launched with native confirm '+route,all(flow.values()),flow)
   p.evaluate('BOFCinematicDirector.cancel();AP10_X.intro=null;openStageSelect(7,{});CF4.focus=true;CF4.flight=3.3;')
   p.wait_for_function('()=>{drawStageSelect(.016);return XART.rdy(CC21_ART.key)}');p.evaluate('CF4.focus=true;CF4.flight=3.3;drawStageSelect(.016)');p.screenshot(path=str(O/('pursuit-'+route+'.png')))
  row=p.evaluate("""()=>{GP4.clock=0;const b={_mr27:true,flash:0};const samples=[];for(let i=0;i<120;i++){GP4.clock=i/60;b.flash=Math.max(0,b.flash-1/60);markHit(b);samples.push(b.flash>0)}return{lit:samples.filter(Boolean).length,total:samples.length}}""")
  ck('Sustained shared hit route retains normal palette windows',25<row['lit']<85,row)
  allunits=[]
  for stage in range(1,10):
   p.evaluate("""n=>{run.stage=n;enemies=[];boss=null;subBoss=null;stageLoadBegin(n,[]);}""",stage)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
   row=p.evaluate("""()=>{const types=Object.values(BF22_ART.models).filter(m=>m.stages.includes(run.stage)).flatMap(m=>m.aliases).slice(0,4);if(!types.length)types.push('s1jet');for(const [i,type] of types.entries())spawnEnemy(type,100+i*100,200,{});const seen=[],old=fv21Frame;fv21Frame=function(n,t,x,y,size,alpha){if(n.startsWith('shield'))seen.push({size,alpha});return old.apply(this,arguments)};try{for(const e of enemies){enemyShieldEquip(e,'bubble_hex');e._esh.phase='active';e._esh.animT=1;e._drawW=e._drawH=999;drawEnemy(e);drawEnemyShieldLayer(e,true);}}finally{fv21Frame=old}return{stage:run.stage,seen,units:enemies.map(e=>({type:e.type,hull:bet24Hull(e),size:e._shield24Size,max:e._elite24Max}))}}""")
   allunits.append(row);ck('Stage '+str(stage)+' shields follow hulls',bool(row['seen']) and all(q['size']<500 and q['alpha']<=.38 for q in row['seen']),row)
  # Verify damage and the authored body pixels, with the native draw owner.
  for stage in [2,6,9]:
   p.evaluate("""n=>{beginStage(n);BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;AP10_X.intro=null;setState(GS.PLAY);boss=subBoss=null;bossActive=subBossActive=false;warnT=0;stagePlan=[];waveIdx=999;enemies=[];pBullets=[];eBullets=[];DBGT.god=true;const types=Object.values(BF22_ART.models).filter(m=>m.stages.includes(n)).flatMap(m=>m.aliases).slice(0,3);types.forEach((t,i)=>spawnEnemy(t,camLeftX()+100+i*120,210+i%2*120,{}));for(const e of enemies){enemyShieldEquip(e,'bubble_hex');e._esh.phase='active';e._esh.animT=1;e.hp*=.5;}}""",stage)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&XART.rdy(BET24_ART.frame.key)&&XART.rdy(BET24_ART.fill.key)&&Object.values(BF22_ART.models).filter(m=>m.stages.includes(run.stage)).flatMap(m=>Object.values(m.banks)).every(a=>XART.rdy(a.key))}')
   row=p.evaluate("""()=>{const seen=[],d=ctx.drawImage,get=XART.get;let tag=null;XART.get=function(key){tag=key;return get.apply(this,arguments)};ctx.drawImage=function(im,...a){if(tag==='bet24_elite_fill')seen.push(a);tag=null;return d.call(this,im,...a)};try{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}finally{ctx.drawImage=d;XART.get=get}return{seen,bars:BET24.bars,units:enemies.map(e=>({type:e.type,hp:e.hp,max:e._elite24Max,size:e._shield24Size}))}}""")
   ck('Native half-health elite fill pixels stage '+str(stage),bool(row['seen']) and all(abs(a[2]-50)<=1 for a in row['seen']),row)
   p.screenshot(path=str(O/('elites-stage-'+str(stage)+'.png')))
  ck('No page/console errors',not errors,errors);br.close()
finally:stop()
out=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors);(O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print('SUMMARY',out['passed'],out['failed']);raise SystemExit(bool(out['failed']))
