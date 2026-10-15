"""Native Forge and live-hit proof for the two recorded weapon complaints."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot,json,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/playthrough_1011/weapons';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio']);p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=1,pilot='maverick',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(1).ready&&pt11Ready("fire_spray")&&pt11Ready("sonic_pulse")}')
  p.evaluate('''()=>{window.WQ={};const Q=WQ;Q.base=forgePreviewNew(4,null,3);Q.fire=forgePreviewNew(4,'fire',3);Q.sonic=forgePreviewNew(1,'kinetic',3);
   for(const a of [Q.base,Q.fire,Q.sonic])a.pilot='maverick';
   Q.reset=function(el){ht27Stop();coopOn=false;diffKey='normal';DIFF=difficultyForRun('arcade','normal');run.mode='arcade';run.pilot='cole';run.stage=1;run.spaceMode=false;run.weapon=4;run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);run.wvars=WEAPONS.map(()=>null);run.forge=el?{4:{elem:el,lv:1}}:{};run.forgeForms={};run.infusion=null;forgeApply();run.lives=30;run.missileLevel=0;
    BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=special=thunderStorm=s6Opening=thaw=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];
    boss=subBoss=null;bossActive=subBossActive=false;subBossDone=subBossTriggered=bossWarned=true;warnT=0;warnKind=null;stagePlan=[];aiQueue=[];spawnClock=9999;
    enemies=[];eBullets=[];pBullets=[];powerups=[];particles=[];pImpacts=[];efxBursts=[];fb10Clouds=[];voids=[];geysers=[];zoneCols=[];zaps=[];explosions=[];l5Rocks=[];l5RockT=99999;setState(GS.PLAY);player.reset();player.dead=player.out=false;player.invuln=40002;player.x=worldWidth()/2;player.y=VH*.80;camX=player.x-VW/2;for(const k of Object.keys(Input.keys))Input.keys[k]=false;};
  }''')
  for batch in range(9):
   p.evaluate('()=>{for(let i=0;i<10;i++)for(const a of [WQ.base,WQ.fire,WQ.sonic])forgePreviewTick(a,260,300,1/60)}');p.wait_for_timeout(5)
  p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#080d18';ctx.fillRect(0,0,VW,VH);
   forgePreviewDraw(WQ.base,0,28,VW/2,VH-28);forgePreviewDraw(WQ.fire,VW/2,28,VW/2,VH-28);
   pcFontCenter('STANDARD FIRE',VW/4,17,10,'#fff',1);pcFontCenter('BLAST FURNACE',VW*.75,17,10,'#ffdc70',1);}''')
  p.locator('#screen').screenshot(path=str(OUT/'fire-forge-comparison.png'))
  q=p.evaluate('''()=>({errors:[WQ.base.err,WQ.fire.err,WQ.sonic.err],draws:PT11.draws.fire_spray,base:WQ.base.bullets.filter(b=>b.kind==='flame').map(b=>b._inf),fire:WQ.fire.bullets.filter(b=>b.kind==='flame').map(b=>b._inf)})''')
  check('Both Forge fire previews run with separate base/forged identities',not any(q['errors']) and q['draws']>0 and q['base']==[None] and q['fire']==['fire'],q)
  p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#080d18';ctx.fillRect(0,0,VW,VH);forgePreviewDraw(WQ.sonic,40,20,VW-80,VH-20);pcFontCenter('SONIC SHOCK FAN',VW/2,18,14,'#ffdc70',1);}''')
  p.locator('#screen').screenshot(path=str(OUT/'sonic-forge-preview.png'))
  check('Sonic Forge spread draws the authored pressure waves',p.evaluate('(PT11.draws.sonic_pulse||0)>0&&WQ.sonic.fired>1'))
  q=p.evaluate('''()=>{const frames=new Set(),b={kind:'flame',_inf:'fire',x:240,bot:450,top:242,lv:3,anim:0};
   for(let i=0;i<16;i++){b.anim=(i+.1)/24;const g=pt11FireGeometry(b);frames.add(g.f);flameDraw(b);}
   return{frames:frames.size,pivot:PT11_ART.fire_spray.every(a=>String(a.pivot)==='80,300'),length:(b.bot-flameSpanTop(b))/((b.bot-b.top)*PLAYER_FLAME_SCALE)};}''')
  check('Sixteen fire poses retain one nozzle and 22% extra visible reach',q['frames']==16 and q['pivot'] and abs(q['length']-1.22)<.001,q)
  p.evaluate('''()=>{WQ.reset('fire');pShoot();const b=pBullets.find(b=>b.kind==='flame');b.bot=player.y-14;b.top=b.bot-flameReach(b.lv);b.anim=.13;const g=pt11FireGeometry(b);
   WQ.geometry={top:g.top,bot:g.y};
   for(const [name,x,y] of [['extension',b.x,g.top+18],['outside',b.x+120,g.top+60],['behind',b.x,b.bot+35]]){
    const e=spawnEnemy('scout',x,y,{pattern:'straight'});e.x=x;e.y=y;e.hp=e.maxhp=10000;e.w=e.h=8;e._qaName=name;e._qx=x;e._qy=y;e.shoots=false;e._entry=0;}
  }''')
  for batch in range(6):
   p.evaluate('''()=>{for(let i=0;i<10;i++){player.invuln=40002;pShoot();for(const e of enemies){e.x=e._qx;e.y=e._qy;e.vx=e.vy=0;e.shoots=false;}updatePlay(1/60);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');p.wait_for_timeout(5)
  q=p.evaluate('enemies.map(e=>({name:e._qaName,hp:e.hp,burn:e._burn}))');vals={a['name']:a for a in q}
  check('Forged flame damages a real enemy inside its added reach',vals['extension']['hp']<10000,q)
  check('Targets beside and behind the authored flame remain unharmed',vals['outside']['hp']==10000 and vals['behind']['hp']==10000,q)
  p.locator('#screen').screenshot(path=str(OUT/'fire-live-contact.png'))
  q=p.evaluate('''()=>{const b=pBullets.find(b=>b.kind==='flame');b.anim=.2;const g=pt11FireGeometry(b);const far=flameHit(b,b.x,g.top+18,4,4);b._inf=null;const plain=pt11FireGeometry(b);const normal=flameHit(b,b.x,g.top+18,4,4);b._inf='ice';const ice=pt11FireGeometry(b);return{far,plain,normal,ice};}''')
  check('Unforging restores the ordinary reach; Ice keeps its own renderer',q['far'] and q['plain'] is None and not q['normal'] and q['ice'] is None,q)
  q=p.evaluate('''()=>{WQ.reset('fire');pShoot();updatePlay(1/60);const b=pBullets.find(b=>b.kind==='flame');const a=pt11FireGeometry(b);run.infusion={elem:'water',lv:1};const same=pt11FireGeometry(b);pShoot();return{same:a&&same&&a.top===same.top,after:pt11FireGeometry(b),element:b._inf};}''')
  check('Held flame follows its own element until the next trigger refresh',q['same'] and q['after'] is None and q['element']=='water',q)
  q=p.evaluate('''()=>{WQ.reset('fire');run.pilot='maverick';run.weapon=3;run.wvars[3]='mavhoming';run.infusion={elem:'kinetic',lv:5};pBullets=[];pShoot();return pBullets.map(b=>({kind:b.kind,lv:b.lv,inf:b._inf}));}''')
  check('Sonic artwork cannot upgrade or infuse Maverick homing lances',q and all(a['kind']=='mavlaser' and a['lv']==1 and a.get('inf') is None for a in q),q)
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] or errors else 0)
