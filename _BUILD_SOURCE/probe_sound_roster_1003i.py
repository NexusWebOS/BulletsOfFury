"""Audit live Stage 6-8 attack/impact routes and all generated mixer voices."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_1003i';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
out={'checks':[],'roster':[],'playback':[]};errors=[]
def ck(v,s):out['checks'].append({'ok':bool(v),'name':s});print(('PASS ' if v else 'FAIL ')+s,flush=True)
def frames(p,n):
 for i in range(0,n,20):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(8)
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':960})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate('()=>{window.auditCalls=[];window.missing=new Set();const play=Snd.play;Snd.play=function(k){auditCalls.push(k);if(!Snd.pools[k])missing.add(k);return play.apply(this,arguments);};Audio.init();Audio.resume();}')
  for stage in [6,7,8]:
   p.evaluate(SETUP,{'stage':stage,'diff':'furious'})
   kinds=p.evaluate('(stage)=>Object.keys(stage===6?S6STORM:stage===7?S7TOXIC:S8MEGA)',stage)
   for kind in kinds:
    p.evaluate(SETUP,{'stage':stage,'diff':'furious'})
    p.evaluate('(kind)=>{auditCalls=[];AV3.events=[];window.E=spawnEnemy(kind,player.x,125,{});if(!E)return;E._entrySweep=null;E._noHit=false;window.attackSounds=[];if(E._mm1003){E._mm1003.homeY=130;E._mm1003.cd=0;}if(E._orbit1003){E._orbit1003.homeY=130;E._orbit1003.cd=0;}}',kind)
    impact=p.evaluate('()=>{if(!E)return null;const hp=E.hp;AV3.last.clear();hitEnemy(E,1,true);return {hit:E.hp<hp,cue:AV3.events.some(q=>q.cue.startsWith("impact_"))};}')
    if impact:ck(impact['hit'] and impact['cue'],f'Level {stage} {kind} damage invokes impact sound')
    p.evaluate('()=>{auditCalls=[];AV3.events=[];AV3.last.clear();}')
    frames(p,420)
    row=p.evaluate('()=>({type:E?.type||"scheduled-stealth-flight",stage:run.stage,sounds:[...new Set(auditCalls)],newCues:[...new Set(AV3.events.map(q=>q.cue))],dead:!!E?.dead,phase:E?._phase,locked:h3Locked(),enemies:enemies.map(e=>e.type)})');row['requested']=kind;out['roster'].append(row)
    ck(bool(row['sounds']),f'Level {stage} {kind} attacks invoke sound');print(row,flush=True)
   # Decode every recording reached by that biome, including retained authored cues.
  ck(p.evaluate('()=>missing.size===0'),'live late-stage roster has no unregistered sound requests')
  out['missing']=p.evaluate('()=>[...missing]')
  # Every new cue is played through Snd, captured downstream of the actual element.
  p.evaluate(SETUP,{'stage':6,'pilot':'cole'})
  p.evaluate('()=>{Audio.stopMusic();Snd.loopStopAll();window.ac=new AudioContext();window.an=ac.createAnalyser();an.fftSize=2048;an.connect(ac.destination);Snd.vol.master=1;Snd.vol.sfx=1;window.claimed=new WeakSet();window.attach=el=>{if(!claimed.has(el)){ac.createMediaElementSource(el).connect(an);claimed.add(el);}};}')
  names=p.evaluate('()=>AV3_CUES')
  for name in names:
   p.evaluate('(name)=>{Snd.prepare("av3_"+name);window.bank=Snd.pools["av3_"+name];}',name)
   p.wait_for_function('()=>bank.list.every(a=>a.readyState>=3)',timeout=30000)
   p.evaluate('(name)=>{for(const a of bank.list)attach(a);ac.resume();bank.i=0;AV3.last.clear();delete Snd._last["av3_"+name];av3Sound(name);}',name)
   peak=0
   for _ in range(8):
    p.wait_for_timeout(40);peak=max(peak,p.evaluate('()=>{const x=new Float32Array(2048);an.getFloatTimeDomainData(x);return Math.max(...x.map(Math.abs));}'))
   row=p.evaluate('()=>({playing:bank.list.some(a=>!a.paused&&a.currentTime>0),src:bank.list[0].src.split("/").pop()})');row.update({'name':name,'peak':peak});out['playback'].append(row)
   ck(peak>.0001 and row['playing'],'audible mixer output: '+name)
   p.evaluate('(name)=>Snd.stopCue("av3_"+name)',name)
  ck(p.evaluate('()=>Object.entries(AV3_ALIASES).every(([k,v])=>BOFA.sfx[k]===BOFA.sfx["av3_"+v]&&Snd.pools[k]===Snd.pools["av3_"+v])'),'direct Snd and Audio.SFX boss routes share the generated files')
  ck(not errors,'zero browser errors');br.close()
finally:stop();out['errors']=errors;(O/'sound-roster.json').write_text(json.dumps(out,indent=2)+'\n')
sys.exit(0 if all(q['ok'] for q in out['checks']) and not errors else 1)
