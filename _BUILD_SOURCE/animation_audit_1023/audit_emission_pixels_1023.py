from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,base64,io,numpy as np,argparse
ap=argparse.ArgumentParser();ap.add_argument('--output',default='emissions');args=ap.parse_args()
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);O=W/args.output;O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
catalog=json.loads((W/'roster/catalog.json').read_text());report={'families':[],'actors':[],'errors':[]};port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  p.evaluate('''()=>{window.PQ23={samples:new Map(),seen:new Set(),muzzles:[],muzzleBase:wm26Emit};wm26Emit=function(owner,x,y,angle,family,color,opt){if(owner===E)PQ23.muzzles.push({x,y,angle,family,time:efxClock});return PQ23.muzzleBase.apply(this,arguments);};PQ23.collect=()=>{for(const b of eBullets)if(!b.dead){const flags=Object.entries(b).filter(([k,v])=>(k.startsWith('_')||['kind','w','h','element','homing'].includes(k))&&['string','number','boolean'].includes(typeof v)&&!['t','life','_age','_ttl','_steer','_homing'].includes(k)),id=run.stage+'|'+b.kind+'|'+JSON.stringify(flags.filter(([k,v])=>typeof v!=='number'||['w','h','_frRealm','_bf22ShotRow','_sp22Shot'].includes(k)));if(!PQ23.samples.has(id))PQ23.samples.set(id,{id,stage:run.stage,kind:b.kind,flags,original:{x:b.x,y:b.y,vx:b.vx,vy:b.vy},actor:E.type,bullet:{...b,dead:false}});}};PQ23.draw=s=>{const b=s.bullet,save=eBullets,saveP=pBullets,x=b.x,y=b.y;eBullets=[b];pBullets=[];b.x=worldWidth()/2;b.y=220;ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);ctx.save();ctx.translate(-camX,0);drawBullets();ctx.restore();b.x=x;b.y=y;eBullets=save;pBullets=saveP;return cv.toDataURL().split(',')[1];};}''')
  for st in catalog['stages']:
   p.evaluate('s=>EA11.setup(s,"normal")',st['stage']);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage);}');p.wait_for_timeout(500)
   for i,spec in enumerate(st['specs']):
    p.evaluate('s=>{AQ23.begin(s);bossWarned=false;PQ23.muzzles=[];}',spec)
    for batch in range(24):
     p.evaluate('()=>{AQ23.step(30);PQ23.collect();}')
     if p.evaluate('()=>E.dead||E._dyingT!=null'):break
    row=p.evaluate('()=>({actor:E.type,shots:Object.fromEntries(AQ23.shotKinds),muzzles:PQ23.muzzles,alive:!E.dead,controller:E._ll18?.phase,keys:[...new Set(AQ23.samples.flatMap(s=>s.keys))]})');row['stage']=st['stage'];row['index']=i;report['actors'].append(row)
   ids=p.evaluate('s=>[...PQ23.samples.values()].filter(q=>q.stage===s).map(q=>q.id)',st['stage'])
   for ident in ids:
    data=p.evaluate('id=>{const s=PQ23.samples.get(id);return{...s,bullet:undefined,image:PQ23.draw(s)}}',ident);im=Image.open(io.BytesIO(base64.b64decode(data.pop('image')))).convert('RGB');pixels=int((np.array(im).max(2)>12).sum());data['pixels']=pixels
    if pixels<2:
     p.wait_for_timeout(350);im=Image.open(io.BytesIO(base64.b64decode(p.evaluate('id=>PQ23.draw(PQ23.samples.get(id))',ident)))).convert('RGB');pixels=int((np.array(im).max(2)>12).sum());data['pixelsAfterDecode']=pixels
    data['file']=f's{st["stage"]}-{len(report["families"]):03}-{data["kind"]}.webp';im.save(O/data['file'],lossless=True);report['families'].append(data)
   (O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'stage':st['stage'],'actors':len(report['actors']),'projectileVariants':len(report['families']),'invisible':[r['kind']for r in report['families']if r.get('pixelsAfterDecode',r['pixels'])<2]}),flush=True)
  br.close()
finally:stop();(O/'report.json').write_text(json.dumps(report,indent=2))
