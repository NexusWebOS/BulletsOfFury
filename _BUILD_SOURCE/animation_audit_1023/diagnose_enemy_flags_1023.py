from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,io,base64,numpy as np
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);O=W/'flag-review';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
source=json.loads((W/'enemy-native/report.json').read_text());cases=[c for c in source['cases']if c['difficulty']=='normal'and c['issues']];results=[];errors=[];port,stop=shoot.serve(str(R))
def img(s):return Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB')
def stats(a,b):
 a=np.array(a).astype(int);b=np.array(b).astype(int);return{'pixels':int((a.max(2)>12).sum()),'bright':int(((a.max(2)>12)&(b.mean(2)-a.mean(2)>20)).sum())}
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'));last=None
  for c in cases:
   if last!=c['stage']:last=c['stage'];p.evaluate('s=>EA11.setup(s,"normal")',last);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage);}')
   p.evaluate('s=>{AQ23.begin(s);bossWarned=false;}',c['spec']);p.evaluate('()=>AQ23.step(120)');p.evaluate('''()=>{E.x=worldWidth()/2;E.y=220;camX=E.x-viewW()/2;E.flash=0;E._noHit=false;if(E._armor17){E._armor17.hullFlash=0;for(const q of E._armor17.parts)q.flash=0;}for(const q of Object.values(E._r30||{}))if(q&&typeof q==='object')q.flash=0;}''');p.wait_for_timeout(300);normal=img(p.evaluate('()=>AQ23.draw(E).image'));hit=p.evaluate('()=>AQ23.hit(E)');native=img(hit['native']['image']);p.wait_for_timeout(200);decoded=img(p.evaluate('()=>AQ23.draw(E).image'));m=stats(normal,native);meta=p.evaluate('''()=>({keys:AQ23.draw(E).keys,geometry:AQ23.invalid.slice(0,3),dead:E.dead,dying:E._dyingT,model:bf22Model(E)?.id,render:E._bf22Rendered,legion:E._ll18?{role:E._ll18.role,phase:E._ll18.phase,age:E._ll18.age}:null,armor:E._armor17?true:false,parts:E._modTurret||null})''');row={'id':c['id'],'stage':last,'type':c['spec']['type'],'index':c['index'],'nativeHP':[hit['hpBefore'],hit['hpAfter']],'flashTimer':hit['timer'],'noHit':hit['noHit'],'native':m,'marked':stats(normal,decoded),'meta':meta};results.append(row)
   if m['bright']<6 or meta['geometry']:
    ctc=Image.new('RGB',(normal.width*3,normal.height));ctc.paste(normal,(0,0));ctc.paste(native,(normal.width,0));ctc.paste(decoded,(normal.width*2,0));ctc.save(O/(c['id']+'.png'))
   (O/'report.json').write_text(json.dumps({'cases':results,'errors':errors},indent=2));print(json.dumps({k:row[k]for k in ['id','native','nativeHP']}|{'geometry':len(meta['geometry'])}),flush=True)
  br.close()
finally:stop();(O/'report.json').write_text(json.dumps({'cases':results,'errors':errors},indent=2))
