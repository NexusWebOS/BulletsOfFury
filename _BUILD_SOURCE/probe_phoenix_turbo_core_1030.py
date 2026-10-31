from pathlib import Path
import sys,json,http.server,hashlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/phoenix_turbo_core_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));checks=[];errors=[];states=[]
def ck(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
SETUP="""cfg=>{diffKey=cfg.rank||'furious';spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,2);B._r30.mode='fight';B.enter=B._noHit=false;B._r30.v18.arenaPhase=2;B.x=340;B.y=174;B._r30.v18.home={x:340,y:174};window.Q=ph21State(B);Q.cool=0;Q.action=null;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;run.armor=run.shield=0;player.x=340;player.y=VH-65;DBGT.god=true;pBullets=[];eBullets=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;PH82.events=[];window.P=ph82Start(B,cfg.kind||'guns');}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank in ['normal','hard','furious']:
   p.evaluate(SETUP,{'rank':rank});p.evaluate(STEP,185);s=p.evaluate('({events:PH82.events,shots:eBullets.filter(q=>q._ph82Owner===B).map(q=>({vx:q.vx,vy:q.vy,intercept:enemyOrdnanceCanIntercept(q)})),hp:B.hp})');states.append({'rank':rank,**s});rounds=[e for e in s['events']if e['event']=='turbo-round']
   ck(rank+' turbo guns emit rapid paired rounds from both cannons',len(rounds)>=20 and set(e['id']for e in rounds)=={'cannonL','cannonR'})
   ck(rank+' all four actual barrel mouths fire in alternating pairs',all(set(e['barrel']for e in rounds if e['id']==id)=={0,1}for id in ['cannonL','cannonR']))
   ck(rank+' cannon bullets remain straight and cannot be intercepted',len(s['shots'])>0 and all(q['vx']==0 and q['vy']>5 and not q['intercept']for q in s['shots']))
   for side in [-1,1]:
    p.evaluate(SETUP,{'rank':rank});p.evaluate('()=>{DBGT.god=false;window.goal=340+110*'+str(side)+';}')
    for i in range(240):p.evaluate('()=>{Input.keys.a=player.x>goal+2;Input.keys.d=player.x<goal-2;}');p.evaluate(STEP,1)
    ck(rank+(' left'if side<0 else' right')+' parallel gun lanes can be escaped without GOD',not p.evaluate('player.dead'))
   for side in [-1,1]:
    p.evaluate(SETUP,{'rank':rank,'kind':'core'});p.evaluate('DBGT.god=false')
    while not p.evaluate('P.locked'):p.evaluate(STEP,1)
    p.evaluate('''side=>{const at=ph82Socket(B,'core'),a=PH82_ART.directions[P.dir]*Math.PI/180,x=at.x+Math.cos(a)/Math.sin(a)*(player.y-at.y);window.goal=clamp(x+side*90,camLeftX()+30,camRightX()-30);}''',side)
    for i in range(150):p.evaluate('()=>{Input.keys.a=player.x>goal+2;Input.keys.d=player.x<goal-2;}');p.evaluate(STEP,1)
    ck(rank+(' left'if side<0 else' right')+' committed core beam can be escaped without GOD',not p.evaluate('player.dead'))
  p.evaluate(SETUP,{'kind':'core'});p.evaluate(STEP,48);p.screenshot(path=str(W/'charge-verified.png'))
  ck('Chest core draws multiple source-authored1015 glow levels',p.evaluate('Object.keys(PH82.draws).filter(k=>k.startsWith("core_")).length>=3'))
  ck('Lava sides stay at the exact left and right visible edges',p.evaluate('PH82.arena.left===Math.floor(camLeftX())&&PH82.arena.right===Math.ceil(camRightX())-48&&PH82.arena.width===48'))
  first=p.evaluate('({...PH82.arena})');p.evaluate('player.x+=100');p.evaluate(STEP,25);second=p.evaluate('({...PH82.arena})');ck('Animated side strips remain edge-anchored after camera movement',second['left']==p.evaluate('Math.floor(camLeftX())')and second['right']==p.evaluate('Math.ceil(camRightX())-48'))
  ck('Side structures animate and scroll independently of lava',second['wallY']!=first['wallY']and second['lavaY']!=first['lavaY']and second['wallY']!=second['lavaY'])
  frozen='({t:P.t,age:Q.age,x:B.x,y:B.y,frame:PH82.arena.frame,lavaY:PH82.arena.lavaY,wallY:PH82.arena.wallY})';before=p.evaluate(frozen);p.evaluate("setState('paused')");p.evaluate(STEP,60);ck('Pause freezes body, charge and both arena animation clocks',p.evaluate(frozen)==before);p.evaluate('setState(GS.PLAY)')
  p.evaluate(STEP,35);p.screenshot(path=str(W/'beam-verified.png'));ck('Laser releases once from the measured chest core',p.evaluate('PH82.events.filter(e=>e.event==="core-beam").length===1&&Object.keys(PH82.draws).some(k=>k.startsWith("beam_"))'))
  ck('No cannon-owned Phoenix laser renderer is called',p.evaluate('!(PH20.draws.beam>0)'))
  origin=p.evaluate('ph82Socket(B,"core")');p.evaluate('window.hpBefore=B.hp;B._lastPart=ph21Part(B,"cannonL");modularHit(11)');p.evaluate(STEP,1);p.screenshot(path=str(W/'hit-verified.png'));ck('Real cannon damage retains native body/part hit flash',p.evaluate('hpBefore-B.hp===11&&B.flash>0&&ph21Part(B,"cannonL").flash>0'))
  p.evaluate(STEP,12);ck('Native white hit flash expires while core light continues',p.evaluate('B.flash<=0&&ph21Part(B,"cannonL").flash<=0'))
  p.evaluate(SETUP,{'kind':'core'});p.evaluate(STEP,104);p.evaluate('''()=>{const at=ph82Socket(B,'core'),a=PH82_ART.directions[P.dir]*Math.PI/180;player.y=447;player.x=at.x+Math.cos(a)/Math.sin(a)*(player.y-at.y);DBGT.god=false;player.invuln=0;}''');p.evaluate(STEP,1);ck('Standing in the actual core beam causes native player death',p.evaluate('player.dead'))
  p.evaluate(SETUP,{});p.evaluate(STEP,95);p.evaluate('()=>{B._lastPart=ph21Part(B,"cannonL");modularHit(ph21Part(B,"cannonL").hp);}');p.evaluate(STEP,60);ck('A destroyed cannon stops firing and selects the intact whole-body damaged bank',p.evaluate('!ph21Alive(B,"cannonL")&&ph82Dead(B)===1&&ph82Frame(B).pose===ph82Pose(B).phase+"_"+ph82Pose(B).f'))
  times=p.evaluate('PH82.events.filter(e=>e.event==="turbo-round"&&e.id==="cannonL").map(e=>e.clock)');ck('Broken left cannon has no delayed launches',len(times)==0 or max(times)<p.evaluate('B._r30.clock')-.8)
  p.evaluate('()=>{B._lastPart=ph21Part(B,"cannonR");modularHit(ph21Part(B,"cannonR").hp);}');ck('Destroying both pods preserves native swoon transition and cancels core/gun fields',p.evaluate('Q.stage==="swoon"&&!ph82Full(B)&&!B._r30.v18.attack'))
  p.evaluate(STEP,220);ck('Existing authored swoon controller remains reachable',p.evaluate('Q.stage==="swoon"&&!!Q.action&&["recede","corner","dive","return"].includes(Q.action.mode)'))
  p.evaluate(SETUP,{});p.evaluate('Q.action=null;B._r30.v18.attack=null;Q.cool=.9;ph82State(B).goal=null;pBullets=[{x:B.x-12,y:B.y+180,vy:-5,dead:false}];ph82Dodge(B);window.startX=B.x;window.goalX=ph82State(B).goal.x;');p.evaluate(STEP,40);ck('Evasion reacts to visible incoming fire and makes the player chase the guns',p.evaluate('goalX>startX&&B.x>startX+25&&PH82.events.some(e=>e.event==="evade"&&e.visibleThreat)'))
  p.evaluate(SETUP,{});positions=[]
  for i in range(360):p.evaluate(STEP,1);positions.append(p.evaluate('[B.x,B.y]'))
  ck('Evasive movement has bounded speed without teleports',max(abs(b[0]-a[0])for a,b in zip(positions,positions[1:]))<3 and max(abs(b[1]-a[1])for a,b in zip(positions,positions[1:]))<2)
  p.evaluate(SETUP,{'kind':'core'});p.evaluate('v18Clear(B)');ck('Clear removes pending beam ownership and live cannon rounds',p.evaluate('!Q.action&&!B._r30.v18.attack&&eBullets.every(q=>q._ph82Owner!==B||q.dead)'))
  p.evaluate(SETUP,{});p.evaluate('B._r30.v18.donorAge=47;Q.action=null;B._r30.v18.attack=null;Q.cool=.5;');p.evaluate(STEP,1);ck('Native timed live-copy return is preserved',p.evaluate('B._r30.mode!=="fight"'))
  p.evaluate(SETUP,{});p.evaluate('()=>{for(const id of ["cannonL","cannonR"]){B._lastPart=ph21Part(B,id);modularHit(ph21Part(B,id).hp);}for(const id of ["wingL","wingR","clawL","clawR","head"]){B._lastPart=ph21Part(B,id);modularHit(ph21Part(B,id).hp);}B._lastPart=ph21Part(B,"core");modularHit(B.hp);}');p.evaluate(STEP,435);ck('Native copied-life defeat downloads home without restoring its HP',p.evaluate('j3State(B).hp[2]===0&&B._r30.v18.form===0&&B._r30.mode==="fight"'))
  p.evaluate('()=>{v18Enter(B,2,6);B._r30.mode="fight";B.enter=B._noHit=false;nb23Start(B,"codeGeysers");}');p.evaluate(STEP,3);ck('New brain night storm remains with its existing owner',p.evaluate('!!nb81Act(B)&&NB81.scene.theme==="night-clouds"'))
  p.evaluate('()=>{v18Enter(B,2,1);B._r30.mode="fight";B.enter=B._noHit=false;}');p.evaluate(STEP,2);ck('Digital-jungle helicopter remains with its existing owner',p.evaluate('hc79Own(B)&&HC79.draws.ground>0'))
  p.evaluate(SETUP,{});p.evaluate('()=>{for(const i of V18.forms)if(i!==2)j3State(B).hp[i]=0;for(const id of ["cannonL","cannonR"]){B._lastPart=ph21Part(B,id);modularHit(ph21Part(B,id).hp);}B._lastPart=ph21Part(B,"core");modularHit(B.hp);}');p.evaluate(STEP,190)
  ck('Last Phoenix defeat retires surviving wings into native zero-HP final anatomy',p.evaluate('B._r30.mode==="v19FinalReform"&&B.parts.map(p=>p.id).join() === "core,left,right"&&B.parts.every(p=>p.hp===0)&&V18.forms.every(i=>j3State(B).hp[i]===0)'))
  p.evaluate(STEP,240);ck('Last Phoenix handoff reaches native final death with no stale part drawing',p.evaluate('B._r30.mode==="dr5Death"&&B.hp===0'))
  ck('No native page, draw or asset errors',not errors);br.close()
finally:stop()
s=(R/'assets/phoenix_turbo_core_art_1030.js').read_text(encoding='utf8');A=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
ck('All467 authored frames use even cells and stable logical canvases',sum(map(len,A['banks'].values()))==467 and all(a['w']%2==a['h']%2==0 for rows in A['banks'].values()for a in rows))
ck('Lava source palette is visibly darker while keeping its drawing',float(np.array(Image.open(R/A['arena']['lava'][0]['path']))[:,:,:3].mean())<35)
ck('All23 whole source poses retain both cannon sockets and measured core',len(A['poses'])==23 and all(len(q['sockets']['cannonL'])==len(q['sockets']['cannonR'])==2 and len(q['core'])==2 for q in A['poses'].values()))
ck('Core engine remains byte-identical',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'errors':errors},indent=2));assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
