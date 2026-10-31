"""Input-only normal difficulty route; no health, kill or encounter shortcuts."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/bastion20/runtime';OUT.mkdir(parents=True,exist_ok=True);errors=[]
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',timeout=90000,wait_until='domcontentloaded');page.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000)
  page.evaluate('''TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TDGAME.G.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Achievements.queue=[];
   window.bot={last:null,decisions:0,cover:0,move:0,fire:0,blindfire:0,grenadeWave:0,stages:[],target:null,controller:false,minHP:6};
   TD.Input.update=function(){const G=TD.game,p=G.player,c=G.bastion,b=window.bot;this.last=this.state;let s={};
    if(G.state==='play'&&!p.dead&&(G.t%12===0||!b.last)){
     b.decisions++;b.minHP=Math.min(b.minHP,p.hp);const stage=c.totalWave+':'+c.phase+':'+(G.boss?.form||'');if(!b.stages.includes(stage))b.stages.push(stage);
     let dodge=0,duck=false;const wall=TD.Bastion.coverAt(G,p.x),live=G.units.filter(u=>!u.dead&&u.phase!=="queued"&&u.y>90).sort((a,b)=>b.y-a.y),near=live.filter(u=>u.phase==='flank');
     for(const e of c.enemyShots){const left=e.duration-e.t;if(Math.abs(e.tx-p.x)<(e.kind==='rocket'?64:33)&&left<.48&&left>-.03){if(e.near||!wall.hp){dodge=p.x<=e.tx?-1:1;if(p.x<95)dodge=1;if(p.x>545)dodge=-1;}else duck=true;}}
     for(const ray of c.coreRays||[]){if(!ray.active||G.boss?.form!=='core')continue;const bx=G.boss.x,by=G.boss.y,dx=Math.cos(ray.angle)*340,dy=Math.sin(ray.angle)*340,ax=p.x-bx,ay=402-by,k=Math.max(0,Math.min(1,(ax*dx+ay*dy)/(dx*dx+dy*dy)));if(Math.hypot(ax-dx*k,ay-dy*k)<42){if(wall.hp)duck=true;else dodge=p.x<320?-1:1;}}
     for(const h of c.hazards){if(Math.abs(p.x-h.x)<(h.kind==='geyser'?91:88)&&h.t<h.delay+h.duration){if(h.kind==='geyser'&&h.delay-h.t<.9){dodge=p.x<=h.x?-1:1;if(p.x<110)dodge=1;if(p.x>530)dodge=-1;}else if(h.kind==='beam'&&h.delay-h.t<.45){if(wall.hp)duck=true;else dodge=p.x<=h.x?-1:1;}}}
     let actor=near[0]||live.find(u=>u.canVault&&u.y>270)||live[0]||(c.turrets||[]).find(t=>t.hp>0)||(c.wallCore?.hp>0?c.wallCore:null);let target=actor?(actor.scale?TD.Bastion.unitBody(actor):{x:actor.x,y:actor.y}):null;
     const barrel=c.barrels.find(a=>!a.dead&&live.filter(u=>{const q=TD.Bastion.unitBody(u);return Math.hypot(q.x-a.x,q.y-(a.y-20))<126;}).length>=2);if(barrel&&!near.length)target={x:barrel.x,y:barrel.y-24};
     if(!target&&G.boss&&!G.boss.dead)target=TD.Bastion.bossBody(G.boss);
     if(target){b.target={x:target.x,y:target.y};this.pointer.active=!b.controller;this.pointer.x=Math.max(24,Math.min(616,target.x));this.pointer.y=Math.max(78,Math.min(449,target.y));}
     s={A:!!target,cover:duck,left:dodge<0,right:dodge>0};if(near.length&&!dodge){s.B=true;s.left=near[0].x<p.x;s.right=!s.left;}
     if(live.length>=3&&b.grenadeWave!==c.totalWave&&p.smoke>0&&!p.grenadeCd){s.Y=true;b.grenadeWave=c.totalWave;}
     if(dodge)b.move++;if(duck)b.cover++;if(s.A)b.fire++;if(duck&&s.A)b.blindfire++;b.last={...s};
    }else s={...(b.last||{})};
    if(b.controller&&b.target&&!s.B&&!s.left&&!s.right){this.pointer.active=false;s.retina=true;const ax=b.target.x-c.cursor.x,ay=b.target.y-c.cursor.y;s.left=ax< -4;s.right=ax>4;s.up=ay< -4;s.down=ay>4;}
    this.state=s;this.raw={};
   };''')
  for i in range(420):
   if page.evaluate('TD.game.state==="clear"||TD.game.state==="gameover"'):break
   page.evaluate('TDGAME.step(60)');page.wait_for_timeout(1)
   if i%30==0:print(page.evaluate('({time:TD.game.time,wave:TD.game.bastion.totalWave,hp:TD.game.player.hp,deaths:TD.game.deaths,boss:TD.game.boss?.hp})'),flush=True)
   if i in [8,29,58,88]:page.evaluate('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/f'route_{i}.png'))
  result=page.evaluate('({state:TD.game.state,time:TD.game.time,wave:TD.game.bastion.totalWave,hp:TD.game.player.hp,deaths:TD.game.deaths,kills:TD.game.kills,coverStops:TD.game.bastion.coverStops,brokenWalls:TD.game.bastion.brokenWalls,barrelKills:TD.game.bastion.barrelKills,damage:TD.game.bastion.damage,pickupLog:TD.game.bastion.pickupLog,gunShots:TD.game.bastion.gunShots,quickShots:TD.game.bastion.quickShots,transitionLog:TD.game.bastion.transitionLog,coreLog:TD.game.bastion.coreLog,boss:TD.game.boss?{form:TD.game.boss.form,hp:TD.game.boss.hp}:null,bot:window.bot})')
  result['errors']=errors;result['scope']='Normal armor input-only complete stage; decisions 200ms, pointer aim. No actor-health writes or kill APIs.';(OUT/'route.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));page.evaluate('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/'route_end.png'));browser.close()
finally:stop()
sys.exit(0 if result['state']=='clear' and result['deaths']==0 and not errors else 1)
