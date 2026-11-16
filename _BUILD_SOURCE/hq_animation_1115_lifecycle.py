from pathlib import Path
import sys,json,time,hashlib
from playwright.sync_api import sync_playwright
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');O=R/'_shots/hq_animation_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append({'name':n,'ok':bool(v),'data':d})
 if not v:print('FAIL',n,str(d)[:700],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?hq19lifecycle');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 p.evaluate("()=>{BAL7.setup({stage:5,kind:'chromehammer',pilot:'cole',diff:'hard',mode:'campaign',fire:false});run.gravityShipReady=true;hf17Warm();}")
 p.wait_for_function("()=>{stageLoadTick();furyShipLoadTick();h3Warm();return stageLoadInfo(5).ready&&hf17Warm()&&furyShipReady();}",polling=50)
 p.evaluate("()=>{window.oldStaticBlits=[];window.earthBlits=[];const get=XART.get,draw=ctx.drawImage,seen=new WeakMap();XART.get=function(k){const im=get.apply(this,arguments);if(im)seen.set(im,k);return im;};ctx.drawImage=function(im,...a){const k=seen.get(im);if(['h3_orbital_overhead_v2','h3_earth_surface_v2','h3_hammer_closeup','h3_orbital_aftermath'].includes(k))oldStaticBlits.push(k);if(k==='h3_earth')earthBlits.push({time:H3.ending?.hq19Return?.t,y:a[1]});return draw.call(this,im,...a);};window.nativeFinalePhases=new Set();const tick=h3EndingTick;h3EndingTick=function(dt){if(H3.ending?.hf17)nativeFinalePhases.add(H3.ending.hf17.phase);return tick.apply(this,arguments);};B.hp=0;bossDie();}")
 phases=set();earth=[];returned=False;frozen=[]
 for i in range(450):
  e=p.evaluate(shoot.STEP,6)
  if e:errors.append(e);break
  q=p.evaluate('({state,hf:H3.ending?.hf17?.phase,last:HQ19.last})');phases.add(q.get('hf'))
  if (q.get('last')or{}).get('mode')=='earth-return':
   r=q['last'];earth.append(r)
   if 5.0<=r['time']<=10.5:
    h=p.evaluate("()=>{const a=ctx.getImageData(4,200,70,600).data;let h=2166136261;for(const v of a)h=Math.imul(h^v,16777619);return{hash:h>>>0,scroll:_stage5SpaceScroll,frozen:HQ19.last.scrollFrozen};}");frozen.append(h)
   if abs(r['time']-1)<.08:p.locator('#screen').screenshot(path=str(O/'space-before-earth.png'))
   if abs(r['time']-3.5)<.08:p.locator('#screen').screenshot(path=str(O/'earth-revealing.png'))
   if abs(r['time']-8)<.08:p.locator('#screen').screenshot(path=str(O/'earth-descent.png'))
  if q['state']=='stageclear':returned=True;break
 phases=set(p.evaluate('[...nativeFinalePhases]'));ck('native Chronos destruction retained before new return',all(x in phases for x in ['drain','pulse','lock','missile','engulf','burst','after']),list(phases))
 ck('native settlement reached once',returned,q['state'])
 ck('retired static dying/orbital/Earth plates never drawn',not p.evaluate('oldStaticBlits'),p.evaluate('oldStaticBlits'))
 draws=p.evaluate('earthBlits');ck('Earth image is not drawn before the reveal',draws and all(x['time']>=2.4 for x in draws),draws[:4])
 seq=[x['ship']for x in earth if x['time']>=4.8 and x.get('ship')];ck('southbound descent scales continuously down',len(seq)>20 and all(a['y']<=z['y']+.01 and a['h']>=z['h']-.01 for a,z in zip(seq,seq[1:])))
 ck('starfield pixels and native scroll stop once Earth settles',len(frozen)>20 and len({x['hash']for x in frozen})==1 and len({x['scroll']for x in frozen})==1 and all(x['frozen']for x in frozen),frozen[::10]);print('Native death and frozen Earth approach checked',flush=True)
 p.evaluate("()=>{D1110.preview('post-5','cole');}");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 launches=set();guards=set();quiet=[];enemy=[];lastMode=None;age0=None;startQuiet=None;firstEnemy=None;seen=[];maxFlights=0;launchOrder=[];guardOrder=[];kills=set();shooters=set()
 for i in range(1100):
  e=p.evaluate(shoot.STEP,6)
  if e:errors.append(e);break
  q=p.evaluate('({state,id:BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id,age:BOFCinematicDirector.current?.age,last:HQ19.last,radio:KD18.radio})');r=q.get('last')or{};mode=r.get('mode')
  if mode!=lastMode:seen.append(mode);print('Native HQ beat',mode,flush=True);lastMode=mode
  if mode=='launch':
   launches.update(x['pilot']for x in r['ships']);maxFlights=max(maxFlights,len(r['ships']))
   for ship in r['ships']:
    if ship['pilot']not in [x['pilot']for x in launchOrder]:launchOrder.append(ship)
  if mode=='quiet':
   if startQuiet is None:startQuiet=q['age']-r['time']
   quiet.append(not r['ships']and not r['enemies'])
  if mode in ['attack','escape-decker','escape-axel']:
   if firstEnemy is None and r['enemies']:firstEnemy=q['age']
   enemy.append(len(r['enemies']))
  if mode in ['escape-decker','escape-axel']:
   guards.update(x['pilot']for x in r['ships']);kills.update(x['id']for x in r['kills']);shooters.update(x['pilot']for x in r['friendlyShots'])
   flights=[x for x in r['ships']if x.get('side')];maxFlights=max(maxFlights,len(flights))
   for ship in flights:
    if ship['pilot']not in [x['pilot']for x in guardOrder]:guardOrder.append(ship)
  if q['state']=='title':break
 ck('all eleven complete HQ beats ran natively',all(x in seen for x in ['land','exit','enter','corridor','welcome','radar','launch','quiet','attack','escape-decker','escape-axel']),seen)
 ck('seven pilots launch first and both guards depart later',launches==set(p.evaluate('HQ19_SQUAD'))and guards=={'decker','axel'},{'first':list(launches),'guards':list(guards)})
 ck('quiet stretch has no enemies or outbound ships',quiet and all(quiet))
 ck('at least five seconds before first enemies',firstEnemy is not None and startQuiet is not None and firstEnemy-startQuiet>=4.99,{'quietStart':startQuiet,'enemyStart':firstEnemy,'delay':firstEnemy-startQuiet})
 ck('Decker and Axel both fire and six attackers are visibly defeated before escape',shooters=={'decker','axel'} and len(kills)==6,{'shooters':list(shooters),'kills':list(kills)});ck('enemy reinforcements remain after the counterattack',enemy and enemy[-1]>=8,enemy[::20]);ck('only one aircraft departs at a time',maxFlights==1,maxFlights);order=launchOrder+guardOrder;ck('all nine departure directions alternate southwest and southeast',len(order)==9 and all(x['side']==('southwest'if i%2==0 else'southeast')for i,x in enumerate(order)),[{'pilot':x['pilot'],'side':x['side']}for x in order])
 ck('escape dialogue keeps framed pilot avatars and one metal size',p.evaluate("KD18.radio.material==='crew'&&KD18.radio.avatar==='pav_axel'&&Math.abs(KD18.radio.frame.w/KD18.radio.frame.h-460/84)<.001"))
 # Every code cell must be distinct in the actual native renderer.
 hs=[]
 for f in range(16):
  p.evaluate("f=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);hq19Backdrop('radar',f,[12,12,888,488]);}",f);hs.append(hashlib.sha256(p.locator('#screen').screenshot()).hexdigest())
 ck('all sixteen actual radar frames are distinct',len(set(hs))==16)
 # Co-op must not duplicate a pilot and must keep the actual second ship.
 p.evaluate("()=>{run.pilot='cole';coopOn=true;run2.pilot='decker';p2Index=PILOTS.findIndex(p=>p.key==='decker');for(const k of hq19Keys())XART.rdy(k);}");p.wait_for_function('()=>hq19Keys().every(k=>XART.rdy(k))',polling=50)
 q=p.evaluate("()=>{setState(GS.CUTSCENE);d1110Viewport();const b=hq19Rows(run.pilot).find(b=>b.hq19==='welcome');d1110Visual(b,{t:3,shown:0,id:'coop',i:0});return HQ19.last;}")
 ck('two actual active co-op pilots are retained',p.evaluate("d1110Active().length===2&&d1110Active().includes('cole')&&d1110Active().includes('decker')"));ck('co-op welcome has all nine pilots exactly once',len(q['cast'])==9 and len(set(x['pilot']for x in q['cast']))==9,q['cast']);p.locator('#screen').screenshot(path=str(O/'coop-welcome.png'))
 # Actual native shared-bus playback, isolated from music.
 p.evaluate("async()=>{BOFCinematicDirector.cancel();Audio.stopMusic();const c=Snd._audioCtx();await c.resume();window.soundAnal=c.createAnalyser();soundAnal.fftSize=2048;aq112Bus().output.connect(soundAnal);}");p.wait_for_timeout(1300)
 sounds=[]
 for key in ['gd_doorOpen','gd_footstepA','gd_footstepB','blip','jetDash','enemyMachineGunLight','expSmall']:
  q=p.evaluate("async k=>{Snd.play(k);let peak=0;const b=new Float32Array(2048);for(let i=0;i<25;i++){await new Promise(r=>setTimeout(r,20));soundAnal.getFloatTimeDomainData(b);for(const x of b)peak=Math.max(peak,Math.abs(x));}return {key:k,peak};}",key);sounds.append(q);ck(key+' decoded native audio is audible',q['peak']>.0001,q)
 ck('zero page console HTTP errors',not errors,errors);b.close()
(O/'lifecycle-qa.json').write_text(json.dumps({'checks':checks,'earthSamples':earth,'sounds':sounds,'errors':errors},indent=2),encoding='utf8');print(sum(x['ok']for x in checks),'/',len(checks),'lifecycle checks',flush=True);assert all(x['ok']for x in checks)
