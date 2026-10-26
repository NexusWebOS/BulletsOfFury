"""Inspect the actual HAMMER/HAMA password routes and original authored plates."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_original_1025';O=O/('after' if '--after' in sys.argv else 'before');O.mkdir(exist_ok=True,parents=True);errors=[];report={}
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  for password in (['hama'] if '--hama' in sys.argv else ['hammer','hama']):
   p=browser.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.evaluate("""password=>{diffKey='furious';DIFF=DIFFS.furious;setState(GS.PASSWORD);pwInput=password;submitPassword();pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(PENDING_STAGE);debugUnlocked=true;DBGT.god=true;player.invuln=0;ht27Warm();c27Warm();window.auditSongTime=0;const song=ht27Song();Object.defineProperty(song,'currentTime',{configurable:true,get(){return auditSongTime},set(v){auditSongTime=v}});Object.defineProperty(song,'paused',{configurable:true,get(){return false}});window.auditTags=new WeakMap();const get=XART.get.bind(XART);XART.get=function(k){const im=get(k);if(im)auditTags.set(im,k);return im};window.auditDraws={};const draw=ctx.drawImage;ctx.drawImage=function(im,...args){const key=auditTags.get(im)||HA21.tags.get(im);if(key&&/hammer|whirl|hama|ht27|c27|hf22|ha21/.test(key))auditDraws[key]=(auditDraws[key]||0)+1;return draw.call(this,im,...args)};}""",password)
   p.wait_for_function("()=>{stageLoadTick();ht27Warm();return stageLoadReady(5)&&c27Warm()&&(!hamaOn()||hama29Ready())&&ht27Song().readyState>=2}",timeout=180000)
   for _ in range(20):
    p.evaluate(STEP,6);p.wait_for_timeout(10)
   samples=[];seen=set()
   for f in range(3000):
    p.evaluate('auditSongTime+=1/60');p.evaluate(STEP,1)
    if f%12==0:
     p.wait_for_timeout(1);s=p.evaluate("()=>({clock:ht27Data()?.clock,mode:ht27Data()?.mode,state:boss?._hammer?.state,pose:ha21Blue(boss)?.kind,c25:c25Own(boss),x:boss?.x})");samples.append(s)
     label=s.get('mode','none')+'-'+s.get('state','none')
     if s.get('state')=='whirlwind' and 290<s.get('x',0)<390: label+='-center'
     if label.endswith('-center') and label not in seen:
      s['whirlRender']=p.evaluate("""()=>{const keys=[],old=ctx.drawImage;ctx.drawImage=function(im,...args){const key=auditTags.get(im)||HA21.tags.get(im);if(key)keys.push(key);return old.call(this,im,...args)};try{drawWorld(0)}finally{ctx.drawImage=old}const r=HAMMER_WHIRL_REEL[hammerWhirlFrame(boss)];return{keys:keys.filter(k=>/arch_whirlwind|blue_tool|hammer_airborne/.test(k)),actual:hammerHeadPoint(boss),expected:{x:boss.x+(r[6]-r[4])*.62,y:boss.y+(r[7]-r[5])*.62}}}""")
     if label not in seen and (s.get('mode') in ['intro','breakdown','break','toss'] or s.get('state') in ['warn','leap','whirlwind']):
      seen.add(label);p.screenshot(path=str(O/(password+'-'+label+'.png')))
   report[password]={'samples':samples,'draws':p.evaluate('auditDraws')}
   # Export the exact original through XART, using the native game context.
   if password=='hammer':
    p.evaluate("XART.rdy('arch_whirlwind_0926')");p.wait_for_function("XART.rdy('arch_whirlwind_0926')")
    for f in range(8):
     png=p.evaluate("""f=>{const im=XART.get('arch_whirlwind_0926'),r=HAMMER_WHIRL_REEL[f];ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(im,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);ctx.restore();return cv.toDataURL('image/png').split(',')[1]}""",f)
     (O/f'original-whirl-{f}.png').write_bytes(base64.b64decode(png))
   print(json.dumps({'password':password,'states':sorted({s['state'] for s in samples}),'last':samples[-1]}),flush=True);p.close()
  browser.close()
finally:stop()
report['errors']=errors;(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps({'errors':errors}),flush=True)
