from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/enemy_patterns_1013';O.mkdir(parents=True,exist_ok=True);errors=[];rows=[];stuns=[];port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  for name in ['msedge','chrome','firefox']:
   b=(pw.firefox.launch() if name=='firefox' else pw.chromium.launch(channel=name,args=['--mute-audio']));p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=90000);p.evaluate(shoot.TRAP_RAF)
   if not p.evaluate('typeof EP13!=="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/enemy_patterns_1013.js')
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':False});p.wait_for_function('()=>{stageLoadTick();ep13Warm();return stageLoadReady(5)&&ep13ReadyArt()}',timeout=180000)
   p.evaluate('()=>{story=null;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;EP13.next=0;EP13.clock=2;for(const k in Input.keys)delete Input.keys[k];pBullets=[];eBullets=[];enemies=[];}')
   # Real shield-break object freezes native tick. It must also cancel active damage globally.
   stun=p.evaluate('''()=>{const e=spawnEnemy('s5frigate',camLeftX()+VW*.5,PLAY.y+120,{});e.hp=e.maxhp=50000;e._ai27={seen:1,visible:true,flinch:0};player.dead=false;player.x=e.x;player.y=PLAY.y+PLAY.h*.8;player.invuln=0;run.shield=3;EP13.owner=null;ep13Start(e,'charge');e._ep13.phase='fire';e._ep13.t=e._ep13.profile.tell+.4;e._ep13.angle=Math.PI/2;const beam=ep13Beam(e);player.x=beam.x;const wouldHit=ep13BeamTouches(beam,player);enemyShieldStunStart(e,{max:20,once:false},null,true);const harmless=!ep13Beam(e);ep13HitSeats();const immediateNoHit=run.shield===3;updatePlay(1/60);const globalCancelled=!e._ep13&&!EP13.owner,stillNoHit=run.shield===3;const cannotRestart=!ep13CanStart(e);return {wouldHit,harmless,immediateNoHit,globalCancelled,stillNoHit,cannotRestart};}''');stun['browser']=name;stuns.append(stun);assert all(v for k,v in stun.items() if k!='browser'),stun;print('stun',name,stun,flush=True)
   difficulties=['easy','normal','hard','furious'] if name=='msedge' else ['furious']
   for d in difficulties:
    for kind in ['sweep','charge','ring','missile']:
     p.evaluate(shoot.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':False});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}',timeout=180000)
     p.evaluate('()=>{story=null;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;}')
     p.evaluate('c=>{diffKey=c.d;DIFF=DIFFS[c.d];enemies=[];eBullets=[];pBullets=[];particles=[];l5Rocks=[];l5RockT=9999;EP13.owner=null;EP13.next=0;EP13.clock=10;EP13.events=[];player.dead=false;player.alive=true;player.invuln=0;player.x=camLeftX()+VW*.5;player.y=PLAY.y+PLAY.h*.83;run.lives=3;run.shield=0;run.speedLevel=0;run._megaShield=null;for(const k in Input.keys)delete Input.keys[k];window.ep13Safe=spawnEnemy("s5frigate",camLeftX()+VW*.48,PLAY.y+PLAY.h*.24,{});const e=ep13Safe;e.hp=e.maxhp=50000;e._ai27={seen:1,visible:true,flinch:0};e._stagger=0;ep13Start(e,c.kind);}',{'d':d,'kind':kind})
     for i in range(22):
      p.evaluate('kind=>{const left=kind!=="ring"&&ep13Safe._ep13?.t>.2&&player.x>camLeftX()+66;for(const key of keybindFor(1).left||[])Input.keys[key]=left;}',kind)
      err=p.evaluate(shoot.STEP,10);assert not err,err;p.wait_for_timeout(3)
     row=p.evaluate('()=>({alive:!player.dead,lives:run.lives,shield:run.shield,released:EP13.events.some(e=>e.event==="release"),x:player.x,y:player.y})');row.update(browser=name,difficulty=d,pattern=kind);rows.append(row);assert row['alive'] and row['lives']==3 and row['released'],row;print('escape',name,d,kind,'PASS',flush=True)
   p.screenshot(path=str(O/f'{name}-final-safety.png'));b.close()
finally:stop()
(O/'safety-verification.json').write_text(json.dumps({'escapes':rows,'shieldStun':stuns,'errors':errors},indent=2));assert not errors,errors
print('PASS',len(rows),'unshielded, base-speed escape fixtures; shield stun in all browsers')
