"""Verify the actual survivor ending, native pixels and full frame coverage."""
from pathlib import Path
import sys,json,base64,hashlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/survivor_1010';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[]});BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';story=null;fb2Talk=null;s6Opening=null;drawVictory._t=0;drawVictory._ready=false;drawVictory._wait=0;drawVictory._waitF=0;drawVictory._sfx={};drawVictory._trueEnding=true;setState(GS.VICTORY);victoryEndingWarm();}")
  p.wait_for_function('victoryEndingReady()&&sv10Warm()&&hl10Warm()',polling=50)
  p.evaluate(shoot.STEP,2);check('Cold ending is ready before spending the survivor clock',p.evaluate('drawVictory._ready&&drawVictory._t<.1&&sv10Warm()'))
  registry=p.evaluate('SV10_ART');check('All eighty-two authored cells are genuinely ready through XART',p.evaluate('sv10Assets().length===82&&sv10Assets().every(a=>XART.rdy(a.key))'))
  check('Legacy dish/still remain archived but are retired from ending warm keys',p.evaluate("!victoryEndingKeys().includes('cinend_symbiote_survivor')&&!victoryEndingKeys().includes('cinend_satellite_dish')"))
  captures=p.evaluate('''async()=>{const size={w:cv.width,h:cv.height},out=[];
   try{cv.width=cv.height=384;ctx.setTransform(1,0,0,1,0,0);
    for(const bank of ['crawl','burst','contact'])for(let f=0;f<SV10_ART[bank].length;f++){
     ctx.clearRect(0,0,384,384);sv10Cell(bank,f,192,192,384);
     out.push({bank,frame:f,png:cv.toDataURL()});if(f%8===7)await new Promise(r=>setTimeout(r,0));}
    return out;
   }finally{cv.width=size.w;cv.height=size.h;ctx.setTransform(SS,0,0,SS,0,0);}}''')
  native=OUT/'native';native.mkdir(exist_ok=True);mismatches=[];registration=[];unique={}
  for q in captures:
   f=native/(q['bank']+'_'+str(q['frame']).zfill(2)+'.png');f.write_bytes(base64.b64decode(q['png'].split(',')[1]))
   pixels=np.array(Image.open(f).convert('RGBA'));a=registry[q['bank']][q['frame']];source=np.array(Image.open(ROOT/a['path']).convert('RGBA'))
   # The game's native canvas is alpha:false. Compare the actual black
   # composite, including semi-transparent generated edge pixels.
   mask=source[:,:,3]>=160;expected=source[:,:,:3].astype(float)*source[:,:,3:4]/255
   delta=np.abs(pixels[:,:,:3].astype(float)-expected);bad=int((delta[mask]>1.01).any(axis=1).sum());mismatches.append(dict(bank=q['bank'],frame=q['frame'],bad=bad,visible=int(mask.sum())))
   unique.setdefault(q['bank'],set()).add(hashlib.sha256(pixels.tobytes()).hexdigest())
   if q['bank']!='contact':
    score=pixels[:,:,1].astype(float)-pixels[:,:,0]-pixels[:,:,2]*.45;score[pixels[:,:,1]<180]=-1000
    remaining=set(map(tuple,np.argwhere(score>score.max()*.72)));groups=[]
    while remaining:
     seed=remaining.pop();todo=[seed];group=[seed]
     while todo:
      y,x=todo.pop()
      for dy,dx in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
       point=(y+dy,x+dx)
       if point in remaining:remaining.remove(point);todo.append(point);group.append(point)
     groups.append(group)
    lens=max(groups,key=lambda g:sum(score[y,x] for y,x in g));mass=sum(score[y,x] for y,x in lens)
    pivot=[float(sum(x*score[y,x] for y,x in lens)/mass),float(sum(y*score[y,x] for y,x in lens)/mass)];registration.append(dict(bank=q['bank'],frame=q['frame'],pivot=pivot))
  check('Native context matches every visible authored sprite pixel on black within one color step',all(q['bad']==0 and q['visible']>0 for q in mismatches),mismatches)
  check('Native reels contain thirty-two, thirty-two and sixteen distinct rendered poses',{k:len(v) for k,v in unique.items()}==dict(crawl=32,burst=32,contact=16))
  check('The actual emerald core stays at its physical pivot within one pixel',all(max(abs(v-192) for v in q['pivot'])<1 for q in registration),registration)
  def seek(q,name=None):
   p.evaluate("q=>{drawVictory._t=VICTORY_DISH_AT+q;ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);}",q)
   if name:p.screenshot(path=str(OUT/(name+'.png')))
   return p.evaluate('SV10.last')
  p.evaluate('SV10.draws={};SV10.events=[];drawVictory._sfx={};');seen={k:set() for k in ['crawl','burst','contact']};states=[]
  for i in range(444):
   s=seek(i/60)
   if s['bank']:seen[s['bank']].add(s['frame'])
   if 'effectFrame' in s:seen['contact'].add(s['effectFrame'])
   if i%30==0:p.wait_for_timeout(4)
   if i%24==0:states.append(s)
  check('Continuous real ending uses all eighty animation cells before the next scene',{k:len(v) for k,v in seen.items()}==dict(crawl=32,burst=32,contact=16),{k:sorted(v) for k,v in seen.items()})
  check('Charge and launch sound each trigger once per playthrough',p.evaluate("SV10.events.length===2&&SV10.events.every(e=>e.available)&&drawVictory._sfx.charge===1&&drawVictory._sfx.launch===1"),p.evaluate('SV10.events'))
  wide=seek(.95,'wide');close=seek(2.7,'close');charge=seek(4.6,'charge');launch=seek(5.55,'launch');empty=seek(6.45,'empty');fade=seek(7.3,'fade')
  check('Close shot makes the whole creature readable above the caption',close['phase']=='close-crawl' and close['root']['width']>=450,close)
  check('The coil becomes a forward-streaming launch then leaves the dish empty',charge['frame']<16 and launch['frame']>=16 and empty['bank'] is None)
  check('Survivor exits into the original black transition',fade['fade']==1 and p.evaluate('HL10.transition.phase===\'survivor\''))
  p.evaluate("()=>{drawVictory._t=VICTORY_WARNING_AT+.4;drawVictory(0);}");p.screenshot(path=str(OUT/'command.png'));check('Original Fury Command scene follows at the unchanged clock',p.evaluate('drawVictory._t===VICTORY_WARNING_AT+.4'))
  p.set_viewport_size(dict(width=480,height=900));p.wait_for_timeout(100);narrow=seek(3.25,'narrow')
  dims=p.evaluate('()=>{const r=cv.getBoundingClientRect();return{x:r.width/cutsceneViewWidth(),y:r.height/VH};}')
  check('Narrow cinematic remains uniformly proportioned',abs(dims['x']/dims['y']-1)<.005,dims)
  a=registry[narrow['bank']][narrow['frame']];k=narrow['root']['width']/a['w'];b=a['opaque_bounds'];box=[narrow['root']['x']+(b[0]-192)*k,narrow['root']['y']+(b[1]-192)*k,narrow['root']['x']+(b[2]-192)*k,narrow['root']['y']+(b[3]-192)*k];W=p.evaluate('cutsceneViewWidth()');H=p.evaluate('VH')
  check('Narrow close-up keeps all tentacles on screen and above the text',box[0]>=0 and box[2]<=W and box[1]>0 and box[3]<H*.72,dict(box=box,W=W,H=H))
  p.evaluate("()=>{run.mode='campaign';drawVictory._trueEnding=false;drawVictory._t=VICTORY_DISH_AT+.1;drawVictory(0);}");check('Ordinary campaign still skips sequel scenes',p.evaluate('drawVictory._t===VICTORY_CARD_AT'))
  p.evaluate("()=>{run.mode='arcade';drawVictory._t=.8;drawVictory(0);}");check('Arcade retains the direct score card',p.evaluate('drawVictory._t===.8'))
  check('No page, console or missing-asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,states=states)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
