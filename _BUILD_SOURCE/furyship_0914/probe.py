"""Render every candidate with the real game's XART and canvas in Chromium.

This is an asset review, not a claim that the replacement is installed in gameplay.
"""
from pathlib import Path
import base64, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/furyship_0914'
pack=json.loads((ROOT/'assets/game/furyship_0914/pack.json').read_text())
port, shutdown=shoot.serve(str(ROOT))
errors=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(args=['--no-sandbox','--mute-audio'])
  page=browser.new_page(viewport={'width':1100,'height':1200})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000)
  page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
  page.evaluate(shoot.TRAP_RAF)
  page.evaluate('''pack=>{
   for(const [k,v] of Object.entries(pack.frames))XART._src['qa_fury_'+k]='assets/game/furyship_0914/'+v.path;
   XART._src.qa_fury_reference=pack.reference;
   window.__furyKeys=Object.keys(pack.frames);
   for(const k of __furyKeys)XART._touch('qa_fury_'+k);
   XART._touch('qa_fury_reference');
  }''',pack)
  page.wait_for_function('()=>__furyKeys.every(k=>XART.rdy("qa_fury_"+k))&&XART.rdy("qa_fury_reference")',timeout=120000)
  page.add_script_tag(path=str(ROOT/'assets/game/furyship_0914/catalog.js'))
  page.add_script_tag(path=str(ROOT/'assets/game/furyship_0914/palette.js'))
  page.evaluate('''()=>{
   window.__maskPaths=Object.values(FURYSHIP_CANDIDATES.frames).map(f=>f.paletteMask).filter(Boolean);
   for(const path of __maskPaths){const key='qa_fury_'+path.replace('.png','');XART._src[key]='assets/game/furyship_0914/'+path;XART._touch(key);}
   window.__furyResolve=path=>{const key='qa_fury_'+path.replace('.png','');return XART.rdy(key)?XART.get(key):null;};
  }''')
  page.wait_for_function('()=>__maskPaths.every(p=>!!__furyResolve(p))',timeout=120000)
  page.evaluate('''()=>{
   window.__furyBlits=[];
   window.__furyDraw=(k,x,y,w,h)=>{const im=XART.get('qa_fury_'+k);ctx.drawImage(im,x,y,w,h);__furyBlits.push(k);};
   window.__furyClear=title=>{ctx.setTransform(2,0,0,2,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#171c25';ctx.fillRect(0,0,480,512);ctx.fillStyle='#b9e7eb';ctx.textAlign='center';ctx.font='12px monospace';ctx.fillText(title,240,24);};
  }''')
  def screenshot(name):
   (OUT/(name+'.png')).write_bytes(base64.b64decode(page.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
  page.evaluate('''()=>{
   __furyClear('FURYSHIP COMPONENT CANDIDATES');
   const pieces=['nose','hull','wing_left','wing_right','engine_left','engine_right'],views=['top','front','left','back','right'];
   ctx.font='9px monospace';views.forEach((v,c)=>ctx.fillText(v,48+c*96,44));
   pieces.forEach((k,r)=>{views.forEach((v,c)=>__furyDraw(k+'_'+v,c*96,r*73+42,96,96));ctx.fillText(k,240,r*73+117);});
  }''')
  screenshot('native_components')
  for family in ['assembly','veil','speed','thrusters','roll','somersault']:
   page.evaluate('''f=>{
    __furyClear('FURYSHIP '+f.toUpperCase()+' CANDIDATE');
    const count=f==='somersault'?12:8;for(let i=0;i<count;i++){
     const x=(i%4)*120,y=Math.floor(i/4)*(count===12?140:200)+42;
     __furyDraw(f+'_'+String(i).padStart(2,'0'),x,y,120,f==='veil'||f==='speed'?160:120);
     ctx.font='10px monospace';ctx.fillText(String(i),x+60,y+(count===12?132:175));
    }
   }''',family)
   screenshot('native_'+family)
  page.evaluate('''()=>{
   __furyClear('SOURCE / GENERATED ROLL: FIT REVIEW');
   __furyDraw('reference',48,130,128,128);__furyDraw('roll_00',304,130,128,128);
   ctx.font='12px monospace';ctx.fillText('Approved frame 13',112,295);ctx.fillText('Generated candidate',368,295);
  }''')
  screenshot('native_reference_comparison')
  palette_checks=page.evaluate('''()=>{
   let checked=0,protectedErrors=0;
   for(const [pilot,pal] of Object.entries(FURYSHIP_CANDIDATES.palettes)){
    if(pal.color!==GRAVITY_PILOT_PAL[pilot]||pal.lum!==GRAVITY_PILOT_LUM[pilot]||pal.model!==SPACE_FIGHTER_MODELS[pilot])throw Error('Palette contract drift: '+pilot);
    for(const [key,f] of Object.entries(FURYSHIP_CANDIDATES.frames)){
     if(!f.paletteMask)continue;
     const src=__furyResolve(f.path),mask=__furyResolve(f.paletteMask),tinted=furyCandidatePalette(key,pilot,__furyResolve);
     if(!tinted)throw Error('Missing palette '+key+' '+pilot);
     const c=document.createElement('canvas');c.width=f.size[0];c.height=f.size[1];const g=c.getContext('2d');
     g.drawImage(src,0,0);const a=g.getImageData(0,0,c.width,c.height).data;
     g.clearRect(0,0,c.width,c.height);g.drawImage(mask,0,0);const m=g.getImageData(0,0,c.width,c.height).data;
     g.clearRect(0,0,c.width,c.height);g.drawImage(tinted,0,0);const b=g.getImageData(0,0,c.width,c.height).data;
     for(let n=0;n<a.length;n+=4)if(m[n+3]===0){for(let j=0;j<4;j++)if(a[n+j]!==b[n+j])protectedErrors++;}
     ctx.drawImage(tinted,0,0);checked++;
    }
   }
   __furyClear('NINE PILOT PALETTES / SOMERSAULT');
   Object.entries(FURYSHIP_CANDIDATES.palettes).forEach(([pilot,pal],i)=>{
    const x=(i%3)*160+16,y=Math.floor(i/3)*150+35;
    ctx.drawImage(furyCandidatePalette('somersault_00',pilot,__furyResolve),x,y,128,128);
    ctx.font='10px monospace';ctx.fillStyle=pal.color;ctx.fillText(pal.model,x+64,y+140);
   });
   return {checked,protectedErrors,masks:__maskPaths.length};
  }''')
  screenshot('native_nine_palettes')
  details=page.evaluate('()=>({count:new Set(__furyBlits).size,keys:[...new Set(__furyBlits)],loopError:window.__err||null})')
  browser.close()
finally:shutdown()
assert details['count']==len(pack['frames'])+1,details
assert not errors and not details['loopError'],errors
assert palette_checks['checked']==450 and palette_checks['protectedErrors']==0,palette_checks
report={'scope':'Candidate asset rendering only; no gameplay integration or behavior verification','renderedAssets':details['count'],'palettes':palette_checks,'pageAndConsoleErrors':errors,'loopError':details['loopError'],'runtimeSha256':hashlib.sha256((ROOT/'assets/game.js').read_bytes()).hexdigest(),'screenshots':[p.name for p in OUT.glob('native_*.png')]}
(OUT/'native_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(str(details['count'])+' XART assets rendered through the game canvas; zero page/console/loop errors.')
