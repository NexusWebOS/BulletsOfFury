import json,http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path(sh.GAME)/'_shots/stagex_water_0928';port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1360,'height':960});p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("""()=>{run.mode='campaign';run.pilot='cole';campaign.unlockedMax=8;campaign.rivalScattered=true;campaign.rivalDefeated=[false,false,false,false,false];sselBoot=0;stateT=2;Input.clearTaps();Input.injectTap('arrowdown');Rival24.mapInput();Input.injectTap('enter');Rival24.mapInput();Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('arrowright');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);XART.rdy('r24_card');XART.rdy('fr27_stagex_terrain');}""")
  p.wait_for_function("()=>XART.rdy('r24_card')&&XART.rdy('fr27_stagex_terrain')")
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);stateT=0;Rival24.cardDraw(.1);}');p.screenshot(path=str(out/'stagex-card.png'))
  report=p.evaluate("()=>({active:!!Rival24.active,alive:boss._rebels.ships.filter(q=>!q.dead).length,hp:boss.hp})")
  p.evaluate("()=>{setState(GS.PLAY);rebelSquadTick(boss,30);story=null;player.invuln=0;boss._rebels.frRadio=null;const q=boss._rebels.ships.find(q=>!q.dead);q.x=worldWidth()/2;q.y=150;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}");p.wait_for_timeout(450);p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');p.screenshot(path=str(out/'stagex-arena.png'))
  p.evaluate("()=>{stageTimer=12;_liquidFrames('nlq2_water');}")
  p.wait_for_function("()=>_liquidFrames('nlq2_water').every(im=>ASSETS.rdy(im))")
  report['water']=p.evaluate("()=>({frames:_liquidFrames('nlq2_water').length,alpha:(()=>{const im=XART.get('fr27_stagex_terrain'),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const x=c.getContext('2d');x.drawImage(im,0,0);return x.getImageData(512,700,1,1).data[3];})()})")
  for i in range(4):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawBG(0);}')
   p.screenshot(path=str(out/('water-'+str(i)+'.png')));p.wait_for_timeout(220)
  from PIL import Image,ImageChops
  images=[Image.open(out/('water-'+str(i)+'.png')).convert('RGB') for i in range(4)]
  report['water']['pixel_changes']=sum(ImageChops.difference(images[0].crop((600,300,720,600)),im.crop((600,300,720,600))).getbbox() is not None for im in images[1:])
  assert report['water']['alpha']==0 and report['water']['frames']==4 and report['water']['pixel_changes']>0,report
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  p.screenshot(path=str(out/'animated-water-in-game.png'))
  report['finish']=p.evaluate('()=>{const which=Rival24.active.rival;Rival24.finish();return {which,defeated:campaign.rivalDefeated,stage:run.stage,active:!!Rival24.active};}')
  report['errors']=errors;(out/'stagex-probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));b.close()
finally:stop()
