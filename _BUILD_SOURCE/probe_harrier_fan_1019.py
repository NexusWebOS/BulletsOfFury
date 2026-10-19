"""Actual copied Harrier rotor blits, fixed axle/rim, hits and module break."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/fans';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{window.HFP19={draws:[]};const get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(key){const im=get.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,key);return im;};ctx.drawImage=function(im){const key=tags.get(im);if(key?.startsWith('hf19_')){const M=this.getTransform();HFP19.draws.push({key,x:M.e,y:M.f,alpha:this.globalAlpha});}return draw.apply(this,arguments);};
   window.hfp19Clear=()=>{ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.shadowBlur=0;ctx.globalCompositeOperation='source-over';ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);};window.hfp19Pixels=()=>Array.from(ctx.getImageData(0,0,cv.width,cv.height).data); }''')
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff=diff,pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{B=boss;v18Budget(B);v18Enter(B,2,6);v18Fight(B);B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=PLAY.y+170;B._drawY=B.y;BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;
    stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;enemies=[];eBullets=[];pBullets=[];Input.keys={};Input.mouse.down=false;player.invuln=1e9;run.shield=0;special=thunderStorm=null;run.sonicT=run.dkT=0;HFP19.draws=[];SC12.refresh();__bofFit();}''')
   row=p.evaluate('''()=>{const records=[];for(let i=0;i<16;i++){B._r30.clock=(i+.2)/HF19_ART.fps;hfp19Clear();const n=HFP19.draws.length;v19Body(B);const calls=HFP19.draws.slice(n),rig=v18Rig(B);for(const id of ['fanL','fanR']){const v=rig.find(v=>v.p.id===id),m=HF19_ART.mounts[id],point=fmcPoint(v,m.sourceAxle[0]/m.sourceSize[0],m.sourceAxle[1]/m.sourceSize[1]),expected=HF19_ART.frames[(i+(id==='fanR'?8:0))%16].key,q=calls.find(q=>q.key===expected);records.push({id,i,key:q?.key,expected,offset:q?Math.hypot(q.x-(point.x-camX),q.y-point.y):999});}}return records;}''')
   ck(diff+' all sixteen poses draw on both real fan axles',len(row)==32 and all(q.get('key')==q['expected'] and q['offset']<.01 for q in row),row)
   row=p.evaluate('''()=>{const v=v18Rig(B).find(v=>v.p.id==='fanL'),m=HF19_ART.mounts.fanL,point=fmcPoint(v,m.sourceAxle[0]/m.sourceSize[0],m.sourceAxle[1]/m.sourceSize[1]),k=Math.min(v.w/m.sourceSize[0],v.h/m.sourceSize[1])/HF19_ART.referenceScale;B.flash=0;v.p.flash=0;hfp19Clear();hf19Rotor(v,B);const after=hfp19Pixels();let changed=0,outside=0;const x0=point.x-camX,y0=point.y;for(let i=0;i<after.length;i+=4)if(Math.max(after[i],after[i+1],after[i+2])>15){changed++;const x=(i/4)%cv.width,y=Math.floor(i/4/cv.width),d=Math.hypot(x+.5-x0,y+.5-y0);if(d>23*k+2||d<6*k-2)outside++;}return{changed,outside};}''')
   ck(diff+' actual changed pixels remain inside the rotor annulus',row['changed']>20 and row['outside']==0,row)
   # The lower missile rack genuinely covers this vertical firing line.
   # Break that covering module through its native hit path, then verify that
   # real ordinary rounds reach the exposed fan; do not bypass collisions.
   p.evaluate('''()=>{const rack=B.parts.find(p=>p.id==='rackL');B._lastPart=rack;hitBoss(rack.hp+1);window.hfp19RackOpen=rack.destroyed;run.spaceMode=false;run.wlevels||=Array(8).fill(0);run.wvars||=Array(8).fill(null);weaponFormSelect(7,{kind:'primary1003b',id:'mg'});chaingunUnlocked=false;run._earnedUnlocks={...(run._earnedUnlocks||{}),chaingun:false};run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];const v=v18Rig(B).find(v=>v.p.id==='fanL');player.x=v.x-(wm26PlayerNose().x-player.x);player.y=v.y+120;player.fireCd=0;window.hfp19HP=v.p.hp;}''');p.keyboard.down('j')
   for i in range(0,65,12):
    p.evaluate('''n=>{for(let i=0;i<n;i++){const v=v18Rig(B).find(v=>v.p.id==='fanL');player.x=v.x-(wm26PlayerNose().x-player.x);player.y=v.y+120;enemies=[];updatePlay(1/60);drawWorld(1/60);}}''',min(12,65-i));p.wait_for_timeout(5)
   p.keyboard.up('j')
   row=p.evaluate('({loss:hfp19HP-B.parts.find(p=>p.id==="fanL").hp,hp:B.hp,rackOpen:hfp19RackOpen})');ck(diff+' actual primary damages the exposed fan module',row['loss']>0 and row['rackOpen'],row)
   row=p.evaluate('''()=>{pBullets=[];eBullets=[];const v=v18Rig(B).find(v=>v.p.id==='fanL');B.flash=v.p.flash=0;hfp19Clear();hf19Rotor(v,B);const before=hfp19Pixels();B._lastPart=v.p;hitBoss(1);hfp19Clear();hf19Rotor(v,B);const after=hfp19Pixels();let changed=0;for(let i=0;i<before.length;i+=4)if(Math.max(Math.abs(before[i]-after[i]),Math.abs(before[i+1]-after[i+1]),Math.abs(before[i+2]-after[i+2]))>15)changed++;return{changed,owner:B.flash,part:v.p.flash};}''');ck(diff+' rotor itself visibly flashes through native owner/part damage',row['changed']>10 and row['part']>0,row)
   frames(30);row=p.evaluate('''()=>{const v=v18Rig(B).find(v=>v.p.id==='fanL'),owner=B.flash,part=v.p.flash;hfp19Clear();hf19Rotor(v,B);const a=hfp19Pixels();B.flash=v.p.flash=0;hfp19Clear();hf19Rotor(v,B);const b=hfp19Pixels();let changed=0,error=0,ink=0;for(let i=0;i<a.length;i+=4){const delta=Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]));if(delta>8)changed++;error+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);if(Math.max(a[i],a[i+1],a[i+2],b[i],b[i+1],b[i+2])>16)ink++;}return{owner,part,changed,normalizedError:error/Math.max(1,ink*3*255)};}''');ck(diff+' rotor damage flash expires back to native purple/metal pixels',row['owner']<=0 and row['part']<=0 and row['normalizedError']<.005,row)
   p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/(diff+'-fans.png')))
   row=p.evaluate('''()=>{B._r30.clock=.01;const left=B.parts.find(p=>p.id==='fanL');left.destroyed=true;HFP19.draws=[];hfp19Clear();v19Body(B);return{keys:HFP19.draws.map(q=>q.key),leftInRig:v18Rig(B).some(v=>v.p.id==='fanL')};}''');ck(diff+' destroyed fan has no rotor while the surviving fan keeps turning',not row['leftInRig'] and 'hf19_rotor_00' not in row['keys'] and 'hf19_rotor_08' in row['keys'],row)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors);report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors);(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');sys.exit(report['failed']>0)
