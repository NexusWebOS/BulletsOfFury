"""Chromium combat/asset proof. Gameplay recordings use the live renderer."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_1005';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[],'clips':[]};errors=[];port,stop=sh.serve(str(R))
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(n)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  ck(p.evaluate('()=>typeof on5RebelLaser==="function"&&Object.keys(ON5_CODES).length>25'),'all overnight layers loaded')
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B._noHit=false;window.G=rg4Init(B);G.releaseAt=9999;G.rescueAt=9999;for(const q of R.ships){q.mode="fight";q.warp=0;q.x=player.x+(q.i-2)*80;q.y=200;q.rg4.cd=9999;q.rg4.act=null;}cf1004Warm();r30Warm();rg4Warm();fb2Warm();}')
  p.wait_for_function('()=>XART.rdy("cf1004_weapons")&&ON5_ART.knight.every(a=>XART.rdy(a.key))&&ON5_ART.fragments.every(a=>XART.rdy(a.key))',timeout=120000,polling=50)
  p.evaluate('()=>{window.artCalls=[];const get=XART.get,draw=ctx.drawImage,map=new Map();XART.get=function(k){const im=get.apply(this,arguments);if(im)map.set(im,k);return im;};ctx.drawImage=function(im){const k=map.get(im);if(k)artCalls.push({k,args:Array.from(arguments).slice(1)});return draw.apply(this,arguments);};}')
  result=p.evaluate('()=>R.ships.map(q=>{player.x=q.x;const hp=q.hp;pBullets=[{kind:"beam",x:q.x,y:player.y-14,w:16,h:player.y,top:-20,bot:player.y-14,life:.5,dmg:3,_ht:0,_hit:[],seat:1}];updatePlay(1/60);return{pilot:q.key,before:hp,after:q.hp};})')
  report['heldLaserHP']=result
  ck(all(q['after']<q['before'] for q in result),'sustained beam damages all five Rebel hulls through actual updatePlay')
  shot(p,'beam-hits-rebels')
  p.evaluate('()=>{window.nyx=R.ships.find(q=>q.key==="nyx");nyx.frCloak=5;player.x=nyx.x;window.oldHP=nyx.hp;pBullets=[{kind:"beam",x:nyx.x,y:player.y-14,w:16,h:player.y,top:-20,bot:player.y-14,life:.5,dmg:3,_ht:0,_hit:[],seat:1}];updatePlay(1/60);}')
  ck(p.evaluate('()=>nyx.hp<oldHP&&!spaceTargets().some(t=>t._retinaId==="nyx-hull")'),'blind sustained laser hits cloaked Nyx without giving missile lock')
  p.evaluate('()=>{pBullets=[];window.beforeHP=R.ships.map(q=>q.hp);G.age=4;rg4GangStart(B,G);}')
  ck(p.evaluate('()=>G.gang&&!G.scene&&!B._noHit&&R.ships.every(q=>q._on5Guard?.hp>0)'),'Gang Mode grants live shields without cinematic freeze')
  shot(p,'live-gang-shield')
  p.evaluate('()=>{const q=R.ships[0];R.hit=q.i;rebelSquadDamage(B,q._on5Guard.hp+10);}')
  ck(p.evaluate('()=>!R.ships[0]._on5Guard&&R.ships[0].hp===beforeHP[0]'),'Gang projection breaks separately without damaging covered hull')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
  ck(p.evaluate('()=>!!j3State(B)'),'finale fixture uses actual three-encounter boss')
  p.evaluate('()=>{window.J=j3State(B);window.S=B._r30;on5FightStart(B);B._noHit=false;}')
  for phase in [0,1]:
   if phase:p.evaluate('()=>{j3Encounter(B,1);}')
   if phase:
    frames(p,160);shot(p,'ghost-intro');frames(p,150)
   else:shot(p,'drone-fight')
   p.evaluate('()=>{window.shotsBefore=0;window.shotFn=f1003bShot;f1003bShot=function(){const q=shotFn.apply(this,arguments);if(q&&!q.dead)shotsBefore++;return q;};eBullets=[];}')
   frames(p,1400)
   types=p.evaluate('()=>S.history.filter(q=>q.event==="attack")')
   report['phase'+str(phase)+'attacks']=types
   ck(p.evaluate('()=>shotsBefore>35&&S.history.filter(q=>q.event==="attack"&&q.encounter===J.encounter).length>=4'),'phase '+str(phase+1)+' emits damaging attacks across all four cycles')
   p.evaluate('()=>{f1003bShot=shotFn;}')
   shot(p,'phase'+str(phase+1)+'-attacks')
  p.evaluate('()=>{j3Encounter(B,2);}')
  frames(p,195);shot(p,'symbiote-void');frames(p,120);shot(p,'symbiote-emergence');frames(p,220)
  ck(p.evaluate('()=>ON5.draws.symbiote>0&&ON5.draws.fragments>0&&artCalls.some(c=>c.k.startsWith("on5_fragments"))'),'generated void and flipped fragments render using game context')
  p.evaluate('()=>{B.hp=J.max[0]*.63;j3Save(B);window.hostHP=B.hp;j3Mimic(B,5);window.knightMax=B.maxhp;B.hp=B.maxhp*.52;j3Save(B);window.knightHP=B.hp;j3Home(B);}')
  ck(p.evaluate('()=>B.hp===hostHP&&J.hp[5]===knightHP'),'Dracula returns to saved HP and retains wounded knight pool')
  p.evaluate('()=>{j3Mimic(B,5);S.mode="fight";B.enter=false;B._noHit=false;}');frames(p,1)
  ck(p.evaluate('()=>B.hp===knightHP&&B.maxhp>6150'),'returning knight retains HP with expanded donor budget')
  # Render the actual whole body in every pose, with independently mounted weapons.
  for i in range(8):
   p.evaluate('(i)=>{window.poseIndex=i;window.savedPose=on5KnightFrame;on5KnightFrame=()=>i;}',i)
   shot(p,'knight-pose-'+str(i));p.evaluate('()=>{on5KnightFrame=savedPose;}')
  ck(p.evaluate('()=>B.parts.map(p=>p.id).sort().join(",")==="core,shield,sword"&&artCalls.filter(c=>c.k.startsWith("on5_knight")).length>=8'),'all eight whole knight poses render with separate sword and shield')
  p.evaluate('()=>{gd4Create(B,5);window.K=cf4Knight(B);K.state="warn";S.on5ShieldCd=0;}');frames(p,180);shot(p,'knight-shield-bash')
  ck(p.evaluate('()=>S.on5KnightN>=1'),'Hammer donor gains independent shield-bash attack')
  p.evaluate('()=>{S.on5Knight=null;S.on5ShieldCd=0;K.state="warn";K.t=0;}');frames(p,110);shot(p,'knight-dark-code')
  ck(p.evaluate('()=>S.on5KnightN>=2&&S.on5Knight?.kind==="code"'),'knight projects shield and casts Dark Code')
  p.evaluate('()=>{on5Shield(B,"red",31);S.wallAge1003=1;const q=r30ShieldBounds(B);window.shieldHP=S.shield;window.shieldTarget=retinaBossTargets(B).find(t=>t._retinaId?.includes("code-wall"));shieldTarget._retinaHit(10);window.firstShieldHP=S.shield;}')
  ck(p.evaluate('()=>firstShieldHP===shieldHP-10'),'code wall loses exact damage rather than silently expiring')
  p.evaluate('()=>{shieldTarget._retinaHit(100);}')
  ck(p.evaluate('()=>S.shield===0&&!S.on5Shield&&CWD.effects.filter(f=>f.owner===B&&f.kind==="chip").length>=24'),'code shield reaches zero with 24 ballistic fragments')
  shot(p,'code-shield-shattered');p.evaluate('()=>{r30Clear(B);}')
  ck(p.evaluate('()=>CWD.effects.some(f=>f.owner===B&&f.kind==="shatter")'),'form cleanup preserves terminal shatter animation')
  p.evaluate('()=>{j3Mimic(B,1);S.mode="fight";B.enter=false;J.on5.supply=.01;}');frames(p,2)
  ck(p.evaluate('()=>powerups.some(p=>p._on5Pill&&p._on5Content==="furybomb")'),'finale periodically supplies a flash bomb pill')
  p.evaluate('()=>{const p=powerups.find(p=>p._on5Pill);breakContainer(p);}')
  ck(p.evaluate('()=>powerups.some(p=>p.kind==="furybomb"&&!p.dead)'),'breaking support pill produces usable flash bomb')
  # Each password goes through native difficulty/pilot setup and direct launch.
  codes=p.evaluate('()=>Object.keys(ON5_CODES)')
  for code in codes:
   v=p.evaluate('(code)=>{pwInput=code;submitPassword();const E=ON5_CODES[code],pending=ON5.pending;pilotIndex=PILOTS.findIndex(p=>p.key==="cole");startRun(E.stage);return{ok:!!pending&&run.stage===E.stage&&!!(E.role==="boss"?boss:subBoss),code,kind:(E.role==="boss"?boss:subBoss)?.kind,phase:j3State(boss)?.encounter,mimic:j3State(boss)?.mimic};}',code)
   report.setdefault('passwords',[]).append(v)
   ck(v['ok'] and (not code.startswith('FINAL') or v['phase']==int(code[-1])-1),code+' launches requested encounter')
  ck(not errors,'zero page and console errors');b.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(c['ok'] for c in report['checks']) and not errors else 1)
