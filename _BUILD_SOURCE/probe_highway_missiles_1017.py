"""Native Stage4 shoulder rockets: gun/Retina interception, escape and atomic return."""
from pathlib import Path
import ast,json,sys,base64,hashlib
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/highway_missiles_1017';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];cases=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof HM17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';startRun(4);
   window.hmNativeDraws={};window.hmSounds={};window.hmArtKey=null;const get=XART.get,draw=ctx.drawImage,blit=hm17Blit;
   XART.get=function(k){if(k.startsWith('hm17_'))hmNativeDraws[k+'-get']=(hmNativeDraws[k+'-get']||0)+1;return get.apply(this,arguments);};
   hm17Blit=function(name){const old=hmArtKey;hmArtKey=HM17_ART[name]?.key;try{return blit.apply(this,arguments);}finally{hmArtKey=old;}};
   ctx.drawImage=function(){if(hmArtKey)hmNativeDraws[hmArtKey]=(hmNativeDraws[hmArtKey]||0)+1;return draw.apply(this,arguments);};
   for(const key of ['nuclearLaunch','atomicDetonate','alertDanger']){const sound=Audio.SFX[key];Audio.SFX[key]=function(){hmSounds[key]=(hmSounds[key]||0)+1;return sound?.apply(this,arguments);};}
  }''')
  def setup(diff='normal',stage=4):
   p.keyboard.up('j')
   p.evaluate(SETUP,dict(stage=stage,pilot='cole',diff=diff))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&hm17Warm()&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;Input.keys={};Input.mouse.down=false;warnT=0;warnKind=null;
    VP12.next=CP12.next=EP13.next=9999;TARGET17.nextTank=9999;HM17.next=1e9;stagePlan=[];subBossTriggered=true;subBossDone=false;
    bossWarned=false;bossDefeated=false;stageEnding=0;aminiTriggered=true;player.invuln=999999;run.shield=0;player.dead=player.out=false;run.speed=0;
    player.x=worldWidth()/2;player.y=VH-100;camX=clamp(player.x-VW/2,0,worldWidth()-VW);HM17.draws={};hmNativeDraws={};hmSounds={};
    ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}''')
  def frames(n):
   for i in range(0,n,8):
    error=p.evaluate(shoot.STEP,min(8,n-i))
    if error:errors.append(error)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}')
   p.screenshot(path=str(O/(name+'.png')))
  def spawn(side=-1,y=230):
   return p.evaluate('''([side,y])=>{window.pad=hm17Spawn(side,y);return{x:pad.x,y:pad.y,hp:pad.hp,base:pad._hm17.anchor+LA1007.scroll};}''',[side,y])
  setup();spawn();p.evaluate('window.padRight=hm17Spawn(1,260)');frames(70);snap('01-tall-roadside-missiles')
  row=p.evaluate('''()=>({plates:hmNativeDraws,positions:[pad,padRight].map(e=>({x:e.x,ground:!tankDrivable(e.x,0,false),leftEdge:e.x-33,rightEdge:e.x+33,phase:e._hm17.phase})),size:[VW,VH,worldWidth(),viewW()],keys:Object.values(HM17_ART).map(a=>({key:a.key,w:a.w,h:a.h,pivot:a.pivot,loaded:XART.rdy(a.key)}))})''')
  check('Both highway shoulders carry tall authored rockets at the regular game FOV',all(e['ground'] for e in row['positions']) and row['plates'].get('hm17_pad',0)>0 and row['plates'].get('hm17_missile',0)>0,row)
  check('All three authored plates have even dimensions, ready native keys and fixed pivots',all(a['loaded'] and a['w']%2==a['h']%2==0 for a in row['keys']),row['keys'])
  row=p.evaluate('''()=>{const e=pad;function image(){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);drawEnemy(e);const d=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return d;}
   const a=image(),hp=e.hp;_dmgBullet={kind:'mg',x:e.x,y:e.y};hitEnemy(e,1);_dmgBullet=null;const b=image();let changed=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>100&&Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>12)changed++;return{pixels:changed,damage:hp-e.hp,flash:e.flash};}''')
  check('Real pad damage flashes the actual rocket and pad pixels',row['pixels']>100 and row['damage']>0 and row['flash']>0,row)
  frames(20);check('Native hit flashes expire normally',p.evaluate('pad.flash<=0'))
  weapons=[('machine gun',0,None),('spread',1,None),('laser',3,None),('flamethrower',4,None),('ice orb',5,'iceorb'),('fire orb',5,'fireorb'),('chaingun',7,None),('Retina missile',0,'missile')]
  for diff in ['easy','normal','hard','furious']:
   for name,weapon,variant in weapons:
    setup(diff);q=spawn();p.evaluate('''([w,v])=>{player.x=pad.x;player.y=pad.y+150;run.weapon=w;run.wlevel=3;run.wlevels[w]=3;run.wvars??=[];run.wvars[w]=v==='missile'?null:v;
     player.fireCd=0;run.bombs=20;if(v==='missile'){retina.target=pad;retina.phase='locked';retina.lockT=5;useBomb();}}''',[weapon,variant])
    if variant!='missile':p.keyboard.down('j')
    frames(95);p.keyboard.up('j')
    row=p.evaluate('''()=>{Input.keys.j=false;return{hp:pad.hp,max:pad.maxhp,dead:pad.dead,phase:pad._hm17.phase,returns:groundTargetingFx.filter(q=>q._hm17Return).length,events:HM17.events};}''');row.update(diff=diff,weapon=name);cases.append(row)
    check(diff+' standing rocket takes actual '+name+' damage',row['hp']<q['hp'],row)
    if name=='machine gun':check(diff+' ordinary gunfire stops the launch with no atomic return',row['dead'] and row['phase']=='destroyed' and row['returns']==0,row)
  setup();spawn();frames(240)
  row=p.evaluate('''()=>({phase:pad._hm17.phase,y:pad.y,shootable:_lockTargets().includes(pad),empty:HM17.empty.length,launch:hmSounds.nuclearLaunch||0})''')
  check('Launch leaves its empty pad on the ground and keeps the rising rocket lockable',row['phase']=='boost' and row['shootable'] and row['empty']==1 and row['launch']==1,row);snap('02-shootable-ascent')
  p.evaluate('''()=>{player.x=pad.x;player.y=pad.y+110;run.weapon=0;run.wlevel=3;run.wlevels[0]=3;player.fireCd=0;}''');p.keyboard.down('j');frames(100);p.keyboard.up('j')
  row=p.evaluate('''()=>{Input.keys.j=false;return{dead:pad.dead,phase:pad._hm17.phase,events:HM17.events,returns:groundTargetingFx.filter(q=>q._hm17Return).length};}''')
  check('Actual gunfire destroys a launched missile before it escapes',row['dead'] and row['phase']=='destroyed' and row['returns']==0,row)
  frames(260);check('A destroyed ascent cannot schedule a delayed return',p.evaluate('!HM17.events.some(q=>q.event==="escaped-return-locked"||q.event==="atomic-impact")'))
  setup();spawn();p.evaluate('''()=>{hm17LeavePad(pad);pad._hm17.phase='boost';pad._hm17.t=0;pad._hm17.velocity=1;pad.y=viewTopY()-40;pad.w=34;pad.h=120;player.x=pad.x;player.y=viewTopY()+90;run.weapon=0;run.wlevel=1;run.wlevels[0]=1;player.fireCd=0;}''')
  check('Retina keeps a lock when only the ascending missile tail is visible',p.evaluate('_lockTargets().includes(pad)&&retinaTargetValid(pad)'))
  hp=p.evaluate('pad.hp');p.keyboard.down('j');frames(20);p.keyboard.up('j')
  check('Ordinary gunfire can still hit that visible tail above the centre boundary',p.evaluate('pad.hp')<hp)
  setup();spawn()
  for i in range(90):
   frames(8)
   if p.evaluate('groundTargetingFx.some(q=>q._hm17Return)'):break
  row=p.evaluate('''()=>{window.return17=groundTargetingFx.find(q=>q._hm17Return);return{phase:pad._hm17.phase,y:pad.y,top:viewTopY(),q:return17?{x:return17.x,y:return17.y,warn:return17.warn,r:return17.radius,track:return17.track,owner:return17.owner,t:return17.t}:null,events:HM17.events};}''')
  check('Only a fully offscreen missile commits exactly one atomic return',row['phase']=='escaped' and row['y']+60<row['top'] and row['q'] and not row['q']['track'] and row['q']['owner'] is None and sum(e['event']=='escaped-return-locked' for e in row['events'])==1,row)
  ring=p.evaluate('''()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);groundTargetingDraw();const d=ctx.getImageData(0,0,cv.width,cv.height).data;let x0=1e9,y0=1e9,x1=0,y1=0;for(let y=0;y<cv.height;y++)for(let x=0;x<cv.width;x++){const i=(y*cv.width+x)*4;if(d[i+3]>60&&Math.max(d[i],d[i+1],d[i+2])>50){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}}ctx.restore();return{w:x1-x0+1,h:y1-y0+1,diameter:return17.radius*2,draws:HM17.draws.returnRetina};}''')
  check('Native warning pixels mark the complete circular blast radius',abs(ring['w']-ring['diameter'])<=4 and abs(ring['h']-ring['diameter'])<=4 and ring['draws']>0,ring)
  q=row['q'];p.evaluate('''()=>{player.x=camRightX()-24;player.y=VH-36;}''');frames(120);snap('03-locked-atomic-target')
  check('The atomic landing point stays committed after the player moves',p.evaluate('return17.x')==q['x'] and p.evaluate('return17.y')==q['y'])
  frames(45);snap('04-missile-returning-from-sky')
  frames(60);snap('05-atomic-mushroom')
  row=p.evaluate('''()=>({events:HM17.events,sounds:hmSounds,atomDraws:P2.draws.atom||0,dead:player.dead,nukes:s67Nukes.length})''')
  check('Return uses actual atomic cloud frames, impact sound and one detonation',row['atomDraws']>0 and row['sounds'].get('atomicDetonate')==1 and sum(q['event']=='atomic-impact' for q in row['events'])==1,row)
  check('Moving outside the committed blast remains safe',not row['dead'],row)
  for mode in ['center','outside']:
   setup();spawn();p.evaluate('''()=>{pad._hm17.phase='boost';pad.y=viewTopY()-100;hm17Escape(pad);window.return17=groundTargetingFx.find(q=>q._hm17Return);player.invuln=0;player.x=return17.x;player.y=return17.y;return17.warn=.5;}''')
   if mode=='outside':p.evaluate('player.x+=return17.radius+20')
   frames(39);row=p.evaluate('''()=>({dead:player.dead,impact:return17.impact,x:player.x,y:player.y,origin:[return17.x,return17.y],radius:return17.radius})''')
   check('Atomic impact '+('hits a pilot who stays on its target' if mode=='center' else 'spares a pilot outside its marked radius'),row['impact'] and row['dead']==(mode=='center'),row)
  setup();spawn();p.evaluate('''()=>{LA1007.scroll=970;mapScroll=970;LA1007.mapPrev=970;pad._hm17.anchor=230-970;pad._hm17.warm=99;window.anchor17=pad._hm17.anchor;_groundSrcPrev=-970;}''');frames(150)
  row=p.evaluate('''()=>({anchor:pad.y+46-LA1007.scroll,expected:anchor17,scroll:LA1007.scroll,alive:!pad.dead})''')
  check('Pad stays bolted to terrain through the reflected highway tile seam',row['alive'] and abs(row['anchor']-row['expected'])<.001 and row['scroll']>1020,row)
  p.evaluate('setState("paused")');before=p.evaluate('[pad._hm17.t,LA1007.scroll]');frames(70);after=p.evaluate('[pad._hm17.t,LA1007.scroll]')
  check('Pause stops the missile clock and terrain together',before==after,dict(before=before,after=after))
  pressures=[]
  for diff in ['normal','hard','furious']:
   setup(diff);p.evaluate('HM17.next=180');frames(2700)
   row=p.evaluate('''()=>({spawns:HM17.events.filter(q=>q.event==='pad-spawn'),config:hm17Config(),living:enemies.filter(e=>e._hm17&&!e.dead).length,returns:groundTargetingFx.filter(q=>q._hm17Return).length})''');pressures.append(len(row['spawns']))
   cap=3 if diff=='normal' else 4
   check(diff+' actual director alternates roadside pads with bounded simultaneous pressure',len(row['spawns'])>=5 and all(q['side']!=row['spawns'][i-1]['side'] for i,q in enumerate(row['spawns']) if i) and row['living']<=cap and row['returns']<=cap,row)
   if diff=='furious':snap('06-furious-highway-pressure')
  check('Roadside pressure increases Normal to Hard to Furious',pressures[0]<pressures[1]<pressures[2],pressures)
  setup();p.evaluate('''()=>{stageTimer=curStage.length-5;HM17.next=0;}''');frames(90)
  check('Additional pads stop before the final boss approach',p.evaluate('!HM17.events.some(q=>q.event==="pad-spawn")'))
  setup(stage=1);p.evaluate('HM17.next=0');frames(180)
  check('Stage reset removes pads and returns; other stages never spawn them',p.evaluate('HM17.events.length===0&&HM17.empty.length===0&&!enemies.some(e=>e._hm17)&&!groundTargetingFx.some(q=>q._hm17Return)'))
  br.close()
finally:stop()
check('No page, console, drawing or missing-asset errors',not errors,errors)
report={'passed':sum(q['passed'] for q in checks),'failed':[q for q in checks if not q['passed']],'errors':errors,'checks':checks,'weapons':cases}
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}),flush=True)
if report['failed'] or errors:sys.exit(1)
