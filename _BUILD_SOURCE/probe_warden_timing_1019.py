"""Native Warden tells, actual claw paths, slow keyboard response and hit pixels."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/warden';O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.WP19={};const hit=playerHit,path=bm9HitPath;playerHit=function(source){if(WP19.live){WP19.hits.push({source:String(source),t:WP19.time});if(WP19.guard)return;}return hit.apply(this,arguments);};
   bm9HitPath=function(from,to,width,label){if(WP19.live)WP19.paths.push({from,to,width,label,t:WP19.time});return path.apply(this,arguments);};
   window.wp19Step=n=>{for(let i=0;i<n;i++){WP19.time+=1/60;updatePlay(1/60);for(const q of eBullets)if(q._s7modOwner===B&&!WP19.seen.has(q)){WP19.seen.add(q);WP19.shots++;}if(i%6===0)drawWorld(1/60);if(B._s7mod.mode!==WP19.mode)break;}};}''')
  def frames(n):
   for i in range(0,n,6):
    p.evaluate('wp19Step(6)');p.wait_for_timeout(5)
    if p.evaluate('B._s7mod.mode!==WP19.mode'):break
  def setup(diff,mode,follow=False,guard=True):
   p.evaluate(SETUP,dict(stage=7,kind='sludgeemperor',diff=diff,pilot='juggernaut'))
   p.wait_for_function('()=>{stageLoadTick();s7mWarm();return stageLoadReady(7)&&XART.rdy("bm9_spider_claws_0")&&bmfReady("game")}',polling=50)
   return p.evaluate('''o=>{B=boss;const M=s7mInit(B);B.enter=false;B._drawY=B.y=250;B.x=worldWidth()/2;B._s7warden.noHit=false;M.lean=M.drop=M.height=0;M.counterTell=null;M.s67Swat=o.follow?3:0;
    VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;spawnClock=999999;stagePlan=[];subBossTriggered=aminiTriggered=true;bossWarned=false;warnT=0;warnKind=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;run._megaShield=false;
    Input.keys={};Input.mouse.down=false;enemies=[];eBullets=[];pBullets=[];powerups=[];groundTargetingFx=[];player.invuln=0;player.fireCd=999999;player.roll=player.somer=null;pilotIndex=PILOTS.findIndex(q=>q.key==='juggernaut');const pilot=PILOTS[pilotIndex];PILOTMOD={spd:pilot.spd,fire:pilot.fire,range:pilot.range,tint:pilot.tint};run.speed=0;
    s7mSet(B,o.mode);const tell=M.warn;M.t=tell+.18;const piece=s7mPose(B).find(q=>q.id==='frontL');const target=piece.bm9Tip?s7mWorld(B,piece.bm9Tip):s7mMuzzle(B,'gunL');M.t=0;player.x=target.x;player.y=target.y;WP19={live:true,time:0,hits:[],paths:[],shots:0,seen:new WeakSet(),mode:o.mode,guard:o.guard,start:{x:player.x,y:player.y},tell};SC12.refresh();__bofFit();return{tell,target,remaining:M.s67Swat,base:playerBaseSpeed()};}''',dict(mode=mode,follow=follow,guard=guard))
  for diff in ['normal','hard','furious']:
   for mode in ['swipeL','battery1009']:
    initial=setup(diff,mode);expected={'normal':{'swipeL':1.1,'battery1009':1.65},'hard':{'swipeL':.94,'battery1009':1.4},'furious':{'swipeL':.8,'battery1009':1.16}}[diff][mode]
    ck(diff+' '+mode+' current native tell',abs(initial['tell']-expected)<1e-9,initial)
    frames(280);row=p.evaluate('({...WP19,seen:undefined,phase:B._s7mod.mode})');rows.append(dict(difficulty=diff,stationary=True,**row));ck(diff+' '+mode+' native danger actually releases',len(row['paths'])>0 if mode=='swipeL' else row['shots']>0,dict(paths=len(row['paths']),shots=row['shots'],phase=row['phase']))
    if mode=='swipeL':
     ck(diff+' stationary positive control contacts the authored claw',any('Warden mechanical claw' in h['source'] for h in row['hits']),row['hits'])
     for direction in ['ArrowLeft','ArrowRight']:
      setup(diff,mode);frames(15);p.keyboard.down(direction);frames(200);p.keyboard.up(direction);row=p.evaluate('({...WP19,moved:Math.hypot(player.x-WP19.start.x,player.y-WP19.start.y),dead:player.dead,roll:!!player.roll,somer:!!player.somer})');rows.append(dict(difficulty=diff,direction=direction,stationary=False,**row));ck(diff+' claw '+direction+' ordinary response',not any('Warden mechanical claw' in h['source'] for h in row['hits']) and row['moved']>50 and not row['roll'] and not row['somer'],dict(hits=row['hits'],moved=row['moved']))
   if diff=='furious':
    initial=setup(diff,'swipeL',True);ck('Furious stomp follow-up keeps its authored .46-second tell',abs(initial['tell']-.46)<1e-9 and initial['remaining']==2,initial)
    for direction in ['ArrowLeft','ArrowRight']:
     setup(diff,'swipeL',True);frames(15);p.keyboard.down(direction);frames(120);p.keyboard.up(direction);row=p.evaluate('({...WP19,seen:undefined,moved:Math.hypot(player.x-WP19.start.x,player.y-WP19.start.y)})');ck('Furious short stomp claw '+direction+' ordinary response',not any('Warden mechanical claw' in h['source'] for h in row['hits']) and row['moved']>40,dict(hits=row['hits'],moved=row['moved']))
   setup(diff,'battery1009')
   damage=p.evaluate('''()=>{const M=B._s7mod,part=M.parts.find(q=>q.id==='frontL');
    function paint(){const pose=s7mPose(B).find(q=>q.id===part.id),q=s7mWorld(B,pose);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);s7mBlit('warden',pose.cell,q.x,q.y,pose.w,pose.h,pose.a+M.lean,1,Math.max(B.flash||0,part.flash||0));const data=ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data;ctx.restore();let white=0,ink=0;for(let i=0;i<data.length;i+=4)if(data[i+3]>200){ink++;if(data[i]>220&&data[i+1]>220&&data[i+2]>220)white++;}return{white,ink};}
    const before=paint(),hp=part.hp;s7mHit(B,3,0,0,part.id);const hit=paint(),timer=part.flash;wp19Step(24);const after=paint();return{loss:hp-part.hp,timer,expired:part.flash,before,hit,after};}''')
   ck(diff+' native Warden module damage visibly flashes',damage['loss']>0 and damage['timer']>0 and damage['hit']['white']>damage['before']['white']+30,damage)
   ck(diff+' Warden module flash expires to authored pixels',damage['expired']<=0 and abs(damage['after']['white']-damage['before']['white'])<5,damage)
   p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/(diff+'-claw.jpg')),type='jpeg',quality=85)
  br.close()
finally:stop()
ck('No browser/console/draw/asset errors',not errors,errors);report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors,method='Actual native Stage7 Warden attacks, slowest ship, real keyboard after .25s delay; one attack isolated, protected contact logger. Stationary controls and warning times are explicit. Not a whole-fight human win claim.');(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');sys.exit(bool(report['failed']))
