"""Chromium visual/audio evidence; clips are invulnerable inspection fixtures, not wins."""
import ast,base64,json,http.server
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overhaul_0927b');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text())
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={'clips':[]}
def shot(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1100,'height':1100});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(70)
  p.evaluate("()=>{Object.keys(POLISH_ART).forEach(k=>XART.rdy('polish_'+k));s7mWarm();furyShipWarm();cmap2Warm();}")
  p.wait_for_function("()=>Object.keys(POLISH_ART).every(k=>XART.rdy('polish_'+k))&&XART.rdy('s7m_warden')&&XART.rdy('cm2_isl_1')")
  report['extraPreviews']=p.evaluate("""()=>{let calls=0;const fx=Audio.SFX,sample=Snd.play,out=[];Snd.play=(...a)=>{calls++;sample.apply(Snd,a);};Audio.SFX=Object.fromEntries(Object.keys(fx).map(k=>[k,()=>{calls++;fx[k]?.();}]));try{for(const c of polishCollection().slice(90)){const P=forgePreviewNew(c.w,null,1);P.variant=c.variant;P.pilot=c.pilot;P.space=c.space;const start=calls;let kinds=new Set();for(let i=0;i<100;i++){forgePreviewTick(P,150,150,1/60);for(const b of P.bullets)kinds.add(b.kind);}out.push({name:c.name,err:P.err,sounds:calls-start,kinds:[...kinds]});}}finally{Audio.SFX=fx;Snd.play=sample;}return out;}""")
  report['mapFlash']=p.evaluate("""()=>{run.mode='campaign';stageSelIndex=0;cmap2Reset();const w=cmap2World(1);cmap2.cam={x:w.x,y:w.y,z:1};ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);polishMapFlash({t:.17,dur:.34,rect:{stage:1}});const d=ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height),a=d.data;let left=d.width,right=0,top=d.height,bottom=0,count=0;for(let y=0;y<d.height;y++)for(let x=0;x<d.width;x++)if(a[(y*d.width+x)*4+3]){left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);count++;}return{left,right,top,bottom,pixels:count,coverage:count/(d.width*d.height),width:d.width,height:d.height};}""")
  shot(p,'selected-island-only')
  p.evaluate("()=>{run.stage=4;run.spaceMode=false;run.pilot='cole';run.forge={};run.wlevels=[1,1,1,1,1,1,0,0,0];run.forgeForms={3:{fire:{elem:'fire',lv:1}},0:{ice:{elem:'ice',lv:1}}};armoryOpen('title');setState(GS.ARMORY);}")
  for i in range(8):p.evaluate(sh.STEP,10);p.wait_for_timeout(80)
  shot(p,'armory-final')
  for c in [{'stage':2,'kind':'magmaward','mini':True,'diff':'furious','seconds':24}, {'stage':3,'kind':'frostcruiser','mini':True,'diff':'furious','seconds':14}, {'stage':5,'kind':'siegebomber','mini':True,'diff':'hard','seconds':27}, {'stage':7,'kind':'sludgeemperor','mini':False,'diff':'normal','seconds':18}]:
   print('RECORD',c,flush=True);p.evaluate(SETUP,c)
   p.evaluate("()=>{run.forge={};run.forgeForms={};run.wvars=[];run.weapon=0;special=null;Input.keys.j=false;}")
   data=p.evaluate(r'''async c=>{
    const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:1700000}),chunks=[];
    rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
    const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
    const seen=[],snaps=[],start=performance.now();let last='',entered=false,reentries=0,finite=true,deadShot=false;rec.start();
    await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;player.invuln=10;powerups=[];
     Input.keys.arrowleft=t%8<4;Input.keys.arrowright=!Input.keys.arrowleft;Input.keys.j=false;
     if(c.stage===5&&t>22&&!deadShot){siegeBomberHit(B,1e6,B.x,B.y,'core');deadShot=true;}
     if(c.stage===5&&deadShot&&t>25.5){stagePlan=[];bossTriggered=true;}
     loop(now);if(!B.enter)entered=true;else if(entered)reentries++;
     for(const b of eBullets)if(!Number.isFinite(b.x+b.y+b.vx+b.vy))finite=false;
     const tag=B.dead?'defeated':B._bomber?.mode||B._er26?.mode||B._s7mod?.mode;if(tag!==last){seen.push({t:+t.toFixed(2),state:tag});last=tag;}
     if(snaps.length<12&&t>(snaps.length+1)*2)snaps.push(ctx.canvas.toDataURL());
     if(t>=c.seconds){clearInterval(timer);Input.keys.arrowleft=Input.keys.arrowright=false;resolve();}
    },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return{video,seen,snaps,reentries,finite};
   }''',c)
   name=c['kind'];(OUT/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',')[1]))
   for i,s in enumerate(data.pop('snaps')):(OUT/f'{name}_video_{i}.png').write_bytes(base64.b64decode(s.split(',')[1]))
   report['clips'].append({**c,**data});report['errors']=errors;(OUT/'review.json').write_text(json.dumps(report,indent=2))
  br.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert all(not q['err'] and q['sounds'] and q['kinds'] for q in report['extraPreviews'])
assert 0<report['mapFlash']['coverage']<.15
assert all(c['finite'] and c['reentries']==0 for c in report['clips'])
