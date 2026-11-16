from pathlib import Path
import sys,json,base64,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/kit';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];samples=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL',name,str(data)[:800],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?kit18qa');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')
 p.wait_for_function("()=>{kd18Warm();return ['kd18_satellite','cd27_neutral_460',...PILOTS.map(p=>'pav_'+p.key)].every(k=>XART.rdy(k));}",polling=50)
 print('loaded',p.evaluate('({VW,VH,SS,canvas:[cv.width,cv.height]})'),flush=True)
 # The native metal renderer must always use the same framed selection portrait.
 for who in p.evaluate('PILOTS.map(p=>p.key)').copy()+['ROOK','NYX','VOSS','KAIA','JACE','CHRONOS','DRACODIA']:
  p.evaluate("()=>{BOFCinematicDirector.cancel();setState(GS.LAUNCH);ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#183b61';ctx.fillRect(0,0,VW,VH);}")
  p.evaluate("who=>dlgBox({who:who.toUpperCase(),full:'Hold formation. The attachment kit is ready. We are tracing the alien signal back to its source.',shown:'Hold formation. The attachment kit is ready.',forceShown:true,y:12,screenSpace:false})",who)
  q=p.evaluate('KD18.radio');samples.append(q)
  mat='chronos'if who=='CHRONOS'else'dracodia'if who=='DRACODIA'else'rebel'if who.isupper()else'crew'
  ck(who+' fixed frame and material',q['material']==mat and round(q['frame']['w'],3)==460 and round(q['frame']['h'],3)==84,q)
  ck(who+' framed avatar is drawn',q['avatar']==('pav_'+who if mat=='crew'else'rr_portrait_'+who.lower()if mat=='rebel'else q['avatar'])and bool(q.get('portraitDraw')),q)
  p.locator('#screen').screenshot(path=str(O/('radio-'+who.lower()+'.png')))
 # Sample actual cinematic canvas pixels, not just the changing frame counter.
 p.evaluate("()=>D1110.preview('post-4','cole')");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 idx=p.evaluate("BOFCinematicDirector.current.beats.findIndex(b=>b.kit17==='satellite')");seen=[];hashes=[]
 for f in range(16):
  t=.45+f/8+.015 if f else .2
  p.evaluate("([i,t])=>{const s=BOFCinematicDirector.current;s.i=i;s.t=t;d1110Visual(s.beats[i],s);}",[idx,t])
  seen.append(p.evaluate('KD18.last.frame'));data=p.locator('#screen').screenshot(path=str(O/('sat-%02d.png'%f)));hashes.append(hashlib.sha256(data).hexdigest())
 ck('all sixteen corruption frames render distinct actual pixels',seen==list(range(16))and len(set(hashes))==16,seen)
 ck('every retired satellite key resolves to code-only source',p.evaluate("()=>['kd17_satellite','d1110_satellite-takeover','c16_art-satellite-takeover'].every(k=>XART.get(k)===XART.get(KD18_SAT.key))"))
 # Isolate the aircraft to prove movement in the authored nozzle pixels.
 for pk in p.evaluate('PILOTS.map(p=>p.key)'):
  p.wait_for_function("pk=>['','_g1','_g2'].every(n=>XART.rdy('ship_'+pk+n))",arg=pk,polling=50);hs=[];states=[]
  for t in [.0,.055,.11,.165,.22,.275]:
   p.evaluate("([pk,t])=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#132344';ctx.fillRect(0,0,VW,VH);pt11OpeningShip(pk,t,VW/2,190,150,.9);}",[pk,t])
   data=p.locator('#screen').screenshot();hs.append(hashlib.sha256(data).hexdigest());states.append(p.evaluate('PT11_UI.ship'))
   if pk=='cole':(O/('thrust-%03d.png'%round(t*1000))).write_bytes(data)
  ck(pk+' actual exhaust animates while combat clock is idle',len(set(hs))>=4 and all(q['plume']for q in states),states)
 # Actual launch, no forced assembly state or fabricated part timer.
 for pk in p.evaluate('PILOTS.map(p=>p.key)'):
  p.evaluate("pk=>{BOFCinematicDirector.cancel();run.pilot=pk;run.mode='campaign';coopOn=false;run.gravityShipReady=false;beginStage(5);warmStage(5);}",pk)
  p.wait_for_function('()=>{stageLoadTick();furyShipLoadTick();return stageLoadInfo(5).ready&&furyShipReady();}',polling=50)
  p.evaluate("()=>{story=null;setState(GS.LAUNCH);drawLaunch._phase=undefined;last=__bofStepNow=performance.now();window.kitDraws=[];if(!window.kitOriginal){window.kitOriginal=furyShipBlit;furyShipBlit=function(k,...a){kitDraws.push(k);return kitOriginal.call(this,k,...a);};}}")
  found=False
  for i in range(220):
   e=p.evaluate(shoot.STEP,6)
   if e:errors.append(e);break
   q=p.evaluate('({phase:gravityMode?.phase,age:gravityMode?.age,start:gravityMode?.partStartAge,count:gravityMode?.partCueCount})')
   if q.get('count')==12 and q.get('age',0)>q.get('start',99)+7.2 and q.get('phase')in['drift','charge']:
    p.evaluate('kitDraws=[]');p.evaluate(shoot.STEP,1);q=p.evaluate('({g:gravityMode,draws:kitDraws,radio:KD18.radio})');found=True;break
  ck(pk+' twelve native separate mounting parts drawn',found and sum(x.endswith('_top')for x in q.get('draws',[]))==12,q)
  p.locator('#screen').screenshot(path=str(O/(pk+'-native-kit.png')));print(pk+' native kit checked',flush=True)
 ck('zero page console HTTP errors',not errors,errors);b.close()
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'samples':samples,'errors':errors},indent=2),encoding='utf8');print(sum(q['ok']for q in checks),'/',len(checks),'native checks',flush=True)
assert all(q['ok']for q in checks)
