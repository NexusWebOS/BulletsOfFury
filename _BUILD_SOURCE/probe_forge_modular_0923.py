"""Real Chromium pointer, wheel and keyboard checks for the modular Forge selector."""
import base64,json,sys,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,TRAP_RAF,serve
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/forge_modular_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[];results={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1500,'height':900})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(TRAP_RAF)
  pg.evaluate(SETUP,{'state':'PLAY','stage':3,'pilot':'axel','invuln':False})
  pg.evaluate("()=>{run.stage=3;run.spaceMode=false;run.weapon=3;run.wlevel=8;run.wlevels=WEAPONS.map(()=>8);run.loadout=[3,0,1,2,4,5];run.forge={};run.forgeForms={};run.forgeElems=Object.fromEntries(Object.keys(INFUSIONS).map(e=>[e,1]));forgeStart();forge.row=1;forge.sel=run.loadout.indexOf(3);forge.esel=0;window.renderForge=()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);drawForge(1/60);ctx.restore();Input.clearTaps();};}")
  for _ in range(8):pg.evaluate('()=>{for(let i=0;i<15;i++)renderForge()}');pg.wait_for_timeout(80)
  pg.wait_for_function("()=>XART.rdy('forge_chamber_modular_0923')&&['track_top','track_middle','track_bottom','thumb_normal','thumb_hover','thumb_pressed','button_normal','button_hover'].every(k=>XART.rdy('forge_scroll_'+k))")
  def tick():pg.evaluate('renderForge()')
  def capture(name):
   tick();(OUT/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]")))
  def snapshot():return pg.evaluate('()=>({esel:forge.esel,first:forge.scroll,charges:run.forgeCombos,row:forge.row,drag:forge.drag,level:forge.preview.lv})')
  def pos(expr):return pg.evaluate("()=>{const W=cutsceneViewWidth(),H=VH,F=forge,D=forgeElemsFor(run.loadout[F.sel]),V=forgeElementRailView(F,D,W,H),r=document.getElementById('screen').getBoundingClientRect(),p="+expr+";return [r.left+p[0]/W*r.width,r.top+p[1]/H*r.height]}")
  def click(expr):
   pg.mouse.move(*pos(expr));pg.mouse.down();tick();pg.mouse.up();tick()
  initial=snapshot();capture('first_firewhip')
  click('[V.down[0]+V.down[2]/2,V.down[1]+V.down[3]/2]')
  results['arrow']=snapshot();assert results['arrow']['first']==1 and results['arrow']['esel']==1,results
  capture('middle_ice')
  pg.mouse.move(*pos('[.1*W,.4*H]'));pg.mouse.wheel(0,100);pg.wait_for_timeout(60);tick()
  results['wheel']=snapshot();assert results['wheel']['esel']==2,results
  pg.keyboard.press('ArrowDown');tick();assert snapshot()['esel']==3
  # Drag the actual thumb through its full range, with real browser pointer events.
  pg.mouse.move(*pos('[V.thumb[0]+V.thumb[2]/2,V.thumb[1]+V.thumb[3]/2]'));pg.mouse.down();tick()
  pg.mouse.move(*pos('[V.thumb[0]+V.thumb[2]/2,V.track[1]+V.track[3]-V.thumb[3]/2]'));tick();pg.mouse.up();tick()
  results['drag_bottom']=snapshot();assert results['drag_bottom']['first']==4,results
  # The last bay selects DARK without combining, even if clicked twice.
  click('[.097*W,.710*H]');click('[.097*W,.710*H]');results['bay']=snapshot()
  assert results['bay']['esel']==8 and results['bay']['charges']==initial['charges'] and results['bay']['row']==1,results
  for _ in range(6):pg.evaluate('()=>{for(let i=0;i<15;i++)renderForge()}');pg.wait_for_timeout(50)
  capture('last_dark');pg.keyboard.press('ArrowDown');tick();assert snapshot()['esel']==8
  click('[V.up[0]+V.up[2]/2,V.up[1]+V.up[3]/2]');assert snapshot()['first']==3
  # Record actual drawing through the game context, including transform-scaled ship height.
  results['draw']=pg.evaluate("()=>{const raw=ctx.drawImage,get=XART.get,hs=[];let shipRequested=false;XART.get=function(key){shipRequested=key==='ship_'+_pilotKey();return get.call(this,key)};ctx.drawImage=function(im,...a){if(shipRequested&&a.length===4)hs.push(a[3]*this.getTransform().d);shipRequested=false;return raw.call(this,im,...a)};try{renderForge()}finally{ctx.drawImage=raw;XART.get=get}return {shipHeights:hs,canvas:ctx.canvas.width,viewport:cutsceneViewWidth(),preview:forge.preview.err};}")
  assert results['draw']['shipHeights'] and max(results['draw']['shipHeights'])>=75,results
  assert not errors,errors
  results['errors']=errors;(OUT/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2));br.close()
finally:stop()
