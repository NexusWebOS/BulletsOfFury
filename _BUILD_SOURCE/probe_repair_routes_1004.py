"""Native combat, input, password and island-map verification. No damage overrides."""
from pathlib import Path
import json,base64,sys,traceback
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004/routes';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={};errors=[]
def frames(p,n,expr='updatePlay(1/60);'):
 for i in range(0,n,60):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(60,n-i));p.wait_for_timeout(8)
def shot(p,name,draw='drawWorld(0)'):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);'+draw+';}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{er26Warm();mm1003Warm();h3Warm();gp4AceWarm();cmap2Warm();}')
  p.wait_for_function('()=>XART.rdy("mr27_storm")&&GP4_MAP_KEYS.every(k=>XART.rdy("gp4_island_"+k))&&Object.values(MM1003_ART).every(a=>XART.rdy(a.key))',timeout=120000)
  p.evaluate(SETUP,{'stage':4,'kind':'stormsovereign','diff':'furious'})
  p.evaluate('()=>{run.weapon=0;run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);run.wvars=WEAPONS.map(()=>null);run.infusion=null;run.forge={};window.fireClock=0;window.stormSample=[];}')
  for k in range(80):
   frames(p,180,'if(!B.dead){const n=B._s4war.shield.active?B._s4war.shield.nodes.find(q=>!q.dead):null;player.x=n?n.x:B.x;player.y=VH-55;player.invuln=1e9;fireClock-=1/60;if(fireClock<=0){pShoot();fireClock=_weaponCadence();}}updatePlay(1/60);')
   row=p.evaluate('()=>({hp:B.hp,max:B.maxhp,dead:B.dead,active:B._s4war.shield.active,nodes:B._s4war.shield.nodes.map(n=>n.hp),mode:B._er26.mode,shieldPhase:B._s4war.shield.phase})');row['seconds']=(k+1)*3
   report.setdefault('storm',[]).append(row)
   if k in [5,14,29]:shot(p,'storm-'+str(k))
   if row['dead']:break
  print('STORM',report['storm'][-1],flush=True);shot(p,'storm-final')
  # Exercise every element/weapon preview, including the previously failing Up transition.
  p.evaluate('()=>{run.mode="campaign";run.forgeElems=Object.fromEntries(Object.keys(INFUSIONS).map(k=>[k,1]));run.loadout=[0,1,2,3,4,5];forgeStart(()=>{});forge.t=2;Input.mouse.down=false;}')
  report['previews']=[]
  for w in range(9):
   for elem in p.evaluate('()=>Object.keys(INFUSIONS)'):
    p.evaluate('(v)=>{window.P=forgePreviewNew(v.w,v.elem,3);}',{'w':w,'elem':elem})
    frames(p,90,'forgePreviewTick(P,300,260,1/60);ctx.setTransform(SS,0,0,SS,0,0);forgePreviewDraw(P,50,100,300,260);')
    err=p.evaluate('()=>P.err')
    if err:report['previews'].append({'weapon':w,'element':elem,'error':err})
  p.evaluate('()=>{forge.row=1;forge.esel=4;}')
  for _ in range(12):p.keyboard.press('ArrowUp');frames(p,2,'ctx.setTransform(SS,0,0,SS,0,0);drawForge(1/60);')
  shot(p,'forge-up','drawForge(0)');print('PREVIEWS',report['previews'],flush=True)
  # Fresh enemy salvos with real ordnance, followed by disarming the caster mid-attack.
  p.evaluate(SETUP,{'stage':8,'diff':'furious'})
  report['enemies']=[]
  for enemy in ['s8manta','s8scout','s8needlejet','s8gunship']:
   p.evaluate('(type)=>{enemies=[];eBullets=[];window.E=spawnEnemy(type,worldWidth()/2,180,{});E._mm1003.homeX=E.x;E._mm1003.homeY=E.y;E._mm1003.target={x:player.x,y:player.y};mm1003Set(E,"fire");}',enemy)
   frames(p,68,'mm1003Tick(E,1/60);')
   report['enemies'].append(p.evaluate('()=>({kind:E._mutator1003,shots:eBullets.length,finite:eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy))})'))
   shot(p,'enemy-'+enemy)
  p.evaluate('()=>{enemies=[];eBullets=[];window.E=spawnEnemy("s8scout",worldWidth()/2,180,{});E._mm1003.target={x:player.x,y:player.y};mm1003Set(E,"fire");E._mm1003.parts.forEach(p=>p.dead=true);mm1003Tick(E,1/60);}')
  report['disarmedCaster']=p.evaluate('()=>E._mm1003.phase==="recover"&&eBullets.length===0')
  # Orb burst collision and splash use actual enemy damage functions.
  report['orbs']=[]
  for el in ['fire','ice','kinetic','water','toxic','dark','lightning']:
   p.evaluate(SETUP,{'stage':3,'diff':'normal'})
   p.evaluate('(el)=>{run.weapon=5;run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);run.wvars=WEAPONS.map(()=>null);run.wvars[5]=el==="fire"?"fireorb":"iceorb";run.forge=el==="fire"?{}:{5:{elem:el,lv:3}};window.E=spawnEnemy("fighter",player.x,player.y-110,{});E.hp=E.maxhp=250;E.w=100;E.h=100;pShoot();window.orb=pBullets.find(q=>q.kind==="orb");}',el)
   frames(p,28,'for(const q of pBullets.slice())if(q.kind==="orb"&&!q.dead)playerOrbTick(q,1/60);')
   report['orbs'].append(p.evaluate('()=>({element:orb?._el,damage:250-E.hp,finite:!!orb&&Number.isFinite(orb.y+orb.spin),burst:efxBursts.length,dead:orb?.dead})'))
   if el=='fire':shot(p,'fire-orb-impact')
  print('ORB',report['orbs'],flush=True)
  # Password routing follows submitPassword -> stage boot -> live encounter.
  report['passwords']=[]
  for code in ['RIFT9','XHARR','XREBEL']:
   p.evaluate('(code)=>{pwInput=code;submitPassword();window.pending= PENDING_STAGE;beginStage(PENDING_STAGE);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;}',code)
   frames(p,2)
   report['passwords'].append(p.evaluate('()=>({pending,stage:run.stage,route:run._gp4StageX,kind:boss?.kind,wing:s6Wing?.ships.length})'))
   shot(p,'password-'+code)
  p.evaluate('()=>{run.mode="arcade";scLeaveStage({bonus:0,rank:"A"});}')
  report['stage6Exit']=p.evaluate('()=>({state,expected:GS.STAGESEL,stage:run.stage,mode:run.mode,unlocked:campaign.unlockedMax})')
  # Let the actual briefing/clock/progression/map draw together at widescreen size.
  p.evaluate('()=>{GP4.death=null;run.mode="campaign";campaign.unlockedMax=8;openStageSelect(1,{boot:true});}')
  frames(p,210,'ctx.setTransform(SS,0,0,SS,0,0);drawStageSelect(1/60);');shot(p,'map-arriving','drawStageSelect(0)')
  frames(p,800,'ctx.setTransform(SS,0,0,SS,0,0);drawStageSelect(1/60);');shot(p,'map-complete','drawStageSelect(0)')
  p.evaluate('()=>{sselCursor=4;}');frames(p,150,'ctx.setTransform(SS,0,0,SS,0,0);drawStageSelect(1/60);');shot(p,'map-hover','drawStageSelect(0)')
  report['map']=p.evaluate('()=>({camera:cmap2.cam,boot:sselBoot,lift:cmap2.lift[4]})')
  # Direct XART render verifies elite full, roll, belly and modular plates together.
  p.wait_for_function('()=>Object.keys(XART._src).filter(k=>k.startsWith("gp4_ace")).every(k=>XART.rdy(k))',timeout=120000)
  shot(p,'approved-stealth-colors','ctx.fillStyle="#101522";ctx.fillRect(0,0,VW,VH);["gp4_ace_top","gp4_ace_br1","gp4_ace_so3","gp4_ace_belly","gp4_ace_damaged"].forEach((key,i)=>{ctx.drawImage(XART.get(key),25+(i%3)*150,35+Math.floor(i/3)*160,130,135);});["#ff3448","#42e35b"].forEach((c,i)=>ctx.drawImage(xartPalette("gp4_ace_top",c),40+i*210,355,130,135))')
  browser.close()
except Exception as e:report['fatal']=str(e);traceback.print_exc()
finally:stop()
report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
