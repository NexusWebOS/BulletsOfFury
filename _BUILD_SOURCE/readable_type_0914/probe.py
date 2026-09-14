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
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);for(let i=1;i<=9;i++){const a=ASSETS.stageFontV4[String(i)];stageText(a,'STAGE '+i,240,17+(i-1)*55,19,null,null,1,.06,1);const text=STAGES[i-1].sub;const h=stageFitH(a,text,450,15,10,.04);stageText(a,text,240,40+(i-1)*55,h,null,null,1,.04,1);}ctx.restore();}""");shot('stage_fonts')
 for p in ['yuri','cole','falva']:
  pg.evaluate("""p=>{run.pilot=p;ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);dlgBox({who:p.toUpperCase(),full:'We have incoming fighters! Lock your missiles onto the enemy and keep moving. Do not let them reach the dam.',shown:'We have incoming fighters! Lock your missiles onto the enemy and keep moving. Do not let them reach the dam.',tint:dialogueNameColor(p),screenSpace:false,y:170});ctx.restore();}""",p);shot('dialogue_'+p)
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);const es=['idle','anger','smile','sad','laugh','crash','victory'];for(let i=0;i<7;i++){const key=pilotPortrait('yuri',es[i]);const im=XART.get(key);ctx.drawImage(im,20+i%4*115,25+Math.floor(i/4)*185,96,105);msgText(es[i],68+i%4*115,150+Math.floor(i/4)*185,12,'#ffffff',1,1);}ctx.restore();}""");shot('yuri_expressions')
 pg.evaluate("""()=>{setState(GS.TITLE);stateT=12;}""")
 for _ in range(10):pg.evaluate('()=>__step(3)')
 shot('main_menu')
 pg.evaluate("""()=>{setState(GS.PILOT);pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.pilot='yuri';}""")
 for _ in range(25):pg.evaluate('()=>__step(3)');pg.wait_for_timeout(10)
 shot('pilot_yuri')
 # Exact glyph coverage and file-backed font readiness, across every shipping face.
 checks=[]
 def check(v,label):checks.append({'pass':bool(v),'label':label});print(('ok 'if v else'FAIL ')+label,flush=True)
 coverage=pg.evaluate("""()=>{const required='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?%&/:;.,-+()[]=<>@';return Object.keys(BOF_COMMAND_FONTS.names).map(k=>({key:k,family:BOF_COMMAND_FONTS.names[k],ready:bmfReady(k),missing:[...required].filter(c=>!bmfGlyph(BMF[k],c))}));}""")
 check(len(coverage)==11 and all(r['ready']and not r['missing']for r in coverage),'all eleven new faces load with uppercase, digits and punctuation')
 check(pg.evaluate("()=>bmfGlyph(BMF.dialogue,'a')===bmfGlyph(BMF.dialogue,'A')&&bmfMeasure('dialogue','Go! 01',14)===bmfMeasure('dialogue','GO! 01',14)"),'mixed-case source text measures and renders as uppercase')
 check(pg.evaluate("async()=>{await document.fonts.load('16px BOFmil');return document.fonts.check('16px BOFmil');}"),'new TrueType game font decodes in Chromium')
 # Compare actual pixels resolved by legacy keys, never cached-image identity or .src.
 yuri=pg.evaluate("""()=>{function hash(key){const im=XART.get(key);const c=document.createElement('canvas');c.width=180;c.height=190;const g=c.getContext('2d');g.drawImage(im,0,0,180,190);const d=g.getImageData(0,0,180,190).data;let h=2166136261;for(const v of d)h=Math.imul(h^v,16777619);return h>>>0;}const poses=['idle','anger','smile','sad','laugh','crash','victory'];const rows=poses.map(e=>({emotion:e,key:pilotPortrait('yuri',e),canonical:hash('yuri_v2_'+e),legacy:hash('port_yuri_'+e),cf:hash('port_cf_yuri_'+(e==='smile'?'happy':e))}));return {rows,talk:pilotPortrait('yuri','talk'),talkHash:hash('port_cf_yuri_talk-wide'),idle:hash('yuri_v2_idle')};}""")
 check(all(r['key'].startswith('yuri_v2_')and r['canonical']==r['legacy']==r['cf']for r in yuri['rows']),'old Yuri portrait keys resolve to the approved new expressions by pixel comparison')
 check(len({r['canonical']for r in yuri['rows']})==7,'seven distinct authored new-Yuri expressions remain available')
 check(yuri['talk']=='yuri_v2_idle'and yuri['talkHash']==yuri['idle'],'talking cannot fall back to the retired Yuri likeness')
 portraits=pg.evaluate("()=>PILOTS.map(p=>{const k=commPortrait(p.key,'idle'),im=XART.get(k);return {pilot:p.key,key:k,w:im.naturalWidth||im.width,h:im.naturalHeight||im.height};})")
 check(all(r['w']==r['h']==64 for r in portraits),'all nine dialogue portraits use the same compact 64px cell')
 layout=pg.evaluate("""()=>{const out=[],saved=msgDrawBlock;msgDrawBlock=function(o){const l=saved(o);out.push({height:l.height,space:o.h,size:l.H,lines:l.lines,w:o.w,alpha:o.alpha});return l;};for(const p of PILOTS){run.pilot=p.key;dlgBox({who:p.key,full:'INCOMING FIGHTERS! LOCK YOUR MISSILES ONTO THE ENEMY AND KEEP MOVING. DO NOT LET THEM REACH THE DAM.',screenSpace:false});}msgDrawBlock=saved;return out;}""")
 check(len(layout)==9 and all(r['height']<=r['space']and r['size']>=12 for r in layout),'all nine dialogue layouts fit at readable size without clipping')
 # Real scene transitions and a live typed radio line over gameplay.
 pg.evaluate("""()=>{run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');beginStage(1);setState(GS.PLAY);player.reset();playerHit=function(){};story={key:'QA',when:'safe',lines:[['YURI','Incoming fighters! Lock your missiles onto the enemy and keep moving.']],i:0,t:0,typed:0,done:false,fade:1};}""")
 ff=imageio_ffmpeg.get_ffmpeg_exe();movie=O/'Yuri_Readable_Dialogue_0914.mp4'
 enc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 for f in range(120):
  pg.evaluate('()=>__step(2)')
  enc.stdin.write(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.93).split(",")[1]')))
  if f==42:shot('yuri_in_game')
 enc.stdin.close();err=enc.stderr.read();assert enc.wait()==0,err
 subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
 # Full sky intro HQ text uses uppercase font at its actual callsite.
 pg.evaluate("""()=>{beginStage(5);run.gravityShipReady=false;furyLegacyShip=false;setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch._furyIntro=null;}""")
 for _ in range(160):pg.evaluate('()=>__step(3)')
 shot('hq_new_font')
 # Representative modal and cinematic renderers.
 pg.evaluate("""()=>{drawCommWindow({name:'YURI',frameKey:'dlg_yuri',tint:'#e23a3a',text:'Good luck, pilot. Keep the skies clear!',appear:1});}""");shot('modal_yuri')
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);cinDialogue({who:'yuri',text:'We are ready to launch. Bring everyone home.'},999,VW,VH);ctx.restore();}""");shot('cinematic_yuri')
 check(not errors and not pg.evaluate('()=>window.__err||null'),'no page, console or game-loop errors across pilot/menu/dialogue/launch')
 proof={'checks':checks,'fonts':coverage,'yuri':yuri,'portraits':portraits,'layout':layout,'errors':errors,'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'video':str(movie),'videoSeconds':4,'decodeExitCode':0,'fixture':'Real game/XART/font renderer; scripted radio line and capture-only invincibility. Silent preview.'}
 (O/'native.json').write_text(json.dumps(proof,indent=2)+'\n');b.close()
 assert all(c['pass']for c in checks)

stop()
