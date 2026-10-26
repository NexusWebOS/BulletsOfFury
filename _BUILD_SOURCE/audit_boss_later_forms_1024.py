from pathlib import Path
import base64,json,subprocess,imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_animation_audit_1024';port,stop=serve(str(R));records=[];errors=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate("()=>{diffKey='furious';debugStartFight({stage:8,role:'boss',kind:'vileexistence',name:'Dracodia'},{pilot:'cole'});}");p.wait_for_function("boss?._r30?.v18",timeout=180000);p.wait_for_timeout(3000);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
 ff=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','10','-i','pipe:0','-vf','scale=960:600:force_original_aspect_ratio=decrease,pad=960:600:(ow-iw)/2:(oh-ih)/2','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(O/'stage8-later-checkpoints-before.mp4')],stdin=subprocess.PIPE)
 for n,form in [(1,0),(2,0),(2,8),(2,1),(2,6),(2,2)]:
  p.evaluate("([n,form])=>{v18Enter(boss,n,form);v18Fight(boss);boss.enter=false;boss._noHit=false;BOFCinematicDirector.cancel();}",[n,form]);p.wait_for_function('v18Warm()',timeout=180000);last=''
  for f in range(350):
   p.evaluate("()=>{player.invuln=999;player.x=clamp(worldWidth()/2+Math.sin(efxClock*.8)*130,camLeftX()+25,camRightX()-25);}");p.evaluate(STEP,6)
   if f%5==0:
    r=p.evaluate("()=>{const b=boss,N=b._r30.v18;return{mode:b._r30.mode,encounter:j3State(b).encounter,form:N.form,attack:N.attack?.type,model:v18Model(b),action:hb20Own(b)?hb20State(b)?.action?.type:null,pose:hb20Own(b)?hb20Pose(b)?.kind:null};}");key=json.dumps(r)
    if key!=last:
     last=key;r['video']=len(records);r['clip']=[n,form];r['seconds']=f/10;records.append(r);(O/f'checkpoint-{n}-{form}-{f}.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL('image/png').split(',')[1]")))
   ff.stdin.write(base64.b64decode(p.evaluate("cv.toDataURL('image/png').split(',')[1]")))
   if f%100==0:p.wait_for_timeout(40)
  print('recorded checkpoint',n,form,flush=True)
 ff.stdin.close();ff.wait();br.close()
stop();(O/'later-checkpoints.json').write_text(json.dumps({'records':records,'errors':errors},indent=2),encoding='utf8');print('errors',errors)
