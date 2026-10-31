from pathlib import Path
import sys,json,http.server
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_terminal_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
source=(Path(__file__).parent/'probe_dracodia_terminal_1030.py').read_text() if Path(__file__).parent.name=='_BUILD_SOURCE' else (W/'probe.py').read_text();SETUP=source.split('SETUP="""',1)[1].split('"""',1)[0];checks=[];errors=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for pilot in ['maverick','yuri','lizzie']:
   p.evaluate('pk=>{run.pilot=pk;}',pilot);p.evaluate(SETUP);p.evaluate(STEP,1580);ck(pilot+' returns in their exact authored aircraft with the other eight pilots present',p.evaluate('Q.squad.length===8&&!Q.squad.includes(run.pilot)&&RD84.draws["ship_south_"+run.pilot]>0'))
  ck('Reunion shows the actual existing blue mechanical gate lifecycle',p.evaluate('RD84.draws.gate_loop>0&&RD84_ART.sources["assets/game/shared/fx/portal_lifecycle_1011/blue_rift_loop_15.png"]!==undefined'))
  p.evaluate(STEP,15);a=p.evaluate('({...RD84.parallax})');p.evaluate(STEP,18);b=p.evaluate('({...RD84.parallax})');ck('River water cycles independently of the fixed foreground quay',a['waterFrame']!=b['waterFrame']and a['nearX']==b['nearX']==0)
  ck('Far river/bridge and near apron have separate world parallax positions',p.evaluate('RD84.parallax.farX===Math.round(camLeftX()*.08)&&RD84.parallax.nearX===0'))
  p.evaluate('beginStage(8);setState(GS.PLAY)');p.evaluate(SETUP);p.evaluate('RD84.reducedMotion=true');p.evaluate(STEP,160);ck('Reduced-motion mode retains timing with softer full-field and body flashes',p.evaluate('Q.flash<=1&&Q.white<=2&&Q.beat>=0&&B._r30.mode==="dr5Death"'));p.evaluate('RD84.reducedMotion=false')
  p.evaluate('beginStage(1)');p.evaluate(STEP,5);ck('Scene reset removes the terminal owner, flashes and scene substitution',p.evaluate('!rd84Own(boss)&&RD84.events.length===0'))
  p.evaluate('beginStage(8);setState(GS.PLAY)');p.evaluate('()=>{spawnBoss("vileexistence");B=boss;v18Enter(B,2,2);B._r30.mode="fight";B.enter=B._noHit=false;for(const id of["cannonL","cannonR"]){B._lastPart=ph21Part(B,id);modularHit(ph21Part(B,id).hp);}}');p.evaluate(STEP,10);ck('Live Phoenix Order controller remains unchanged before final death',p.evaluate('ph83Own(B)&&!rd84Own(B)'))
  p.evaluate('()=>{v18Enter(B,2,6);B._r30.mode="fight";B.enter=B._noHit=false;nb23Start(B,"codeGeysers");}');p.evaluate(STEP,3);ck('Live brain attack remains with its established owner',p.evaluate('!!nb81Act(B)&&!rd84Own(B)'))
  ck('No native browser/draw errors in the selected-pilot and reset runs',not errors);br.close()
finally:stop()
s=(R/'assets/dracodia_terminal_art_1030.js').read_text();A=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
def restore(a):
 out=Image.new('RGBA',a['logical']);im=Image.open(R/A['pages'][a['key']]['path']).convert('RGBA');x,y,w,h=a['rect'];out.paste(im.crop((x,y,x+w,y+h)),(a['pivot'][0]+a['offset'][0],a['pivot'][1]+a['offset'][1]));return out
whole=restore(A['banks']['roar_0'][12]);broken=restore(A['banks']['body_shatter'][0]).crop((256,256,768,768));ck('Shatter frame zero exactly reconstructs every original body pixel',np.array_equal(np.array(whole),np.array(broken)))
ck('All nine current aircraft have both entry and return depth banks',all(len(A['banks']['ship_north_'+pk])==len(A['banks']['ship_south_'+pk])==32 for pk in A['pilots']))
(W/'boundaries.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2));assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
