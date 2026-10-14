"""Native CP12 ambush health, arrival/fire and interruption verification."""
from pathlib import Path
import sys, json, socketserver, os
from playwright.sync_api import sync_playwright

R=Path(__file__).resolve().parents[1]
if not (R/'assets/game.js').exists():
    R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot
O=R/'_shots/cp12_health_1013'; O.mkdir(parents=True,exist_ok=True)
socketserver.TCPServer.request_queue_size=256
port,stop=shoot.serve(str(R))
report={'checks':[],'fixtures':[],'interruptions':[],'pageErrors':[],'consoleErrors':[]}
def check(name,ok,data=None):
    report['checks'].append({'name':name,'passed':bool(ok),'data':data})
    assert ok,(name,data)

PREP=r'''c=>{
 diffKey=c.d;DIFF=DIFFS[c.d];coopOn=c.coop;story=null;debugFight=null;
 waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;
 subBossActive=false;bossActive=false;warnT=0;if(wfx){wfx.fseq=null;wfx.fire=null;wfx.fireCd=9999;}
 stageTimer=1;VP12.next=9999;VP12.stage=run.stage;VP12.clock=1;
 CP12.next=9999;CP12.stage=run.stage;CP12.lastTimer=1;CP12.age=0;CP12.events=[];CP12.serial=c.side;
 enemies=[];eBullets=[];pBullets=[];particles=[];wm26Releases=[];
 EP13.owner=null;EP13.next=9999;EP13.clock=10;EP13.events=[];
 player.dead=false;player.invuln=1e9+2;player.x=camLeftX()+VW*.5;player.y=PLAY.y+PLAY.h*.85;
 for(const k in Input.keys)delete Input.keys[k];
 const type=run.stage===1?'s1jetDelta':'ash';
 const ordinary=spawnEnemy(type,camLeftX()+VW*.5,PLAY.y+PLAY.h*.25,{pattern:'straight'});
 window.ordinaryHp={hp:ordinary.hp,maxhp:ordinary.maxhp,type:ordinary.type};enemies=enemies.filter(e=>e!==ordinary);
 cp12Ambush();window.unit=enemies.find(e=>e._cp12&&!e.dead);
 window.cp12SeenBullets=new Set();window.cp12Draws=0;window.cp12History=[];
 return {ordinary:ordinaryHp,ambush:{hp:unit.hp,maxhp:unit.maxhp,type:unit.type},coop:coopActive()};
}'''
OBSERVE=r'''()=>{
 const u=unit,q=u._cp12;for(const b of eBullets)if(b._cp12)cp12SeenBullets.add(b);
 const r={t:q.t,scale:q.scale,round:q.round,visible:u.x>=camLeftX()-u.w/2&&u.x<=camRightX()+u.w/2&&u.y>=PLAY.y-u.h/2&&u.y<=PLAY.y+PLAY.h+u.h/2,dead:!!u.dead,dying:u._dyingT!=null,seen:cp12SeenBullets.size,hp:u.hp};
 cp12History.push(r);return r;
}'''

try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio'])
  p=browser.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:report['pageErrors'].append(str(e)))
  p.on('console',lambda m:report['consoleErrors'].append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('window.__bofFrames>4',timeout=120000)
  p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate('()=>{const old=drawEnemy;drawEnemy=function(e){if(e===window.unit)window.cp12Draws++;return old.apply(this,arguments);};}')
  for stage in ([int(os.environ['CP12_STAGE'])] if os.environ.get('CP12_STAGE') else [1,2]):
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=180000)
   for d in ['easy','normal','hard','furious']:
    for coop in [False,True]:
     for side in [0,1,2]:
      c={'d':d,'coop':coop,'side':side};hp=p.evaluate(PREP,c)
      key=f'stage{stage}-{d}-{"coop" if coop else "solo"}-side{side}'
      check(key+' family HP',hp['ordinary']['hp']==hp['ambush']['hp'] and hp['ordinary']['maxhp']==hp['ambush']['maxhp'],hp)
      # Co-op constructor equality is exhaustive; native motion uses solo fixtures.
      if coop:
       report['fixtures'].append({'stage':stage,**c,**hp});continue
      history=[]
      for i in range(57):
       err=p.evaluate(shoot.STEP,4);assert not err,(key,i,err)
       p.wait_for_timeout(1);s=p.evaluate(OBSERVE);history.append(s)
       if d=='normal' and side==0 and i in [7,25,38]:
        p.screenshot(path=str(O/f'{key}-{i}.png'))
      result=p.evaluate('()=>({events:CP12.events,draws:cp12Draws,seen:cp12SeenBullets.size,round:unit._cp12.round,scale:unit._cp12.scale,enemyDead:unit.dead,enemyDying:unit._dyingT,blocked:{bossActive,subBossActive,warnT,playerDead:player.dead,debugFight,wfx:!!wfx?.fseq},history:cp12History})')
      check(key+' native frame batches completed',True)
      check(key+' depth settles at normal scale',any(abs(h['scale']-1)<.001 and h['t']>=1.15 for h in history),result)
      check(key+' visible before launch',all(h['round']==0 for h in history if h['t']<2.2) and any(h['visible'] and h['t']<2.2 for h in history),result)
      check(key+' native rendered',result['draws']>100,result)
      rounds=3 if d=='furious' else 2
      check(key+' full missile volleys',result['round']==rounds and result['seen']==3*rounds,result)
      report['fixtures'].append({'stage':stage,**c,**hp,**result,'arrival':history[7],'beforeFire':history[25],'firing':history[38]})
      print(key,hp['ambush']['hp'],'HP',result['seen'],'missiles PASS',flush=True)
    # Each difficulty tests removal during tell and during release, both death paths.
    for mode in ['dead-before','dying-before','dead-after','dying-after']:
     hp=p.evaluate(PREP,{'d':d,'coop':False,'side':0})
     n=105 if mode.endswith('before') else 141
     for i in range(0,n,3):
      err=p.evaluate(shoot.STEP,3);assert not err,(stage,d,mode,err);p.wait_for_timeout(1)
     before=p.evaluate('()=>({round:unit._cp12.round,count:CP12.events.filter(e=>e.event==="rocket-volley").length})')
     p.evaluate('(mode)=>{if(mode.startsWith("dead-"))unit.dead=true;else unit._dyingT=0;}',mode)
     for i in range(30):
      err=p.evaluate(shoot.STEP,3);assert not err,(stage,d,mode,err);p.wait_for_timeout(1)
     after=p.evaluate('()=>({round:unit._cp12.round,count:CP12.events.filter(e=>e.event==="rocket-volley").length})')
     check(f'{stage}-{d}-{mode} no ghost volley',before==after,{'before':before,'after':after})
     report['interruptions'].append({'stage':stage,'difficulty':d,'mode':mode,'before':before,'after':after})
  browser.close()
 check('page errors',not report['pageErrors'],report['pageErrors'])
 check('console errors',not report['consoleErrors'],report['consoleErrors'])
finally:
 stop()
 report['summary']={'checks':len(report['checks']),'passed':sum(c['passed'] for c in report['checks']),'fixtures':len(report['fixtures']),'interruptions':len(report['interruptions'])}
 (O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps(report['summary']),flush=True)
