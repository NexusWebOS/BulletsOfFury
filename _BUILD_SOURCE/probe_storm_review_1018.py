"""Native review UI, every generated pose, generator feedback and co-op comms."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/storm_assault_1018/native';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/storm_assault_1018/index.html?scene=shield')
  p.wait_for_function('document.querySelector("#status").textContent.startsWith("Spinning")')
  f=p.locator('#game').content_frame;w=p.frames[1];w.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  def frames(n):
   for i in range(0,n,12):w.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  w.wait_for_function('ST18.draws.radio>0');p.screenshot(path=str(O/'review-shield.png'))
  check('Live review uses full native playfield, current housing and isolated saves',w.evaluate('SC12.mode==="sides"&&__stormReviewStorage&&boss._ship==="stormsovereign"&&boss._s4war.shield.active'))
  row=w.evaluate('''()=>{const b=boss,n=b._s4war.shield.nodes[0];b._sa14.glow=0;window.nodeDamage=n;window.nodePixel=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);mr27Over(b);const d=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return d;};
   n.flash=0;const a=nodePixel(),hp=n.hp;_dmgBullet={kind:'mg',x:n.x,y:n.y};_lastHitX=n.x;_lastHitY=n.y;b._s4ShieldHit=n;b._s4CoreHit=null;hitBoss(1);_dmgBullet=null;const c=nodePixel();let pixels=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-c[i]),Math.abs(a[i+1]-c[i+1]),Math.abs(a[i+2]-c[i+2]))>18)pixels++;return{pixels,flash:n.flash,hp:hp-n.hp};}''')
  check('Spinning generator takes real primary damage with visible hit pixels',row['pixels']>25 and row['flash']>0 and row['hp']>0,row)
  frames(30);check('Generator hit flash expires',w.evaluate('nodeDamage.flash<=0'))
  row=w.evaluate('''()=>{const out=[];ctx.save();ctx.setTransform(1,0,0,1,0,0);for(const [name,bank]of Object.entries(ST18_ART))for(let i=0;i<bank.frames.length;i++){
   const a=bank.frames[i],im=XART.get(a.key);ctx.clearRect(0,0,cv.width,cv.height);st18Blit(name,i,200,200,180);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let ink=0;for(let p=3;p<d.length;p+=4)if(d[p]>50)ink++;
   out.push({name,i,w:im.width,h:im.height,ink,even:im.width%2===0&&im.height%2===0});}ctx.restore();return out;}''')
  check('All 32 registered generated poses render through native XART and game drawImage',len(row)==32 and all(q['even'] and q['ink']>10 for q in row),row)
  # Moving the boss never drags the shield objectives into the ram lane.
  row=w.evaluate('''()=>{const b=boss,before=b._s4war.shield.nodes.map(n=>({x:n.x,y:n.y}));er26Set(b,'sa14-drive');b.x+=90;b.y+=240;stage4ShieldSyncNodes(b);return{fixed:b._s4war.shield.nodes.every((n,i)=>n.x===before[i].x&&n.y===before[i].y)};}''')
  check('Rotating generators remain at their station when the hull charges',row['fixed'],row)
  w.evaluate('''()=>{window.reviewBreakNodes=(nodes)=>{const b=boss;for(const n of nodes)for(let i=0;i<2&&!n.dead;i++){b._s4ShieldHit=n;b._s4CoreHit=null;_lastHitX=n.x;_lastHitY=n.y;_dmgBullet={kind:'mg',x:n.x,y:n.y};hitBoss(1e6);}_dmgBullet=null;};reviewBreakNodes(boss._s4war.shield.nodes.slice(0,2));}''');frames(2)
  check('Two surviving generators still keep the shield up',w.evaluate('boss._s4war.shield.active&&boss._s4war.shield.nodes.filter(n=>!n.dead).length===2'))
  w.evaluate('reviewBreakNodes(boss._s4war.shield.nodes.slice(2))');frames(2)
  check('Destroying all four generators immediately gives exposed-core guidance',w.evaluate('!boss._s4war.shield.active&&boss._st18.radio.id==="weakspots"'))
  # Restart via the visible selectors; no test-only product hooks.
  p.select_option('#scene','helpers');p.wait_for_function('document.querySelector("#status").textContent.startsWith("South")');frames(165)
  check('Review helper scene reaches native south-entry wing',w.evaluate('boss._s4war.coreTurrets.length===2&&boss._s4war.coreTurrets.every(d=>!!d._sg17)'))
  p.select_option('#flight','decker');p.wait_for_function('!busy');frames(2)
  check('Playing Decker produces live Cole radio guidance',w.evaluate('boss._st18.radio.who==="cole"'));p.screenshot(path=str(O/'review-decker-cole-comms.png'))
  p.select_option('#flight','both');p.wait_for_function('!busy');frames(2)
  row=w.evaluate('''()=>({seats:seatList().length,pilots:seatList().map(s=>withSeat(s,()=>_pilotKey())),speaker:boss._st18.radio.who,rows:SC12.layout.rows,field:SC12.layout.field})''')
  check('Actual Cole/Decker co-op uses Axel comms and both side-HUD rows',row['seats']==2 and row['pilots']==['cole','decker'] and row['speaker']=='axel' and row['rows']==2,row)
  p.screenshot(path=str(O/'review-coop-axel-comms.png'))
  p.select_option('#flight','cole');p.wait_for_function('!busy');p.select_option('#scene','panic');p.wait_for_function('document.querySelector("#status").textContent.startsWith("Overload")');frames(45)
  check('Review overload scene starts real glow and non-pausing comms',w.evaluate('boss._p4Final.phase==="panic"&&boss._sa14.glow>.5&&boss._st18.radio.id==="overload"&&!story&&state===GS.PLAY'))
  p.screenshot(path=str(O/'review-overload.png'));frames(400)
  check('Review naturally completes ram and overhead return into pursuit',w.evaluate('boss._p4Final.phase==="rear"&&boss._sa14.angle===Math.PI&&boss._p4Final.roadSpeed>950'))
  # Compact rendering also uses the existing housing and does not hide counts.
  p.set_viewport_size(dict(width=700,height=1000));frames(2)
  check('Narrow review switches to its existing compact HUD while keeping radio',w.evaluate('SC12.mode==="compact"&&ST18.draws.radio>0'))
  p.screenshot(path=str(O/'review-compact.png'))
  check('Review has no native page, console, draw or asset errors',not errors,errors[:20]);br.close()
finally:stop()
report=dict(checks=checks,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),errors=errors)
(O/'review-report.json').write_text(json.dumps(report,indent=2));print(f"{report['passed']} passed / {report['failed']} failed",flush=True)
sys.exit(1 if report['failed'] else 0)
