"""Native current-owner Herald attack timing, module routing and pixels."""
from pathlib import Path
import argparse,ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/herald';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='before');ap.add_argument('--seconds',type=int,default=60);a=ap.parse_args()
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
errors=[];cases=[];checks=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.HB19={};const tell=hd1003Tell,shot=hd1003Shot,beam=s81003Beam;
   hd1003Tell=function(b){const r=tell.apply(this,arguments);if(HB19.live&&b===B)HB19.attacks.push({time:HB19.time,mode:b._hd1003.mode,attack:b._hd1003.attack,warm:b._hd1003.warm,lanes:b._hd1003.lanes.map(L=>({id:L.id,delay:L.delay,aim:L.aim}))});return r;};
   hd1003Shot=function(b,L,a){const n=eBullets.length,r=shot.apply(this,arguments);if(HB19.live&&eBullets.length>n)HB19.shots.push({time:HB19.time,attack:b._hd1003.attack,part:L.id,angle:a,speed:Math.hypot(eBullets.at(-1).vx,eBullets.at(-1).vy)});return r;};
   s81003Beam=function(b,L){const r=beam.apply(this,arguments);if(HB19.live&&b===B)HB19.beams.push({time:HB19.time,attack:b._hd1003.attack,part:L.id});return r;};
   window.hb19Step=n=>{for(let i=0;i<n;i++){HB19.time+=1/60;player.invuln=1e9;updatePlay(1/60);
    HB19.peak=Math.max(HB19.peak,eBullets.filter(q=>!q.dead&&q._heraldOwner1003===B).length);const C=hc1007CrossState(B);if(C?.mode==='live')HB19.crossFrames++;
    if(i%12===0)drawWorld(1/60);
   }};}''')
  for diff in ['normal','hard','furious']:
   for disarmed in [False,True]:
    name=diff+('-disarmed' if disarmed else '-intact');p.evaluate(SETUP,dict(stage=8,kind='heralddeath',mini=True,diff=diff,pilot='cole'))
    p.evaluate('''disarmed=>{B=subBoss;B.enter=B._noHit=false;B._be=null;B.y=B.ty;B._drawY=B.y;B._hd1003.mode='rest';B._hd1003.age=0;B._hd1003.seq=0;
     if(disarmed)for(const id of ['gunL','gunR','wingL','wingR'])hd1003Break(B,hd1003Part(B,id));
     VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;bossWarned=false;warnT=0;warnKind=null;
     BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;
     Input.keys={};Input.mouse.down=false;powerups=[];enemies=[];pBullets=[];eBullets=[];HB19={live:true,time:0,attacks:[],shots:[],beams:[],crossFrames:0,peak:0};SC12.refresh();__bofFit();}''',disarmed)
    p.wait_for_function('()=>{stageLoadTick();hd1003Warm();return stageLoadReady(8)&&XART.rdy(HD1003_ART.key)&&XART.rdy(HC1006_FX.key)&&bmfReady("game")}',polling=50)
    for sec in range(a.seconds):
     for batch in range(5):p.evaluate('hb19Step(12)');p.wait_for_timeout(5)
     if sec in [2,5,9,17,31,a.seconds-1]:
      p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/f'{a.tag}-{name}-{sec+1:03}.png'))
    row=p.evaluate('''()=>({difficulty:diffKey,metrics:HB19,history:B._hd1003.history,parts:B._hd1003.parts.map(q=>({id:q.id,hp:q.hp,dead:q.dead})),hp:B.hp,max:B.maxhp})''');row['disarmed']=disarmed;cases.append(row)
    # Actual hit path and its damaged native pixels; do not substitute timer-only assertions.
    flash=p.evaluate('''()=>{const part=hd1003Part(B,HB19.disarmed?'head':'core'),point=hd1003Center(B,part),hp=B.hp;hitSubBoss(3,point.x,point.y);
     const pf=part.flash,bf=B.flash,draw=()=>heraldDeathDraw(B),snap=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);draw();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
     part.flash=B.flash=0;const before=snap();part.flash=pf;B.flash=bf;const after=snap();let pixels=0;for(let i=0;i<after.length;i+=4)if(after[i+3]>80&&Math.max(Math.abs(after[i]-before[i]),Math.abs(after[i+1]-before[i+1]),Math.abs(after[i+2]-before[i+2]))>15)pixels++;
     return{hpLoss:hp-B.hp,partTimer:pf,ownerTimer:bf,pixels};}''')
    ck(name+' native damage and actual hit-flash pixels',flash['hpLoss']>0 and flash['partTimer']>0 and flash['pixels']>20,flash)
    p.evaluate('hb19Step(30)');ck(name+' part flash expires on actual clock',p.evaluate('B._hd1003.parts.every(q=>q.flash===0)'))
    print(json.dumps(dict(case=name,attacks=len(row['metrics']['attacks']),shots=len(row['metrics']['shots']),beams=len(row['metrics']['beams']),peak=row['metrics']['peak'],book=row['history'])),flush=True)
    (O/(a.tag+'-report.json')).write_text(json.dumps(dict(cases=cases,checks=checks,errors=errors),indent=2)+'\n')
  br.close()
finally:stop()
ck('No browser/console/draw/asset errors',not errors,errors);(O/(a.tag+'-report.json')).write_text(json.dumps(dict(cases=cases,checks=checks,errors=errors),indent=2)+'\n');sys.exit(bool(errors) or any(not c['passed'] for c in checks))
