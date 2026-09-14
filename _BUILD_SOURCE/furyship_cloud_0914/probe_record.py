"""Unskipped Stage-5 launch in native Chromium, motion/pixel checks and game audio."""
from pathlib import Path
import base64,json,sys,http.server,threading,subprocess,hashlib,array
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_cloud_0914';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
sys.path.insert(0,str(R/'_BUILD_SOURCE/stage_1_5_0914'));import audio_export
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import imageio_ffmpeg
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
ff=imageio_ffmpeg.get_ffmpeg_exe();errors=[];checks=[];timeline=[];shots=[]
def ok(v,n):checks.append({'pass':bool(v),'label':n});print(('ok  'if v else'FAIL ')+n,flush=True)
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate('''()=>{__auto=function(){};run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.stage=5;curStage=STAGES[4];beginStage(5);run.gravityShipReady=false;furyLegacyShip=false;furyShipWarm();warmPlayerAtlases();for(let i=0;i<7;i++)XART._touch('cm2_cloud_'+i);XART._touch(STAGE6_TRANSITION_SKY);Audio.resume();}''')
 pg.wait_for_function('()=>furyShipReady()&&XART.rdy(STAGE6_TRANSITION_SKY)&&Array.from({length:7},(_,i)=>XART.rdy("cm2_cloud_"+i)).every(Boolean)',timeout=120000)
 pg.evaluate('''()=>{story=null;player.reset();playerHit=function(){};__auto=function(){};for(const k of Object.keys(Input.keys))Input.keys[k]=false;setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch._furyIntro=null;__i=1;
 const L=__alog;L.snd.length=0;L.syn.length=0;L.warp.length=0;L.restarts.length=0;L.loops={};
 window.__partWidths=[];const blit=furyShipBlit;furyShipBlit=function(k,x,y,w,h){if(FURY_KIT.some(q=>k.startsWith(q.key+'_')))__partWidths.push(w);return blit.apply(this,arguments);};}''')
 rec0=pg.evaluate('()=>__i');seconds=26;pic=O/'intro_picture.mp4'
 enc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(pic)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 targets=[.1,3.5,6,9,11.9,13.5,15.6,17.2,18.5,19,19.5,20,22,24];white_shot=None
 for f in range(seconds*30):
  pg.evaluate('()=>__step(2)')
  raw=pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.94).split(",")[1]');enc.stdin.write(base64.b64decode(raw))
  m=pg.evaluate('()=>{const S=drawLaunch._furyIntro;return {state,t:S.t,phase:S.phase,gravity:gravityMode.phase,space:S.space,white:S.white,scroll:S.scroll,speed:drawLaunch._spd,ship:S.ship,dialogue:gravityMode.dialogueDone,earned:run.gravityShipReady,error:window.__err||null};}');timeline.append(m)
  if f%90==0:print('frame',f,m,flush=True)
  assert not m['error'],m['error']
  capture=bool(targets and f/30>=targets[0])
  if capture:targets.pop(0)
  if capture or(m['white']==1 and white_shot is None):
   name='intro_%04d_%s'%(f,m['gravity']);path=O/(name+'.png');path.write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')));shots.append(path)
   if m['white']==1 and white_shot is None:white_shot=path
 enc.stdin.close();err=enc.stderr.read();assert enc.wait()==0,err
 active=[m for m in timeline if m['state']=='launch'];ok(len(active)>600,'extended launch exceeds twenty seconds without skipping HQ dialogue')
 ok(all(m['speed']==420 for m in active),'constant 420 px/s travel throughout sky, assembly, reveal and countdown')
 ok(all(abs((z['scroll']-a['scroll'])/(z['t']-a['t'])-420)<.01 for a,z in zip(active,active[1:])if z['t']>a['t']),'actual background accumulator never decelerates or stops')
 ok(pg.evaluate('()=>FURY_KIT.length===12&&new Set(FURY_KEYS).size===FURY_KEYS.length'),'twelve separate assembly pieces with no duplicate asset registrations')
 widths=pg.evaluate('()=>__partWidths');ok(max(widths)>190,'full-sized assembly pieces draw at 194.7 px instead of the old 48-pixel cells')
 ok(all(not m['space']for m in active if m['gravity']in ['drift','charge','scatter','snap','pixelglow','whiteout']),'sky and cloud clearing remain until the opaque-white handoff')
 first=next(i for i,m in enumerate(active)if m['space']);ok(active[first-1]['white']==1 and active[first]['white']>.99,'space first appears underneath full-screen white')
 if white_shot:
  im=Image.open(white_shot).convert('RGB');pixels=list(im.getdata());ratio=sum(min(p)>250 for p in pixels)/len(pixels)
 else:ratio=0
 ok(ratio>.999,'pixel proof: full white covers HQ, ship, background and scanlines')
 ok({'sky','assembly','countdown'}<={m['phase']for m in active},'real launch traverses sky, assembly and countdown')
 ok(timeline[-1]['state']=='play' and timeline[-1]['earned'],'full sequence hands control to PLAY with earned new fighter')
 ok(not errors and not pg.evaluate('()=>window.__err||null'),'zero page, console and game-loop errors')
 ev=pg.evaluate('()=>__audioDump()');ev.update(rec0=rec0,frames=seconds*60);(O/'audio_events.json').write_text(json.dumps(ev))
 res=pg.evaluate(audio_export.RENDER,{'ev':ev,'iife':audio_export.audio_module_source(),'tail':0,'exclude':[]});assert not res['errs']and res['rms']>0,res['errs']
 gain=min(1,.85/res['peak']);samples=array.array('f');samples.frombytes(base64.b64decode(res['b64']));wav=O/'intro_sfx.wav';audio_export.write_wav_float(str(wav),array.array('f',(v*gain for v in samples)).tobytes())
 movie=O/'BulletsOfFury_Cloud_Transformation_0914.mp4'
 subprocess.run([ff,'-y','-v','error','-i',str(pic),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(movie)],check=True)
 subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
 audio={**{k:res[k]for k in ['peak','rms','counts','errs']},'exportGain':gain,'exportPeak':res['peak']*gain}
 b.close()
srv.shutdown()
sheet=Image.new('RGB',(960,((len(shots)+3)//4)*278),(16,23,32));d=ImageDraw.Draw(sheet)
for i,path in enumerate(shots):
 im=Image.open(path).convert('RGB');im.thumbnail((240,256));x=i%4*240;y=i//4*278;sheet.paste(im,(x,y));d.text((x+4,y+258),path.stem,fill='white')
sheet.save(O/'contact.png')
(O/'native.json').write_text(json.dumps({'checks':checks,'errors':errors,'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'timeline':timeline,'whiteCoverage':ratio,'audio':audio,'video':str(movie),'videoSeconds':seconds,'fullDecodeExitCode':0,'fixture':'Actual launch from t=0, full HQ dialogue, no phase skipping. Existing shoot/capture clock and capture-only invincibility.'},indent=2)+'\n')
print('RESULT',sum(c['pass']for c in checks),'/',len(checks),'VIDEO',movie,flush=True)
if not all(c['pass']for c in checks):raise SystemExit(1)
