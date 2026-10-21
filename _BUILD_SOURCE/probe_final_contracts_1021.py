from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,ast,json,base64,http.server,argparse
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/final_version_1021/contracts';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
ap=argparse.ArgumentParser();ap.add_argument('--browser',default='msedge');a=ap.parse_args();checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,ok=bool(ok),data=data));(O/(a.browser+'-report.json')).write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def shot(p,name,draw='drawWorld(0)'):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);'+draw+';}');(O/(a.browser+'-'+name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=(pw.firefox.launch() if a.browser=='firefox' else pw.chromium.launch(**({'channel':a.browser} if a.browser!='chromium' else {}),args=['--autoplay-policy=no-user-gesture-required']))
  p=br.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(600,400)
  p.evaluate(SETUP,dict(stage=5,pilot='lizzie'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}')
  p.evaluate('BOFCinematicDirector.cancel();story=null;run._earnedUnlocks={chaingun:true};chaingunUnlocked=true;run._chainSeeded=true;run.loadout=[7,1,2,3,4,5,6];')
  for pilot in ['cole','axel','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:
   for weapon in range(8):
    row=p.evaluate('''([pilot,w])=>{run.pilot=pilot;run.spaceMode=true;run.dkT=run.sonicT=30;lzMount={mode:'dock',x:12,y:34};player.out=true;player._hammerEvap=10;player._spin={t:1};const live={player,bullets:pBullets,lz:lzMount,space:run.spaceMode,pilot:run.pilot};const P=forgePreviewNew(w,'fire',w===7?1:3),sides=new Set(),kinds=new Set();for(let i=0;i<240;i++){forgePreviewTick(P,260,300,1/60);for(const b of P.bullets){kinds.add(b.kind);if(b.kind==='chaingun')sides.add(b.x<VW/2?'left':'right');}if(i%30===0)forgePreviewDraw(P,20,20,260,300);}window.PR=P;return{pilot,w,error:P.err,fired:P.fired,kinds:[...kinds],sides:[...sides],restored:player===live.player&&pBullets===live.bullets&&lzMount===live.lz&&run.spaceMode===live.space&&run.pilot===live.pilot};}''',[pilot,weapon]);ck(pilot+' Forge weapon '+str(weapon),not row['error'] and row['fired']>0 and row['restored'] and bool(row['kinds']),row)
   shot(p,'forge-'+pilot,'forgePreviewDraw(PR,20,20,260,300)')
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=5,pilot='cole',kind='siegebomber',mini=True,diff=diff))
   row=p.evaluate('''()=>{B._bomber.mode='recover';const S=B._bomber;let rewards=0;const reward=continueRewardResolve;continueRewardResolve=function(o){if(o===B)rewards++;return reward.apply(this,arguments);};try{siegeBomberHit(B,S.core,NaN,NaN,'core');const coreOnly={hp:B.hp,dead:!!B.dead,live:S.parts.filter(p=>p.hp>0).length};for(const m of S.parts)siegeBomberHit(B,m.hp,NaN,NaN,m.id);siegeBomberHit(B,100,NaN,NaN,'core');return{coreOnly,dead:B.dead,hp:B.hp,rewards};}finally{continueRewardResolve=reward;}}''');ck(diff+' siege bomber survives core loss; dies once at zero total HP',row['coreOnly']['hp']>0 and not row['coreOnly']['dead'] and row['dead'] and row['hp']==0 and row['rewards']==1,row)
  # Every completed replacement must actually be selected by the native hull renderer.
  models=p.evaluate('Object.entries(AF21_ART.models).filter(([id,m])=>!m.aliases.some(a=>["nyx","rook","kaia","jace","voss"].includes(a))).map(([id,m])=>({id,stage:m.stages[0],type:m.aliases[0]}))')
  for model in models:
   p.evaluate(SETUP,dict(stage=model['stage'],pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
   p.evaluate('''type=>{window.E=spawnEnemy(type,worldWidth()/2,220,{});E.x=worldWidth()/2;E.y=220;E.hp=Math.max(20,E.hp);E._scaleIn=null;E._spawnScale=null;for(const b of Object.values(AF21_ART.models[AF21.aliases.get(E.type).id].banks))XART.rdy(b.key);}''',model['type'])
   p.wait_for_function('()=>Object.values(AF21.aliases.get(E.type).M.banks).every(b=>XART.rdy(b.key))')
   row=p.evaluate('''()=>{function cap(){ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#071626';ctx.fillRect(0,0,VW,VH);drawEnemy(E);return ctx.getImageData(0,0,cv.width,cv.height).data;}const before=cap();hitEnemy(E,.01,true);const after=cap();let pixels=0;for(let i=0;i<after.length;i+=4)if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2])pixels++;const hit=E.flash;E.flash=0;cap();return{type:E.type,rendered:E._af21Rendered,flash:hit,pixels};}''');ck(model['id']+' native hull replacement and damaged pixels',bool(row.get('rendered')) and row['pixels']>10 and row['flash']>0,row);shot(p,'air-'+model['id'],'ctx.fillStyle="#071626";ctx.fillRect(0,0,VW,VH);drawEnemy(E)')
  p.evaluate(SETUP,dict(stage=5,pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}')
  p.evaluate('s5RunInit();s5run.gates.forEach(g=>g.y=-900);s5run.gates[0].x=worldWidth()/2-70;s5run.gates[0].y=220;s5run.gates[7].x=worldWidth()/2+70;s5run.gates[7].y=420;s5run.gates[7].glow=1;')
  shot(p,'portal-pair','ctx.fillStyle="#071626";ctx.fillRect(0,0,VW,VH);s5RunDraw()')
  row=p.evaluate('''()=>{const a={...FV21.draws};s5RunDraw();return{violet:(FV21.draws.portal||0)-(a.portal||0),blue:(FV21.draws.portal_blue||0)-(a.portal_blue||0)};}''');ck('Stage5 first/final gates use single violet/blue portal-only loop',row['violet']==1 and row['blue']==1,row)
  p.evaluate('s5GateOutStart();s5GateOutTick(.45)');shot(p,'portal-arrival','ctx.fillStyle="#071626";ctx.fillRect(0,0,VW,VH);s5GateOutDraw();drawPlayer()')
  ck('return portal carries ship then clears',p.evaluate('()=>{let last=player.y,move=0;for(let i=0;i<80;i++){s5GateOutTick(1/60);if(player.y>last)move++;last=player.y;}return !s5GateOut&&move>20;}'))
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',pilot='cole',diff=diff))
   p.evaluate('''()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;window.G=rg4Init(B);G.gang=true;G.scene=null;G.rescueDone=true;G.rescueAt=Infinity;G.releaseAt=999;window.D=rd21State(B);G.ord=[];for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.evadeT=0;}H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();story=null;rg4Warm();}''')
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}')
   for form in ['star','bowling','H','X']:
    row=p.evaluate('''()=>{G.ord=[];eBullets=[];for(const q of R.ships)q.rg4.act=null;rd21FleetStart(B,G,D);const name=D.fleet.name,seen=new Set();for(let i=0;i<660&&D.fleet;i++){seen.add(D.fleet.phase);rd21Fleet(B,G,D,1/60);if(i%30===0)for(const q of R.ships)fr27RebelDrawShip(q);}return{name,seen:[...seen],missiles:eBullets.filter(o=>o._ra4Rocket).map(o=>({hp:o.hp,homing:o.lock?.key,dead:o.dead,shootable:o._shootable})),reset:R.ships.every(q=>q._rd21Scale===1),finite:R.ships.every(q=>Number.isFinite(q.x+q.y))};}''');ck(diff+' '+form+' formation warns, volleys, scatters and returns',row['name']==form and len(row['seen'])==5 and row['reset'] and row['finite'] and len(row['missiles'])==10 and all(x['hp']>0 for x in row['missiles']),row)
   for mode in ['regular','multi']:
    row=p.evaluate('''mode=>{const q=R.ships.find(q=>q.key==='nyx');q._rd21Cloak=true;q.frCloak=10;const target=retinaBossTargets(B).find(t=>String(t._retinaId).startsWith('nyx'));retina.phase=mode==='regular'?'locked':'idle';retina.target=target;player._retinaScan=mode==='multi'?{marks:[{phase:'locked',target}]}:null;rd21NyxLock(B,q);retina.phase='idle';player._retinaScan=null;return{target:!!target,revealed:!q._rd21Cloak,fade:q._ra7Reveal,armed:q.rg4.armed};}''',mode);ck(diff+' Nyx '+mode+' Retina reveals and prepares counterattack',row['target'] and row['revealed'] and row['fade']>0 and row['armed']=='cloak',row)
   for pilot,kind in [('kaia','windspread'),('voss','depthram'),('jace','swervehelix'),('nyx','shadowcast')]:
    row=p.evaluate('''([pilot,kind])=>{for(const q of R.ships)q.rg4.act=null;G.ord=[];eBullets=[];const q=R.ships.find(q=>q.key===pilot);q._rd21Cloak=false;rd21Personal(q,R,G,kind);const seen=new Set();let min=1,max=1;for(let i=0;i<540&&q.rg4.act;i++){seen.add(q.rg4.act.phase);rg4AttackTick(q,R,G,1/60);min=Math.min(min,q._rd21Scale);max=Math.max(max,q._rd21Scale);if(i%12===0)fr27RebelDrawShip(q);}return{finished:!q.rg4.act,seen:[...seen],min,max,shots:eBullets.length,ord:G.ord.length};}''',[pilot,kind]);ck(diff+' '+pilot+' personal attack completes with recovery',row['finished'] and len(row['seen'])>=2 and (kind!='depthram' or row['min']<.4 and row['max']>1.3),row)
  p.evaluate(SETUP,dict(stage=1,pilot='juggernaut'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}');p.evaluate('startSpecial();for(const key of Object.keys(Input.keys))delete Input.keys[key];')
  row=p.evaluate('''()=>{const k=keybindFor(1);for(const b of [...k.charge,...k.up])Input.keys[b]=true;for(let i=0;i<160;i++)chargeTick(1/60);const wind=chargeLevel(),y=player.y;for(const key of Object.keys(Input.keys))delete Input.keys[key];chargeTick(1/60);const dash=!!player._chgDash,invuln=player.invuln;for(let i=0;i<100;i++){chargeTick(1/60);if(i%12===0)drawChargeFX();}return{wind,dash,invuln,moved:y-player.y,finished:!player._chgDash};}''');ck('Juggernaut real bound input charges, launches, moves and finishes safely',row['wind']>.9 and row['dash'] and row['invuln']>0 and row['moved']>50 and row['finished'],row)
  ck('No renderer/runtime errors',not errors,errors);br.close()
finally:stop()
(O/(a.browser+'-report.json')).write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(checks=len(checks),passed=sum(c['ok'] for c in checks),errors=errors)),flush=True);sys.exit(bool(errors) or not all(c['ok'] for c in checks))
