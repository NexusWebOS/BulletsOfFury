"""Native HUD checks: live model, actual keyboard actions, pixels and persistence."""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/hud27';O.mkdir(exist_ok=True);checks=[];errors=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  url=f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1015-hud27-r1'
  p.goto(url,wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate
  ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";ART.warm([...Object.keys(TD_HUD27_ART.assets),"pav_yuri"]);');p.keyboard.press('Shift');p.wait_for_function('ART.progress(Object.keys(TD_HUD27_ART.assets))===1&&!!ART.get("pav_yuri")',timeout=120000)
  def frames(n):
   while n:k=min(n,30);ev(f'TDGAME.step({k})');p.wait_for_timeout(1);n-=k
  def fresh(l):ev(f'TD.game.sel=TD.MISSIONS.findIndex(m=>m.id==={l});TDGAME.start();TD.Achievements.queue=[];')
  def shot(n):ev('TD.game.player.inv=0;TD.game.player.flash=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(n+'.png')))
  def model():ev('TDGAME.render()');return ev('TD.CornerHUD26.last')
  check('all generated HUD components and80font cells decode with even dimensions',ev('Object.values(TD_HUD27_ART.assets).length===90&&Object.values(TD_HUD27_ART.assets).every(m=>m.size.every(n=>n%2===0))'))
  check('all80 generated glyphs are registered and renderable',ev('Object.values(TD_HUD27_ART.font.glyphs).length===80&&Object.values(TD_HUD27_ART.font.glyphs).every(g=>!!ART.get(g.key))'))
  fresh(3);frames(5);shot('stage3_corner_hud');v=model();check('stage3 selected Yuri portrait and live lives/health',v['pilot']=='yuri'and v['lives']==ev('TD.game.lives')and v['hp']==ev('TD.game.player.hp'))
  ev('window.hud26Draws=[];window.hud26Original=ART.draw;ART.draw=function(ctx,k,...a){hud26Draws.push(k);return hud26Original(ctx,k,...a);};TDGAME.render();ART.draw=hud26Original;void 0;')
  check('old full-width top and bottom panels are no longer drawn',ev('!["pb20_hud_top","pb20_hud_bottom"].some(k=>hud26Draws.includes(k))&&["corner26_portrait","corner26_health","hud27_equipment"].every(k=>hud26Draws.includes(k))'))
  check('three HUD regions are confined to the top corners and center',v['regions']=={'left':[8,8,208,56],'center':[220,8,200,36],'right':[428,8,204,78]})
  ev('TD.game.score=54321');v=model();check('score and high score follow the live score',v['score']==54321 and v['highScore']>=54321)
  ev('TD.game.score=120');v=model();check('high score does not fall on a lower/new run',v['score']==120 and v['highScore']>=54321)
  ev('TD.game.player.hp=TD.game.player.max/2');half=model();shot('stage3_half_health');check('generated health fills clip proportionally',half['healthFillPixels']==64)
  ev('TD.game.player.hp=0');empty=model();check('empty health draws no fill',empty['healthFillPixels']==0)
  ev('TD.game.player.hp=TD.game.player.max');full=model();check('full health restores all generated fill segments',full['healthFillPixels']==128)
  ev('TD.game.player.weapons=[{id:"minigun",ammo:12,reserve:60,lv:1}];TD.game.player.wi=0;TD.game.player.inv=999;')
  check('stage3 finite gun ammunition is displayed',model()['ammo']=='12')
  p.keyboard.down('j');frames(1);p.keyboard.up('j');v=model();check('stage3 shooting updates the live ammo counter',int(v['ammo'])<12)
  p.keyboard.down('r');frames(1);p.keyboard.up('r');check('stage3 jump input reports the current JUMPING action',model()['status']=='JUMPING')
  frames(42);p.keyboard.press('u');frames(2);check('stage3 grenade animation reports GRENADE',model()['status']=='GRENADE')
  fresh(7);frames(150);shot('stage7_corner_hud');v=model();check('stage7 automatic cover reports IN COVER with unlimited rifle ammo',v['status']=='IN COVER'and v['ammo']=='∞')
  p.keyboard.press('f');frames(2);check('prone input updates action status',model()['status'] in ['PRONE','WALL PRONE'])
  p.keyboard.down('d');frames(4);check('moving while prone reports CRAWLING',model()['status']=='CRAWLING');p.keyboard.up('d');frames(1)
  p.keyboard.press('h');frames(2);check('actual roll into prone reports its current action',model()['status']=='ROLL TO PRONE');shot('stage7_rolling');frames(32)
  p.keyboard.press('f');frames(2);p.keyboard.down('i');frames(12);check('retina input reports FREE AIM',model()['status']=='FREE AIM');p.keyboard.up('i');frames(12)
  p.keyboard.down('Shift');p.keyboard.down('j');frames(12);check('cover firing reports BLINDFIRE',model()['status']=='BLINDFIRE');shot('stage7_blindfire');p.keyboard.up('j');p.keyboard.up('Shift');frames(12)
  ev('TD.game.player.groundGun="minigun";TD.game.player.gunAmmo=75;');check('stage7 finite powerup ammo is displayed',model()['ammo']=='75')
  p.keyboard.down('j');frames(12);p.keyboard.up('j');v=model();check('actual stage7 minigun fire consumes the shown ammo',int(v['ammo'])<75)
  ev('TD.game.player.inv=0;TD.Bastion.harm(TD.game,5)');v=model();shot('stage7_low_health');check('damage changes the generated health fill',v['hp']==1 and v['healthFillPixels']==21)
  fresh(3);ev('TD.game.units=[];TD.game.fortress.pending=[];TD.game.player.x=400;TD.game.player.y=428;TD.game.boss=TD.makeGosfer(TD.game,400,195);');frames(165);shot('gosfer_corner_hud');check('Gosfer boss bar remains separate from player HUD',ev('TD.game.boss.name==="GOSFER"&&TD.game.boss.shield&&!!ART.get("pb20_hud_boss")'))
  ev('window.hud27BossY=null;const old=ART.draw;ART.draw=function(ctx,k,x,y,...a){if(k==="pb20_hud_boss")window.hud27BossY=y;return old(ctx,k,x,y,...a);};TDGAME.render();ART.draw=old;void 0;');check('boss bar clears the player health gauge vertically',ev('window.hud27BossY===113'))
  ev('TD.game.boss.state="dialogue";TD.game.boss.line=1;TD.game.boss.lineT=.5;');shot('dialogue_corner_hud');check('portrait dialogue retains its generated frame',ev('!!ART.get("pb20_hud_dialogue")'))
  fresh(7);frames(120);ev('TD.game.player.inv=0;TD.game.player.flash=0;TD.Hud27.roomBrightness=1;');shot('room_brightness_before')
  ev('TD.Hud27.roomBrightness=.75;');shot('room_brightness_after')
  from PIL import ImageStat,ImageChops
  before=Image.open(O/'room_brightness_before.png').convert('RGB');after=Image.open(O/'room_brightness_after.png').convert('RGB');sx=before.width/640;sy=before.height/480
  regions=[(12,130,90,285),(540,120,625,285),(300,280,340,290)]
  ratios=[]
  for x0,y0,x1,y1 in regions:
   box=(round(x0*sx),round(y0*sy),round(x1*sx),round(y1*sy));a=sum(ImageStat.Stat(before.crop(box)).sum);z=sum(ImageStat.Stat(after.crop(box)).sum);ratios.append(z/a)
  check('room pixels are25percent darker in the native renderer',all(.73<q<.77 for q in ratios))
  box=(round(442*sx),round(22*sy),round(610*sx),round(65*sy));check('equipment HUD is unaffected by room darkening',ImageChops.difference(before.crop(box),after.crop(box)).getbbox()is None)
  v=model();check('custom generated Overdrive font draws every HUD string',v['font']=='Overdrive Arcade HUD'and ev('TD.Hud27.stats.glyphs>0&&TD.Hud27.lastText.length===7'))
  check('ammo and action labels are centered inside their inset fields',ev('TD.Hud27.lastText.slice(-2).every(t=>t.x===565&&t.width<=t.boxWidth)&&TD.Hud27.lastText.at(-2).y===32&&TD.Hud27.lastText.at(-1).y===58'))
  for gun in ['rifle','shotgun','laser','minigun']:
   ev(f'TD.game.player.groundGun="{gun}";TD.game.player.gunAmmo=87;TDGAME.render();');shot('equipped_'+gun)
   check('correct generated HUD gun for '+gun,ev('!!ART.get(TD.CornerHUD26.last.weaponKey)&&TD.CornerHUD26.last.weaponKey===({rifle:"hud27_gun_rifle",shotgun:"hud27_gun_spread_shotgun",laser:"hud27_gun_fusion_beam",minigun:"hud27_gun_minigun"})[TD.game.player.groundGun]'))
  ev('TD.game.player.groundGun="rifle";TD.game.player.hp=TD.game.player.max;');shot('stage7_final_hud')
  fill=Image.open(R/'expansion/topdown/art/hud27/frames/hud27_fill.png').convert('RGBA')
  uninterrupted=all(any(fill.getpixel((x,y))[3]>0 and fill.getpixel((x,y))[1]>fill.getpixel((x,y))[0] for y in range(fill.height))for x in range(1,127))
  check('generated health fill has no segment gaps',uninterrupted)
  saved=ev('localStorage.getItem(TD.CornerHUD26.storageKey)');p.reload(wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev('TDGAME.freeze();TD.pilot="yuri";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Achievements.queue=[];TDGAME.render();');check('high score persists across a page reload',ev('TD.CornerHUD26.last.highScore')==int(saved))
  check('no browser, shader or asset errors',not errors)
  result={'build':'overdrive1015-hud27-r1','passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks),'checks':checks,'errors':errors,'roomBrightnessRatios':ratios,'scope':'Native Chromium screenshots, real keyboard actions and HUD state fixtures; no physical controller testing.'};(O/'report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result));b.close()
finally:stop()
sys.exit(0 if not result['failed']and not errors else 1)
