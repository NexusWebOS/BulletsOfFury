"""Actual Chromium fixtures for the protected dialogue and orbital homecoming.
Uses shoot.py server/RAF handling. Does not claim a campaign clear or balance playtest.
"""
from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/feedback_1003h';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
TSET=(R/'_BUILD_SOURCE/probe_teamscene_1002.py').read_text(encoding='utf-8').split('SETUP = r"""')[1].split('"""')[0]
report={'checks':[],'screens':[]};errors=[]
def check(v,s):
 report['checks'].append({'ok':bool(v),'name':s});print(('PASS ' if v else 'FAIL ')+s,flush=True)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(name)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,30):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(30,n-i));p.wait_for_timeout(8)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':960})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.wait_for_function('()=>{h3Warm();return H3_ART.every(k=>XART.rdy("h3_"+k))&&furyShipReady();}',timeout=120000)
  check(p.evaluate('()=>H3_ART.every(k=>XART.rdy("h3_"+k))'),'all active generated assets loaded')
  # Capture the CURRENT hull through its actual live render function.
  p.evaluate(SETUP,{'stage':5,'pilot':'axel'})
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);ctx.imageSmoothingEnabled=false;furyShipDrawFlight(VW/2,VH/2,200,"axel",{key:"base"},0);}')
  (O/'current_furyship.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  # All flight sources, colors and cardinal views use actual source-cell blits.
  p.evaluate(SETUP,{'stage':6,'diff':'furious'})
  p.wait_for_function('()=>XART.rdy("fb2_stealth_red")&&XART.rdy("fb2_stealth_green")&&XART.rdy("fb2_stealth_orange")',timeout=60000)
  p.evaluate('()=>{window.blitKeys=[];const g=XART.get;XART.get=function(k){blitKeys.push(k);return g.apply(this,arguments)};window.fixtureJets=[];for(const [i,role]of ["red","green","orange"].entries()){const q=fb2FlightSpawn({direction:"south",role,x:camLeftX()+80+i*(viewW()-160)/2,y:150});q.y=160;fixtureJets.push(q);}window.plain=spawnEnemy("s1jetbomber_b",camLeftX()+viewW()/2,290,{});enemies=[...fixtureJets,plain];}')
  shot(p,'stealth-bombers')
  check(p.evaluate('()=>["red","green","orange"].every(k=>blitKeys.includes("fb2_stealth_"+k))'),'all approved bomber palette sources reach the game canvas')
  check(p.evaluate('()=>{blitKeys=[];drawEnemy(plain);return blitKeys.includes("fb2_stealth_red")}'),'untagged reinforcement bomber no longer falls back to old hull')
  # Natural Cole team scene entry, with both player control routes held down.
  for pilot in ['yuri','cole']:
   p.evaluate(TSET,{'pilot':pilot});p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;}')
   for i in range(35):
    frames(p,30)
    if p.evaluate('()=>fb2TalkActive()'):break
   check(p.evaluate('()=>fb2TalkActive()'),pilot+' naturally reaches team scene')
   p.evaluate('()=>{window.before={i:fb2Talk.i,t:stageTimer,x:player.x,y:player.y,hp:run.lives,bombs:run.bombs};window.foe={type:"s1jetbomber_b",x:90,y:100,t:0,hp:10,w:50,h:50,vy:2};enemies.push(foe);window.foeY=foe.y;window.held=Input.hold;Input.hold=function(s,a){return ["fire","bomb","special"].includes(a)||held.apply(this,arguments);};}')
   for key in ['KeyZ','Space','Enter']:p.keyboard.down(key)
   frames(p,45,'pShoot();useBomb();startSpecial();updatePlay(1/60);drawWorld(1/60);')
   check(p.evaluate('()=>fb2Talk.i===before.i&&fb2Talk.shown<fb2Talk.beats[0].text.length'),pilot+' confirm/fire cannot reveal or skip dialogue')
   check(p.evaluate('()=>foe.y===foeY&&stageTimer===before.t&&player.x===before.x&&player.y===before.y&&run.bombs===before.bombs&&!special&&eBullets.length===0&&pBullets.length===0'),pilot+' no AI, weapons, ammo spend or movement during dialogue')
   for key in ['KeyZ','Space','Enter']:p.keyboard.up(key)
   p.evaluate('()=>Input.hold=held');frames(p,170);shot(p,'team-'+pilot)
   p.evaluate('()=>window.demoEvidence={shots:0,release:false};')
   for i in range(290):
    frames(p,30,'updatePlay(1/60);if(fb2Talk?.demo){demoEvidence.shots=Math.max(demoEvidence.shots,fb2Talk.demo.fired);demoEvidence.release=demoEvidence.release||!!fb2Talk.demo.released;}drawWorld(1/60);')
    if p.evaluate('()=>s6Wing?.choice&&!fb2TalkActive()'):break
   check(p.evaluate('()=>s6Wing?.choice&&!fb2TalkActive()'),pilot+' complete reading sequence releases the existing route choice')
   if pilot=='cole':check(p.evaluate('()=>demoEvidence.shots>0&&demoEvidence.release&&run.weapon===1&&run.wlevel===3'),'scripted Callisto demonstration survives combat freeze and restores loadout')
  # Rebel intro runs on ordinary and Stage X contexts; each speaks in own portrait.
  p.evaluate(SETUP,{'stage':6,'diff':'furious'})
  p.evaluate('()=>{spawnBoss("rebelsquad");window.B=boss;B._be=null;B.enter=false;B.x=worldWidth()/2;B.y=150;}')
  check(p.evaluate('()=>!!B?._rebels'),'rebel encounter fixture exists')
  frames(p,250);shot(p,'rebel-voss')
  p.evaluate('()=>{window.introBefore={i:B._rebels.h3Intro.i,bombs:run.bombs,hp:B.hp};pShoot();useBomb();startSpecial();Audio.startMusic("boss6");}')
  check(p.evaluate('()=>pBullets.length===0&&run.bombs===introBefore.bombs&&!special'),'rebel approach rejects firing instead of erasing spent shots')
  check(p.evaluate('()=>H3.lastMusic==="stagex"'),'rebel boss6 requests route to Stage X track')
  p.evaluate('()=>{Audio.init();Audio.resume();Audio.startMusic("boss6");}')
  p.wait_for_function('()=>Snd.cur===Snd.music.stagex&&!Snd.cur.paused&&Snd.cur.readyState>=3',timeout=60000)
  check(p.evaluate('()=>Snd.cur.src.endsWith("LevelX.mp3")&&Snd.cur.loop'),'actual rebel encounter plays looping Stage X MP3')
  for stage in [1,3,5,7,9]:
   check(p.evaluate('(stage)=>{const saved=run.stage;run.stage=stage;Audio.startMusic("boss"+stage);run.stage=saved;return Snd.cur===Snd.music.stagex;}',stage),'rebel music stays Stage X in Level '+str(stage))
  seen=set()
  for i in range(130):
   frames(p,30)
   status=p.evaluate('()=>({done:!!B._rebels.frIntro.done,who:B._rebels.h3Intro.rows[B._rebels.h3Intro.i]?.who,t:B._rebels.h3Intro.t})')
   if status.get('who') in ['VOSS','NYX','ROOK','KAIA','JACE'] and status['who'] not in seen and status['t']>1:
    seen.add(status['who']);shot(p,'rebel-'+status['who'].lower())
   if status['done']:break
  check(len(seen)==5,'all five rebel pilots receive a readable portrait introduction')
  check(p.evaluate('()=>REBEL_KEYS.every(k=>XART.rdy("rr_portrait_"+k)&&XART.get("rr_portrait_"+k).width===256)'),'all five generated complete portrait frames are drawable')
  check(p.evaluate('()=>B._rebels.frIntro.done&&!B._noHit'),'rebel intro finishes naturally and releases boss vulnerability')
  check(p.evaluate('()=>B._rebels.ships.every(q=>q.x>=camLeftX()+50&&q.x<=camRightX()-50)'),'all five arrival ships remain inside frame')
  # Measured pitch rectangles visually checked at all four angles.
  p.wait_for_function('()=>XART.rdy("fr27_rebel_pitch")',timeout=60000)
  for f in range(4):
   p.evaluate('(f)=>{B._rebels.ships.forEach((q,i)=>{q.x=camLeftX()+60+i*(viewW()-120)/4;q.y=180+(i%2)*130;q.frSomersault=true;q.evadeT=.38*(1-(f+.2)/4);q.rfHeading=null;});}',f)
   shot(p,'rebel-pitch-'+str(f))
  # Requested balance is scoped to campaign Hammer armor.
  for diff in ['normal','furious']:
   p.evaluate(SETUP,{'stage':5,'pilot':'yuri','diff':diff})
   p.evaluate('()=>{spawnBoss(curStage.boss);window.B=boss;B._be=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=160;window.A=fr27BeginArmor(B);}')
   check(p.evaluate('()=>Math.abs(A.max-(diffKey==="furious"?Math.round(B.maxhp*.75):B.maxhp*.3))<.001&&B.hp===B.maxhp'),diff+' armor target; main boss health unchanged')
  # The raw artwork and the portrait alias both pass through the engine's own draw.
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#030811";ctx.fillRect(0,0,VW,VH);dlgBox({who:"CRONOS",portrait:false,portraitKey:"fb2_hammer_avatar",full:"NOW, LET US DANCE!",shown:"NOW, LET US DANCE!",forceShown:true,pw:VW-24,y:180});}')
  (O/'hammer-avatar.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  check(p.evaluate('()=>XART.rdy("fb2_hammer_avatar")&&XART.get("fb2_hammer_avatar").width===XART.get("h3_hammer_portrait").width'),'Hammer dialogue resolves to the regenerated actual head')
  p.evaluate('()=>{fb2Intro=null;B.hp=0;bossDie();}')
  check(p.evaluate('()=>!!H3.ending&&boss.dead&&bossDefeated'),'actual Hammer defeat starts ending and preserves defeat/reward path')
  for name,n in [('orbital-overhead',150),('earth-surface',240),('hammer-face',240),('hammer-turn',105),('hammer-shock',95),('hammer-explosion',80),('aftermath-color',180),('aftermath-mid',100),('aftermath-mono',130),('welcome-earth',150)]:
   frames(p,n);shot(p,name)
  # Same frozen geometry; only chroma changes, verified on Chromium output pixels.
  chroma=p.evaluate('()=>{const c=document.createElement("canvas");c.width=320;c.height=180;const g=c.getContext("2d");return [0,2.8,5.5].map(t=>{h3AftermathDraw(g,0,0,320,180,t);const d=g.getImageData(0,0,320,180).data;let sum=0;for(let i=0;i<d.length;i+=4)sum+=Math.max(d[i],d[i+1],d[i+2])-Math.min(d[i],d[i+1],d[i+2]);return sum/(d.length/4);});}')
  report['aftermathChroma']=chroma;check(chroma[0]>chroma[1]>chroma[2] and chroma[2]<.01,'static aftermath smoothly reaches true monochrome')
  check(p.evaluate('()=>state===GS.PLAY&&H3.ending&&H3.ending.events.has("head-blast")'),'ending owns the full timeline through animated facial destruction')
  p.evaluate('()=>window.welcomes=new Set();')
  for i in range(110):
   frames(p,30,'if(H3.ending?.phase==="welcome")welcomes.add(H3_CHEERS[H3.ending.cheer]?.[0]);updatePlay(1/60);drawWorld(1/60);')
   if p.evaluate('()=>H3.ending?.phase==="descent"'):break
  check(p.evaluate('()=>H3.ending?.cheer===9'),'all nine pilots finish cheering before descent')
  frames(p,180);shot(p,'earth-descent');frames(p,260);shot(p,'earth-arrival');frames(p,95);shot(p,'earth-fade');frames(p,100)
  check(p.evaluate('()=>state===GS.STAGECLEAR&&!H3.ending'),'Earth descent fades and reaches normal Stage Clear')
  check(not errors,'no page or console errors')
  b.close()
finally:
 stop();report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'passed':sum(c['ok'] for c in report['checks']),'failed':sum(not c['ok'] for c in report['checks']),'errors':errors}),flush=True)
raise SystemExit(1 if errors or any(not c['ok'] for c in report['checks']) else 0)
