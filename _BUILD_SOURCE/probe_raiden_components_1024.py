from pathlib import Path
import hashlib,json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/raiden_components_1024';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS 'if ok else'FAIL ')+name,flush=True)
STATS=r"""()=>{const c=document.querySelector('#stage'),p=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let hash=2166136261,visible=0,white=0;for(let i=0;i<p.length;i++){hash=Math.imul(hash^p[i],16777619)>>>0;if(i%4===3&&p[i]>64){visible++;if(p[i-1]>240&&p[i-2]>240&&p[i-3]>240)white++;}}return{hash,visible,white};}"""
RASTER=r"""async()=>{const read=async path=>{const im=new Image();im.src=path;await im.decode();const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d',{willReadFrequently:true});x.drawImage(im,0,0);return{im,p:x.getImageData(0,0,c.width,c.height).data};};const out={components:[],units:[]};for(const part of FOUNDRY.components){const a=await read(part.image),h=await read(part.hit),n=await read(part.native);let visible=0,mismatch=0;for(let i=3;i<a.p.length;i+=4){if(a.p[i]>64)visible++;if(a.p[i]!==h.p[i])mismatch++;}out.components.push({id:part.id,role:part.role,ok:visible>30&&mismatch===0&&a.im.naturalWidth===512&&n.im.naturalWidth===256,deckHole:part.largest_central_deck_hole});}for(const u of FOUNDRY.units){const a=await read(u.master),b=await read(u.bare);await read(u.image);let edge=0;const w=a.im.naturalWidth;for(let y=0;y<w;y++)for(let x=0;x<w;x++)if((x===0||y===0||x===w-1||y===w-1)&&a.p[(y*w+x)*4+3]>64)edge++;const mounts=u.mounts.map(m=>{const x=Math.round(m.kind==="running_gear"?u.body_position[0]+(m.base_attachment_pixel[0]-256)*u.body_scale:m.position[0]),y=Math.round(m.kind==="running_gear"?u.body_position[1]+(m.base_attachment_pixel[1]-256)*u.body_scale:m.position[1]);return{id:m.id,alpha:b.p[(y*w+x)*4+3]};});out.units.push({id:u.id,edge,mounts,ok:edge===0&&mounts.every(m=>m.alpha>128)});}return out;}"""
basepaths=['assets/game.js','_BUILD_SOURCE/test_fl.js','index.html','assets/data/ART_TAXONOMY.json'];baseline={p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in basepaths}
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport={'width':1480,'height':1050});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text)if e.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/art-packs/raiden-components-1024/index.html');p.wait_for_function('window.foundryReady')
  ras=p.evaluate(RASTER);(O/'raster.json').write_text(json.dumps(ras,indent=2)+'\n')
  check('201 complete components decode with even master/native frames and matching hit alpha',len(ras['components'])==201 and all(c['ok']for c in ras['components']))
  check('All 24 base hulls have continuous central deck/armor surfaces',sum(c['role']=='base'for c in ras['components'])==24 and all(c['deckHole']==0 for c in ras['components']if c['role']=='base'))
  check('All default assemblies fit their canvases and every mount has a painted base underneath',all(u['ok']for u in ras['units']),[u for u in ras['units']if not u['ok']])
  matched=p.evaluate('''()=>{const parts=new Map(FOUNDRY.components.map(c=>[c.id,c]));return FOUNDRY.units.map(u=>({id:u.id,ok:u.matched_set===u.id&&u.mounts.every(m=>m.compatible.includes(m.default)&&m.compatible.every(id=>m.kind==='running_gear'?parts.get(id).palette===u.gear_palette:parts.get(id).owner===u.id))}));}''')
  check('All 24 vehicles restrict every compatible option to their matched design and running-gear palette',len(matched)==24 and all(u['ok']for u in matched),[u for u in matched if not u['ok']])
  for tier,count in [('enemy',16),('miniboss',4),('boss',4),('library',201)]:
   p.click(f'nav button[data-tier={tier}]');p.wait_for_function('Array.from(document.querySelectorAll("#cards img")).every(i=>i.complete&&i.naturalWidth>0)');check(tier+' gallery count',p.locator('#cards article').count()==count);p.screenshot(path=str(O/f'gallery-{tier}.png'),full_page=True)
  p.click('nav button[data-tier=boss]');p.click('[data-id=iron_bastion_landship]>button');p.wait_for_selector('#workbench[open]')
  fitted=p.evaluate(STATS);p.click('#bare');bare=p.evaluate(STATS);p.screenshot(path=str(O/'landship-complete-base.png'))
  p.click('#swap');bare_swapped=p.evaluate(STATS);check('Swapping all weapons leaves the complete bare chassis raster unchanged',bare==bare_swapped)
  p.click('#fitted');swapped=p.evaluate(STATS);check('Interchangeable complete weapon objects produce a different fitted loadout',swapped['hash']!=fitted['hash']);p.screenshot(path=str(O/'landship-swapped.png'))
  p.locator('#aim').focus();p.keyboard.press('End');aimed=p.evaluate(STATS);check('Turrets aim independently over intact base armor',aimed['hash']!=swapped['hash']);p.screenshot(path=str(O/'landship-aimed.png'))
  p.click('#bare');check('Aiming weapons preserves the same complete base',p.evaluate(STATS)==bare);p.click('#fitted')
  p.select_option('#component','');check('A hardpoint can be left empty without removing any hull geometry',p.locator('#component').input_value()=='');p.click('#bare');check('Unoccupied hardpoints preserve the base raster',p.evaluate(STATS)==bare)
  p.click('#reset');p.wait_for_function('document.querySelector("#stage").dataset.mode==="fitted"');check('Reset restores original default fitout',p.evaluate(STATS)==fitted)
  p.click('#close')
  ground=p.evaluate('FOUNDRY.units.filter(u=>u.running_gear).map(u=>({id:u.id,tier:u.tier,mounts:u.mounts.filter(m=>m.kind==="running_gear")}))')
  check('All seven mobile ground hulls register independent running gear',len(ground)==7 and all(len(u['mounts'])==(12 if u['id']=='wheeled_flak'else 18)for u in ground))
  for u in ground:
   p.click(f'nav button[data-tier={u["tier"]}]');p.click(f'[data-id={u["id"]}]>button');p.wait_for_selector('#workbench[open]')
   original=p.evaluate(STATS);p.click('#bare');hull=p.evaluate(STATS);p.screenshot(path=str(O/f'{u["id"]}-hull-only.png'));p.click('#fitted')
   p.click('#gear');no_gear=p.evaluate(STATS);check(u['id']+' running gear removes independently with weapons retained',no_gear['hash']!=original['hash'] and no_gear['hash']!=hull['hash']);p.screenshot(path=str(O/f'{u["id"]}-no-running-gear.png'));p.click('#gear')
   if u['id']!='wheeled_flak':p.click('#belts')
   wheels=p.evaluate(STATS);p.screenshot(path=str(O/f'{u["id"]}-individual-wheels.png'))
   wm=next(m for m in u['mounts']if '/rubber_tire' in m['default']or'/road_wheel' in m['default']);p.select_option('#hardpoint',wm['id']);p.select_option('#component','');removed=p.evaluate(STATS)
   check(u['id']+' one wheel removes independently',removed['hash']!=wheels['hash']);p.screenshot(path=str(O/f'{u["id"]}-one-wheel-removed.png'))
   p.select_option('#component',wm['default']);check(u['id']+' replacing the wheel restores its pixels',p.evaluate(STATS)==wheels)
   p.click('#flash');flash=p.evaluate(STATS);p.wait_for_timeout(220);recovered=p.evaluate(STATS)
   check(u['id']+' wheel flashes visibly and recovers',flash['white']>recovered['white'] and recovered==wheels)
   p.click('#bare');check(u['id']+' hull is unchanged after removing running gear',p.evaluate(STATS)==hull);p.click('#close')
  for tier,key in [('enemy','steel_interceptor'),('miniboss','missile_corvette'),('boss','quad_laser_citadel')]:
   p.click(f'nav button[data-tier={tier}]');p.click(f'[data-id={key}]>button');p.wait_for_selector('#workbench[open]');p.screenshot(path=str(O/f'{key}-fitted.png'));p.click('#bare');p.screenshot(path=str(O/f'{key}-bare.png'));p.click('#close')
  for u in p.evaluate('FOUNDRY.units.map(u=>({id:u.id,tier:u.tier}))'):
   p.click(f'nav button[data-tier={u["tier"]}]');p.click(f'[data-id={u["id"]}]>button');p.wait_for_selector('#workbench[open]');p.locator('#stage').screenshot(path=str(O/f'matched-{u["id"]}.png'))
   before=p.evaluate(STATS);p.click('#swap');after=p.evaluate(STATS);check(u['id']+' matched alternate loadout renders',before['hash']!=after['hash']);p.locator('#stage').screenshot(path=str(O/f'matched-{u["id"]}-alternate.png'));p.click('#close')
  p.set_viewport_size({'width':390,'height':844});p.click('nav button[data-tier=boss]');p.screenshot(path=str(O/'mobile-gallery.png'),full_page=True);check('Mobile gallery has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  p.click('[data-id=stormwing_sky_carrier]>button');p.wait_for_selector('#workbench[open]');p.screenshot(path=str(O/'mobile-builder.png'),full_page=True);check('Mobile component builder fits viewport',p.evaluate('document.querySelector("#workbench").getBoundingClientRect().width<=innerWidth'))
  browser.close()
finally:stop()
check('Shipping game files retain starting hashes',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in baseline.items()));check('No browser page or console errors',not errors,errors)
report=dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks),checks=checks);(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('FINAL SUMMARY',report['passed'],report['failed']);raise SystemExit(bool(report['failed']))
