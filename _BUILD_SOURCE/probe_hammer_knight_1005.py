"""Focused native fixtures, not an unassisted campaign completion claim."""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,sys,base64,io
sys.path.insert(0,str(Path(__file__).resolve().parent));import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/hammer_knight_1005';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
checks=[];errors=[];port,stop=sh.serve(str(R))
def ck(v,n): checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def ticks(p,n):
 for i in range(0,n,15):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}',min(15,n-i));p.wait_for_timeout(4)
def snap(p,n):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 d=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'));(O/(n+'.png')).write_bytes(d);return Image.open(io.BytesIO(d)).convert('RGB')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate('()=>r30Warm()');p.wait_for_function('()=>Object.values(HK5_ART).flat().every(a=>XART.rdy(a.key))',timeout=120000)
  ck(True,'all 49 isolated native alpha cells decode')
  for form in [8,5]:
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'yuri','diff':'furious'})
   p.evaluate('(form)=>{window.S=B._r30;window.J=j3State(B);j3Encounter(B,2);j3Mimic(B,form);on5FightStart(B);window.D=gd4Create(B,form);}',form)
   if form==8:
    ticks(p,50);snap(p,'hammer-armor');ck(p.evaluate('()=>{const v=fmcRig(B)[0];return v.y-v.h*.5>PLAY.y+25&&v.y+v.h*.5<bottomHudLayout().rail.y-8&&v.key.startsWith("hk5_hammer");}'),'copied Hammer body stays visibly inside the arena during activation')
    ticks(p,170);snap(p,'hammer-activation-complete');ck(p.evaluate('()=>D.p._hammer.frArmor?.activated'),'copied Hammer finishes source chromium activation')
    p.evaluate('()=>{B.x=D.p.x=worldWidth()/2;B.y=D.p.y=220;D.p._hammer.hkSide=-1;hammerState(D.p,"hkSideTell");}');snap(p,'hammer-left-warning');ticks(p,73);snap(p,'hammer-left-strike')
    p.evaluate('()=>{const h=D.p._hammer;h.frArmor.hp=h.frArmor.max*.4;D.p.hp=B.hp;fr27Restore(D.p,.1,false,true);window.heal=h.recovery;window.target=retinaBossTargets(B).find(t=>t.kind==="hammer");}')
    snap(p,'hammer-heal-target');p.evaluate('()=>{if(target)retinaMissileDamage(target,25,{kind:"retinaMissile",tgt:target});}')
    ck(p.evaluate('()=>!!target&&heal.status==="cancelled"&&D.p._hammer.state==="fr_stun"'),'actual copied hammer Retina missile cancels healing and starts stun')
    snap(p,'hammer-heal-stopped')
    p.evaluate('()=>{hammerState(D.p,"throw");D.p._hammer.throw={phase:"return",x:B.x-150,y:B.y+150,t:0,angle:0,trail:[],reflected:true,speed:560};hammerBoomerangTick(D.p,1/60);}')
    ck(p.evaluate('()=>!!D.p._hammer.throw&&Math.hypot(D.p._hammer.throw.x-hammerGripPoint(D.p).x,D.p._hammer.throw.y-hammerGripPoint(D.p).y)>100'),'live thrown Hammer returns toward a separate hand anchor')
    snap(p,'hammer-thrown-return');p.evaluate('()=>D.p._hammer.throw=null')
    p.evaluate('()=>{D.p._hammer.frArmor.hp=0;B.hp=J.hp[8]=B.maxhp*.08;}');ticks(p,40);snap(p,'hammer-emergency');ticks(p,150)
    ck(p.evaluate('()=>D.p._hammer.gp4FailsafeSeen&&D.p._hammer.frArmor.rage'),'source emergency reserve hands off to aggressive copied stance')
   else:
    for kind,seconds in [('leapSlash',5),('shieldSmite',4),('shieldCode',5),('armageddon',8)]:
     p.evaluate('(kind)=>{B.x=worldWidth()/2;B.y=180;hk5AttackStart(B,kind);}',kind)
     ims=[]
     for i in range(seconds*5):
      ticks(p,12);ims.append(snap(p,kind+'-'+str(i)).resize((480,512)))
     ims[0].save(O/(kind+'.gif'),save_all=True,append_images=ims[1:],duration=200,loop=0)
    ck(p.evaluate('()=>HK5.draws.edgeArrow>0'),'mandatory side retinas and direction arrows rendered in native fight')
    ck(p.evaluate('()=>HK5.events.some(q=>q.kind==="leapSlash"&&q.phase==="rise")'),'native downward-to-rising sword combo completes')
  ck(p.evaluate('()=>Object.keys(HK5.draws).some(k=>k.startsWith("hk5_effects_8"))'),'generated code fireball animation actually renders')
  p.evaluate(SETUP,{'stage':8,'pilot':'yuri','diff':'furious'})
  p.evaluate('()=>{pwInput="HAMR8";submitPassword();startRun(8);window.B=boss;window.S=B._r30;window.J=j3State(B);stagePlan=[];enemies=[];player.invuln=1e9;BOFCinematicDirector.cancel();story=null;}')
  ticks(p,260);snap(p,'hammer-password')
  ck(p.evaluate('()=>J.mimic===8&&S.mode==="fight"&&gd4Create(B,8).p._hammer.frArmor.activated'),'HAMR8 launches the new copy through the actual password flow')
  # Proper musical route data is initialized through the live startRun wrapper.
  for route in ['regular','hammer','hama']:
   p.evaluate(SETUP,{'stage':5,'pilot':'yuri','diff':'furious'})
   p.evaluate('(route)=>{if(route!=="regular"){ht27Pending=true;if(route==="hama"){hamaPending=true;ht27Variant=HAMA_VARIANT;}else ht27Variant=null;startRun(5);}else spawnBoss(curStage.boss);window.B=boss;bossActive=true;story=null;fb2Intro=null;fb2Talk=null;BOFCinematicDirector.cancel();B.enter=B._noHit=false;B._hammer.balance0922=true;B.x=worldWidth()/2;B.y=180;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];player.invuln=1e9;if(B._hammerTime){const d=B._hammerTime;d.mode="attack";d.locked=d.shield=false;d.musicStarted=true;d.clock=40;ht27Song()?.pause();}B._hammer.mode="chaingun";hammerSpellStart(B);window.lockedXs=B._hammer.spellTargets.map(q=>q.x);player.x+=120;}',route)
   p.evaluate('()=>{for(let i=0;i<60;i++)HT27_BASE.hammerTick(B,1/60);}')
   ck(p.evaluate('()=>JSON.stringify(B._hammer.spellTargets.map(q=>q.x))===JSON.stringify(lockedXs)'),route+' actual initialized encounter has committed lightning columns')
   snap(p,route+'-bottom-lightning')
   p.evaluate('()=>{window.groundCalls=0;window.fovCalls=0;const g=hammerGroundReticleDraw,w=combatWarningDraw;hammerGroundReticleDraw=function(){groundCalls++;return g.apply(this,arguments);};combatWarningDraw=function(){fovCalls++;return w.apply(this,arguments);};hammerState(B,"mega_charge");B._hammer.t=.8;HT27_BASE.draw(B);hammerGroundReticleDraw=g;combatWarningDraw=w;}')
   ck(p.evaluate('()=>groundCalls===0&&fovCalls>0'),route+' super lightning warning draws FOV with no ground retinas')
   snap(p,route+'-super-fov')
  ck(not errors,'no native browser or renderer errors')
  br.close()
finally:
 stop();(R/'docs/qa/hammer_knight_1005.json').write_text(json.dumps({'checks':checks,'errors':errors,'limitations':'Protected encounter fixtures; no claim of an unassisted Furious clear.'},indent=2),encoding='utf-8')
if errors or any(not q['ok'] for q in checks):raise SystemExit(1)
