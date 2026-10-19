"""Delivered review page,16 registered animation frames, full FOV and actual controls."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage4_engine_1018/review';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage4_engine_1018/');p.wait_for_function("""ready&&!busy&&game.contentWindow.eval("subBossActive&&!!mr27Part(subBoss,'gunC')")""");g=p.frames[1]
  check('Warden review starts with isolated saves and the new central weapon',g.evaluate('window.__stage4ReviewStorage&&run.stage===4&&diffKey==="normal"&&SC12.active()&&wc18Ready()'))
  g.locator('body').click(position=dict(x=850,y=600));p.keyboard.down('j');p.wait_for_timeout(300)
  check('Actual keyboard fire reaches the review game',g.evaluate('Input.down("j")&&pBullets.length>0'));p.keyboard.up('j')
  row=g.evaluate('''()=>{const b=subBoss,p=mr27Shape(b,'gunC'),out=[];for(let i=0;i<16;i++){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);const key=WC18_ART.frames[i].key,ready=XART.rdy(key),ok=mr27Blit('iron',100+i,p,0,null,b),d=ctx.getImageData(0,0,cv.width,cv.height).data;let pixels=0;for(let k=3;k<d.length;k+=4)if(d[k]>100)pixels++;ctx.restore();out.push({key,ready,ok,pixels});}drawWorld(0);return out;}''')
  check('All16 poses draw actual XART pixels through the game context',all(q['ready'] and q['ok'] and q['pixels']>200 for q in row),row)
  p.screenshot(path=str(O/'warden-review.png'))
  for diff in ['normal','hard','furious']:
   p.select_option('#difficulty',diff);p.wait_for_function('!busy');p.select_option('#scene','highway');p.wait_for_function('!busy&&game.contentWindow.eval("enemies.some(e=>e._hm17)")')
   p.wait_for_timeout(500)
   row=g.evaluate('''()=>{const tanks=enemies.filter(groundTrafficVehicle),pairs=[];for(let i=0;i<tanks.length;i++)for(let j=i+1;j<tanks.length;j++)if(groundTrafficTouch(tanks[i],tanks[j]))pairs.push([i,j]);return{tanks:tanks.length,pairs,pads:enemies.filter(e=>e._hm17&&!e.dead).length,size:[VW,VH,viewW()],hud:SC12.active()};}''')
   check(diff+' review shows separated tanks, both shoulders and regular side HUD',row['tanks']>=5 and not row['pairs'] and row['pads']>=2 and row['size']==[480,512,480] and row['hud'],row)
   p.screenshot(path=str(O/(diff+'-highway.png')))
  p.select_option('#scene','return');p.wait_for_function('!busy&&game.contentWindow.eval("groundTargetingFx.some(q=>q._hm17Return)")')
  check('Atomic return scene exposes the actual committed ground target',g.evaluate('groundTargetingFx.some(q=>q._hm17Return&&!q.track&&q.owner===null)'))
  p.screenshot(path=str(O/'return-warning.png'))
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage4_engine_1018/frames.html');p.wait_for_function('frames.length===16&&frames.every(q=>q.complete&&q.naturalWidth===256)')
  p.click('#play');p.check('#onion');p.locator('#frame').fill('9')
  row=p.evaluate('''()=>({pose,onion:document.querySelector('#onion').checked,size:WC18_ART.frames.map(a=>[a.w,a.h,a.pivot]),pixels:g.getImageData(0,0,512,512).data.filter((v,i)=>i%4===3&&v>100).length})''')
  check('All16 even frames render with fixed pivots and working onion scrubbing',row['pose']==9 and row['onion'] and all(a==[256,256,[128,104]] for a in row['size']) and row['pixels']>10000,row)
  p.screenshot(path=str(O/'onion-firing.png'))
  check('Every generated pose has a native registered draw',p.evaluate('()=>{for(let i=0;i<16;i++){pose=i;draw();if(!g.getImageData(210,180,90,90).data.some((v,k)=>k%4===3&&v>100))return false;}return true;}'))
  br.close()
finally:stop()
check('No review page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
