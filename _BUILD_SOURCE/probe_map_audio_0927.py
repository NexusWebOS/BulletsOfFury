"""Real menu input and repeated miniboss-audio verification in Chromium."""
from pathlib import Path
import ast,base64,json
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927');report={};errors=[]
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>{run.mode='campaign';run.pilot='cole';campaign.bonusUnlocked=false;campaign.unlockedMax=8;_selFlash=null;window.sselCommitted=false;openStageSelect(4,{});}")
  for _ in range(8):p.evaluate(sh.STEP,3);p.wait_for_timeout(100)
  report['map']=p.evaluate("""()=>{const fire=(keybindFor(1).fire||[]).find(k=>!k.startsWith('pad_'));Input.injectTap(fire);drawScene(1/60);
   const selected=_selFlash?.rect?.stage;if(!_selFlash)return {selected};_selFlash.t=_selFlash.dur*.5;
   ctx.setTransform(SS,0,0,SS,0,0);drawScene(0);const fills=[],draws=[],rotations=[],fill=ctx.fillRect,draw=ctx.drawImage,rotate=ctx.rotate;
   ctx.fillRect=function(...a){fills.push(a);return fill.apply(this,a);};ctx.drawImage=function(...a){draws.push(a.length);return draw.apply(this,a);};
   try{selFlashDraw();}finally{ctx.fillRect=fill;ctx.drawImage=draw;}
   ctx.rotate=function(a){rotations.push(a);return rotate.call(this,a);};try{sselShipDraw();}finally{ctx.rotate=rotate;}
   return {selected,committed:window.sselCommitted,fills,draws,rotations};}""")
  (OUT/'map-selected.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
  p.evaluate("()=>{_selFlash=null;window.sselCommitted=false;window.cues={};const real=Snd.play;Snd.play=function(k,v){cues[k]=(cues[k]||0)+1;return real.call(Snd,k,v);};}")
  report['minibossAudio']=[]
  for stage,kind in [(2,'magmaward'),(3,'frostcruiser'),(9,'voidhorizon')]:
   p.evaluate(SETUP,{'stage':stage,'kind':kind,'mini':True,'diff':'normal'});p.evaluate("()=>{cues={};stageTimer=30;window.startClock=combatAudioClock0927;}")
   for _ in range(22):
    p.evaluate("()=>{for(let f=0;f<60;f++){player.invuln=999;updatePlay(1/60);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}");p.wait_for_timeout(12)
   report['minibossAudio'].append(p.evaluate('stage=>({stage,stageTimer,combatElapsed:combatAudioClock0927-startClock,cues})',stage))
  report['errors']=errors;(OUT/'map-audio.json').write_text(json.dumps(report,indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert report['map']['selected']==4 and report['map']['committed']
assert not report['map']['fills'] and report['map']['draws']
assert all(abs(x)<.0001 for x in report['map']['rotations'])
assert all(sum(n for k,n in c['cues'].items() if k.startswith('combat'))>2 for c in report['minibossAudio'])
