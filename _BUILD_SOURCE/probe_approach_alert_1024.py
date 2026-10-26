from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
import json,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/critical_enemy_alert_1024';O.mkdir(exist_ok=True);port,stop=serve(str(R));checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
 for name,stage,role,natural in [('boss',5,'boss',False),('miniboss',5,'mini',False),('natural-mini',2,'mini',True),('natural-boss',5,'boss',True),('harrier',6,'boss',True)]:
  p=b.new_page(viewport={'width':1100,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(2,2);p.evaluate("([stage,role])=>{diffKey='furious';debugStartFight({stage,role,kind:role==='boss'?'hammer':'siegemaster',name:'Alert review'},{pilot:'cole'});}",[stage,role]);p.wait_for_function('XART.rdy("alert_critical_1024")',timeout=60000);p.evaluate(TRAP_RAF);p.wait_for_timeout(20)
  if natural:
   p.evaluate("""([stage,role])=>{debugFight=null;warnT=0;warnKind=null;story={lines:[['SYSTEM','STALE APPROACH TEXT']],i:0,typed:40,t:0,when:'combat'};_bossCard={lines:['STALE BOSS TITLE'],t:0};enemies=[];stagePlan=[];waveIdx=999;boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=role==='boss';subBossTriggered=role==='boss';bossWarned=role==='mini';stageTimer=role==='boss'?curStage.length+1:curStage.length*.86;mapScroll=SUBBOSS[stage]?.afterScroll||0;BOFCinematicDirector.cancel();if(stage===6){s6Opening=null;s6Wing.line=null;s6Wing.choice=false;s6Wing.route='left';s6Wing.routeFightT=99;GP4.route='left';}}""",[stage,role])
   for i in range(60):
    p.evaluate(STEP,1)
    if p.evaluate('warnT>0'):break
    p.wait_for_timeout(20)
  r=p.evaluate("()=>({warnT,warnKind,story:!!story,card:!!_bossCard})");ck(name+' native approach has no title or radio',r['warnT']>0 and r['warnKind']==('sub'if role=='mini'else'boss')and not r['story']and not r['card'],r)
  r=p.evaluate("""()=>{warnT=1.2;const calls=[],text=[],get=XART.get,draw=ctx.drawImage,fill=ctx.fillText,stroke=ctx.strokeText;let active=false;XART.get=function(k){const im=get.apply(this,arguments);if(active)calls.push(k);return im;};ctx.fillText=function(...a){if(active)text.push(a[0]);return fill.apply(this,a);};ctx.strokeText=function(...a){if(active)text.push(a[0]);return stroke.apply(this,a);};const alert=drawApproachAlert;drawApproachAlert=function(){active=true;try{return alert.apply(this,arguments);}finally{active=false;}};try{drawWorld(0);}finally{XART.get=get;ctx.drawImage=draw;ctx.fillText=fill;ctx.strokeText=stroke;drawApproachAlert=alert;}return{calls,text};}""");ck(name+' real alert draws authored sign and no added lettering',r['calls'].count('alert_critical_1024')==1 and not r['text']and'enemy_approaching'not in r['calls'],r);(O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
  # Native countdown still completes into the original encounter.
  for i in range(20):p.evaluate(STEP,6);p.wait_for_timeout(5)
  r=p.evaluate('()=>({warnT,kind:boss?.kind,mini:subBossActive,sub:!!subBoss})');ck(name+' countdown still spawns its encounter',r['warnT']<=0 and(bool(r['kind'])if role=='boss'else r['mini']or r['sub']),r);p.close()
 ck('No page or console errors',not errors,errors);b.close()
stop();out={'checks':checks,'errors':errors,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)};(O/'results.json').write_text(json.dumps(out,indent=2),encoding='utf8');raise SystemExit(0 if not out['failed']else 1)
