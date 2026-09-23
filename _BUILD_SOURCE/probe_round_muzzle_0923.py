"""Real Chromium: generated circular muzzles on player beam and spaceship hardpoints."""
import base64,json,sys,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,TRAP_RAF,serve
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/round_muzzle_players_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[];results={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4')
  pg.evaluate(TRAP_RAF);pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False})
  pg.evaluate("""()=>{story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;
    player.x=240;player.y=420;player.invuln=0;player.dead=false;player.roll=0;shake=0;camX=0;efxClock=.12;
    window.roundDraws=[];let active=null;const muzzle=roundLaserMuzzleDraw;
    roundLaserMuzzleDraw=function(g,x,y,size,col,frame){active={x,y,size,col,frame};try{return muzzle(...arguments)}finally{active=null}};
    const draw=ctx.drawImage;ctx.drawImage=function(im,x,y,w,h){if(active){const m=ctx.getTransform();roundDraws.push({...active,source:[im.width,im.height],centered:Math.abs(x+w/2)<1e-6&&Math.abs(y+h/2)<1e-6,matrix:[m.a,m.b,m.c,m.d,m.e,m.f]});}return draw.apply(this,arguments)};
    for(let i=0;i<8;i++)XART.rdy('laser_round_muzzle_'+i);
    for(const k of ['forge_fire_laser_0918','forge_elem_ice_laser_0918'])XART.rdy(k);
  }""")
  pg.wait_for_function("()=>[0,1,2,3,4,5,6,7].every(i=>XART.rdy('laser_round_muzzle_'+i))&&XART.rdy('forge_fire_laser_0918')&&XART.rdy('forge_elem_ice_laser_0918')")
  def shot(name):
   pg.evaluate('()=>{roundDraws=[];shake=0;drawWorld(0)}');pg.wait_for_timeout(30)
   pg.evaluate('()=>{roundDraws=[];drawWorld(0)}')
   (OUT/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]")))
   values=pg.evaluate('()=>roundDraws');assert values and all(q['centered'] and q['source']==[128,128] for q in values),values
   results[name]=values
  for lv in range(1,6):
   pg.evaluate("lv=>{pBullets=[{kind:'beam',x:240,top:80,bot:player.y-14,lv,w:14+lv*4,t:.1}];}",lv)
   shot(f'held_level_{lv}');assert len(results[f'held_level_{lv}'])==1
  for element in ['fire','ice']:
   pg.evaluate("e=>{pBullets[0]._inf=e;pBullets[0]._infLv=1}",element);shot('held_'+element)
  pg.evaluate(SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':False})
  pg.evaluate("()=>{run.spaceMode=true;story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;player.invuln=0;player._spaceMuzzle=.08;player.x=240;player.y=420;}")
  for i in range(4):pg.evaluate('()=>drawWorld(0)');pg.wait_for_timeout(100)
  shot('spaceship');assert len(results['spaceship'])==2,results['spaceship']
  assert abs(results['spaceship'][0]['y']-results['spaceship'][1]['y'])<.01
  assert results['spaceship'][0]['x']!=results['spaceship'][1]['x']
  # Shared enemy laser flashes must ride their live follow callback as the barrel moves.
  pg.evaluate("()=>{player._spaceMuzzle=0;window.mount={x:200,y:250};_navalFlashes.length=0;navalFlash(null,mount,1,BPFX_MUZZLE_LASER,{n:8,hpx:40,follow:()=>mount});mount={x:290,y:300};}")
  shot('shared_boss');assert any(q['x']==290 and q['y']==300 for q in results['shared_boss'])
  assert not errors,errors
  (OUT/'results.json').write_text(json.dumps({'cases':results,'errors':errors},indent=2));print('PASS: five beam tiers, fire/ice beams, two spaceship muzzles and moving boss socket; no browser errors.');br.close()
finally:stop()
