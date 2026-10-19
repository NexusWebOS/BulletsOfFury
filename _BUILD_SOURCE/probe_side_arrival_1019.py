"""Native large side arrivals and rocket-plane commitment, real hit pixels."""
from pathlib import Path
import json,http.server,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/side-arrival';O.mkdir(parents=True,exist_ok=True)
checks=[];rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.SA19={live:false};const play=updatePlay,warning=combatWarningTick,ground=groundTargetingSpawn;
   groundTargetingSpawn=function(spec){const actor=typeof E==='undefined'?null:E;if(SA19.live&&spec.owner===actor){SA19.warning??=SA19.time;SA19.release??=SA19.time;SA19.groundRacks++;SA19.groundWarns.push(spec.warn);SA19.fixedGround&&=spec.track===false;const impact=spec.onImpact;spec={...spec,onImpact:g=>{if(E===actor)SA19.groundImpacts++;return impact?.(g);}};}return ground.call(this,spec);};
   combatWarningTick=function(owner){if(SA19.live&&owner===E)SA19.warning??=SA19.time;return warning.apply(this,arguments);};
   updatePlay=function(dt){if(SA19.live)SA19.time+=dt;const r=play.apply(this,arguments);if(SA19.live){const visible=E.x>camLeftX()&&E.x<camRightX()&&E.y>PLAY.y&&E.y<VH;
    if(visible)SA19.visible??=SA19.time;if(SA19.last?.visible&&visible)SA19.maxVisibleStep=Math.max(SA19.maxVisibleStep,Math.hypot(E.x-SA19.last.x,E.y-SA19.last.y));SA19.last={x:E.x,y:E.y,visible};
    for(const b of eBullets)if(!SA19.seen.has(b)){SA19.seen.add(b);SA19.rounds++;SA19.release??=SA19.time;}if(E.dead||E._dyingT!=null)SA19.dead??=SA19.time;
   }return r;};
   window.sa19Pool=()=>E.hp+(E._esh?.energy||0)+(E._r30?E._r30.left.hp+E._r30.right.hp+E._r30.turret.hp:0);
   window.sa19Snap=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,-camX*SS,0);drawEnemy(E);const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
  }''')
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  for stage,kind in [(4,'s4rocket'),(4,'s4bomber'),(5,'s5skimmer'),(6,'s6skimmer'),(9,'s9comet')]:
   for diff in ['normal','hard','furious']:
    for side in [1,-1]:
     for arm in (['baseline','current'] if kind=='s4rocket' else ['current']):
      p.evaluate('SA19.live=false');p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff]);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
      initial=p.evaluate('''c=>{window.AC19_OFF=c.arm==='baseline'?1:0;for(const e of enemies)e.dead=true;enemies=[];aiQueue=[];powerups=[];eBullets=[];pBullets=[];groundTargetingReset();stagePlan=[];spawnClock=999999;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;EP13.owner=null;EB11.clock=EB11.nextTell=0;AIR17.clock=AIR17.nextTell=0;
       const W=worldWidth(),top=c.kind==='s4rocket',x=top?W*(c.side>0?.27:.73):c.side>0?-90:W+90,y=top?-72:VH*.24;
       player.x=clamp(top?x:c.side>0?40:W-40,40,W-40);player.y=VH*.8;camX=clamp(player.x-VW/2,0,W-VW);
       const opt={_side:c.side};if(c.kind==='s6skimmer')opt._jetManeuver='bomb';if(c.kind==='s9comet')opt._s9Role='slider';spawnEnemy(c.kind,x,y,opt);window.E=enemies.at(-1);run.pilot='cole';pilotIndex=PILOTS.findIndex(q=>q.key==='cole');PILOTMOD={...PILOTS[pilotIndex]};run.weapon=0;run.wlevel=0;run.wlevels=WEAPONS.map(()=>0);run.loadout=[0];run.forge={};run.forgeForms={};run.infusion=null;run._primary1003b='mg';run.spaceMode=false;special=thunderStorm=null;run.sonicT=run.dkT=0;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.mouse.down=false;player.fireCd=0;run.missileLevel=0;
       SA19={live:false,time:0,visible:null,warning:null,release:null,dead:null,rounds:0,groundRacks:0,groundImpacts:0,groundWarns:[],fixedGround:true,maxVisibleStep:0,last:null,seen:new WeakSet()};drawEnemy(E);return{x:E.x,y:E.y,w:E.w};}''',dict(kind=kind,side=side,arm=arm))
      p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50);p.evaluate('SA19.live=true');frames(1);alive=p.evaluate('!E.dead&&E._dyingT==null')
      for i in range(80):
       if p.evaluate('SA19.release!=null||SA19.dead!=null'):break
       frames(12)
      m=p.evaluate('({...SA19,seen:undefined,last:undefined,x:E.x,y:E.y,hp:E.hp})');rows.append(dict(stage=stage,difficulty=diff,kind=kind,side=side,arm=arm,initial=initial,metrics=m));tag=f'{diff} {kind} {side}'
      if arm=='baseline':ck(tag+' reproduces lost rocket-plane firing window',m['rounds']==0,m);continue
      ck(tag+' remains alive through its offscreen entry',alive,m)
      attack=m['release'] is not None and m['warning'] is not None and ((m['rounds']>0 and m['release']>m['warning']) or (m['groundRacks']>0 and min(m['groundWarns'])>=1.2 and m['fixedGround']))
      ck(tag+' enters, warns and releases native ordnance',m['visible'] is not None and attack,m)
      ck(tag+' has continuous visible motion',m['maxVisibleStep']<10,m['maxVisibleStep'])
      p.evaluate('SA19.live=false;window.saClean=sa19Snap();window.saHP=sa19Pool();player.x=E.x;player.y=E.y+70;pBullets=[];pShoot();for(const b of pBullets){b.x=E.x;b.y=E.y+3;b.vx=0;b.vy=-1;b.dmg=.25;}');frames(1)
      hit=p.evaluate('''()=>{const b=sa19Snap();let white=0;for(let i=0;i<b.length;i+=4)if(b[i+3]>64&&Math.min(b[i],b[i+1],b[i+2])>160&&Math.min(saClean[i],saClean[i+1],saClean[i+2])<120)white++;return{loss:saHP-sa19Pool(),timer:E.flash,white};}''')
      ck(tag+' real primary hit changes native hull or shield pixels',hit['loss']>0 and hit['timer']>0 and hit['white']>10,hit)
      p.evaluate('pBullets=[];player.x=worldWidth()/2;player.y=VH-50');frames(24)
      expiry=p.evaluate('''()=>{const timer=E.flash,a=sa19Snap();E.flash=0;const b=sa19Snap();E.flash=timer;let error=0,ink=0;for(let i=0;i<a.length;i+=4){error+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);if(Math.max(a[i],a[i+1],a[i+2],b[i],b[i+1],b[i+2])>16)ink++;}return{timer,error:error/Math.max(1,ink*3*255)};}''')
      ck(tag+' hit flash expires on the native renderer',expiry['timer']<=0 and expiry['error']<.005,expiry)
      if m['groundRacks']:
       frames(75);impact=p.evaluate('SA19.groundImpacts');ck(tag+' committed ground bomb reaches its native impact',impact>0,impact)
      if diff=='normal' and side==1:p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');p.screenshot(path=str(O/(kind+'.jpg')),type='jpeg',quality=80)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors);q=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/'native-report.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8');sys.exit(q['failed']>0)
