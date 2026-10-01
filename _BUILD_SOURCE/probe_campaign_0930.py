from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_0930';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=sh.serve(str(R));errors=[];report={}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
  p.evaluate("()=>{run.mode='campaign';run.pilot='yuri';campaign.unlockedMax=8;campaign.rank={1:'S',2:'A',3:'B'};campaign.bonusUnlocked=false;campaign.rivalScattered=false;Rival24.mapAvailable=false;Rival24.flying=false;Rival24.mapFocused=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;cmap2Warm();}")
  p.wait_for_function("()=>Object.keys(MAP30_ART).every(k=>XART.rdy('map30_'+k))&&cmap2Keys().every(k=>XART.rdy(k))&&PILOTS.every(p=>XART.rdy('ship_'+p.key))",timeout=60000)
  p.wait_for_timeout(4000);p.screenshot(path=str(O/'overview.png'))
  report['clicks']=[]
  for stage in [2,3,4,5,6,7,8,1]:
   point=p.evaluate("s=>{const q=cmap2ToScreen(...Object.values(cmap2World(s))),r=cv.getBoundingClientRect();return {x:r.left+(q.x+campaignViewOffset())/campaignViewWidth()*r.width,y:r.top+q.y/VH*r.height};}",stage)
   p.mouse.click(point['x'],point['y'],delay=160);p.wait_for_timeout(180)
   report['clicks'].append({'expected':stage,'actual':p.evaluate('()=>sselCursor'),'state':p.evaluate('()=>state')})
  p.evaluate(sh.TRAP_RAF)
  report['layout']=p.evaluate("()=>({world:[CM2_W,CM2_H],hub:cmap2World('hub'),portal:cmap2World(9),cam:cmap2.cam,stagePoints:CM2_ISLANDS.map(s=>({s,...cmap2World(s)})),errors:cmap2._err})")
  report['headings']=p.evaluate("""()=>{const out=[];for(const s of [1,4,7,3,6,2]){sselCursor=s;for(let i=0;i<180;i++){sselShipUpdate(1/60);out.push({head:sselShip.head,face:sselShip.face,bank:sselShip.bank});}}return {count:out.length,horizontal:out.every(q=>Math.abs(Math.abs(q.head)-Math.PI/2)<.00001&&q.bank===0),faces:[...new Set(out.map(q=>q.face))]};}""")
  # Native canvas reads: all nine portraits' left/right map hulls.
  data=p.evaluate("""()=>{const c=document.createElement('canvas');c.width=720;c.height=9*105;const g=c.getContext('2d');g.fillStyle='#122331';g.fillRect(0,0,c.width,c.height);g.font='18px monospace';g.fillStyle='#fff';PILOTS.forEach((p,i)=>{g.fillText(p.key,12,i*105+48);[-1,1].forEach((face,n)=>{const im=map30ShipFrame('ship_'+p.key,face);g.drawImage(im,190+n*265,i*105+5,145,90);});});return c.toDataURL().split(',')[1];}""")
  (O/'ship_headings.png').write_bytes(base64.b64decode(data))
  # Selection uses the real menu handler. Don't assign the result under test.
  p.evaluate("()=>{sselCursor=1;cmap2.focus='map';window.sselCommitted=false;_selFlash=null;sselZoom=null;Input.injectTap('arrowright');}")
  p.evaluate(sh.STEP,6);report['navigation']=p.evaluate('()=>({stage:sselCursor,focus:cmap2.focus})')
  p.evaluate(sh.STEP,180);p.screenshot(path=str(O/'selection.png'))
  # The sun-wave remains scenery, and clicking it reports the lock.
  v=p.evaluate("()=>{const q=cmap2ToScreen(MAP30.westX,600),r=cv.getBoundingClientRect();return {x:r.left+(q.x+campaignViewOffset())/campaignViewWidth()*r.width,y:r.top+q.y/VH*r.height,stage:sselCursor};}")
  p.mouse.click(v['x'],v['y']);report['frontier']=p.evaluate('()=>({stage:sselCursor,toast:cmap2.toast,bonus:campaign.bonusUnlocked})')
  p.evaluate(sh.STEP,3);p.screenshot(path=str(O/'frontier.png'))
  # Far-north portal still reaches the correct camera and island hit test.
  p.evaluate("()=>{campaign.bonusUnlocked=true;openStageSelect(9,{});sselBoot=0;sselUnlockCine=null;s9MapCine=null;riftReturn=null;}")
  for i in range(5):p.evaluate(sh.STEP,60);p.wait_for_timeout(40)
  report['portal']=p.evaluate('()=>{const q=cmap2ToScreen(...Object.values(cmap2World(9)));return {point:q,hit:cmap2IslandAt(q.x,q.y,9,9),cam:cmap2.cam};}')
  p.screenshot(path=str(O/'portal.png'))
  p.set_viewport_size({'width':1000,'height':900});p.evaluate("()=>{campaign.bonusUnlocked=false;openStageSelect(4,{});sselBoot=0;sselUnlockCine=null;}")
  for i in range(5):p.evaluate(sh.STEP,60);p.wait_for_timeout(50)
  p.screenshot(path=str(O/'compact.png'));report['errors']=errors;b.close()
finally:stop();(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not errors,errors
assert all(q['expected']==q['actual'] and q['state']=='stagesel' for q in report['clicks']),report['clicks']
assert report['headings']['horizontal'] and set(report['headings']['faces'])=={-1,1}
assert report['navigation']['stage']!=1
assert report['frontier']['stage']==v['stage'] and 'SEALED' in report['frontier']['toast']
assert report['portal']['hit']==9
