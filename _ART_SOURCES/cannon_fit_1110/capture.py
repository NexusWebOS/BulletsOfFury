from pathlib import Path
import sys,io,base64,json
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/cannon-fit';sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];checks=[];frames=[];stages=[]
def check(name,ok,detail=None):
 checks.append({'name':name,'pass':bool(ok),'detail':detail})
def shot(p,phase):
 encoded=p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
 frames.append(Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGB').resize((480,512),Image.Resampling.NEAREST));stages.append(phase)
def pods(p):
 return p.evaluate("[TC119.draws.pod0_d0_0||0,TC119.draws.pod1_d0_0||0]")
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate("()=>{EA11.setup(6,'furious');stagePlan=[];enemies=[];powerups=[];DBGT.god=false;player.invuln=99999;spawnBoss('thunderhead');window.B=boss;}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&fb112Ready()}');p.evaluate(STEP,190)
  p.evaluate("()=>{fb112Cancel(B);B._fb112.phase='recover';B._fb112.dur=99;B._fb112.t=0;B._tc119.flow=null;B._tc119.di=0;B._fb112.heading=Math.PI/2;}")
  for i in range(12):p.evaluate(STEP,3);shot(p,'before')
  p.evaluate("()=>{B._fb112.phase='warn';B._fb112.attack='storm-cyclone';B._fb112.dur=99;B._fb112.t=2;tm115State(B).launched=false;}")
  p.evaluate(STEP,1);active_start=pods(p)
  for i in range(40):p.evaluate(STEP,3);shot(p,'firing')
  active_end=pods(p);check('Normal cannon faces are suppressed for the entire firing loop',active_end==active_start,{'before':active_start,'after':active_end});check('Both cannon effects are drawn',p.evaluate('tm115State(B).beams.length===2&&CF121.draws>0'))
  p.evaluate("()=>{B._fb112.phase='recover';B._fb112.dur=99;B._fb112.t=0;}");tail_start=pods(p);tail=[]
  # Every native recovery tick, including the last pose before expiration.
  for i in range(16):
   p.evaluate(STEP,1);shot(p,'recovery');tail.append(p.evaluate('({beams:tm115State(B).beams.length,frames:CF121.sockets.slice(-2).map(s=>s.frame),pods:[TC119.draws.pod0_d0_0||0,TC119.draws.pod1_d0_0||0]})'))
  still_active=[v for v in tail if v['beams']]
  check('No original cannon face is drawn during wind-down',all(v['pods']==tail_start for v in still_active),still_active)
  check('Recovery reaches its final authored pose',any(27 in v['frames'] for v in still_active))
  check('Cannon faces return only after the beam expires',tail[-1]['beams']==0 and all(v>old for v,old in zip(tail[-1]['pods'],tail_start)),tail[-1])
  for i in range(14):p.evaluate(STEP,3);shot(p,'after')
  # Native hit selection and return to ordinary energy frames.
  p.evaluate("()=>{B._fb112.phase='warn';B._fb112.t=2;tm115State(B).launched=false;for(const part of B._fb112.parts.filter(p=>p.type==='pressure'))part.flash=.18;}");p.evaluate(STEP,1)
  check('Active cannons retain native hit-flash selection',p.evaluate("tm115State(B).beams.every(b=>b.part.flash>0)"))
  p.evaluate(STEP,20);check('Hit flashes expire while the beam keeps animating',p.evaluate("tm115State(B).beams.length===2&&tm115State(B).beams.every(b=>b.part.flash<=0)"))
  hp=p.evaluate('B.hp');cancel_start=pods(p);p.evaluate("()=>{B._fb112.phase='recover';B._fb112.t=0;fb112Cancel(B);}");p.evaluate(STEP,1);cancel_end=pods(p);check('Cancellation removes the energy and restores both cannon faces',p.evaluate('tm115State(B).beams.length===0')and all(v>old for v,old in zip(cancel_end,cancel_start)))
  state=p.evaluate('({draws:CF121.draws,paths:Object.values(CF121.art).map(a=>a.path),sockets:CF121.sockets,hp:B.hp})');check('The new complete-coverage artwork is loaded',all('cannon_fit_1110' in n for n in state['paths']));check('Visual change retains native health',state['hp']==hp);br.close()
 frames[32].save(O/'in-game.png');frames[0].save(O/'before.png');frames[-1].save(O/'after.png')
 pal=frames[32].quantize(colors=192);gif=[f.quantize(palette=pal,dither=Image.Dither.NONE)for f in frames];durations=[50 if s!='recovery' else 20 for s in stages];gif[0].save(O/'attack-and-return.gif',save_all=True,append_images=gif[1:],duration=durations,loop=0,optimize=True)
 close=[f.crop((0,210,480,310))for f in gif];close[0].save(O/'opening-closeup.gif',save_all=True,append_images=close[1:],duration=durations,loop=0,optimize=True)
 report={'errors':errors,'checks':checks,'state':state,'frames':len(frames)};(O/'capture.json').write_text(json.dumps(report,indent=2));print(json.dumps({'errors':errors,'checks':checks,'frames':len(frames)}));assert not errors and all(c['pass']for c in checks)
finally:stop()
