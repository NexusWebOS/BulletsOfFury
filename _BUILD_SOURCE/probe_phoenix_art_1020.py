"""Actual live animation keys, avian module breaks and source-boss isolation."""
from pathlib import Path
from PIL import Image
from io import BytesIO
from playwright.sync_api import sync_playwright
import ast,base64,http.server,json
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_phoenix_1020';checks=[];errors=[]
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
def value(file,needle):return next(n.args[0].value for n in ast.walk(ast.parse((R/'_BUILD_SOURCE'/file).read_text())) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and needle in n.args[0].value)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets));BOOT=value('probe_dracodia_phoenix_1020.py','window.volcanoSetup=')
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='cole',diff='normal'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}',polling=80);p.evaluate(BOOT)
  p.evaluate('()=>{volcanoSetup("normal","arms","cannon");window.PHK=new Set();const get=XART.get,draw=ctx.drawImage,tag=new WeakMap();XART.get=function(k){const im=get.apply(this,arguments);if(im)tag.set(im,k);return im;};ctx.drawImage=function(im){const key=tag.get(im);if(key)PHK.add(key);return draw.apply(this,arguments);};}')
  row=p.evaluate('''()=>{for(let i=0;i<128;i++){F.t=i/32;F.arm.left.charge=F.arm.right.charge=F.charge=i/127;v19Body(B);ph20Plume(vp23Socket(P,'left'),0);fztBeamDraw({_ph20:true,_ph20Time:i/24,width:12,len:200,x:150,y:150,a:0});}return{motion:[...PHK].filter(k=>k.startsWith('vp23_phoenix_')),muzzle:[...PHK].filter(k=>k.startsWith('ph20_plume_')),beam:[...PHK].filter(k=>k.startsWith('ph20_beam_'))};}''')
  ck('PixelLab wing and charge poses blit in the native renderer',len(row['motion'])>=50,row)
  ck('All16 PixelLab muzzle bloom frames actually blit',len(row['muzzle'])==16,row['muzzle']);ck('All16 PixelLab infernal beam frames actually blit',len(row['beam'])==16,row['beam'])
  p.evaluate('()=>{volcanoSetup("normal","arms","cannon");VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;player.fireCd=999999;}');film=[]
  def step(n):
   out=p.evaluate(shoot.STEP,n)
   if out:errors.append(out)
  def frame():return Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGB')
  for group,ids in [('arms',['left','shoulderL','right','shoulderR']),('core',['ventL','ventR','legL','legR','core']),('head',['head'])]:
   for id in ids:
    p.evaluate('''id=>{F.trans=0;B._noHit=false;B._lastPart=B.parts.find(q=>q.id===id);GP4.clock+=1;modularHit(B._lastPart.hp+1);}''',id)
    for i in range(6):step(5);film.append(frame())
   if group!='head':p.evaluate('F.trans=0;B._noHit=false')
  film[0].save(O/'module-breaks.webp',save_all=True,append_images=film[1:],duration=85,loop=0,quality=88)
  ck('Native break sequence reaches the surviving phoenix skull',p.evaluate('VP23.events.some(q=>q.event==="phase"&&q.phase==="head")'))
  ck('All ten actual modules break and remain destroyed',p.evaluate('B.parts.every(q=>q.destroyed&&q.hp===0)'))
  # Shared functions delegate source boss calls. The Stage8 renderer must not
  # recolor, attach phoenix projectiles to, or claim the original Furnace actor.
  row=p.evaluate('''()=>{const source={_fz:{phase:'arms'},x:200,y:200,w:200},before=eBullets.length;fztShot(source,200,200,0,150,20);const q=eBullets.at(-1);return{owned:!!vp23Proxy(source),tagged:!!q._ph20Feather,native:q.kind==='fztFireball',added:eBullets.length-before};}''');ck('Original Furnace projectile owner stays native and untagged',not row['owned'] and not row['tagged'] and row['native'] and row['added']==1,row)
  ck('No native art or update errors',not errors,errors);br.close()
finally:stop()
(O/'phoenix-art-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));raise SystemExit(not all(q['passed'] for q in checks) or bool(errors))
