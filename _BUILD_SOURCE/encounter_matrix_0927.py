"""54 real Chromium encounter behavior/audio inspections, not player victories."""
import ast,base64,json,http.server
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/encounters');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];results=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1050,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  catalog=p.evaluate('()=>STAGES.slice(0,9).map((s,i)=>({stage:i+1,boss:s.boss,mini:SUBBOSS[i+1]?.kind}))')
  p.evaluate("()=>{window.soundCalls={};const play=Snd.play;Snd.play=function(n,v){soundCalls[n]=(soundCalls[n]||0)+1;return play.call(Snd,n,v);};}")
  for d in ['normal','hard','furious']:
   for entry in catalog:
    for mini in [True,False]:
     kind=entry['mini'] if mini else entry['boss'];c={'stage':entry['stage'],'diff':d,'mini':mini,'kind':kind};print('RUN',c,flush=True)
     if not kind:continue
     p.evaluate(SETUP,c)
     p.evaluate("""()=>{timeScale=1;special=null;run.sonicT=run.dkT=0;lzMount=null;run.forge={};run.infusion=null;run._lifeCombatT=0;run._lifeThreat=0;run.weapon=0;run.wlevel=3;run.wlevels=[3,1,1,1,1,1,0,0,0];run.spaceLevels=[3,3,3];run.spaceWeapon=0;run._spaceVolleyCd=100;s6Opening=null;powerups=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;window.soundCalls={};window.M={patterns:[],forms:[],maxShots:0,totalShots:0,maxMove:0,entered:false,reentries:0,finite:true,quietPatterns:{},positions:[],initialHp:B.hp};}""")
     for sec in range(75):
      p.evaluate("""()=>{for(let i=0;i<60;i++){const x=B.x,y=B.y,oldEnter=B.enter;player.invuln=10;updatePlay(1/60);if(!B.enter)M.entered=true;else if(M.entered)M.reentries++;M.maxMove=Math.max(M.maxMove,Math.hypot(B.x-x,B.y-y));
       const mode=B._hammer?.state||B._er26?.mode||B._bomber?.mode||B._s7mod?.state||B._late27?.mode||B._whv?.st||B._v24?.pattern?.type||B._ovState||B._s9rift?.mode||B._s9fusion?.phase||B.phase||'unlabelled';
       if(!M.patterns.includes(mode))M.patterns.push(mode);const form=B._vForm??B._er26?.form??B._s3Nuclear?.mode;if(form!=null&&!M.forms.includes(form))M.forms.push(form);
       M.maxShots=Math.max(M.maxShots,eBullets.length);M.finite=M.finite&&Number.isFinite(B.x+B.y)&&eBullets.every(q=>Number.isFinite(q.x+q.y));
       for(const q of eBullets)if(!q._matrixSeen){q._matrixSeen=true;M.totalShots++;}
       if(i%10===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/6);}
      }}""")
      p.wait_for_timeout(8)
      if sec in [10,30,55] and d=='normal':
       (OUT/f"{entry['stage']}-{'mini' if mini else 'boss'}-{sec}.png").write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
     r=p.evaluate('c=>({...c,...M,hp:B.hp,maxhp:B.maxhp,cues:soundCalls,zoom:viewZoom(),state,enemyCount:enemies.length})',c);results.append(r)
     (OUT/'report.json').write_text(json.dumps({'cases':results,'errors':errors},indent=2),encoding='utf-8');print({k:r[k] for k in ['stage','diff','mini','patterns','totalShots','maxMove']},flush=True)
  br.close()
finally:stop()
assert not errors,errors
assert all(r['finite'] and r['entered'] and r['reentries']==0 for r in results)
