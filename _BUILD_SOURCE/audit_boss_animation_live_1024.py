from pathlib import Path
import base64,json,subprocess,imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_animation_audit_1024';O.mkdir(exist_ok=True);port,stop=serve(str(R));errors=[];reports=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
 for stage,seconds in [(5,150),(8,210)]:
  p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate("stage=>{diffKey='furious';debugStartFight({stage,role:'boss',kind:stage===5?'hammer':'vileexistence',name:stage===5?'Chronos':'Dracodia'},{pilot:'cole'});}",stage)
  p.wait_for_function('boss && (boss._hammer||boss._r30)',timeout=180000);p.wait_for_timeout(2500);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{window.auditCanvas=document.createElement('canvas');auditCanvas.width=960;auditCanvas.height=600;window.auditGrab=()=>{const g=auditCanvas.getContext('2d');g.fillStyle='#000';g.fillRect(0,0,960,600);const k=Math.min(960/cv.width,600/cv.height);g.drawImage(cv,(960-cv.width*k)/2,(600-cv.height*k)/2,cv.width*k,cv.height*k);return auditCanvas.toDataURL().split(',')[1];};}")
  ff=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','10','-i','pipe:0','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(O/f'stage{stage}-furious-before.mp4')],stdin=subprocess.PIPE)
  timeline=[];last='';p.keyboard.down('j');p.keyboard.down('c')
  for f in range(seconds*10):
   if f%100==0:
    p.keyboard.up('a');p.keyboard.up('d');p.keyboard.down('a'if f//100%2 else'd')
   p.evaluate('()=>{player.invuln=999; if(coopOn)coopOn=false;}');p.evaluate(STEP,6)
   if f%5==0:
    r=p.evaluate("()=>{const b=boss,h=b?._hammer,S=b?._r30,N=S?.v18,J=S?j3State(b):null;return{t:efxClock,state,hs:h?.state,ht:h?.t,mode:S?.mode,encounter:J?.encounter,form:N?.form,attack:N?.attack?.type,action:h?.hb20?.action?.type,hp:b?.hp,blue:h?ha21Blue(b)?.kind:null,pose:S&&hb20Own(b)?hb20Pose(b)?.kind:null,playing:BOFCinematicDirector.current?.id};}")
    key=json.dumps({k:v for k,v in r.items()if k not in ['t','ht','hp']})
    if key!=last:
     last=key;r['video']=f/10;timeline.append(r)
     (O/f'stage{stage}-{len(timeline):03}.png').write_bytes(base64.b64decode(p.evaluate('auditGrab()')))
   ff.stdin.write(base64.b64decode(p.evaluate('auditGrab()')))
   if f%100==0:print('stage',stage,'seconds',f/10,flush=True);p.wait_for_timeout(40)
  ff.stdin.close();ff.wait();p.close();reports.append({'stage':stage,'timeline':timeline});(O/'timeline.json').write_text(json.dumps({'runs':reports,'errors':errors},indent=2),encoding='utf8')
 br.close()
stop();print('DONE errors',errors)
