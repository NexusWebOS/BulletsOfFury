from pathlib import Path
import sys,json,http.server,base64,time
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/maneuver_safety_1007/whirl_comparison';O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None;port,stop=shoot.serve(str(R));rows=[];errors=[]
TEST='''c=>{BAL7.setup({stage:5,kind:'chromehammer',diff:c.diff,pilot:'juggernaut',level:0,seed:7});const b=B,h=b._hammer;b.x=24;b.y=200;b.enter=b._noHit=false;player.x=55;player.y=c.y;player.dead=false;player.invuln=0;run.shield=0;h.whirl={l:24,r:worldWidth()-24,dir:1,pass:1,passes:2,reel:0};hammerWhirlLane(b,false);h.hitCd=0;const warm=h.whirl.warm,cy=h.whirl.y+36;let t=0;const dir=player.y>=cy?1:-1;for(let i=0;i<300&&!player.dead;i++){t+=1/60;BAL7.q.t=t;if(!c.stationary&&t>=.4)player.y=clamp(player.y+dir*playerBaseSpeed()*1.35,PLAY.y+12,VH-12);h.t+=1/60;hammerCombatTick(b,1/60);if(t>warm+1.6)break;}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return{...c,warm,survived:!player.dead,yEnd:player.y,hits:BAL7.q.hits};}'''
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--mute-audio'])
  for candidate in [False,True]:
   p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   p.goto(f'http://127.0.0.1:{port}/index.html?quality=performance');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
   if candidate:p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_recovery_candidate_1007b.js'))
   p.evaluate("()=>BAL7.setup({stage:5,kind:'chromehammer',diff:'normal'})")
   for i in range(1500):
    p.evaluate('()=>{stageLoadTick();drawWorld(0);}');p.wait_for_timeout(20)
    if p.evaluate('()=>stageLoadInfo(5).ready'):break
   for diff in ['easy','normal','hard','furious']:
    for y in [200,300,400]:
     for stationary in [False,True]:
      rows.append(p.evaluate(TEST,dict(candidate=candidate,diff=diff,y=y,stationary=stationary)))
   (O/('after.png' if candidate else 'before.png')).write_bytes(base64.b64decode(p.evaluate("()=>cv.toDataURL().split(',')[1]")));p.close()
  b.close()
finally:stop()
(O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2),encoding='utf-8')
for candidate in [False,True]:
 r=[q for q in rows if q['candidate']==candidate];print('candidate',candidate,'moving',sum(q['survived'] for q in r if not q['stationary']),'/12','controlsHit',sum(not q['survived'] for q in r if q['stationary']),'/12')
print('errors',errors);assert not errors
