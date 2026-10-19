"""Native toxic skimmer top/side entrances, real attack and hit pixels."""
from pathlib import Path
import json,http.server,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/sewer-entry';O.mkdir(parents=True,exist_ok=True)
checks=[];rows=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.SEP19={live:false};const play=updatePlay,warn=combatWarningTick;
   combatWarningTick=function(owner){if(SEP19.live&&owner===E)SEP19.firstWarning??=SEP19.time;return warn.apply(this,arguments);};
   updatePlay=function(dt){if(SEP19.live)SEP19.time+=dt;const r=play.apply(this,arguments);if(SEP19.live){
    if(E.x>=camLeftX()&&E.x<=camRightX()&&E.y>=PLAY.y&&E.y<=VH)SEP19.visible??=SEP19.time;
    for(const q of eBullets)if(!SEP19.seen.has(q)){SEP19.seen.add(q);SEP19.rounds++;SEP19.firstRound??=SEP19.time;}
    if(SEP19.last)SEP19.maxStep=Math.max(SEP19.maxStep,Math.hypot(E.x-SEP19.last.x,E.y-SEP19.last.y));SEP19.last={x:E.x,y:E.y};
   }return r;};
   window.sep19Snap=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,-camX*SS,0);drawEnemy(E);const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
  }''')
  for diff in ['normal','hard','furious']:
   for edge in ['top','left','right']:
    for arm in (['baseline','current'] if edge=='top' else ['current']):
     p.evaluate('SEP19.live=false');p.evaluate('d=>EA11.setup(7,d)',diff);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&bmfReady("game")}',polling=50)
     initial=p.evaluate('''c=>{window.SE19_OFF=c.arm==='baseline'?1:0;for(const e of enemies)e.dead=true;enemies=[];aiQueue=[];eBullets=[];pBullets=[];powerups=[];stagePlan=[];stageTimer=0;spawnClock=999999;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;EP13.owner=null;EB11.clock=EB11.nextTell=0;
      const W=worldWidth(),x=c.edge==='top'?W*.70:c.edge==='left'?-55:W+55,y=c.edge==='top'?-124:VH*(c.edge==='left'?.22:.34),opt=c.edge==='top'?{_stagger:.32}:{_side:c.edge==='left'?1:-1};
      spawnEnemy('s7skimmer',x,y,opt);window.E=enemies.at(-1);player.x=W/2;player.y=VH*.8;camX=clamp(player.x-VW/2,0,W-VW);run.pilot='cole';pilotIndex=PILOTS.findIndex(q=>q.key==='cole');PILOTMOD={...PILOTS[pilotIndex]};run.weapon=0;run.wlevel=0;run.spaceMode=false;run.missileLevel=0;for(const k of Object.keys(Input.keys))Input.keys[k]=false;player.fireCd=0;
      SEP19={live:false,time:0,visible:null,firstWarning:null,firstRound:null,rounds:0,maxStep:0,last:null,seen:new WeakSet()};drawEnemy(E);return{entry:!!E._se19Entry,dir:E._dir,x:E.x,y:E.y};}''',dict(edge=edge,arm=arm))
     p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50);p.evaluate('SEP19.live=true')
     for i in range(45):
      p.evaluate(shoot.STEP,12);p.wait_for_timeout(5)
      if p.evaluate('SEP19.firstRound!=null'):break
     metrics=p.evaluate('({...SEP19,seen:undefined,last:undefined,x:E.x,y:E.y,dead:!!E.dead})');rows.append(dict(difficulty=diff,edge=edge,arm=arm,initial=initial,metrics=metrics))
     if arm=='baseline':ck(diff+' native top entrance reproduces the missing visible pass',metrics['visible'] is None and metrics['firstRound'] is None,metrics);continue
     ck(diff+' '+edge+' enters view and releases a native attack',metrics['visible'] is not None and metrics['firstRound'] is not None and metrics['rounds']>0,metrics)
     ck(diff+' '+edge+' keeps motion continuous through entry',metrics['maxStep']<6,metrics['maxStep'])
     ck(diff+' '+edge+' has a visible charge before its release',metrics['firstWarning'] is not None and metrics['firstRound']-metrics['firstWarning']>=.4,metrics)
     if edge=='top':
      p.evaluate('SEP19.live=false;window.sepClean=sep19Snap();window.sepHP=E.hp;window.sepShield=E._esh?.energy||0;player.x=E.x;player.y=E.y+60;pBullets=[];pShoot();for(const b of pBullets){b.x=E.x;b.y=E.y+2;b.vx=-2.8;b.vy=-1;b.dmg=.25;}');p.evaluate(shoot.STEP,1)
      hit=p.evaluate('''()=>{const flashed=sep19Snap();let white=0;for(let i=0;i<flashed.length;i+=4)if(flashed[i+3]>64&&Math.min(flashed[i],flashed[i+1],flashed[i+2])>160&&Math.min(sepClean[i],sepClean[i+1],sepClean[i+2])<120)white++;return{damage:sepHP-E.hp+sepShield-(E._esh?.energy||0),hullLoss:sepHP-E.hp,shieldLoss:sepShield-(E._esh?.energy||0),flash:E.flash,white};}''')
      ck(diff+' top arrival takes real primary damage with visible hit pixels',hit['damage']>0 and hit['flash']>0 and hit['white']>10,hit)
      p.evaluate('pBullets=[]');p.evaluate(shoot.STEP,20);expiry=p.evaluate('''()=>{const timer=E.flash,a=sep19Snap();E.flash=0;const b=sep19Snap();E.flash=timer;let diff=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>10)diff++;return{timer,diff};}''')
      ck(diff+' native hit flash expires to the authored hull',expiry['timer']<=0 and expiry['diff']<5,expiry)
      p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/(diff+'-top.jpg')),type='jpeg',quality=82)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors);report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');sys.exit(report['failed']>0)
