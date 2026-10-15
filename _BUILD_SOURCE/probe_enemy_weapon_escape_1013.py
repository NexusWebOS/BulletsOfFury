from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/enemy_weapon_identity_1013';rows=[];errors=[];port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=90000);p.evaluate(shoot.TRAP_RAF)
  for stage,typ,kind in [(7,'mm1003_riflelocust','rifle'),(9,'s9beacon','shards')]:
   for d in ['easy','normal','hard','furious']:
    p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':False});p.wait_for_function('(n)=>{stageLoadTick();ep13Warm();return stageLoadReady(n)&&ep13ReadyArt()&&XART.rdy("warpprismshard_0")}',arg=stage,timeout=180000)
    p.evaluate('c=>{diffKey=c.d;DIFF=DIFFS[c.d];story=null;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;enemies=[];eBullets=[];pBullets=[];particles=[];EP13.owner=null;EP13.next=9999;EP13.clock=10;EP13.events=[];player.dead=false;player.invuln=0;player.x=camLeftX()+VW*.5;player.y=PLAY.y+PLAY.h*.83;run.lives=3;run.shield=0;run.speedLevel=0;run._megaShield=null;for(const k in Input.keys)delete Input.keys[k];window.unit=spawnEnemy(c.type,camLeftX()+VW*.5,PLAY.y+PLAY.h*.22,{});unit.hp=unit.maxhp=50000;unit._ai27={seen:1,visible:true,flinch:0};unit._stagger=0;if(unit._mm1003)unit._mm1003.phase="rest";ep13Start(unit,c.kind);}',{'d':d,'type':typ,'kind':kind})
    for i in range(48):
     p.evaluate('kind=>{const left=kind==="rifle"&&unit._ep13?.t>.2&&player.x>camLeftX()+66;for(const k of keybindFor(1).left||[])Input.keys[k]=left;}',kind)
     err=p.evaluate(shoot.STEP,5);assert not err,err;p.wait_for_timeout(1)
    row=p.evaluate('()=>({alive:!player.dead,lives:run.lives,shield:run.shield,release:EP13.events.some(e=>e.event==="release"),x:player.x,y:player.y})');row.update(stage=stage,difficulty=d,type=typ);rows.append(row);assert row['alive'] and row['lives']==3 and row['release'],row;print('escape',stage,d,typ,'PASS',flush=True)
  b.close()
finally:stop()
(O/'escape-verification.json').write_text(json.dumps({'escapes':rows,'errors':errors},indent=2));assert not errors,errors
print('PASS',len(rows),'native base-speed unshielded weapon escapes')
