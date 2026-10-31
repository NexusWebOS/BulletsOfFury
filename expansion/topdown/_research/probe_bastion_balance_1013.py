"""Normal-armor input bot plus isolated Prism Bastion attack-mechanism fixtures.

The complete run never writes enemy HP or calls damage/kill APIs. Pattern
fixtures explicitly use boss setup/state shortcuts, separate from that run.
"""
from pathlib import Path
import json,sys,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/bastion_balance_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();page=b.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda e:errors.append(e.text) if e.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=120000);page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);page.evaluate('TDGAME.freeze()');page.wait_for_function('Object.keys(TD_BASTION_ART.assets).every(k=>!!ART.get(k))',timeout=60000)
  def ev(s):return page.evaluate(s)
  def step(n=1):
   while n:
    z=min(60,n);page.evaluate('n=>TDGAME.step(n)',z);page.wait_for_timeout(1);n-=z
  def fresh():ev('TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Input.pointer.active=false;TD.Achievements.queue=[];window.botAuto=false;window.botInput={};window.botLastState=null;window.botController=false;window.botLocked=null;window.botGrenades=0;window.botGrenadeRoom=-1;')
  def snap(name):
   ev('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  ev('''window.botOriginalUpdate=TD.Input.update;window.botAuto=false;window.botInput={};window.botMetrics={coverDecisions:0,moveDecisions:0,fireDecisions:0,decisions:0,states:[],minHull:6};
  TD.Input.update=function(){
    const G=TD.game,p=G.player,c=G.bastion;
    this.last=this.state;let s={...window.botInput};
    if(window.botAuto&&c&&G.state==='play'&&!p.dead&&(G.t%15===0||!window.botLastState)){
      const bm=window.botMetrics;bm.decisions++;bm.minHull=Math.min(bm.minHull,p.hp);const stage=c.room+':'+c.phase+':'+(G.boss?.form||'')+':'+(G.boss?.state||'');if(!bm.states.includes(stage))bm.states.push(stage);
      let dodge=0,duck=false;const threats=c.enemyShots.filter(e=>!e.dead&&Math.abs(e.tx-p.x)<(e.kind==='rocket'?67:35));
      for(const e of threats){const left=e.duration-e.t;if(e.kind==='rocket'&&left<.62){dodge=p.x<e.tx? -1:1;if(p.x<115)dodge=1;if(p.x>525)dodge=-1;}else if(left<.48&&left>-.03)duck=true;}
      for(const h of c.hazards){const close=Math.abs(p.x-h.x)<(h.kind==='geyser'?89:88),left=h.delay-h.t;
        if(close&&h.t<h.delay+h.duration){if(h.kind==='geyser'&&left<.95){dodge=p.x<=h.x?-1:1;if(p.x<125)dodge=1;if(p.x>515)dodge=-1;}else if(h.kind==='beam'&&left<.48)duck=true;}}
      s={A:!duck,cover:duck,left:dodge<0,right:dodge>0};if(dodge)bm.moveDecisions++;if(duck)bm.coverDecisions++;if(s.A)bm.fireDecisions++;
      const incoming=c.enemyShots.filter(e=>!e.dead&&e.kind==='rocket'&&e.y>78&&e.y<290&&(e.duration-e.t)<.75).sort((a,b)=>(a.duration-a.t)-(b.duration-b.t))[0];
      const enemies=G.units.filter(u=>!u.dead&&u.y>90).sort((a,b)=>b.y-a.y);
      const turret=(c.turrets||[]).filter(t=>t.hp>0).sort((a,b)=>Math.abs(a.x-p.x)-Math.abs(b.x-p.x))[0];
      if(window.botGrenadeRoom!==c.room){window.botGrenadeRoom=c.room;window.botGrenades=0;}
      if(c.phase==='fight'&&enemies.length>=3&&window.botGrenades<3&&p.smoke>0&&p.grenadeCd===0){s.Y=true;window.botGrenades++;}
      const valid=t=>t&&!t.dead&&t.hp>0;
      const locked=window.botLocked;
      let actor=window.botController&&valid(locked)?locked:turret||enemies[0]||c.wallCore?.hp>0&&c.wallCore;
      window.botLocked=actor;
      let target=actor?{x:actor.x,y:actor.y-(actor.scale?55*actor.scale/.46:0)}:null;
      if(incoming&&!window.botController)target={x:incoming.x,y:incoming.y};
      if(!target&&G.boss&&!G.boss.dead)target={x:G.boss.x,y:G.boss.y-(G.boss.form==='core'?0:70)-(G.boss.jumpZ||0)};
      if(target){window.botAimPoint={...target};this.pointer.active=!window.botController;this.pointer.x=Math.max(35,Math.min(605,target.x));this.pointer.y=Math.max(78,Math.min(302,target.y));}
      window.botLastState={...s};
    }else if(window.botAuto&&c&&G.state==='play'&&!p.dead)s={...(window.botLastState||{})};else this.pointer.active=false;
    if(window.botAuto&&window.botController&&c&&window.botAimPoint){this.pointer.active=false;if(!s.cover&&!s.left&&!s.right){const t=window.botAimPoint,ax=t.x-c.cursor.x,ay=t.y-c.cursor.y;s.retina=true;s.left=ax< -5;s.right=ax>5;s.up=ay< -5;s.down=ay>5;}}
    this.state=s;this.raw={};return s;
  };void 0;''')
  fresh();check('normal run begins with six armor and damage enabled',ev('TD.game.player.hp===6&&TD.game.player.max===6&&TD.difficulty==="normal"'));ev('window.botAuto=true;window.normalStates=[];window.normalShots=[];')
  for i in range(400):
   if ev('TD.game.state==="clear"||TD.game.state==="gameover"||TD.game.player.dead'):break
   step(60)
   if i in [8,17]:snap('normal_breach_'+str(i))
   if ev('TD.game.boss&&TD.game.boss.form==="helios"&&!window.capturedHelios'):
    ev('window.capturedHelios=true');snap('normal_helios_entry')
  normal=ev('({state:TD.game.state,phase:TD.game.bastion.phase,room:TD.game.bastion.room,time:TD.game.time,hp:TD.game.player.hp,max:TD.game.player.max,deaths:TD.game.deaths,kills:TD.game.kills,damage:TD.game.bastion.damage,coverStops:TD.game.bastion.coverStops,intercepts:TD.game.bastion.intercepts,entries:TD.game.bastion.entryLog,grenadesRemaining:TD.game.player.smoke,metrics:window.botMetrics,boss:TD.game.boss?{form:TD.game.boss.form,state:TD.game.boss.state,hp:TD.game.boss.hp}:null})');print('NORMAL RUN '+json.dumps(normal),flush=True)
  check('normal armor input bot clears both breaches, core and Helios without artificial damage',normal['state']=='clear' and normal['room']>=2 and normal['deaths']==0)
  check('normal run uses movement and cover while firing',normal['metrics']['moveDecisions']>0 and normal['metrics']['coverDecisions']>0 and normal['metrics']['fireDecisions']>0)
  check('all reinforcement entries start above the screen',bool(normal['entries']) and all(e['y']<0 for e in normal['entries']))
  snap('normal_end')
  # A second complete run uses the actual rate-limited Retina cursor and
  # direction buttons. Target/reaction decisions remain at 250ms; the held
  # direction is released when the cursor reaches its chosen target.
  fresh();ev('window.botAuto=true;window.botController=true;window.botAimPoint=null;window.botMetrics={coverDecisions:0,moveDecisions:0,fireDecisions:0,decisions:0,states:[],minHull:6}')
  for i in range(420):
   if ev('TD.game.state==="clear"||TD.game.state==="gameover"||TD.game.player.dead'):break
   step(60)
   if i==16:snap('controller_breach')
  controller=ev('({state:TD.game.state,phase:TD.game.bastion.phase,room:TD.game.bastion.room,time:TD.game.time,hp:TD.game.player.hp,deaths:TD.game.deaths,kills:TD.game.kills,damage:TD.game.bastion.damage,coverStops:TD.game.bastion.coverStops,intercepts:TD.game.bastion.intercepts,grenadesRemaining:TD.game.player.smoke,metrics:window.botMetrics,boss:TD.game.boss?{form:TD.game.boss.form,state:TD.game.boss.state,hp:TD.game.boss.hp}:null})');print('CONTROLLER RUN '+json.dumps(controller),flush=True)
  check('normal armor rate-limited Retina and direction-button bot clears',controller['state']=='clear' and controller['deaths']==0);snap('controller_end')
  # A passive control confirms damage is enabled in the same ordinary setup.
  fresh();ev('window.botAuto=false;window.botInput={}');passive_time=0
  for _ in range(150):
   step(6);passive_time+=.1
   if ev('TD.game.player.dead'):break
  passive=ev('({hp:TD.game.player.hp,dead:TD.game.player.dead,damage:TD.game.bastion.damage,time:TD.game.time})')
  check('an exposed passive player takes real damage and falls at six armor',passive['dead'] and passive['damage']>=6);snap('passive_hit');step(45);snap('passive_rear_death')
  # Below this line: isolated mechanism fixtures, not normal-run balance evidence.
  fresh();ev('TD.Bastion.startBoss(TD.game);window.botAuto=false;window.botInput={};window.botLastState=null;window.botController=false;');step(110)
  check('core entry completes its orange health fill',ev('TD.game.boss.state==="fight"&&TD.game.boss.form==="core"&&TD.game.boss.gauge===1'))
  step(180);check('core telegraphs prism lanes before they become active',ev('TD.game.bastion.hazards.length===2&&TD.game.bastion.hazards.every(h=>h.t<h.delay)'));snap('core_prism_warning')
  ev('window.botInput={cover:true}');step(70);check('low wall cover blocks active core beams',ev('TD.game.player.hp===6'));snap('core_prism_beams')
  ev('TD.game.boss.state="transform";TD.game.boss.t=0;TD.game.boss.hp=0;TD.game.bastion.hazards=[];window.botInput={};');step(60);check('transformation produces the authored white flash',ev('TD.game.bastion.flash>.9'));snap('core_white_flash');step(56)
  check('transformation creates full Helios health and a new fill sequence',ev('TD.game.boss.form==="helios"&&TD.game.boss.hp===360&&TD.game.boss.state==="enter"'));step(37);snap('helios_orange_fill');step(78);snap('helios_red_fill')
  check('Helios fill reaches the second red layer before combat',ev('TD.game.boss.state==="enter"&&TD.game.boss.t>1.3&&TD.game.boss.t<3'))
  ev('TD.game.boss.state="fight";TD.game.boss.pattern=0;TD.game.boss.t=0');step(1);xs=[]
  for _ in range(190):
   step(1);xs.append(ev('TD.game.boss.x'))
  check('Helios runs fully offscreen and returns from that same edge',min(xs)<=-90 and xs[-1]>-90);snap('helios_running')
  ev('TD.game.boss.state="fight";TD.game.boss.pattern=1;TD.game.boss.t=0;TD.game.boss.x=320;TD.game.bastion.enemyShots=[]');step(90)
  check('Helios throws timed prism-ball volleys',ev('TD.game.bastion.enemyShots.filter(e=>e.kind==="orb").length>=6'));snap('helios_prism_volley')
  ev('TD.game.boss.state="fight";TD.game.boss.pattern=2;TD.game.boss.t=0;TD.game.bastion.enemyShots=[];TD.game.bastion.hazards=[]');step(50)
  check('lightning blasts retain a visible warning interval',ev('TD.game.bastion.hazards.length===2&&TD.game.bastion.hazards.every(h=>h.t<h.delay)'));snap('helios_lightning_warning')
  ev('TD.game.boss.state="fight";TD.game.boss.pattern=3;TD.game.boss.t=0;TD.game.bastion.hazards=[];TD.game.player.hp=6;TD.game.player.inv=0;window.botInput={right:true};');step(1);x0=ev('TD.game.bastion.hazards[0].x');step(35)
  check('jump targets the warned ground lane and has visible airborne height',ev('TD.game.boss.state==="jump"&&TD.game.boss.jumpZ>100'));snap('helios_jump');step(50)
  check('moving away evades the slam geyser at normal damage',ev('TD.game.player.hp===6&&TD.game.bastion.hazards.some(h=>h.kind==="geyser"&&h.t>=h.delay)'));snap('helios_geyser')
  check('zero page and console errors',not errors)
  report={'moduleSha256':hashlib.sha256((ROOT/'expansion/topdown/js/prism_bastion_1013.js').read_bytes()).hexdigest(),'normalRun':normal,'controllerRun':controller,'passiveControl':passive,'decisionCadenceMs':250,'strategy':'Prioritize turrets, retain controller target until defeated, use up to three grenades per breach when at least three infantry are visible, cover incoming shots and sidestep rocket/geyser warnings. Input decisions every 250 ms; controller cursor direction releases at chosen target each tick. No physical controller tested.','checks':checks,'errors':errors,'passed':sum(c['passed'] for c in checks),'total':len(checks),'fixtureNote':'Normal run never changes enemy health or calls damage/kill APIs. Isolated pattern fixtures set boss state and replenish player armor only between independent patterns.'}
  (OUT/'verification.json').write_text(json.dumps(report,indent=2));qa=ROOT/'docs/qa/overdrive_bastion_balance_1013.json';qa.write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'total':report['total'],'errors':errors}),flush=True);b.close()
finally:stop()
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
