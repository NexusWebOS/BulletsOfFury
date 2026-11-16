from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/dialogue';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];label=sys.argv[1]if len(sys.argv)>1 else'before'
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?night-dialogue=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 matrix=p.evaluate("()=>{const rows=[];for(const st of [GS.PLAY,GS.CUTSCENE,GS.RIVAL,GS.RIVALALLY]){state=st;for(const pilot of PILOTS)rows.push({state:st,who:pilot.key,material:kd18Material({who:pilot.key.toUpperCase(),portrait:pilot.key})});}state=GS.TITLE;return rows;}")
 checks.append({'name':'crew speakers retain crew metal in every dialogue context','ok':all(q['material']=='crew'for q in matrix),'data':matrix})
 matrix2=p.evaluate("()=>{const out=[];for(const st of [GS.PLAY,GS.CUTSCENE,GS.RIVAL,GS.RIVALALLY]){state=st;for(const who of ['VOSS','NYX','ROOK','KAIA','JACE','CHRONOS','CHRONUS','CRONOS','DRACODIA','LORD OF SHADOWS'])out.push({state:st,who,material:kd18Material({who})});}state=GS.TITLE;return out;}")
 checks.append({'name':'named enemies retain their rust/purple/blue materials','ok':all(q['material']==('chronos'if q['who']in['CHRONOS','CHRONUS','CRONOS']else'dracodia'if q['who']in['DRACODIA','LORD OF SHADOWS']else'rebel')for q in matrix2),'data':matrix2})
 p.evaluate("()=>{BOFCinematicDirector.cancel();run.pilot='cole';pilotIndex=8;run.mode='campaign';setState(GS.RIVALALLY);kd18Warm();for(const k of ['pav_decker','pav_cole','system_avatar_1109'])XART.rdy(k);}")
 p.wait_for_function("()=>{kd18Warm();return XART.rdy('pav_decker')&&XART.rdy('cd27_neutral_460')&&bmfReady('dialogue')}",polling=50)
 q=p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#080d14';ctx.fillRect(0,0,cv.width/SS,VH);dlgBox({who:'DECKER',portrait:'decker',full:'The team is ready. Choose your wingmen.',shown:'The team is ready. Choose your wingmen.',forceShown:true,fade:1,y:100,screenSpace:false});return KD18.radio;}")
 checks.append({'name':'actual friendly ally-window dialogue paints crew material with selection avatar','ok':q.get('material')=='crew'and q.get('avatar')=='pav_decker','data':q});p.screenshot(path=str(O/(label+'-ally-decker.png')))
 checks.append({'name':'no page or console errors','ok':not errors,'data':errors});b.close()
(O/(label+'.json')).write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Native dialogue material dispatch in four contexts,36 crew/40 enemy cases, plus actual ally-window dialogue render. Does not claim full Rival Fight UI or campaign traversal.'},indent=2),encoding='utf8');print(json.dumps({'passed':sum(q['ok']for q in checks),'failed':sum(not q['ok']for q in checks),'badCrew':[q for q in matrix if q['material']!='crew'],'errors':errors},indent=2),flush=True)
