"""Later-phase native inspection: forced setup states, not campaign victories."""
from pathlib import Path
import ast,base64,json,http.server
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/late-phases');OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
CASES=[]
for diff in ['normal','hard','furious']:
 for phase in ['core','head']:CASES.append({'stage':2,'kind':'infernoreaver','mini':False,'diff':diff,'phase':phase,'seconds':38})
 for phase in ['shield','guns','laser']:CASES.append({'stage':7,'kind':'sludgeemperor','mini':False,'diff':diff,'phase':phase,'seconds':25})
for kind,mini in [('frostcruiser',True),('cryospear',False)]:CASES.append({'stage':3,'kind':kind,'mini':mini,'diff':'furious','phase':'nuclear','seconds':75})
port,stop=sh.serve(sh.GAME);errors=[];cases=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1000,'height':1050})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>{window.cues={};const real=Snd.play;Snd.play=function(n,v){cues[n]=(cues[n]||0)+1;return real.call(Snd,n,v);};}")
  for c in CASES:
   print('RUN',c,flush=True);p.evaluate(SETUP,c)
   p.evaluate("""c=>{timeScale=1;special=null;run.sonicT=run.dkT=0;run._spaceVolleyCd=100;run.infusion=null;for(const k of Object.keys(Input.keys))Input.keys[k]=false;
    if(c.stage===2){furnaceSync(B);B.x=worldWidth()/2;B.y=150;B._fz.pools.left=B._fz.pools.right=0;if(c.phase==='head')B._fz.pools.body=0;furnaceEnter(B,c.phase);B._fz.trans=0;if(B._mwBarrier)B._mwBarrier.active=false;}
    if(c.stage===7){s7mInit(B);B._be=null;B._s7FinalNoBar=false;mapScroll=s7mEndScroll();B.x=worldWidth()/2;B.y=175;s7mSet(B,'recover');for(const id of ['frontL','frontR','rearL','rearR']){s7mSet(B,'recover');s7mHit(B,1e6,0,0,id);}if(c.phase!=='shield'){s7mSet(B,'recover');s7mHit(B,1e6,0,0,'core');}if(c.phase==='laser')for(const id of ['gunL','gunR']){s7mSet(B,'recover');s7mHit(B,1e6,0,0,id);}s7mSet(B,'recover');B._s7mod.seq=0;}
    window.P={modes:[],forms:[],events:[],maxBullets:0,finite:true,reentries:0,entered:false};cues={};}""",c)
   for sec in range(c['seconds']):
    p.evaluate("""c=>{for(let i=0;i<60;i++){player.invuln=999;updatePlay(1/60);const mode=B._fz?.attack||B._er26?.mode||B._s7mod?.mode,form=B._fz?.phase||B._s3Nuclear?.mode||B._er26?.form||s7mStage(B._s7mod);
     if(mode&&!P.modes.includes(mode))P.modes.push(mode);if(form&&!P.forms.includes(form))P.forms.push(form);if(!B.enter)P.entered=true;else if(P.entered)P.reentries++;
     P.maxBullets=Math.max(P.maxBullets,eBullets.length);P.finite=P.finite&&Number.isFinite(B.x+B.y)&&eBullets.every(q=>Number.isFinite(q.x+q.y));
     if(i%10===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/6);}}
     if(c.phase==='shield')s7mHit(B,1,0,0,'core');}""",c)
    p.wait_for_timeout(10)
    if sec in [5,13,23,46,68]:
     (OUT/f"{c['stage']}-{c['phase']}-{c['kind']}-{c['diff']}-{sec}.png").write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
   r=p.evaluate('c=>({...c,...P,cues,hp:B.hp,state,phase:B._s7mod?s7mStage(B._s7mod):null})',c);cases.append(r)
   (OUT/'report.json').write_text(json.dumps({'cases':cases,'errors':errors},indent=2),encoding='utf-8');print({k:r[k] for k in ['stage','phase','diff','modes','forms','cues']},flush=True)
  br.close()
finally:stop()
assert not errors,errors
assert all(c['finite'] and not c['reentries'] for c in cases)
