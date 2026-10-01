import sys,json,base64,http.server,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
OUT=ROOT/'_shots/encounters_0930';OUT.mkdir(parents=True,exist_ok=True);rows=[];errors=[]
def ok(v,n,d=None):
 rows.append(dict(ok=bool(v),name=n,detail=d));print(('OK ' if v else 'FAIL ')+n, d or '',flush=True)
def grab(p,n):
 b=base64.b64decode(p.evaluate("()=>cv.toDataURL('image/png')").split(',')[1]);(OUT/(n+'.png')).write_bytes(b);return hashlib.sha256(b).hexdigest()
SETUP="""c=>{ht27Stop();debugFight=null;coopOn=false;diffKey=c.diff||'furious';DIFF=DIFFS[diffKey];run.pilot='yuri';run.mode='campaign';beginStage(c.stage);setState(GS.PLAY);player.reset();story=null;special=null;s6Opening=null;s6Wing=null;
 stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;l5Rocks=[];player.x=VW/2;player.y=VH-110;player.invuln=999;return true;}"""
port,stop=sh.serve(str(ROOT))
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1000,'height':1100})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' or 'draw error' in m.text else None)
 p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>(window.__bofFrames|0)>4');p.evaluate(sh.TRAP_RAF)
 p.evaluate("()=>{for(const a of Object.values(ENC30_ART))XART.rdy(a.key);}")
 p.wait_for_function('()=>Object.values(ENC30_ART).every(a=>XART.rdy(a.key))')
 p.evaluate(SETUP,{'stage':4});p.wait_for_timeout(1600);p.evaluate('()=>drawWorld(0)')
 r=p.evaluate("""()=>{const types=['sandtank','roadtank','s4interceptor','s4heavyjet','s4command'];
  for(let i=0;i<5;i++){const e=spawnEnemy(types[i],camLeftX()+90+i%3*145,140+Math.floor(i/3)*190,{});e._modAngle=Math.PI/2;e._stagger=0;if(e._r30)e._r30.warning={t:.3,dur:1.2,x:player.x,y:player.y};}
  drawWorld(0);return enemies.map(e=>({type:e.type,parts:!!e._r30,hp:e.hp,draw:e._drawW}));}""")
 ok(len(r)==5 and all(x['parts'] and x['draw'] for x in r),'all five Stage4 replacement rigs render',r);grab(p,'stage4_modular')
 r=p.evaluate("""()=>{const e=enemies.find(e=>e._modJet);e._esh=null;e._noHit=false;e._r30.left.hp=1;
 _dmgBullet={x:e.x-e.w*.35,y:e.y,kind:'mg',lv:3};hitEnemy(e,2);_dmgBullet=null;
 return {hp:e._r30.left.hp,disabled:modularJetPoint(e,-1)._disabled,right:modularJetPoint(e,1)._disabled,flash:e.flash};}""")
 ok(r['hp']==0 and r['disabled'] and not r['right'] and r['flash']>0,'shooting a wing module destroys and disables that gun',r)
 r=p.evaluate("""()=>{const e=enemies.find(e=>e._modTank===4);e.x=camLeftX()+120;e.y=player.y-120;e._r30.rocketCd=0;e._r30.warning=null;eBullets=[];
 modularTankTick(e,.01);const tell=!!e._r30.warning;modularTankTick(e,.3);const before=eBullets.length;modularTankTick(e,1);
 return {tell,before,shots:eBullets.length,down:eBullets.every(b=>b.vy>0)};}""")
 ok(r['tell'] and r['before']==0 and r['shots']==2 and r['down'],'tank pods warn before two downward missiles',r)
 p.evaluate(SETUP,{'stage':6});p.wait_for_timeout(1200);p.evaluate('()=>drawWorld(0)')
 p.evaluate("()=>{spawnBoss('warhive');bossActive=true;boss.enter=false;whvAceSpawn(boss);const W=boss._whv;W.mode='ace';const A=W.ace;A.x=VW/2;A.y=VH*.32;A.roll=null;A.somer=null;A.inverted=false;A.desp=null;A.dash=null;A.vx=0;A.st='fight';boss.x=A.x;boss.y=A.y;drawWorld(0);}")
 grab(p,'stage6_blue_ace')
 r=p.evaluate("""()=>{const A=boss._whv.ace;const h=warhiveHitTest(boss,A.x-60,A.y);if(h)hitBoss(3);return {hit:h,flash:A.fl.wingL,body:A.fl.body,w:boss.w};}""")
 ok(r['hit'] and r['flash']>0 and r['body']==0,'blue ace wing has its own target and flash',r)
 poses=[]
 for motion in ['roll','somer']:
  for f in [0,2,4,6]:
   p.evaluate("c=>{const A=boss._whv.ace;A.roll=null;A.somer=null;A[c.motion]={t:c.f/8*(c.motion==='roll'?.46:.62),dir:1};drawWorld(0);}",{'motion':motion,'f':f})
   poses.append(grab(p,f'ace_{motion}_{f}'))
 ok(len(set(poses))==8,'ace roll and somersault use distinct generated poses')
 p.evaluate(SETUP,{'stage':6});p.wait_for_timeout(1200);p.evaluate('()=>drawWorld(0)')
 p.evaluate("()=>{const e=spawnEnemy('s6bomber',VW/2,220,{});e._r30BombAt=efxClock;drawWorld(0);}");grab(p,'stage6_bomber')
 p.evaluate(SETUP,{'stage':7});p.wait_for_timeout(1600);p.evaluate('()=>drawWorld(0)')
 p.evaluate("()=>{mapScroll=1400;drawBG(0);for(const e of stage7SluiceEvents())e.tier=99;const e=stage7SluiceEvents()[0];e.row=_masterSrcY+VH*.57;e.tier=0;e.side=-1;e.live=true;e.done=false;e.t=0;}")
 hashes=[]
 for age in [-.2,.05,.18,.4,.7,1.02]:
  p.evaluate("age=>{const e=stage7SluiceEvents()[0];e.t=stage7SluiceWarn()+age;drawWorld(0);}",age)
  hashes.append(grab(p,'vent_'+str(age)))
 ok(len(set(hashes))==6,'vent warning, initial spray, full stream and decay render distinctly')
 r=p.evaluate("""()=>{const e=stage7SluiceEvents()[0],own=playerHit;let hits=0;playerHit=()=>{hits++;};player.invuln=0;player.dead=false;player.out=false;player.y=e.row-_masterSrcY;
 e.t=stage7SluiceWarn()-.2;player.x=250;stage7SluiceTick(.001);const warning=hits;
 e.t=stage7SluiceWarn()+.4;player.x=365;stage7SluiceTick(.001);const outside=hits;
 player.x=250;stage7SluiceTick(.001);playerHit=own;return {warning,outside,inside:hits};}""")
 ok(r=={'warning':0,'outside':0,'inside':1},'vent damage matches visible spray and leaves outside lane safe',r)
 p.evaluate('()=>{mapScroll=0;drawBG(0);}')
 for dy in [1100,600,100,0]:
  p.evaluate("dy=>{ctx.clearRect(0,0,VW,VH);entryConnectorDraw(7,dy);}",dy);grab(p,'sewer_entry_'+str(dy))
 ok(not errors,'no browser errors',errors[:12]);b.close()
stop();(OUT/'results.json').write_text(json.dumps(rows,indent=2));sys.exit(0 if all(r['ok'] for r in rows) else 1)
