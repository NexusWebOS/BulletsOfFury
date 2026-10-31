from pathlib import Path
import sys,json,http.server,hashlib
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/neural_night_storm_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));errors=[];checks=[];states=[]
def ck(name,value):checks.append({'name':name,'passed':bool(value)});print(('PASS 'if value else'FAIL ')+name,flush=True)
SETUP="""cfg=>{diffKey=cfg.rank||'furious';spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,6);B._r30.mode='fight';B.enter=B._noHit=false;B._r30.v18.arenaPhase=2;B.x=340;B.y=220;B._r30.v18.home={x:340,y:220};player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;run.armor=run.shield=0;player.x=340+(cfg.side||0);player.y=VH-65;DBGT.god=true;for(const k of Object.keys(Input.keys))Input.keys[k]=false;NB81.events=[];nb23Start(B,cfg.type||'codeGeysers');window.P=B._r30.v18.attack;}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank,n in [('normal',3),('hard',4),('furious',5)]:
   for side in [-1,1]:
    p.evaluate(SETUP,{'rank':rank,'side':side});base=p.evaluate('({hp:B.hp,goal:P.safeX,tell:P.tell,targets:P.targets})');p.evaluate('DBGT.god=false')
    for i in range(round((base['tell']+2.8+.4)*60)):
     p.evaluate('()=>{Input.keys.a=player.x>P.safeX+2;Input.keys.d=player.x<P.safeX-2;}');p.evaluate(STEP,1)
    q=p.evaluate('({dead:player.dead,x:player.x,hp:B.hp,releases:NB81.events.filter(e=>e.event==="lightning-release").length,targets:P.targets})');states.append({'rank':rank,'side':side,**q})
    ck(rank+(' left'if side<0 else' right')+' ordinary movement escapes storm without GOD',not q['dead']and abs(q['x']-base['goal'])<7)
    ck(rank+(' left'if side<0 else' right')+' original HP/count/cadence retained',q['hp']==base['hp']and q['releases']==n and all(abs(t['at']-i*{'normal':.40,'hard':.34,'furious':.29}[rank])<1e-6 for i,t in enumerate(q['targets'])))
  p.evaluate(SETUP,{});p.evaluate(STEP,45);p.screenshot(path=str(W/'charge-verified.png'))
  ck('One metal ground asterisk is rendered beneath the casting brain',p.evaluate('NB81.draws.asterisk>0&&NB81.warning.kind==="single-metal-asterisk"&&NB81.warning.y>B.y+100'))
  ck('Charge chooses authored pulsing 1015 glow frames',p.evaluate('Object.keys(NB81.draws).filter(k=>k.startsWith("glow_")).length>=3'))
  ck('Night arena is cloud-only with two world-anchored parallax rates',p.evaluate('NB81.scene.theme==="night-clouds"&&NB81.scene.worldX===0&&NB81.scene.far!==NB81.scene.near&&NB81.draws.sky>0&&NB81.draws.clouds>0'))
  p.evaluate('window.sceneX=NB81.scene.worldX;player.x+=120');p.evaluate(STEP,1);ck('Lateral player movement does not drag the night plate',p.evaluate('NB81.scene.worldX===sceneX'))
  before=p.evaluate('({t:P.t,clock:B._r30.clock,scene:NB81.scene,dim:NB81.dim})');p.evaluate("setState('paused')");p.evaluate(STEP,90);ck('Pause freezes charge, background and storm darkness',p.evaluate('({t:P.t,clock:B._r30.clock,scene:NB81.scene,dim:NB81.dim})')==before);p.evaluate('setState(GS.PLAY)')
  p.evaluate(STEP,65);p.screenshot(path=str(W/'eruption-verified.png'))
  ck('Screen darkens during storm without dimming the foreground warning/body',p.evaluate('NB81.dim===8'))
  ck('No individual rectangular geyser plates are rendered',p.evaluate('Object.entries(NB23.draws).filter(([k])=>k.includes("warn_geyser")).every(([,n])=>n===0)&&NB81.draws.boxesSuppressed>0'))
  ck('Targets vary horizontally and vertically rather than forming rows of boxes',p.evaluate('new Set(P.targets.map(q=>q.y)).size>=4&&Math.max(...P.targets.map(q=>q.x))-Math.min(...P.targets.map(q=>q.x))>200'))
  q=p.evaluate('''()=>{const expect=nb81Targets(P.seed,P.targets.length,P.bounds.left,P.bounds.right,P.bounds.top,P.safeLeft);return{repeat:expect.every((q,i)=>q.x===P.targets[i].x&&q.y===P.targets[i].y),saved:JSON.stringify(P.targets.map(q=>[q.x,q.y]))};}''');ck('A committed storm seed reproduces the exact original locations',q['repeat'])
  p.evaluate('player.x=camRightX()-30');p.evaluate(STEP,15);ck('Storm targets never chase the player after commitment',p.evaluate('JSON.stringify(P.targets.map(q=>[q.x,q.y]))')==q['saved'])
  p.evaluate('v18Clear(B);nb23Start(B,"codeGeysers");window.nb81Next=B._r30.v18.attack');ck('Next cast uses a different randomized eruption pattern',p.evaluate('JSON.stringify(nb81Next.targets.map(q=>[q.x,q.y]))')!=q['saved'])
  p.evaluate(SETUP,{});p.evaluate(STEP,70);p.evaluate('()=>{B._lastPart=B.parts[0];window.hpBefore=B.hp;modularHit(11);}');p.evaluate(STEP,1);p.screenshot(path=str(W/'hit-verified.png'))
  ck('Native damage still registers with an expiring white hit flash',p.evaluate('hpBefore-B.hp===11&&B.flash>0&&B.parts[0].flash>0'));p.evaluate(STEP,12);ck('White hit flash clears while charge animation continues',p.evaluate('B.flash<=0&&B.parts[0].flash<=0'))
  # Verify native plume damage from actual opaque source pixels, not a fake hit callback.
  p.evaluate(SETUP,{});p.evaluate(STEP,115)
  q=p.evaluate('''()=>{const q=P.targets[0],age=P.t-P.tell,a=nb23Cell('geyser',Math.floor(age/.85*NB23_ART.banks.geyser.length));let found=false;for(let y=Math.max(200,q.y-140);y<Math.min(VH-60,q.y+7)&&!found;y+=2)for(let x=q.x-20;x<q.x+20;x+=2)if(nb23PixelAt(a,q,x,y)){player.x=x;player.y=y;found=true;break;}DBGT.god=false;player.invuln=0;return{found,age};}''');p.evaluate(STEP,1);ck('Standing in actual lightning plume pixels causes native player death',q['found']and p.evaluate('player.dead'))
  p.evaluate(SETUP,{});p.evaluate(STEP,180);ck('Each staggered eruption emits exactly one lightning sound',p.evaluate('NB81.events.filter(e=>e.event==="lightning-release").length===5'))
  dimShot=Image.open(__import__('io').BytesIO(p.screenshot())).convert('RGB');dark=float(np.array(dimShot.crop((300,100,390,160))).mean())
  p.evaluate('v18Clear(B)');p.evaluate(STEP,1);ck('Cancelling clears storm ownership, darkness and pending cues',p.evaluate('!nb81Act(B)&&!B._r30.v18.attack&&NB81.dim===0&&NB81.audioOwner===null'))
  brightShot=Image.open(__import__('io').BytesIO(p.screenshot())).convert('RGB');bright=float(np.array(brightShot.crop((300,100,390,160))).mean());ck('Actual cloud pixels darken substantially during storm and recover after cancel',dark<bright*.75)
  p.evaluate(SETUP,{});p.evaluate('()=>{B._lastPart=B.parts[0];modularHit(B.hp);}');p.evaluate(STEP,435);ck('Native defeat returns home without healing the destroyed brain life',p.evaluate('B._r30.v18.form===0&&B._r30.mode==="fight"&&j3State(B).hp[6]===0&&!nb81Act(B)'))
  p.evaluate(SETUP,{'type':'eyeExpansion'});p.evaluate(STEP,100);ck('Approved full-width warm eye beams retain their existing owner',p.evaluate('!!nb80Act(B)&&!nb81Act(B)&&P.widthStep===5&&NB80.draws.beam_5>0'))
  p.evaluate(SETUP,{'type':'cloudAegis'});p.evaluate('()=>{P.t=P.tell+.4;window.hpBefore=B.hp;modularHit(25);}');ck('Finite cloud shield still absorbs native damage',p.evaluate('B.hp===hpBefore&&P.shield===P.maxShield-25&&!nb81Act(B)'))
  p.evaluate('()=>{v18Enter(B,2,1);B._r30.mode="fight";B.enter=B._noHit=false;}');p.evaluate(STEP,2);ck('Digital jungle helicopter remains under its separate owner',p.evaluate('hc79Own(B)&&!nb81Act(B)&&HC79.draws.ground>0'))
  p.evaluate('()=>{v18Enter(B,2,0);B._r30.mode="fight";B.enter=B._noHit=false;for(const i of V18.forms)if(i!==0)j3State(B).hp[i]=0;rd78Start(B);}');ck('Main-body Luminaire and other arenas remain separate',p.evaluate('!!rd78Act(B)&&!nb81Act(B)'))
  ck('No native page, asset or console errors',not errors);br.close()
finally:stop()
s=(R/'assets/neural_night_storm_art_1030.js').read_text();A=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
ck('All54 glow poses retain even cells and a common384px logical body',sum(map(len,A['banks'].values()))==54 and all(a['w']%2==a['h']%2==0 and a['logical']==[384,384]for rows in A['banks'].values()for a in rows))
ck('Night and cloud plates retain fixed even680px dimensions',all(Image.open(R/a['path']).size==(680,680)for a in A['arena'].values()))
ck('Core game engine remains byte-identical',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'errors':errors},indent=2));assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
