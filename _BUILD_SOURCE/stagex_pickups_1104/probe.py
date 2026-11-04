import sys,json,base64,time
from pathlib import Path
from playwright.sync_api import sync_playwright
W=Path(__file__).parent;sys.path.insert(0,str(W.parent/('coleforge_1104'if(W.parent/'coleforge_1104').exists()else'BOF-Space-Arsenal-FX-1104')));from native_common import SETUP,TRAP_RAF
errors=[];checks=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1700,'height':1050})
 p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,body='window.BOF_ONLINE_CONFIG={};',content_type='application/javascript'));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:250])if m.type=='error'or'DRAW ERROR'in m.text else None)
 p.goto('http://127.0.0.1:65043/game/index.html?quality=high&stagex-pickups=1104',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4',timeout=60000);p.evaluate(TRAP_RAF);p.evaluate(SETUP,{'stage':6,'diff':'furious','pilot':'cole'})
 p.evaluate('''()=>{CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=999999;_adaptiveSpawnT=999999;tryAdaptiveReinforcement=()=>{};subBossDone=subBossTriggered=aminiTriggered=true;curStage={...curStage,length:99999};run._gp4StageX='left';CC21.owner='left';CC21.card=3.001;AP10_X.intro=null;GP4.routeReady=false;sxp114Warm();window.puKeys=Object.values(SXP114.banks).map(b=>b.key);puKeys.forEach(k=>XART.rdy(k));}''')
 for i in range(500):
  if p.evaluate('()=>{stageLoadTick();return puKeys.every(k=>XART.rdy(k));}'):break
  p.wait_for_timeout(30)
 p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 p.wait_for_timeout(900)
 tests=p.evaluate('''()=>{const out=[],ck=(ok,name,data)=>out.push({ok:!!ok,name,data});
  ck(sxp114Active(),'Stage X route selects new pickup family');
  const D=ctx.drawImage,calls=[];ctx.drawImage=function(...a){calls.push({n:a.length,sx:a[1],sy:a[2],sw:a[3],sh:a[4],dx:a[5],dy:a[6],dw:a[7],dh:a[8],alpha:this.globalAlpha,blend:this.globalCompositeOperation,blur:this.shadowBlur});return D.apply(this,a);};
  for(let f=0;f<8;f++){calls.length=0;drawCrate(240,200,f*.10+.001,0);const q=calls[0];ck(q&&q.sx===f*64&&q.sw===64&&q.dw===64&&q.dh===64,'power native frame'+f+' selected without size change');}
  calls.length=0;drawCrate(240,200,.21,.1);ck(calls[0]?.sx===512,'power authored white hit cell selected');
  calls.length=0;drawCapsule(240,200,.21,0);ck(calls[0]?.sx===128&&calls[0].dw===64,'capsule new powered frame selected');
  powerups=[{kind:'speed',x:240,y:300,t:.21,vy:0,w:18,h:18}];calls.length=0;drawPowerups();ck(calls.some(c=>c.sw===36&&c.dw===36&&c.alpha===1&&c.blend==='source-over'&&c.blur===0),'loose speed uses fixed36 source-over frame');
  run._gp4StageX='right';ck(sxp114Active(),'both Stage X routes covered');
  delete run._gp4StageX;ck(!sxp114Active(),'regular Stage6 keeps existing family');
  for(const stage of[1,5,7,8,9]){run.stage=stage;run._gp4StageX='left';ck(!sxp114Active(),'Stage'+stage+' never uses Stage X art');}
  ctx.drawImage=D;run.stage=6;run._gp4StageX='left';CC21.owner='left';CC21.card=3.001;powerups=[];
  run.speedLevel=0;applyPowerup({kind:'speed',x:player.x,y:player.y});ck(run.speedLevel===1,'native speed upgrade0 to1');for(let i=0;i<8;i++)applyPowerup({kind:'speed',x:player.x,y:player.y});ck(run.speedLevel===5,'native speed cap5 retained');
  const box={kind:'crate',x:player.x,y:player.y-90,t:0,vy:0,w:28,h:28,hp:5,flash:0,wtype:0,bob:0};powerups=[box];pBullets=[{kind:'mg',x:box.x,y:box.y+8,vx:0,vy:-8,w:8,h:16,dmg:1,lv:1,t:0}];window.qaBox=box;
  updatePlay(1/60);ck(box.hp<5&&box.flash>0,'real bullet damages and flashes native crate',{hp:box.hp,flash:box.flash});
  pBullets=[{kind:'mg',x:box.x,y:box.y+8,vx:0,vy:-8,w:8,h:16,dmg:50,lv:5,t:0}];updatePlay(1/60);ck(box.dead&&powerups.some(q=>q.kind==='weapon'),'native break/reward preserved');
  return out;}''');checks.extend(tests)
 print('NATIVE',len(checks),'failed',[q for q in checks if not q['ok']],flush=True)
 # Visible native scene: three actual pickup drawers at their actual logical sizes.
 p.evaluate('''()=>{run._gp4StageX='left';run.speedLevel=0;arcBanner=null;powerups=[{kind:'crate',x:player.x-90,y:VH*.53,t:.3,vy:0,w:28,h:28,hp:5,flash:0,wtype:0,bob:0},{kind:'capsule',x:player.x+90,y:VH*.53,t:.3,vy:0,w:22,h:32,hp:5,flash:0,bob:0},{kind:'speed',x:player.x,y:VH*.70,t:.3,vy:0,w:18,h:18,bob:0}];pBullets=[];eBullets=[];enemies=[];}''')
 for i in range(12):
  p.evaluate('()=>{stateT+=1/60;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  p.wait_for_timeout(20)
 # Let a native main frame paint the separate HUD canvases as well.
 p.evaluate('()=>{if(__bofPendingRAF)__bofPendingRAF(performance.now());}')
 p.screenshot(path=str(W/'stagex-native.png'));(W/'stagex-playfield.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
 (W/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'drawError':p.evaluate('window.__bofDrawError||null')},indent=2),encoding='utf8');b.close()
