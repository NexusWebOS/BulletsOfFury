"""Chromium raster/interaction QA for all 24 modular units and the weapon pack."""
from pathlib import Path
import hashlib
import json
from playwright.sync_api import sync_playwright
import shoot

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/raiden_modular_1024'
OUT.mkdir(parents=True,exist_ok=True)
errors=[];checks=[]


def check(name,ok,detail=None):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)


RASTER=r"""async()=>{
 const load=async path=>{const im=new Image();im.src=path;await im.decode();return im;};
 const pixels=im=>{const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d',{willReadFrequently:true});x.imageSmoothingEnabled=false;x.drawImage(im,0,0);return x.getImageData(0,0,c.width,c.height).data;};
 const result={units:[],effects:[],sheets:[],files:0};
 for(const asset of ART_PACK.assets){
  if(!asset.modular){
   for(const res of ['master','native']){
    const im=await load(asset[res]),p=pixels(im);let visible=0,clear=0,edge=0;
    for(let i=0;i<p.length;i+=4){if(p[i+3]>64){visible++;const x=(i/4)%im.naturalWidth,y=Math.floor(i/4/im.naturalWidth);if(x===0||y===0||x===im.naturalWidth-1||y===im.naturalHeight-1)edge++;}if(p[i+3]===0)clear++;}
    result.effects.push({id:asset.id,res,ok:visible>20&&clear>20&&edge===0&&im.naturalWidth%2===0&&im.naturalHeight%2===0});result.files++;
   }continue;
  }
  const unit={id:asset.id,modules:asset.parts.length,reconstructions:[],parts:[],ok:true};
  for(const res of ['master','native']){
   const whole=await load(asset[res]);result.files++;const ref=pixels(whole);
   const c=document.createElement('canvas');c.width=whole.naturalWidth;c.height=whole.naturalHeight;
   const ctx=c.getContext('2d',{willReadFrequently:true});ctx.imageSmoothingEnabled=false;
   const ownerCount=new Uint8Array(c.width*c.height);
   for(const part of asset.parts){
    const [im,hit]=await Promise.all([load(part[res]),load(part['hit_'+res])]);result.files+=2;
    const p=pixels(im),h=pixels(hit);ctx.drawImage(im,0,0);let count=0,alphaMismatch=0,whiteMismatch=0;
    for(let i=0;i<p.length;i+=4){if(p[i+3]>0){ownerCount[i/4]++;if(p[i+3]>16)count++;}if(p[i+3]!==h[i+3])alphaMismatch++;if(h[i+3]>192&&(h[i]<250||h[i+1]<250||h[i+2]<250))whiteMismatch++;}
    const ok=count>5&&alphaMismatch===0&&whiteMismatch===0&&im.naturalWidth===whole.naturalWidth&&im.naturalHeight===whole.naturalHeight&&im.naturalWidth%2===0&&im.naturalHeight%2===0;
    unit.parts.push({id:part.id,res,count,alphaMismatch,whiteMismatch,ok});unit.ok&&=ok;
   }
   const actual=ctx.getImageData(0,0,c.width,c.height).data;let differences=0,overlap=0;
   for(let i=0;i<actual.length;i++)if(actual[i]!==ref[i])differences++;
   for(const count of ownerCount)if(count>1)overlap++;
   unit.reconstructions.push({res,differences,overlap,ok:differences===0&&overlap===0});unit.ok&&=differences===0&&overlap===0;
  }
  for(const sheet of asset.module_sheets){const im=await load(sheet.path);result.files++;result.sheets.push({path:sheet.path,ok:im.naturalWidth===sheet.size[0]&&im.naturalHeight===sheet.size[1]});}
  result.units.push(unit);
 }
 for(const sheet of ART_PACK.sheets){const im=await load(sheet.path);result.files++;result.sheets.push({path:sheet.path,ok:im.naturalWidth===sheet.size[0]&&im.naturalHeight===sheet.size[1]});}
 return result;
}"""

CANVAS_STATS=r"""()=>{const c=document.querySelector('#detail-canvas'),p=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let hash=2166136261,opaque=0,white=0;for(let i=0;i<p.length;i++){hash=Math.imul(hash^p[i],16777619)>>>0;if(i%4===3&&p[i]>64){opaque++;if(p[i-1]>240&&p[i-2]>240&&p[i-3]>240)white++;}}return{hash,opaque,white};}"""

CONTACT=r"""async(group)=>{
 const units=ART_PACK.assets.filter(a=>a.group===group),cols=4,cell=400,rows=Math.ceil(units.length/cols);
 const canvas=document.createElement('canvas');canvas.id='qa-contact';canvas.width=cols*cell;canvas.height=rows*(cell+32);
 const ctx=canvas.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.fillStyle='#191d21';ctx.fillRect(0,0,canvas.width,canvas.height);
 for(let i=0;i<units.length;i++){
  const a=units[i],col=i%cols,row=Math.floor(i/cols),scale=360/(a.master_size[0]*1.5),offsetX=col*cell+20+a.master_size[0]*.25*scale,offsetY=row*(cell+32)+38+a.master_size[0]*.25*scale;
  ctx.font='13px monospace';ctx.fillStyle='#f6ba4c';ctx.fillText(a.name,col*cell+15,row*(cell+32)+20);ctx.fillStyle='#aaa';ctx.font='10px monospace';ctx.fillText(a.parts.length+' MODULES',col*cell+15,row*(cell+32)+36);
  for(const p of a.parts){const im=new Image();im.src=p.master;await im.decode();ctx.drawImage(im,Math.round(offsetX+p.explode[0]*.8*scale),Math.round(offsetY+p.explode[1]*.8*scale),a.master_size[0]*scale,a.master_size[1]*scale);}
 }
 canvas.style.cssText='display:block;width:1600px;height:auto';document.body.replaceChildren(canvas);document.body.style.margin='0';document.documentElement.style.background='#191d21';
 return {width:canvas.width,height:canvas.height};
}"""

port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio'])
  page=browser.new_page(viewport={'width':1480,'height':1080},device_scale_factor=1);page.set_default_timeout(180000)
  page.on('pageerror',lambda e:errors.append('page: '+str(e)))
  page.on('console',lambda e:errors.append('console: '+e.text) if e.type=='error' else None)
  page.on('requestfailed',lambda r:errors.append('request: '+r.url+' '+str(r.failure)))
  url=f'http://127.0.0.1:{port}/art-packs/raiden-reference-1024/index.html'
  page.goto(url);page.wait_for_function('window.artPackReady')
  data=page.evaluate(RASTER);(OUT/'raster-report.json').write_text(json.dumps(data,indent=2)+'\n')
  check('All 24 enemies/minibosses/bosses use at least three real independent modules',len(data['units'])==24 and all(u['modules']>=3 for u in data['units']))
  check('All 170 modules decode with matching alpha, even canvases and actual white hit pixels',all(p['ok'] for u in data['units'] for p in u['parts']),[p for u in data['units'] for p in u['parts'] if not p['ok']])
  check('Master and native assemblies reconstruct exactly in real Chromium with zero overlapping part pixels',all(u['ok'] for u in data['units']),[u for u in data['units'] if not u['ok']])
  check('All 36 weapon effects retain decoded transparent exports',len(data['effects'])==72 and all(r['ok'] for r in data['effects']))
  check('All 58 category and per-unit module sheets decode at registered dimensions',len(data['sheets'])==58 and all(r['ok'] for r in data['sheets']))
  for group,count in [('projectiles',24),('lasers',12),('enemies',16),('minibosses',4),('bosses',4)]:
   page.click(f'.tabs button[data-group={group}]');page.wait_for_function('Array.from(document.querySelectorAll("#grid img")).every(im=>im.complete&&im.naturalWidth>0)')
   check(f'Gallery {group}: all {count} designs visible',page.locator('#grid .card').count()==count)
   page.screenshot(path=str(OUT/f'gallery-{group}.png'),full_page=True)
  page.click('[data-id=iron_bastion_landship] .sprite-button');page.wait_for_selector('#detail[open]')
  check('Landship opens all 14 module controls',page.locator('#module-list .part-row').count()==14)
  page.select_option('#module-select','upper_left_barrel');before=page.evaluate(CANVAS_STATS)
  page.click('#flash-part');page.wait_for_timeout(35);during=page.evaluate(CANVAS_STATS)
  page.screenshot(path=str(OUT/'landship-hit.png'))
  page.wait_for_timeout(190);after=page.evaluate(CANVAS_STATS)
  check('Selected real module flashes white and its exact original pixels return after expiry',during['white']>before['white'] and during['hash']!=before['hash'] and before==after,dict(before=before,during=during,after=after))
  page.click('#toggle-part');hidden=page.evaluate(CANVAS_STATS)
  check('Hiding one gun removes its actual pixels',hidden['opaque']<before['opaque'] and hidden['hash']!=before['hash'])
  page.click('#toggle-part');check('Restoring a module returns the exact assembly',page.evaluate(CANVAS_STATS)==before)
  page.locator('#explode').focus();page.keyboard.press('End');exploded=page.evaluate(CANVAS_STATS)
  check('Explode control moves the actual independent module pixels',exploded['hash']!=before['hash'])
  page.screenshot(path=str(OUT/'landship-exploded.png'))
  page.check('#mounts');page.screenshot(path=str(OUT/'landship-mounts.png'));page.uncheck('#mounts')
  page.click('#reset-parts');check('Reset restores complete registered assembly',page.evaluate(CANVAS_STATS)==before)
  page.click('#close')
  for ground in ['jungle','sand','sea','check','dark']:
   page.select_option('#background',ground);check('Background '+ground,page.locator('#grid').get_attribute('data-ground')==ground)
  for group,unit in [('enemies','ember_gunship'),('minibosses','quad_battery_fortress'),('bosses','stormwing_sky_carrier')]:
   page.click(f'.tabs button[data-group={group}]');page.click(f'[data-id={unit}] .sprite-button');page.wait_for_selector('#detail[open]');page.locator('#explode').focus();page.keyboard.press('End');page.screenshot(path=str(OUT/f'{unit}-exploded.png'));page.click('#close')
  page.set_viewport_size({'width':390,'height':844});page.click('.tabs button[data-group=bosses]');page.screenshot(path=str(OUT/'gallery-mobile.png'),full_page=True)
  check('Mobile gallery has no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  page.click('[data-id=quad_laser_citadel] .sprite-button');page.wait_for_selector('#detail[open]');page.screenshot(path=str(OUT/'mobile-inspector.png'),full_page=True)
  check('Mobile module inspector stays within viewport width',page.evaluate('document.querySelector("#detail").getBoundingClientRect().width<=innerWidth'))
  page.click('#close')
  page.set_viewport_size({'width':1600,'height':1000})
  for group in ['enemies','minibosses','bosses']:
   page.goto(url);page.wait_for_function('window.artPackReady');size=page.evaluate(CONTACT,group);page.screenshot(path=str(OUT/f'{group}-all-modules.png'),full_page=True)
  browser.close()
finally:stop()
baseline=json.loads((OUT/'game-baseline.json').read_text())
check('Shipping game files retain their starting hashes',all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in baseline.items()))
check('No page, console or request errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),png_files_drawn=data['files'],checks=checks)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(f"FINAL SUMMARY: {report['passed']} passed / {report['failed']} failed; {data['files']} PNGs decoded/drawn",flush=True)
raise SystemExit(bool(report['failed']))
