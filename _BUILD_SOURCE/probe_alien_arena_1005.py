"""Real Chromium pixels, attack routes and short live-engine recordings."""
from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import json, base64, io, sys
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/alien_arena_1005';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[],'clips':[]};errors=[];port,stop=sh.serve(str(R))
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def ticks(p,n):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){player.invuln=1e9+2;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(8)
def raw(p):return base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'))
def shot(p,n,bg=False):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);'+('ctx.save();const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);drawBG(0);ctx.restore();' if bg else 'drawWorld(0);')+'}')
 data=raw(p);(O/(n+'.png')).write_bytes(data);report['screens'].append(n);return Image.open(io.BytesIO(data)).convert('RGB')
def clip(p,n,seconds):
 ims=[]
 for f in range(seconds*6):
  ticks(p,10);ims.append(Image.open(io.BytesIO(raw(p))).convert('RGB').resize((480,512)))
 ims[0].save(O/(n+'.gif'),save_all=True,append_images=ims[1:],duration=167,loop=0,optimize=False)
 report['clips'].append({'name':n,'seconds':seconds,'fps':6,'audio':False})
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1200,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500);p.evaluate('()=>{aa5Warm();pw5Warm();r30Warm();gp4AceWarm();}')
  p.wait_for_function('()=>Object.values(AA5_ART).every(a=>a.every(c=>XART.rdy(c.key)))&&XART.rdy("bmfx_alert_red_impact_imminent")',timeout=120000,polling=50)
  ck(True,'all generated code/void/component cells decode in real Chromium')
  p.evaluate('()=>{window.artCalls=[];const get=XART.get,draw=ctx.drawImage,map=new Map();XART.get=function(k){const im=get.apply(this,arguments);if(im)map.set(im,k);return im;};ctx.drawImage=function(im){const k=map.get(im);if(k)artCalls.push({k,args:Array.from(arguments).slice(1)});return draw.apply(this,arguments);};}')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.J=j3State(B);window.S=B._r30;j3Encounter(B,2);}')
  ticks(p,50);shot(p,'void-expands');ticks(p,100);shot(p,'screen-engulfed');ticks(p,105);shot(p,'fiend-emerges');ticks(p,300)
  ck(p.evaluate('()=>S.mode==="fight"&&J.encounter===2&&AA5.draws.void>0&&AA5.draws.code>0&&J.aa5ArenaDrawn'),'full-view void reveals animated arena and giant fiend')
  p.evaluate('()=>{J.aa5Clock=5;}');a=shot(p,'arena-layer-a',True);p.evaluate('()=>{J.aa5Clock=5.55;}');b=shot(p,'arena-layer-b',True)
  diff=ImageChops.difference(a,b);green=sum(g>r*1.5 and g>bl*1.3 and g>45 for r,g,bl in a.getdata())
  box=(int(a.width*.43),int(a.height*.43),int(a.width*.57),int(a.height*.60));center=list(a.crop(box).getdata());dark=sum(max(q)<25 for q in center)/len(center)
  report['arenaPixels']={'green':green,'centralDarkRatio':dark,'movingPixels':sum(max(q)>10 for q in diff.getdata())}
  ck(green>150 and dark>.95,'central corridor stays black while perimeter code remains green')
  ck(report['arenaPixels']['movingPixels']>400,'real arena pixels animate between simulation timestamps')
  ck(p.evaluate('()=>{const t=J.aa5Clock;drawBG(0);drawBG(0);return J.aa5Clock===t;}'),'paused draw calls leave code and vortex clock unchanged')
  p.evaluate('()=>{S.attack=null;S.cd=0;J.attacks=0;J.aa5Clock=0;}');clip(p,'dracula-live',28)
  types=p.evaluate('()=>S.history.filter(q=>q.event==="draculaPattern").map(q=>q.type)');report['draculaAttacks']=types
  ck('aa5Void' in types and 'aa5Dive' in types,'Furious Dracula executes portal battery and committed body dive')
  shot(p,'dracula-attack')
  p.evaluate('()=>{j3Home(B);S.mode="fight";B.enter=false;B.hp=J.max[0]*.62;j3Save(B);window.hostHP=B.hp;}')
  for i in range(8):
   p.evaluate('(i)=>{j3Mimic(B,i);S.mode="fight";B.enter=false;}',i);ticks(p,90);shot(p,'copy-'+str(i))
   ck(p.evaluate('()=>aa5Arena(B)&&B.maxhp===J.max[J.active]&&J.aa5ArenaDrawn'),'copy '+str(i)+' keeps animated arena and accurate independent life')
   if i>0:
    ticks(p,720)
    ck(p.evaluate('(i)=>{const D=J.gp4Donors[i];return D&&D.aa5Visit>=12&&D.age<32&&S.mode==="fight";}',i),'copy '+str(i)+' runs its campaign controller beyond twelve seconds')
    if i!=5:
     ck(p.evaluate('(i)=>S.history.some(q=>q.event==="donorUpgrade"&&q.source===i)',i),'copy '+str(i)+' performs its warned alien ordnance upgrade')
  p.evaluate('()=>{j3Mimic(B,1);S.mode="fight";B.enter=false;}');ticks(p,2440)
  ck(p.evaluate('()=>S.mode==="transform1003j"&&J.gp4Donors[1].age>=31.7'),'Furious copied boss completes forty seconds before returning to host')
  p.evaluate('()=>{j3Home(B);}');ck(p.evaluate('()=>B.hp===hostHP'),'return to host retains its exact damaged HP')
  p.evaluate('()=>{j3Encounter(B,1);}');ticks(p,150);shot(p,'ghost-intro');ticks(p,170)
  ck(p.evaluate('()=>r30Parts(B).length===9&&new Set(retinaBossTargets(B).map(t=>t._retinaId)).size===9'),'ghost renders nine shapes with distinct live targeting anchors')
  shot(p,'ghost-modular')
  # Capture isolated exact-alpha white hits through the native game context.
  p.evaluate('()=>{B.flash=0;B.parts.forEach(p=>p.flash=0);S.attack=null;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#000";ctx.fillRect(0,0,VW,VH);j3Body(B);}')
  normal=Image.open(io.BytesIO(raw(p))).convert('RGB');p.evaluate('()=>{B.parts.forEach(p=>p.flash=.12);ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#000";ctx.fillRect(0,0,VW,VH);j3Body(B);}')
  white=Image.open(io.BytesIO(raw(p))).convert('RGB');white_hits=sum(min(q)>230 and min(q)-min(n)>35 for n,q in zip(normal.getdata(),white.getdata()))
  ck(white_hits>500,'ghost has visible native white hit pixels across its modules');report['whiteHitPixels']=white_hits
  p.evaluate('()=>{window.arm=B.parts.find(p=>p.id==="armL");B._lastPart=arm;modularHit(arm.hp+1);}');shot(p,'ghost-breakup')
  ck(p.evaluate('()=>arm.destroyed&&B.parts.find(p=>p.id==="clawL").destroyed&&D27_MODULE_DEBRIS.length>=2&&!r30Parts(B).some(v=>v.p.id==="armL")'),'ghost arm and claw detach into opaque burning spinning debris')
  p.evaluate('()=>{B.hp=B.maxhp*.49;S.attack=null;S.cd=0;S.seq=4;}');clip(p,'ghost-live',26);shot(p,'ghost-unbound')
  ghost_types=p.evaluate('()=>S.history.filter(q=>q.event==="attack"&&q.encounter===1).map(q=>q.type)');report['ghostAttacks']=ghost_types
  ck(all(t in ghost_types for t in ['ghostPinch','ghostCross','ghostWarp','ghostRail']) and p.evaluate('()=>S.aa5Unbound'),'ghost performs new physical/warp/rail signatures and Furious alternate reactor')
  p.evaluate('()=>{window.debrisBefore=D27_MODULE_DEBRIS.length;B.hp=0;r30Break(B);}')
  shot(p,'ghost-death')
  ck(p.evaluate('()=>S.aa5Collapsed&&D27_MODULE_DEBRIS.length>debrisBefore&&aa5GhostRig(B).length===0'),'ghost death breaks the remaining authored plates into opaque debris')
  p.evaluate('()=>{j3Encounter(B,0);S.mode="takeover";S.t=1.8;}');shot(p,'drone-consumed')
  p.evaluate('()=>{on5FightStart(B);S.seq=0;S.cd=0;}');clip(p,'mutated-drone-live',28)
  ck(p.evaluate('()=>S.history.some(q=>q.event==="attack"&&q.type==="hostCross")&&S.history.some(q=>q.event==="attack"&&q.type==="hostRoll")'),'mutated drone adds crossed cannon lanes and warned charge')
  p.evaluate(SETUP,{'stage':6,'kind':'warhive','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{whvAceSpawn(B);B._whv.mode="ace";window.A=B._whv.ace;A.st="fight";A.x=player.x;A.y=210;A.roll=A.somer=A.dash=A.desp=null;A.gunCd=A.mslCd=A.dashCd=A.rollCd=A.somerCd=999;eBullets=[];whvAceGuns(B,A,.22);}')
  ck(p.evaluate('()=>A._pw5Gun&&eBullets.length===0'),'elite turret rain starts with a real warning before any pellet')
  ticks(p,35);shot(p,'elite-turret-fov');ck(p.evaluate('()=>A._pw5Gun.t<A._pw5Gun.tell&&eBullets.length===0'),'elite charge window permits escape without immediate damage')
  ticks(p,42);shot(p,'elite-rain');ck(p.evaluate('()=>eBullets.some(p=>p.kind==="s6tracer")&&eBullets.length<=8'),'elite fires bounded staggered visible tracers after FOV')
  clip(p,'elite-live',12)
  p.evaluate('()=>{eBullets=[];B._whv.shots=[];player.x=worldWidth()/2;player.y=VH-110;window.danger={x:player.x,y:player.y-90,vx:0,vy:5,kind:"mg",w:7,h:7,t:0};window.safe={...danger,x:player.x+110};eBullets.push(danger,safe);pw5Collect();efxClock=.2;}');shot(p,'pellet-impact-warning')
  ck(p.evaluate('()=>PW5.threats.some(q=>q.p===danger)&&!PW5.threats.some(q=>q.p===safe)&&PW5.draws>0'),'only approaching collision-lane pellet glows with authored impact asterisk')
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};window.G=rg4Init(B);G.releaseAt=9999;G.rescueAt=9999;for(const q of R.ships){q.mode="fight";q.warp=0;q.x=player.x+(q.i-2)*75;q.y=180;q.rg4.cd=9999;q.rg4.act=null;}eBullets=[];const q=R.ships.find(q=>q.key==="rook");window.slug=rg4Round(q,Math.PI/2,4.5,"s6tracer",{_ra4Slug:true});player.x=slug.x;slug.y=player.y-100;pw5Collect();}')
  shot(p,'rebel-slug-warning');ck(p.evaluate('()=>PW5.threats.some(q=>q.p===slug)'),'Rebel heavy gun uses the same approaching-pellet warning')
  p.evaluate(SETUP,{'stage':1,'pilot':'cole'});ck(p.evaluate('()=>!aa5Arena(B)&&PW5.threats.length===0'),'arena and warnings clear when another mission begins')
  ck(not errors,'zero page and console errors');browser.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if all(c['ok'] for c in report['checks']) and not errors else 1)
