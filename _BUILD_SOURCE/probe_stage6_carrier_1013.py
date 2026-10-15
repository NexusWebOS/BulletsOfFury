from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
BROWSER=sys.argv[1] if len(sys.argv)>1 else 'msedge'
O=R/'_shots/stage6_carrier_1013'/('fx-'+BROWSER);O.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R));errors=[];rows=[];checks=[]
def check(name,value):
 checks.append({'name':name,'pass':bool(value)})
 if not value: raise AssertionError(name)
try:
 with sync_playwright() as pw:
  b=pw.firefox.launch() if BROWSER=='firefox' else pw.chromium.launch(channel=BROWSER,args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text+' '+str(m.location)) if m.type=='error' and not m.location.get('url','').endswith('/favicon.ico') else None)
  p.on('response',lambda r:print('HTTP_ERROR '+str(r.status)+' '+r.url,flush=True) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  if not p.evaluate('!!window.BOF_STAGE6_CARRIER'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/stage6_carrier_1013.js')
  p.evaluate(shoot.SETUP,{'state':'PLAY','stage':6,'pilot':'cole','invuln':True})
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&SC13.keys.every(k=>XART.rdy(k));}',timeout=180000)
  p.evaluate('()=>{s6Opening=null;s6Wing=null;story=null;run._mission29OpeningDone=true;debugFight=null;subBoss=null;subBossActive=false;subBossDone=true;warnT=0;stagePlan=[];stageTimer=50;Input.keys={};mapScroll=2200;player.invuln=100000;player.x=240;player.y=410;}')
  for diff in ['easy','normal','hard','furious']:
   p.evaluate('d=>{diffKey=d;DIFF=DIFFS[d];run._gp4StageX=null;bossDefeated=false;enemies=[];eBullets=[];pBullets=[];spawnBoss("warhive");}',diff)
   result=p.evaluate('''()=>{let minGap=999,peak=0,charged=0,forward=false,back=false;
    for(let f=0;f<3600;f++){warhiveTick(boss,1/60);let s=BOF_STAGE6_CARRIER.snapshot();forward ||= s.direction===1;back ||= s.direction===-1;
     const active=s.lasers.filter(l=>l.t>=l.warm&&l.t<l.warm+l.fire);peak=Math.max(peak,active.length);charged=Math.max(charged,s.lasers.length);
     const intervals=active.map(l=>[l.x-l.width/2-9,l.x+l.width/2+9]).sort((a,b)=>a[0]-b[0]);let end=camLeftX()+18,best=0;
     for(const q of intervals){best=Math.max(best,q[0]-end);end=Math.max(end,q[1]);}best=Math.max(best,camRightX()-18-end);minGap=Math.min(minGap,best);
     if(f%240===0)drawWorld(1/60);
    }return {difficulty:diffKey,minGap,peak,charged,reverses:forward&&back,stats:{...SC13.stats},snapshot:BOF_STAGE6_CARRIER.snapshot()};}''')
   rows.append(result);check(diff+' minimum open interval at least 60px',result['minGap']>=60);check(diff+' slow traverse reverses',result['reverses']);check(diff+' bounded simultaneous beams',result['peak']<=3)
   print(json.dumps({k:v for k,v in result.items() if k not in ['snapshot','stats']}),flush=True)
  # Capture native charge, beam, recovery and permanent wreck states.
  p.evaluate('()=>{diffKey="normal";DIFF=DIFFS.normal;bossDefeated=false;eBullets=[];spawnBoss("warhive");for(let i=0;i<230;i++)warhiveTick(boss,1/60);}')
  for label,step in [('charge',30),('beam',55),('cooldown',28)]:
   p.evaluate('(n)=>{for(let i=0;i<n;i++)warhiveTick(boss,1/60);drawWorld(1/60)}',step)
   raw=p.evaluate('ctx.canvas.toDataURL("image/png")').split(',')[1];(O/(label+'.png')).write_bytes(base64.b64decode(raw))
  visuals=p.evaluate('''()=>{const b=boss,C=b._cargo13,oldLasers=C.lasers.slice(),saved=C.guns.map(g=>({...g})),oldHit=playerHit,oldX=player.x,oldY=player.y,oldT=b.t;
   const out={widths:[],frames:[],lights:[],muzzles:[]};
   try{let hits=0;playerHit=()=>{hits++;};const g=C.guns[2],p=sc13Muzzle(b,2);
    for(const d of ['easy','normal','hard','furious']){const cfg=SC13_CFG[d],L={id:2,t:cfg.warm+.15,warm:cfg.warm,fire:cfg.fire,width:cfg.width,fired:true};C.lasers=[L];
     player.y=p.y+120;const margin=Math.max(3,(player._hx||9)-3);player.x=p.x+cfg.width/2+margin-.1;hits=0;sc13LaserTick(b,0);const inside=hits===1;
     player.x=p.x+cfg.width/2+margin+.1;hits=0;sc13LaserTick(b,0);out.widths.push({d,width:sc13BeamWidth(L),inside,outside:hits===0});
    }
    const L={id:2,t:1.15,warm:1,fire:.6,width:34,fired:true};C.lasers=[L];
    for(let f=0;f<4;f++){L.t=1+.08+f/16;ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);sc13BeamDraw(b,L);
     const data=ctx.getImageData(Math.floor(p.x-30),Math.floor(p.y+120),60,40).data;let red=0,dark=0,hash=0;
     for(let i=0;i<data.length;i+=4){if(data[i+3]>150&&data[i]>data[i+1]*1.5&&data[i]>data[i+2]*1.3){red++;if(data[i]<170)dark++;}hash=(hash*31+data[i]+data[i+3])>>>0;}
     out.frames.push({red,dark,hash});
    }
    for(let id=0;id<6;id++){const gun=C.guns[id];C.lasers=[{id,t:1.19,warm:1,fire:.6,width:34,fired:true}];gun.pose=2;gun.heat=1;
     const m=sc13Muzzle(b,id);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);sc13MuzzleDraw(b,gun);const a=ctx.getImageData(Math.floor(m.x-37),Math.floor(m.y-37),74,74).data;let pixels=0;for(let i=3;i<a.length;i+=4)if(a[i]>128)pixels++;
     out.muzzles.push({id,pixels});
     gun.pose=1;gun.heat=.2;b.t=1;const early=sc13Light(b,gun);gun.heat=.9;b.t=1.2;const charged=sc13Light(b,gun);gun.pose=2;const fire=sc13Light(b,gun);gun.pose=0;gun.cool=.3;const cool=sc13Light(b,gun);gun.dead=true;const off=sc13Light(b,gun);
     out.lights.push({id,early,charged,fire,cool,off});Object.assign(gun,saved[id]);
    }
   }finally{playerHit=oldHit;player.x=oldX;player.y=oldY;b.t=oldT;C.lasers=oldLasers;C.guns.forEach((g,i)=>Object.assign(g,saved[i]));drawWorld(1/60);}return out;}''')
  for q in visuals['widths']:check(q['d']+' visible red core and collision width',q['width']=={'easy':32,'normal':34,'hard':36,'furious':38}[q['d']] and q['inside'] and q['outside'])
  check('four distinct authored beam animation frames',len(set(q['hash'] for q in visuals['frames']))==4)
  check('broad predominantly dark red beam pixels',all(q['red']>1000 and q['dark']>q['red']*.40 for q in visuals['frames']))
  for q in visuals['muzzles']:check('visible muzzle flash on gun '+str(q['id']),q['pixels']>250)
  for q in visuals['lights']:check('charge fire cool dark sequence gun '+str(q['id']),q['charged']['level']>q['early']['level'] and q['fire']['phase']=='fire' and q['cool']['phase']=='cool' and q['off']['level']==0)
  (O/'visual-qa.json').write_text(json.dumps(visuals,indent=2))
  continuous=p.evaluate('''()=>{const C=boss._cargo13,old=_dmgBullet,g=C.guns[3],other=C.guns[5],before=g.hp,otherBefore=other.hp,p=sc13Mount(boss,3);
   _lastHitX=_lastHitY=null;C.hit=null;_dmgBullet={kind:'beam',x:p.x,w:10,top:-20,bot:450,dmg:4};hitBoss(4);const fresh=g.hp<before;
   const after=g.hp;const stale=sc13Mount(boss,5);_lastHitX=stale.x;_lastHitY=stale.y;C.hit=5;hitBoss(4);const current=g.hp<after&&other.hp===otherBefore;
   const fg=C.guns[4],fBefore=fg.hp,m=sc13Mount(boss,4);_lastHitX=_lastHitY=null;C.hit=null;
   _dmgBullet={kind:'flame',x:m.x,w:20,top:m.y-50,bot:m.y+70,lv:1,dmg:3};hitBoss(3);const flameFresh=fg.hp<fBefore;
   const ff=fg.hp;C.hit=5;_lastHitX=stale.x;_lastHitY=stale.y;hitBoss(3);const flameCurrent=fg.hp<ff&&other.hp===otherBefore;
   const round=C.guns[2],rb=round.hp,m2=sc13Mount(boss,2);_dmgBullet={kind:'mg',x:m2.x,y:m2.y+10,dmg:2,vx:0,vy:-22};
   const roundContact=warhiveHitTest(boss,_dmgBullet.x,_dmgBullet.y);hitBoss(2);const rapidRound=roundContact&&round.hp<rb&&other.hp===otherBefore;
   _dmgBullet=old;C.hit=null;_lastHitX=_lastHitY=null;return{fresh,current,flameFresh,flameCurrent,rapidRound};}''')
  for k,v in continuous.items():check('continuous geometry '+k,v)
  checks_state=p.evaluate('''()=>{const C=boss._cargo13;const hp=C.core;C.directId='core';warhiveDamage(boss,999);const shield=C.core===hp;
   C.queue=[{id:0,at:0},{id:1,at:1}];C.lasers=[{id:0,t:.2,warm:1,fire:.5,width:18,fired:false}];C.directId=0;warhiveDamage(boss,1e6);
   const removed=C.guns[0].dead&&!C.queue.some(q=>q.id===0)&&!C.lasers.some(q=>q.id===0);
   C.directId=1;warhiveDamage(boss,1e6);const exposed=sc13Open(boss);C.directId='core';warhiveDamage(boss,5);const damage=C.core===hp-5;
   const targets=[];warhiveRetinaTargets(boss,targets);drawWorld(1/60);
   return{shield,removed,exposed,damage,targetCount:targets.length,opaque:C.guns[0].pose===3&&C.guns[1].pose===3};}''')
  for k,v in checks_state.items():check('damage '+k,v==5 if k=='targetCount' else v)
  raw=p.evaluate('ctx.canvas.toDataURL("image/png")').split(',')[1];(O/'modules-broken.png').write_bytes(base64.b64decode(raw))
  p.evaluate(shoot.STEP,90)
  raw=p.evaluate('ctx.canvas.toDataURL("image/png")').split(',')[1];(O/'permanent-gap.png').write_bytes(base64.b64decode(raw))
  death=p.evaluate('''()=>{const score=run.score;boss._cargo13.directId='core';warhiveDamage(boss,1e7);for(let i=0;i<180;i++)warhiveTick(boss,1/60);
    return{dead:boss.dead,defeated:bossDefeated,score:run.score-score,noAce:boss._whv.ace===null,clean:boss._cargo13.lasers.length===0&&boss._cargo13.queue.length===0,crashed:boss._cargo13.crashed};}''')
  for k,v in death.items():check('death '+k,v==30000 if k=='score' else v)
  for i in range(14):p.evaluate(shoot.STEP,30)
  completion=p.evaluate('()=>({state,stageEnding,bossDefeated,summary:state===GS.FLYOVER||state===GS.STAGECLEAR||state===GS.RESULTS})')
  print('COMPLETION '+json.dumps(completion),flush=True);check('native completion transition',completion['summary'])
  p.screenshot(path=str(O/'complete.png'))
  route=p.evaluate('''()=>{run._gp4StageX='left';spawnBoss('warhive');const stageX=!boss._cargo13&&!!boss._whv;run._gp4StageX=null;spawnBoss('rebelsquad');return{stageX,rebels:!!boss._rebels&&!boss._cargo13};}''')
  check('Stage X original Harrier preserved',route['stageX']);check('rebel branch preserved',route['rebels'])
  specials=p.evaluate('''()=>{coopOn=false;spawnBoss('warhive');const C=boss._cargo13;C.mode='recover';C.ready=true;C.x=240;C.y=72;sc13Sync(boss);sc13FinalizeBudget(boss);
   _dmgBullet=null;_lastHitX=_lastHitY=null;player.x=sc13Mount(boss,0).x;const core=C.core,g0=C.guns[0].hp,g5=C.guns[5].hp;
   C.hit='core';hitBoss(7);const noCoords=C.guns[0].hp<g0&&C.core===core;
   const after=C.guns[0].hp,stale=sc13Mount(boss,5);_lastHitX=stale.x;_lastHitY=stale.y;C.hit=5;bombHitBosses(.015);
   const bomb=C.guns[0].hp<after&&C.guns[5].hp===g5&&C.core===core;
   const afterBomb=C.guns[0].hp;detonateBomb({x:boss.x,y:boss.y,vy:-2,t:0});const localBomb=C.guns[0].hp<afterBomb&&C.core===core;
   C.directId=0;warhiveDamage(boss,1e6);C.directId=1;warhiveDamage(boss,1e6);const openCore=C.core;C.hit=5;hitBoss(10);
   const exposedSpecial=C.core<openCore&&C.guns[5].hp===g5;
   coopOn=true;spawnBoss('warhive');const D=boss._cargo13,target=boss.maxhp;D.mode='recover';D.ready=true;sc13FinalizeBudget(boss);
   const sum=D.core+D.guns.reduce((n,g)=>n+g.hp,0),scaled=sum===target&&boss.hp===target;D.directId=0;warhiveDamage(boss,1);
   const firstHit=target-boss.hp===1;coopOn=false;diffKey='insanity';const alias=sc13Config()===SC13_CFG.furious;diffKey='normal';DIFF=DIFFS.normal;
   _lastHitX=_lastHitY=null;return{noCoords,bomb,localBomb,exposedSpecial,scaled,firstHit,alias};}''')
  for k,v in specials.items():check('special and co-op '+k,v)
  # Real updatePlay/loop smoke pass with movement and player fire.
  p.evaluate('()=>{setState(GS.PLAY);spawnBoss("warhive");bossDefeated=false;player.invuln=10000;for(const k of keybindFor(1).fire||[])Input.keys[k]=true;}')
  for i in range(16):
   p.evaluate('i=>{for(const name of ["left","right"])for(const k of keybindFor(1)[name]||[])Input.keys[k]=(name==="right")===(i%4<2)}',i)
   err=p.evaluate(shoot.STEP,30);check('live frame batch '+str(i),err is None);p.wait_for_timeout(10)
  p.screenshot(path=str(O/'live.png'))
  # Proper stage loading and weather clock: native boss progress, full HUD.
  p.evaluate(shoot.SETUP,{'state':'PLAY','stage':6,'pilot':'cole','invuln':True})
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&SC13.keys.every(k=>XART.rdy(k));}',timeout=180000)
  p.evaluate('()=>{s6Opening=null;story=null;run._mission29OpeningDone=true;s6Wing=null;stagePlan=[];subBoss=null;subBossActive=false;subBossDone=true;warnT=0;stageTimer=75;mapScroll=levelScrollRange();player.x=240;player.y=420;player.invuln=10000;bossDefeated=false;spawnBoss("warhive");}')
  for i in range(18):p.evaluate(shoot.STEP,20);p.wait_for_timeout(10)
  p.screenshot(path=str(O/'native-stage6-hud.png'));b.close()
finally:
 stop();(O/'qa.json').write_text(json.dumps({'checks':checks,'results':rows,'errors':errors},indent=2),encoding='utf-8')
print(json.dumps({'checks':len(checks),'errors':errors,'output':str(O)}));assert not errors
