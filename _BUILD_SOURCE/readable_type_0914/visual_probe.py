"""Native Chromium pixels and real damage paths; no mock assets/context."""
from pathlib import Path
import sys,json,base64,hashlib,http.server,subprocess
import imageio_ffmpeg
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
R=Path(__file__).resolve().parents[2];O=R/'_shots/readable_type_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
port,stop=shoot.serve(str(R));errors=[];checks=[]
def ok(v,n):
 checks.append({'pass':bool(v),'label':n});print(('ok 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate('''()=>{__auto=function(){};run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');beginStage(5);furyShipWarm();XART._touch('dlg_rect_0914');for(let i=0;i<6;i++)XART.rdy('np5_ast_'+i);for(const st of ['idle','damaged','critical'])XART.rdy('ns9c_sm_'+st);msgFaceUse('dialogue');for(const p of PILOTS)pilotPortrait(p.key,'idle');}''')
 pg.wait_for_function('()=>XART.rdy("dlg_rect_0914")&&furyShipReady()&&Array.from({length:6},(_,i)=>XART.rdy("np5_ast_"+i)).every(Boolean)',timeout=120000)
 for _ in range(10):pg.evaluate('()=>__step(3)');pg.wait_for_timeout(20)
 def shot(name):
  (O/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
 pg.evaluate('''()=>{ctx.save();ctx.setTransform(document.querySelector('#screen').width/VW,0,0,document.querySelector('#screen').height/VH,0,0);ctx.fillStyle='#172031';ctx.fillRect(0,0,VW,VH);for(let i=0;i<6;i++){const im=XART.get('np5_ast_'+i);ctx.drawImage(im,15+i%3*155,12+Math.floor(i/3)*180,140,140);}ctx.restore();}''');shot('asteroid_art')
 pg.evaluate("""()=>{for(const p of PILOTS){for(const e of ['idle','happy','anger','sad','laugh','crash','victory'])commPortrait(p.key,e);pilotPortrait(p.key,'idle');}for(const a of Object.values(ASSETS.stageFontV4))void a.img;}""")
 pg.wait_for_function("()=>bmfReady('dialogue')&&bmfReady('game')&&Object.values(ASSETS.stageFontV4).every(a=>artReady(a))&&PILOTS.every(p=>XART.rdy('comm_'+p.key+'_idle'))",timeout=120000)
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);for(let i=1;i<=9;i++){const a=ASSETS.stageFontV4[String(i)];stageText(a,'STAGE '+i+' - '+STAGES[i-1].name,240,22+(i-1)*55,20,null,null,1,.06,1);}ctx.restore();}""");shot('stage_fonts')
 for p in ['yuri','cole','falva']:
  pg.evaluate("""p=>{run.pilot=p;ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);dlgBox({who:p.toUpperCase(),full:'We have incoming fighters! Lock your missiles onto the enemy and keep moving. Do not let them reach the dam.',shown:'We have incoming fighters! Lock your missiles onto the enemy and keep moving. Do not let them reach the dam.',tint:dialogueNameColor(p),screenSpace:false,y:170});ctx.restore();}""",p);shot('dialogue_'+p)
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);const es=['idle','anger','smile','sad','laugh','crash','victory'];for(let i=0;i<7;i++){const key=pilotPortrait('yuri',es[i]);const im=XART.get(key);ctx.drawImage(im,20+i%4*115,25+Math.floor(i/4)*185,96,105);msgText(es[i],68+i%4*115,150+Math.floor(i/4)*185,12,'#ffffff',1,1);}ctx.restore();}""");shot('yuri_expressions')
 pg.evaluate("""()=>{setState(GS.TITLE);stateT=12;}""")
 for _ in range(10):pg.evaluate('()=>__step(3)')
 shot('main_menu')
 pg.evaluate("""()=>{setState(GS.PILOT);pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.pilot='yuri';}""")
 for _ in range(25):pg.evaluate('()=>__step(3)');pg.wait_for_timeout(10)
 shot('pilot_yuri')
 print('ERRORS',errors,pg.evaluate('()=>window.__err||null'));b.close()
stop()
