from pathlib import Path
import json,base64,subprocess,imageio_ffmpeg,sys
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_integrity_1024';port,stop=serve(str(R));checks=[];errors=[];timeline=[]
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
def writer(path):return subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','10','-i','pipe:0','-vf','scale=960:600:force_original_aspect_ratio=decrease,pad=960:600:(ow-iw)/2:(oh-ih)/2','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE)
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5&&typeof BI24!=="undefined"',timeout=180000)
 p.mouse.click(2,2);p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'hammer',name:'Chronos'},{pilot:'cole'});bi24Warm();}");p.wait_for_function('boss?._hammer&&bi24Warm()',timeout=180000);p.wait_for_timeout(500);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
 # Explicit review checkpoints use the native draw owner, no mock canvas.
 p.evaluate("()=>{BOFCinematicDirector.cancel();boss._hammerTime=null;boss._hammer.hb20Pickup=null;boss._hammer.hc11Counter=null;boss._hammer.hammerDestroyed=false;boss._hammer.recovery=null;boss.x=worldWidth()/2;boss.y=viewTopY()+245;}")
 for state,variant in [(s,v)for v in ['blue','red','armor']for s in ['storm_raise','spell','hammer_stun']]:
  p.evaluate(STEP,24)
  r=p.evaluate("""([s,v])=>{const b=boss,h=b._hammer;b.x=worldWidth()/2;b.y=viewTopY()+245;h.state=s;h.t=.9;h.spellTargets=[];h.pillars=[];h._hf22Red=v==='red';const A=fr27Armor(b)||(h.frArmor={hp:0,max:b.maxhp,barrier:0,checkpoints:[]});A.activated=v==='armor';A.hp=v==='armor'?A.max:0;const q=ha21Blue(b);if(q){XART.rdy(q.a.key);XART.rdy(q.a.white);}return q?.kind;}""",[state,variant]);p.wait_for_timeout(30)
  r=p.evaluate("""()=>{const b=boss,q=ha21Blue(b);b.flash=0;for(const p of b.parts||[])p.flash=0;const keys=[],draw=ctx.drawImage;ctx.drawImage=function(im,...a){const k=HA21.tags.get(im);if(k)keys.push(k);return draw.call(this,im,...a);};try{drawWorld(0);}finally{ctx.drawImage=draw;}const before=ctx.getImageData(0,0,cv.width,cv.height).data;markHit(b,.12);drawWorld(0);const after=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<after.length;i+=4)if(after[i]>240&&after[i+1]>240&&after[i+2]>240&&before[i]+before[i+1]+before[i+2]<650)white++;return{kind:q?.kind,head:hammerHeadPoint(b),expected:q?hb20World(q.a,q.a.tip,b,q.k,q.rot):null,white,keys};}""")
  ck(variant+' '+state+' real new body pixels and flash',r['kind'].startswith('bi24_')and r['white']>80 and any(k.startswith('bi24_')for k in r['keys']),r);ck(variant+' '+state+' hammer head follows displayed pose',r['head']==r['expected'],r['head']);(O/(variant+'-'+state+'.png')).write_bytes(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
 if '--checks-only' in sys.argv:
  ck('No page or console errors',not errors,errors);br.close();stop();(O/'chronos-pose-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
 # Fresh native fight, normal fire and Retina inputs, no forced actions.
 p.evaluate("()=>{debugStartFight({stage:5,role:'boss',kind:'hammer',name:'Chronos'},{pilot:'cole'});}");p.evaluate(STEP,30);ff=writer(O/'chronos-after.mp4');p.keyboard.down('j');p.keyboard.down('c');last=''
 for f in range(900):
  if f%80==0:p.keyboard.up('a');p.keyboard.up('d');p.keyboard.down('a'if f//80%2 else'd')
  p.evaluate('()=>{player.invuln=999;}');p.evaluate(STEP,6)
  if f%5==0:
   r=p.evaluate("()=>({state:boss?._hammer?.state,pose:boss?._hammer?ha21Blue(boss)?.kind:null,hp:boss?.hp,t:efxClock})");k=json.dumps({a:b for a,b in r.items()if a not in ['hp','t']})
   if k!=last:last=k;r['seconds']=f/10;timeline.append(r)
  ff.stdin.write(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
  if f%100==0:print('Chronos native seconds',f/10,flush=True);p.wait_for_timeout(10)
 ff.stdin.close();ff.wait();p.keyboard.up('j');p.keyboard.up('c');p.keyboard.up('a');p.keyboard.up('d')
 if '--stage5-only' in sys.argv:
  ck('No page or console errors',not errors,errors);br.close();stop();(O/'chronos-results.json').write_text(json.dumps({'checks':checks,'timeline':timeline,'errors':errors},indent=2),encoding='utf8');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
 p.evaluate("()=>{debugStartFight({stage:8,role:'boss',kind:'vileexistence',name:'Dracodia'},{pilot:'cole'});}");p.evaluate(STEP,3);p.evaluate('v18Warm()');p.wait_for_function('boss?._r30?.v18&&v18Warm()',timeout=180000);p.evaluate("()=>{v18Enter(boss,2,8);v18Fight(boss);boss.enter=false;boss._noHit=false;BOFCinematicDirector.cancel();}");ff=writer(O/'corrupt-hammer-after.mp4')
 for f in range(350):
  p.evaluate('()=>{player.invuln=999;player.x=worldWidth()/2+Math.sin(efxClock)*80;}');p.evaluate(STEP,6);ff.stdin.write(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
  if f%100==0:p.wait_for_timeout(10)
 ff.stdin.close();ff.wait();ck('No page or console errors',not errors,errors);br.close()
stop();(O/'chronos-results.json').write_text(json.dumps({'checks':checks,'timeline':timeline,'errors':errors,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)},indent=2),encoding='utf8');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
