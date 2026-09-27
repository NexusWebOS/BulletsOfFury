"""Native input, damage and decoded-audio checks; fixtures are not campaign wins."""
from pathlib import Path
import ast,json,base64,http.server
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927');errors=[];report={}
tree=ast.parse(Path('_BUILD_SOURCE/probe_overnight_0927.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  report['manual']=[]
  for target in ['enemy','hammer','bomber']:
   p.evaluate(SETUP,5)
   p.evaluate("""target=>{timeScale=1;run.spaceMode=true;run.bombs=5;run.missileLevel=0;run._spaceVolleyCd=100;run.sonicT=run.dkT=0;run.spaceWeapon=0;special=null;lzMount=null;
    for(const k of Object.keys(Input.keys))Input.keys[k]=false;
    if(target==='enemy'){B=spawnEnemy('s5space_scavenger',player.x,player.y-100,{});B.hp=B.maxhp=1000;}
    else if(target==='hammer'){spawnBoss('chromehammer');B=boss;B.enter=false;B._noHit=false;hammerState(B,'hammer');B._hammer.balance0922=true;B.x=player.x;B.y=player.y-100;}
    else{spawnSubBoss__inner('siegebomber');B=subBoss;B.enter=false;B.x=player.x;B.y=player.y-100;}
    window.before={hp:B.hp,ammo:run.bombs};window.missiles=0;window.bombKey=(keybindFor(1).bomb||[]).find(k=>!k.startsWith('pad_'));Input.injectTap(bombKey);
   }""",target)
   for i in range(8):
    p.evaluate("()=>{for(let f=0;f<5;f++){updatePlay(1/60);missiles=Math.max(missiles,pBullets.filter(q=>q.kind==='gmiss').length);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}");p.wait_for_timeout(20)
   result=p.evaluate('target=>({target,before,after:B.hp,ammo:run.bombs,missiles,key:bombKey,locks:!!retina.target})',target);report['manual'].append(result)
  report['specials']=[]
  for pilot in ['maverick','falva','yuri','cole','decker','freezer','lizzie']:
   p.evaluate(SETUP,5)
   report['specials'].append(p.evaluate("""k=>{timeScale=1;run.spaceMode=true;run.spaceWeapon=1;run.pilot=k;pilotIndex=PILOTS.findIndex(p=>p.key===k);run.sonicT=run.dkT=0;lzMount=null;run.weapon=0;run.spaceLevels=[3,3,3];run._thunderStormUnlocked=false;special=null;startSpecial();window.kinds=new Set();
    const hold=(keybindFor(1).fire||[]).find(k=>!k.startsWith('pad_'));for(const key of Object.keys(Input.keys))Input.keys[key]=false;
    for(let f=0;f<180;f++){Input.keys[hold]=f<140;updatePlay(1/60);for(const q of pBullets)kinds.add(q.kind);}
    return {pilot:k,special:special?.pilot,kinds:[...kinds],rollers:rollers?.length,charging:run._spaceShadowCharge};}""",pilot))
  p.evaluate(SETUP,5)
  report['audio']=p.evaluate("""async()=>{Snd.stopMusic();Snd.loopStopAll();const C=Snd._audioCtx();await C.resume();const analyser=C.createAnalyser();analyser.fftSize=2048;const bins=new Float32Array(analyser.fftSize),out=[];
   const names=Object.values(AUDIO_0927_GROUPS).flat();
   for(const name of names){Snd.prepare(name);await new Promise(r=>setTimeout(r,150));const pool=Snd.pools[name];for(const slot of pool.slots){if(!slot?.attached)continue;const el=slot.el;if(!el._qaSource){el._qaSource=C.createMediaElementSource(el);el._qaSource.connect(C.destination);}el._qaSource.connect(analyser);}
    Snd._last[name]=-999;const accepted=Snd.play(name);let peak=0,playing=false;
    for(let i=0;i<8;i++){await new Promise(r=>setTimeout(r,35));analyser.getFloatTimeDomainData(bins);for(const x of bins)peak=Math.max(peak,Math.abs(x));for(const s of pool.slots)if(s?.attached&&!s.el.paused&&s.el.currentTime>0)playing=true;}
    out.push({name,accepted,playing,peak,ready:pool.slots.filter(s=>s?.attached).map(s=>s.el.readyState)});Snd.stopCue(name);for(const s of pool.slots)if(s?.el?._qaSource)s.el._qaSource.disconnect(analyser);
   }return out;}""")
  report['errors']=errors;(OUT/'input-audio.json').write_text(json.dumps(report,indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert all(x['after']<x['before']['hp'] and x['missiles'] and x['ammo']==x['before']['ammo']-1 for x in report['manual'])
assert all(x['accepted'] and x['playing'] and x['peak']>.001 for x in report['audio'])
