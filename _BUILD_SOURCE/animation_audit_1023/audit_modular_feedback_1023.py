from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,io
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);O=W/'modular-native';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
results=[];errors=[];port,stop=shoot.serve(str(R))
def img(s):return Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB')
def add(meta,before,after):
 a=np.array(img(before)).astype(int);b=np.array(img(after)).astype(int);meta['brightPixels']=int(((a.max(2)>12)&(b.mean(2)-a.mean(2)>20)).sum());meta['visible']=meta['brightPixels']>6;results.append(meta);print(json.dumps(meta),flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'));p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  p.evaluate('''()=>{window.MD23draw=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);ctx.save();ctx.translate(-camX,0);drawSubBoss();ctx.restore();return cv.toDataURL().split(',')[1];};}''')
  for diff in ['normal','hard','furious','easy']:
   p.evaluate('d=>BAL7.setup({stage:1,kind:"razorback",mini:true,diff:d,fire:false})',diff);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1);}');p.wait_for_timeout(300)
   count=p.evaluate('()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;const list=B._rzbPair?.actors||[B];list.forEach((b,i)=>{b.x=worldWidth()/2+(list.length>1?(i?100:-100):0);b.y=180;b._rzb.state="guns";b._rzb.trans=0;b._rzb.a=0;b._rzb.pools={...b._rzb.max};b.enter=false;b._noHit=false;});camX=worldWidth()/2-viewW()/2;return list.length;}')
   for actor in range(count):
    for part in ['left','right','turret','hull']:
     p.evaluate('''([i,part])=>{window.MD23b=(B._rzbPair?.actors||[B])[i];const R=MD23b._rzb;R.flash={};R.state=['left','right'].includes(part)?'guns':part;R.trans=0;R.pools={...R.max};}''',[actor,part]);before=p.evaluate('MD23draw()');meta=p.evaluate('''part=>{const b=MD23b,R=b._rzb,pos=['left','right'].includes(part)?rzbWorld(b,part==='left'?-57:57,96):{x:b.x,y:b.y},hp=R.pools[part];const delta=razorbackHit(b,.1,pos.x,pos.y);return{poolBefore:hp,poolAfter:R.pools[part],delta,timer:R.flash[part]};}''',part);after=p.evaluate('MD23draw()');add({'owner':'razorback','difficulty':diff,'actor':actor,'part':part,**meta},before,after)
   p.evaluate('d=>BAL7.setup({stage:6,kind:"siegefortress17",mini:true,diff:d,fire:false})',diff);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&SC13.keys.map(k=>XART.rdy(k)).every(Boolean);}');p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;const C=B._cargo13;C.mode='fight';C.ready=true;C.x=worldWidth()/2;C.y=140;B.enter=B._noHit=false;sc13Sync(B);camX=worldWidth()/2-viewW()/2;}''')
   for part in list(range(6))+['core']:
    p.evaluate('''part=>{const C=B._cargo13;C.coreFl=0;for(const g of C.guns)g.fl=g.flash=0;if(part==='core'){for(const g of C.guns)g.dead=true;s6r18Opening(B,1);}}''',part);before=p.evaluate('MD23draw()');meta=p.evaluate('''part=>{const C=B._cargo13,pos=part==='core'?sc13Core(B):sc13Mount(B,part),hp=part==='core'?C.core:C.guns[part].hp;hitSubBoss(.1,pos.x,pos.y);return{poolBefore:hp,poolAfter:part==='core'?C.core:C.guns[part].hp,timer:part==='core'?C.coreFl:C.guns[part].fl};}''',part);after=p.evaluate('MD23draw()');add({'owner':'siegefortress17','difficulty':diff,'part':part,**meta},before,after)
  # Terrain-anchored barrel: move the inspection map anchor, not just e.y.
  catalog=json.loads((W/'roster/catalog.json').read_text());p.evaluate('()=>EA11.setup(4,"normal")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4);}')
  spec=next(s for r in catalog['stages']if r['stage']==4 for s in r['specs']if s['type']=='s4barrel');p.evaluate('s=>{AQ23.begin(s);bossWarned=false;AQ23.step(60);E._fb9Anchor.mapY=220+levelSrcY();E._fb9Anchor.x=worldWidth()/2;}',spec);p.wait_for_timeout(200);before=p.evaluate('AQ23.draw(E).image');m=p.evaluate('()=>AQ23.hit(E)');add({'owner':'barrel-map-anchor','poolBefore':m['hpBefore'],'poolAfter':m['hpAfter'],'timer':m['timer']},before,m['native']['image'])
  # Frost veteran: the entry immunity is intentional, then each real socket is vulnerable.
  p.evaluate('()=>EA11.setup(8,"normal")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8);}')
  spec=next(s for r in catalog['stages']if r['stage']==8 for s in r['specs']if s['type']=='pt11frostcarrier');p.evaluate('s=>{AQ23.begin(s);bossWarned=false;E.enter=E._noHit=false;E.x=worldWidth()/2;E.y=E._drawY=180;camX=E.x-viewW()/2;}',spec);p.wait_for_timeout(200);parts=p.evaluate('E._mr27.parts.map(p=>p.id)')
  for part in parts:
   p.evaluate('()=>{E.flash=0;for(const q of E._mr27.parts)q.flash=0;}');before=p.evaluate('AQ23.draw(E).image');m=p.evaluate('''part=>{const q=mr27Part(E,part),pos=mr27Shape(E,part),hp=q.hp,old=_dmgBullet;_dmgBullet={kind:'mg',lv:1,x:pos.x,y:pos.y};hitEnemy(E,.1);_dmgBullet=old;return{poolBefore:hp,poolAfter:q.hp,timer:q.flash,image:AQ23.draw(E).image};}''',part);add({'owner':'frost-veteran','part':part,**{k:v for k,v in m.items()if k!='image'}},before,m['image'])
  br.close()
finally:stop();(O/'report.json').write_text(json.dumps({'cases':results,'errors':errors},indent=2))
