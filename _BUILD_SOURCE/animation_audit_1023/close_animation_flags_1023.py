from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,base64,io,numpy as np
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
D=json.loads((W/'roster/catalog.json').read_text());out=[];errors=[];port,stop=shoot.serve(str(R))
def image(s):return np.array(Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB')).astype(int)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  for diff in ['easy','normal','hard','furious']:
   for stage,typ,idx in [(4,'s4barrel',6),(4,'s4barrel',7),(7,'s7pipe',3),(6,'s1jetbomber_b',26),(6,'s1jetbomber_b',46)]:
    p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff]);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage);}')
    specs=next(s['specs']for s in D['stages']if s['stage']==stage);spec=specs[idx];assert spec['type']==typ;p.evaluate('s=>{AQ23.begin(s);bossWarned=false;E.hp=E.maxhp=10000;}',spec)
    for i in range(1 if stage==6 else 12):p.evaluate('()=>AQ23.step(12)'if stage==6 else'()=>AQ23.step(30)')
    p.evaluate('''()=>{E.x=worldWidth()/2;E.y=220;camX=E.x-viewW()/2;if(E._fb9Anchor){E._fb9Anchor.x=E.x;E._fb9Anchor.mapY=E.y+levelSrcY();}E.flash=0;}''');p.wait_for_timeout(150);before=image(p.evaluate('AQ23.draw(E).image'));native=p.evaluate('AQ23.hit(E)');after=image(native['native']['image']);bright=int(((before.max(2)>12)&(after.mean(2)-before.mean(2)>20)).sum());row={'difficulty':diff,'stage':stage,'type':typ,'index':idx,'diagnosticHealthOverride':10000,'anchoredMapPlacement':typ=='s4barrel','brightPixels':bright,'hpBefore':native['hpBefore'],'hpAfter':native['hpAfter'],'passed':bright>6,'nativeGeometryErrors':p.evaluate('AQ23.invalid.length')};out.append(row);print(json.dumps(row),flush=True)
  br.close()
finally:stop();(W/'flag-closure.json').write_text(json.dumps({'cases':out,'errors':errors},indent=2))
