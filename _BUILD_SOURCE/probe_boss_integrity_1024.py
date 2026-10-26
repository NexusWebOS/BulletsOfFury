from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
import base64,json,subprocess,imageio_ffmpeg,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_integrity_1024';port,stop=serve(str(R));errors=[];checks=[]
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5&&typeof BI24!=="undefined"',timeout=180000);p.mouse.click(2,2);p.evaluate("()=>{diffKey='furious';debugStartFight({stage:8,role:'boss',kind:'vileexistence',name:'Dracodia'},{pilot:'cole'});}");p.wait_for_function('boss?._r30?.v18',timeout=180000);p.evaluate('()=>{v18Warm();bi24Warm();}');p.wait_for_function('v18Warm()&&bi24Warm()',timeout=180000);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
 for diff in ['normal','hard','furious']:
  for n,form,actor in [(0,0,'dracodia'),(2,2,'phoenix')]:
   p.evaluate("([diff,n,form])=>{diffKey=diff;v18Budget(boss);j3State(boss).ph21=null;v18Enter(boss,n,form);v18Fight(boss);boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=viewTopY()+235;BOFCinematicDirector.cancel();}",[diff,n,form])
   p.evaluate(STEP,3)
   r=p.evaluate("()=>{drawWorld(0);const q=BI24.current.get(boss);return {bank:q?.a.key,size:q?.size,parts:boss.parts.length,targets:retinaBossTargets(boss).length,hp:boss.hp};}");ck(diff+' '+actor+' whole actor actually drawn',actor in(r.get('bank')or''),r)
   (O/f'{actor}-{diff}.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
   r=p.evaluate("""()=>{const b=boss,n=D27_MODULE_DEBRIS.length,p=b.parts.find(p=>p.id===(ph21Own(b)?'cannonL':'left'));b._lastPart=p;const hp=p.hp;modularHit(Math.max(1,hp+1));return{before:n,after:D27_MODULE_DEBRIS.length,dead:p.destroyed,hp:p.hp,live:retinaBossTargets(b).length,events:BI24.events.slice(-2)};}""");ck(diff+' '+actor+' module break produces no PNG body tile',r['before']==r['after']and r['dead'],r)
   p.evaluate(STEP,24)
   r=p.evaluate("""()=>{const q=bi24AttackPose(boss,ph21Own(boss)?'phoenix':'dracodia'),c=bi24DamagePlate(q,boss),g=document.createElement('canvas');g.width=q.a.w;g.height=q.a.h;const x=g.getContext('2d');x.drawImage(XART.get(q.a.key),q.f%q.a.cols*q.a.w,Math.floor(q.f/q.a.cols)*q.a.h,q.a.w,q.a.h,0,0,q.a.w,q.a.h);const a=x.getImageData(0,0,g.width,g.height).data,d=c.getContext('2d').getImageData(0,0,g.width,g.height).data;let alpha=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i+3]!==d[i+3])alpha++;if(a[i]!==d[i]||a[i+1]!==d[i+1]||a[i+2]!==d[i+2])color++;}drawWorld(0);return{alpha,color};}""");ck(diff+' '+actor+' disabled module burns out without cutting hull alpha',r['alpha']==0 and r['color']>80,r)
   (O/f'{actor}-{diff}-disabled.png').write_bytes(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
 # Full actor flash without replacing native expiry timers.
 for n,form,actor in [(0,0,'dracodia'),(2,2,'phoenix')]:
  p.evaluate("([n,form])=>{v18Budget(boss);j3State(boss).ph21=null;v18Enter(boss,n,form);v18Fight(boss);boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=viewTopY()+230;}",[n,form])
  r=p.evaluate("""()=>{const b=boss;b.flash=0;for(const p of b.parts)p.flash=0;drawWorld(0);const before=ctx.getImageData(0,0,cv.width,cv.height).data;b._lastPart=b.parts.find(p=>p.id===(ph21Own(b)?'cannonL':'left'));modularHit(1);drawWorld(0);const after=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<after.length;i+=4)if(after[i]>240&&after[i+1]>240&&after[i+2]>240&&before[i]+before[i+1]+before[i+2]<650)white++;return {white,flash:b.flash};}""");ck(actor+' native damaged pixels visibly flash',r['white']>80,r);p.evaluate(STEP,24);r=p.evaluate('boss.flash');ck(actor+' native flash expires',r<=0,r)
 # The full displayed health budget still gates phase progression exactly once.
 for n,form,actor in [(0,0,'dracodia'),(2,2,'phoenix')]:
  p.evaluate("([n,form])=>{v18Budget(boss);j3State(boss).ph21=null;v18Enter(boss,n,form);v18Fight(boss);boss.enter=false;boss._noHit=false;}",[n,form])
  r=p.evaluate("""()=>{const b=boss,total=b.hp,host=rb23Host(b),ids=host?['left','right']:['cannonL','cannonR'];let dealt=0;for(const id of ids){const p=b.parts.find(p=>p.id===id),before=b.hp;b._lastPart=p;modularHit(p.hp+1);dealt+=before-b.hp;}const alive=b.hp,still=b._r30.mode,part=b.parts.find(p=>p.id==='core');b._lastPart=part;modularHit(b.hp+1);const next=b._r30.mode,hp=b.hp;modularHit(99999);return{total,dealt,alive,still,next,hp,after:b.hp,core:part.hp,debris:D27_MODULE_DEBRIS.length};}""");ck(actor+' full health budget gates one native progression',r['total']==r['dealt']+r['alive']and r['alive']>0 and r['still']=='fight'and r['next']!='fight'and r['hp']==r['after']==0 and r['debris']==0,r)
 # All delivered cells, including native white bank, decode via real renderer.
 r=p.evaluate("""()=>{let drawn=0;for(const a of Object.values(BI24_ART.banks))for(let f=0;f<a.count;f++){ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,64,64);ctx.drawImage(XART.get(a.white),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,64,0,64,64);drawn++;}return drawn;}""");ck('Every new actor/hit cell decodes and draws',r>100,r)
 if '--checks-only' in sys.argv:
  ck('No page or console errors',not errors,errors);br.close();stop();(O/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)},indent=2),encoding='utf8');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
 # Natural native attack clocks in short review checkpoints; no scripted poses.
 for n,form,actor in [(0,0,'dracodia'),(2,2,'phoenix')]:
  p.evaluate("([n,form])=>{diffKey='furious';v18Budget(boss);j3State(boss).ph21=null;v18Enter(boss,n,form);v18Fight(boss);boss.enter=false;boss._noHit=false;BOFCinematicDirector.cancel();}",[n,form])
  ff=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','10','-i','pipe:0','-vf','scale=960:600:force_original_aspect_ratio=decrease,pad=960:600:(ow-iw)/2:(oh-ih)/2','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(O/(actor+'-after.mp4'))],stdin=subprocess.PIPE)
  for f in range(300):
   p.evaluate('()=>{player.invuln=999;player.x=worldWidth()/2+Math.sin(efxClock)*80;}');p.evaluate(STEP,6);ff.stdin.write(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
   if f%50==0:p.wait_for_timeout(10)
  ff.stdin.close();ff.wait()
 ck('No page or console errors',not errors,errors);br.close()
stop();(O/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)},indent=2),encoding='utf8');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
