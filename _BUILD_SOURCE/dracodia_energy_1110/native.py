from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,base64,io,subprocess,http.server
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/dracodia-energy'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
BOOT="""()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(8,'boss'),{pilot:'cole'});spawnBoss('vileexistence');debugFight.spawned=true;warnT=0;DBGT.god=false;DBGT.speed=1;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;stagePlan=[];enemies=[];powerups=[];window.B=boss;}"""
CHECKPOINT="""()=>{window.formCheckpoint=(form,y)=>{v18Clear(B);spawnBoss('vileexistence');B=boss;const J=j3State(B);for(const i of V18.forms)if(i!==form)J.hp[i]=0;v18Enter(B,2,form);B._r30.mode='fight';B.enter=B._noHit=false;B._r30.v18.arenaPhase=2;B.x=worldWidth()/2;B.y=y;B._r30.v18.home={x:B.x,y:B.y};B._r30.cd=100;player.dead=player.out=false;player.x=worldWidth()/2;player.y=VH-65;player.invuln=1e9;player.roll=player.somer=null;DBGT.god=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;pBullets=[];eBullets=[];playerLocks=[];stagePlan=[];enemies=[];powerups=[];camX=(worldWidth()-VW)/2;D124.events=[];return B.hp;};}"""
def step(p,n=1):
 e=p.evaluate(STEP,n);assert e is None,e
def shot(p):return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")))).convert('RGB').resize((480,512),Image.Resampling.NEAREST)
def record(p,name,seconds,done=None):
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','480x512','-framerate','15','-i','pipe:0','-an','-c:v','ffv1','-level','3',str(W/(name+'.mkv'))],stdin=subprocess.PIPE);rows=[];saved=set()
 try:
  for i in range(round(seconds*15)):
   step(p,4);row=p.evaluate("()=>{const P=B._r30.v18.form===2?ph21State(B).action:B._r30.v18.attack;return {phase:P?._d124Eye?d124Pulse(P).phase:P?._d124Storm?'storm':P?.phase||P?.type,t:P?.t||0,mode:B._r30.mode,kind:P?.kind||P?.type};}");rows.append(row);im=shot(p);encoder.stdin.write(im.tobytes());tag=row['phase']or'hover'
   if (tag not in saved and row['t']>.25)or(name=='lightning'and any(abs(row['t']-v)<.04 for v in [1.55,3,4.45])):
    saved.add(tag);im.save(O/(name+'-'+tag+('-'+str(i)if name=='lightning'else'')+'.png'))
   if i%90==0:print(json.dumps({'clip':name,'seconds':round(i/15,1),'phase':row['phase']}),flush=True)
   if done and p.evaluate(done):break
 finally:encoder.stdin.close();assert encoder.wait(timeout=60)==0
 return {'seconds':len(rows)/15,'rows':rows,'events':p.evaluate('D124.events'),'draws':p.evaluate('D124.draws')}
def main():
 errors=[];clips={};port,stop=serve(str(R))
 try:
  with sync_playwright()as pw:
   br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5&&typeof D124!=="undefined"');p.evaluate(TRAP_RAF);p.evaluate(BOOT);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}');p.evaluate(CHECKPOINT);print('Native game and new effects ready',flush=True)
   p.evaluate("()=>{formCheckpoint(2,174);ph82Start(B,'core');}");clips['phoenix-core']=record(p,'phoenix-core',5)
   p.evaluate("()=>{for(const id of ['cannonL','cannonR']){const part=ph21Part(B,id);B._lastPart=part;for(let i=0;i<8&&part.hp>0;i++)modularHit(part.hp+1);}ph21State(B).cool=0;ph83State(B).seed=11;PH83.events=[];}")
   for i in range(900):
    step(p,4)
    if p.evaluate("ph21State(B).action?.phase==='charge'"):break
   assert p.evaluate("ph21State(B).action?.phase==='charge'"),'Phoenix charge not reached'
   clips['phoenix-vortex']=record(p,'phoenix-vortex',20,"PH83.events.some(e=>e.event==='order-complete')")
   p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'eyeExpansion');}");clips['eye-lasers']=record(p,'eye-lasers',3.8)
   p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'codeGeysers');}");clips['lightning']=record(p,'lightning',5.6)
   p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'cloudAegis');}");clips['shield']=record(p,'shield',5)
   br.close()
 finally:stop()
 (O/'native-capture.json').write_text(json.dumps({'errors':errors,'clips':clips},indent=2));print(json.dumps({'errors':errors,'clips':{k:v['seconds']for k,v in clips.items()}}),flush=True);assert not errors,errors
if __name__=='__main__':main()
