"""Check real menu draws, alias pixels and Stage 6 Wind reward in Chromium."""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,sys,base64
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/wind_icons_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,yes,data=None):
    checks.append(dict(name=name,passed=bool(yes),data=data));print(('PASS ' if yes else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='cole',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready}')
  p.wait_for_function('()=>{const all=AP10_FX_ART.wind_icons.flatMap(a=>[a.key,forgeBadgeKey("wind",a.slot,a.level)]).concat(["ap10_wind_symbol","inf_wind","turn_inf_wind_0918"]);return all.map(k=>XART.rdy(k)).every(Boolean)}',polling=50)
  # Read every alias using the real game context, never .src or object identity.
  q=p.evaluate('''()=>{const read=k=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.clearRect(0,0,128,128);ctx.drawImage(XART.get(k),0,0);const a=Array.from(ctx.getImageData(0,0,128,128).data);ctx.restore();return a;};const same=(a,b)=>a.every((v,i)=>v===b[i]);return {icons:AP10_FX_ART.wind_icons.map(a=>({slot:a.slot,level:a.level,matching:same(read(a.key),read(forgeBadgeKey('wind',a.slot,a.level))),path:XART._src[forgeBadgeKey('wind',a.slot,a.level)]})),symbols:['inf_wind','turn_inf_wind_0918'].map(k=>({key:k,matching:same(read(k),read('ap10_wind_symbol'))})),separate:!same(read('inf_wind'),read('ap10_wind_icon_5'))};}''')
  check('All45 upgrade keys use their matching registered projectile badge and level',len(q['icons'])==45 and all(a['matching'] and '/wind_icons_1011/' in a['path'] for a in q['icons']),q['icons'])
  check('Reward and element aliases use the separate Wind symbol, distinct from the tornado-orb weapon',all(a['matching'] for a in q['symbols']) and q['separate'],q['symbols'])
  plate=Image.new('RGB',(640,1152),(8,15,24))
  for a in p.evaluate('AP10_FX_ART.wind_icons'):
   data=p.evaluate('k=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);ctx.drawImage(XART.get(k),0,0);ctx.restore();return ctx.canvas.toDataURL().split(",")[1]}',a['key'])
   from io import BytesIO
   im=Image.open(BytesIO(base64.b64decode(data))).crop((0,0,128,128)).convert('RGB')
   plate.paste(im,((a['level']-1)*128,a['slot']*128))
  plate.save(OUT/'native-badges.png')
  p.evaluate('''()=>{BOFCinematicDirector.cancel();story=null;boss=subBoss=null;bossActive=subBossActive=false;powerups=[];run.mode='campaign';run.pilot='cole';run.stage=6;run.spaceMode=false;run._earnedUnlocks={chaingun:true,laserMist:true,lightningOrb:true};run.forgeElems={wind:1};run.forgeForms={};run.forge={};run.loadout=[0,1,2,3,4,5];run.wlevels=Array(9).fill(5);for(let w=0;w<9;w++){run.forgeForms[w]={wind:{elem:'wind',lv:5}};run.forge[w]={elem:'wind',lv:5};}forgeStart();forge.t=3;drawForge(0);}''')
  p.wait_for_timeout(350);p.evaluate('()=>{forge.row=1;forge.sel=0;window.__bofFit?.();ctx.setTransform(SS,0,0,SS,0,0);drawForge(0)}');p.screenshot(path=str(OUT/'forge.png'))
  # Observe authored keys immediately before actual menu drawImage calls.
  q=p.evaluate('''()=>{const get=XART.get,draw=ctx.drawImage;let key,seen=[];try{XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...args){if(key?.startsWith('micon_forge_wind_')||key==='inf_wind')seen.push(key);return draw.call(this,im,...args)};drawForge(0);return [...new Set(seen)];}finally{XART.get=get;ctx.drawImage=draw;}}''')
  check('Actual Forge renders the new Wind projectile badges and elemental selector',any(k.startswith('micon_forge_wind_') for k in q) and 'inf_wind' in q,q)
  p.set_viewport_size(dict(width=640,height=900))
  p.evaluate('()=>{armoryOpen("forge");setState(GS.ARMORY);window.__bofFit?.();armory.tab=FORGE_WEAPONS.indexOf(3);armory.i=3;armory.scroll=0;ctx.setTransform(SS,0,0,SS,0,0);drawArmory(0)}');p.wait_for_timeout(350)
  p.evaluate(shoot.STEP,2)
  q=p.evaluate('''()=>{const get=XART.get,draw=ctx.drawImage;let key,seen=[];try{XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...args){if(key?.startsWith('micon_forge_wind_'))seen.push(key);return draw.call(this,im,...args)};drawArmory(0);return [...new Set(seen)];}finally{XART.get=get;ctx.drawImage=draw;}}''')
  p.screenshot(path=str(OUT/'armory.png'));check('Actual upgrade menu renders a Wind projectile badge',bool(q),q)
  p.set_viewport_size(dict(width=1280,height=1000));p.evaluate('window.__bofFit?.()')
  p.evaluate('()=>{state=GS.PLAY;powerups=[];run._stageElements=[];forgeBossDrop(worldWidth()/2,VH*.35);drawWorld(0)}')
  q=p.evaluate('powerups.map(q=>({kind:q.kind,elem:q.elem}))');p.screenshot(path=str(OUT/'stage6-drop.png'))
  check('The real Stage6 boss reward handler creates a Wind elemental pickup',q==[dict(kind='forgecombo',elem='wind')],q)
  q=p.evaluate('''()=>{const get=XART.get,draw=ctx.drawImage;let key,seen=[];try{XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...args){seen.push(key);return draw.call(this,im,...args)};drawPowerups();return seen;}finally{XART.get=get;ctx.drawImage=draw;}}''')
  check('The actual boss pickup draw uses the gust symbol', 'ap10_wind_symbol' in q and not any(str(k).startswith('ap10_wind_icon') for k in q),q)
  p.evaluate('()=>{run.forgeElems={};run._stageElements=[];applyPowerup(powerups[0]);powersStart();powersScr.t=2;window.__bofFit?.();ctx.setTransform(SS,0,0,SS,0,0);drawPowers(0)}');p.wait_for_timeout(350)
  q=p.evaluate('''()=>{const get=XART.get,draw=ctx.drawImage;let key,seen=[];try{XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...args){if(key==='inf_wind')seen.push(key);return draw.call(this,im,...args)};drawPowers(0);return {keys:seen,elems:powersScr.elems};}finally{XART.get=get;ctx.drawImage=draw;}}''')
  p.screenshot(path=str(OUT/'powers.png'));check('Collecting the real drop displays Wind with the gust emblem on Powers Gained',q['elems']==['wind'] and 'inf_wind' in q['keys'],q)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/wind_icons_1011/index.html');p.wait_for_function('ready===46&&total===46')
  check('The review loads all45 levels and the independent Wind symbol',p.locator('.levels img').count()==45 and p.locator('.symbol img').count()==1)
  p.screenshot(path=str(OUT/'preview.png'));p.set_viewport_size(dict(width=480,height=900));p.wait_for_timeout(80)
  check('The badge review fits a narrow viewport',p.evaluate('document.documentElement.scrollWidth<=innerWidth'));p.screenshot(path=str(OUT/'preview-mobile.png'))
  check('No page, console, renderer or missing-asset errors',not errors,errors);br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();report=dict(passed=sum(a['passed'] for a in checks),failed=sum(not a['passed'] for a in checks),checks=checks,errors=errors)
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
