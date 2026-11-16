from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/loading';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];label=sys.argv[1]if len(sys.argv)>1 else'before'
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?night-loading=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{BOFOnline.submitScore=()=>{};BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');coopOn=false;diffKey='hard';Input.clearTaps();Input.mouse.down=false;NightDone=0;d1110Play('night-delayed-art',c16Rows('post-6','cole'),()=>{NightDone++;setState(GS.TITLE);});}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 p.evaluate("()=>{window.NightRealReady=XART.rdy;window.NightGate='cp15_cole';XART.rdy=function(k){return k===NightGate?false:NightRealReady.call(this,k);};}")
 q=p.evaluate("()=>{for(let i=0;i<1080;i++)BOFCinematicDirector.tick(1/60);BOFCinematicDirector.draw();const s=BOFCinematicDirector.current;return{i:s?.i,t:s?.t,shown:s?.shown,age:s?.age,done:NightDone};}")
 checks.append({'name':'18-second delayed required artwork cannot advance the scene or typewriter','ok':q.get('i')==0 and q.get('t',1)==0 and q.get('shown')==0,'data':q});p.screenshot(path=str(O/(label+'-delayed.png')))
 q=p.evaluate("()=>{NightGate=null;for(let i=0;i<60;i++)BOFCinematicDirector.tick(1/60);BOFCinematicDirector.draw();const s=BOFCinematicDirector.current;return{i:s?.i,t:s?.t,shown:s?.shown,done:NightDone};}")
 checks.append({'name':'delayed art release starts at the beginning of the first line','ok':q.get('i')==0 and .9<q.get('t',0)<1.1 and 0<q.get('shown',0)<=30,'data':q});p.screenshot(path=str(O/(label+'-resumed.png')))
 q=p.evaluate("()=>{BOFCinematicDirector.cancel();NightDone=0;d1110Play('night-loading-input',c16Rows('post-6','cole'),()=>{NightDone++;setState(GS.TITLE);});NightGate='cp15_cole';for(let i=0;i<30;i++)BOFCinematicDirector.tick(1/60);const s=BOFCinematicDirector.current;D1110.paused=true;const age=s.age;for(let i=0;i<60;i++)BOFCinematicDirector.tick(1/60);const paused=s.age===age&&s.t===0;D1110.paused=false;Input.injectTap('j');Input.mouse.down=true;BOFCinematicDirector.tick(1/60);NightGate=null;BOFCinematicDirector.tick(1/60);const q={paused,i:s.i,shown:s.shown,t:s.t};Input.mouse.down=false;Input.clearTaps();return q;}")
 checks.append({'name':'paused loading remains frozen and held A/mouse cannot reveal after decode','ok':q['paused']and q['i']==0 and q['shown']==0 and q['t']<.1,'data':q})
 q=p.evaluate("()=>{BOFCinematicDirector.cancel();NightDone=0;d1110Play('night-skip-loading',c16Rows('post-6','cole'),()=>{NightDone++;setState(GS.TITLE);});NightGate='cp15_cole';for(let i=0;i<30;i++)BOFCinematicDirector.tick(1/60);Input.injectTap('enter');BOFCinematicDirector.tick(1/60);BOFCinematicDirector.finish();XART.rdy=NightRealReady;return{done:NightDone,state};}")
 checks.append({'name':'Start can skip an undecoded scene exactly once','ok':q['done']==1 and q['state']=='title','data':q})
 p.evaluate("()=>{BOFCinematicDirector.cancel();Input.clearTaps();NightDone=0;campaignIntroStart(()=>{NightDone++;setState(GS.TITLE);});}");p.wait_for_function('()=>fury14Ready(FURY14.openKeys)',polling=50)
 q=p.evaluate("()=>{const ready=XART.rdy;XART.rdy=function(k){return k==='cin_war_earth_peace'?false:ready.call(this,k)};try{for(let i=0;i<6;i++)drawCampaignIntro(.1);Input.injectTap('enter');drawCampaignIntro(.1);return{done:NightDone,state,t:campaignIntro?.t};}finally{XART.rdy=ready}}")
 checks.append({'name':'Start can leave the opening when a background never decodes','ok':q['done']==1 and q['state']=='title','data':q})
 b.close()
(O/(label+'.json')).write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Controlled native readiness fault injection for a real required cockpit/background key, retaining production director/input/render paths. Demonstrates a delayed or failed decode contract, not a spontaneous network-failure report.'},indent=2),encoding='utf8');print(json.dumps({'checks':checks,'errors':errors},indent=2),flush=True)
