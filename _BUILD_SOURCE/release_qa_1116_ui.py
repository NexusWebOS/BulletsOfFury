from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/ui';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?release-ui=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate("()=>{BOFOnline.submitScore=()=>{};coopOn=false;run.pilot='cole';pilotIndex=8;run.mode='campaign';debugFight=null;BOFCinematicDirector.cancel();story=null;}")
 for width,height,label in [(1440,1000,'desktop'),(390,844,'narrow')]:
  p.set_viewport_size({'width':width,'height':height})
  for name in ['TITLE','MODESEL','DIFF','PILOT','PASSWORD','OPTIONS','HELP','ACHIEVEMENTS','VAULT','ARMORY','CAMPHUB','FORGE']:
   e0=len(errors)
   try:
    p.evaluate("name=>{Input.clearTaps();Input.mouse.down=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;if(name==='FORGE'){run.loadout=[0,1,2,3,4,5];run.forgeElems={fire:1,ice:1};forgeStart(()=>{});}else setState(GS[name]);}",name)
    for i in range(20):p.evaluate(shoot.STEP,6);p.wait_for_timeout(5)
    q=p.evaluate('({state,width:cv.width,height:cv.height,rect:{w:cv.getBoundingClientRect().width,h:cv.getBoundingClientRect().height}})');q.update({'viewport':label,'requested':name,'errors':errors[e0:]});q['aspectPreserved']=abs(q['rect']['w']/q['rect']['h']-q['width']/q['height'])<.01;rows.append(q)
    p.screenshot(path=str(O/f'{label}-{name.lower()}.jpg'),type='jpeg',quality=84)
   except Exception as e:rows.append({'viewport':label,'requested':name,'exception':str(e)})
  print(label+' native menu survey captured',flush=True)
 # Native mouse coordinates must follow the newly letterboxed display rectangle.
 p.set_viewport_size({'width':390,'height':844});p.evaluate("()=>{run.loadout=[0,1,2,3,4,5];forgeStart(()=>{});}")
 for i in range(20):p.evaluate(shoot.STEP,6);p.wait_for_timeout(2)
 at=p.evaluate("()=>{const r=cv.getBoundingClientRect(),x=cutsceneViewWidth()*.083,y=VH*.294;return{x:r.left+x/(cv.width/SS)*r.width,y:r.top+y/(cv.height/SS)*r.height,vx:x,vy:y};}")
 p.mouse.move(at['x'],at['y']);p.mouse.down();p.evaluate(shoot.STEP,1);p.mouse.up();p.evaluate(shoot.STEP,1);point=p.evaluate('({x:Input.mouse.x,y:Input.mouse.y})')
 rows.append({'requested':'FORGE pointer registration','aspectPreserved':abs(point['x']-at['vx'])<2 and abs(point['y']-at['vy'])<2,'data':{'expected':at,'actual':point}})
 # Returning to combat restores native playfield and side-HUD geometry.
 p.set_viewport_size({'width':1440,'height':1000});p.evaluate(shoot.SETUP,{'state':'PLAY','stage':4,'pilot':'cole','invuln':True})
 for i in range(20):p.evaluate(shoot.STEP,6);p.wait_for_timeout(2)
 p.evaluate('()=>SC12.refresh()');q=p.evaluate('({state,width:cv.width,height:cv.height,rect:{w:cv.getBoundingClientRect().width,h:cv.getBoundingClientRect().height}})');q['requested']='PLAY restoration';q['aspectPreserved']=abs(q['rect']['w']/q['rect']['h']-q['width']/q['height'])<.01;rows.append(q);p.screenshot(path=str(O/'play-restored.png'))
 b.close()
(O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors,'scope':'Native menu render survey at desktop and narrow widths, backing/display aspect and letterboxed pointer registration plus gameplay restoration. Direct native state/Forge entry; not exhaustive interaction, entitlement or accessibility certification.'},indent=2),encoding='utf8');print(json.dumps({'screens':len(rows),'errors':errors,'exceptions':[r for r in rows if r.get('exception')],'badAspect':[r for r in rows if not r.get('aspectPreserved')]}),flush=True)
